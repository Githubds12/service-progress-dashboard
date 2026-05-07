import os
import re
from datetime import datetime, date
import json
import math
import subprocess
import google.generativeai as genai
import csv
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

REPORT_DIR = r"c:\Users\Gorri\Documents\Reports"
TXT_FILE = os.path.join(REPORT_DIR, "trackers", "List of Services done.txt")
TIME_LOG_FILE = os.path.join(REPORT_DIR, "trackers", "Time Log.txt")
HTML_FILE = os.path.join(REPORT_DIR, "dashboard", "Dashboard.html")

def get_ordinal(n):
    if 11 <= n % 100 <= 13:
        return f"{n}th"
    else:
        return str(n) + {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")

def parse_txt():
    with open(TXT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('Dashboard Stats:')
    body = parts[0].strip()
    old_stats_str = parts[1].strip() if len(parts) > 1 else ""
    
    prev_avg_services = 0.0
    prev_recovery_pace = 0.0
    
    m_avg = re.search(r'Average Daily Services:\s+([\d.]+)', old_stats_str)
    if m_avg: prev_avg_services = float(m_avg.group(1))
    m_pace = re.search(r'Recovery Pace:\s+([\d.]+)', old_stats_str)
    if m_pace: prev_recovery_pace = float(m_pace.group(1))
    
    lines = body.split('\n')
    days = []
    current_day = None
    header = lines[0].strip() 
    
    is_history = False
    for line in lines[1:]:
        line = line.strip()
        if not line or line == '----------': continue
        if line.startswith('### Previous History'):
            is_history = True
            continue
        if re.match(r'^\d+(st|nd|rd|th)\s+[a-zA-Z]+,\s+[a-zA-Z]+$', line):
            current_day = {'date': line, 'services': [], 'summary': '', 'earnings': 0, 'count': 0, 'is_history': is_history}
            days.append(current_day)
        elif line.startswith('Daily Summary:'):
            current_day['summary'] = line
            m = re.search(r'(\d+)\s+service[s]?,\s+(\d+)\s+rs', line, re.IGNORECASE)
            if m:
                current_day['count'] = int(m.group(1))
                current_day['earnings'] = int(m.group(2))
        elif re.match(r'^\d+\.', line):
            if current_day is not None:
                current_day['services'].append(line)
                
    today_dt = date.today()
    today_str = f"{get_ordinal(today_dt.day)} {today_dt.strftime('%B, %A')}"
    if not any(today_str.split(',')[0] in d['date'] for d in days):
        body += f"\n{today_str}\nDaily Summary: 0 services, 0 rs\n----------"
        days.append({'date': today_str, 'services': [], 'summary': 'Daily Summary: 0 services, 0 rs', 'earnings': 0, 'count': 0})
    return header, days, body, prev_avg_services, prev_recovery_pace

def parse_time_log():
    if not os.path.exists(TIME_LOG_FILE): return []
    with open(TIME_LOG_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    days = []
    entries = re.split(r'Date:\s+', content)[1:]
    for entry in entries:
        lines = entry.strip().split('\n')
        date_str = lines[0]
        logs = []
        perf_note = ""
        total_h = 0.0
        for line in lines[1:]:
            if line.startswith('-'):
                match = re.search(r'-\s+(.*?):\s+(\d+\.?\d*)h', line)
                if match:
                    act, h = match.groups()
                    logs.append({'activity': act, 'hours': float(h)})
                    total_h += float(h)
            elif "Performance Note:" in line:
                perf_note = line.split('Performance Note:')[1].strip()
        days.append({'date': date_str, 'logs': logs, 'total': total_h, 'note': perf_note})
    return days

def calculate_complexity_stats():
    csv_path = os.path.join(REPORT_DIR, "dashboard", "powerbi_master_data.csv")
    if not os.path.exists(csv_path): return None
    comp_map = {}
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    c_idx = row.get('Complexity Index')
                    if not c_idx or c_idx == 'Unknown': continue
                    comp = int(c_idx)
                    earn = float(row.get('Earnings (RS)', 0))
                    if comp not in comp_map: comp_map[comp] = []
                    comp_map[comp].append(earn)
                except: continue
    except: return None
    if not comp_map: return None
    sorted_comp = sorted(comp_map.keys())
    return {
        'labels': sorted_comp,
        'avg_earnings': [round(sum(comp_map[c])/len(comp_map[c]), 2) for c in sorted_comp],
        'counts': [len(comp_map[c]) for c in sorted_comp]
    }

def calculate_stats(days):
    current_days = [d for d in days if not d.get('is_history', False)]
    total_services = sum(len(d['services']) for d in current_days)
    total_earnings = sum(d['earnings'] for d in current_days)
    start_date = date(2026, 5, 7)
    today_dt = date.today()
    days_elapsed = max((today_dt - start_date).days, 1)
    avg_daily = total_earnings / days_elapsed
    avg_daily_services = total_services / days_elapsed
    target_total = 90000
    remaining_target = target_total - total_earnings
    days_remaining = max(30 - days_elapsed, 1)
    recovery_pace_services = remaining_target / 400 / days_remaining
    projected_total = avg_daily * 30
    recommended_today = math.ceil(recovery_pace_services * 1.2)
    
    today_str_check = f"{get_ordinal(today_dt.day)} {today_dt.strftime('%B')}"
    completed_today = next((len(d['services']) for d in days if today_str_check in d['date']), 0)

    explanation = f"Target: ₹90,000. Pace: {round(recovery_pace_services, 1)} services/day."
    try:
        model = genai.GenerativeModel('gemini-pro-latest')
        prompt = f"Analyze progress: {total_earnings}/90000. Completed today: {completed_today}/{recommended_today}. Write 1-2 sentence tip with Sanskrit header."
        response = model.generate_content(prompt)
        if response and response.text: explanation = response.text.strip().replace('"', '')
    except: pass

    return {
        'total_services': total_services, 'total_earnings': total_earnings,
        'avg_daily': round(avg_daily, 2), 'avg_daily_services': round(avg_daily_services, 2),
        'days_elapsed': days_elapsed, 'recovery_pace_services': round(recovery_pace_services, 1),
        'days_remaining': days_remaining, 'recommended_today': int(recommended_today),
        'completed_today': completed_today, 'explanation': explanation,
        'today_date': f"{get_ordinal(today_dt.day)} {today_dt.strftime('%B, %Y')}",
        'projected_total': round(projected_total, 2),
        'projection_sentence': f"Projected: ₹{round(projected_total, 2)}. {'On track!' if projected_total >= 90000 else 'Increase pace.'}"
    }

def update_txt(body, stats):
    new_stats = f"\nDashboard Stats:\n- Total Services: {stats['total_services']}\n- Total Earnings: {stats['total_earnings']} rs\n- Average Daily Earning: {stats['avg_daily']} rs/day\n- Average Daily Services: {stats['avg_daily_services']} services/day\n- Recovery Pace: {stats['recovery_pace_services']} Services / day\n- Projected Monthly Total: ₹{stats['projected_total']}\n"
    with open(TXT_FILE, 'w', encoding='utf-8') as f:
        f.write(body + "\n\n" + new_stats.strip() + "\n")

def update_html(header, days, stats, complexity_stats=None):
    labels = [d['date'].split(',')[0] for d in days]
    earnings = [d['earnings'] for d in days]
    services = [d['count'] for d in days]
    
    services_by_day = []
    for d in days:
        services_list = ""
        for s in d['services']:
            match = re.search(r'^\d+\.\s+\[(\d\d:\d\d)\]\s+(.*?)\s+-\s+(.*?)\s+-\s+(\d+)rs', s)
            if match:
                time, name, pkg, price = match.groups()
                services_list += f'<li class="service-item-detail"><div style="display:flex; justify-content:space-between;"><b>{name}</b><small>{time}</small></div><div style="display:flex; justify-content:space-between; font-size:9px;"><span>{pkg}</span><b style="color:var(--success);">₹{price}</b></div></li>'
            else:
                services_list += f'<li class="service-item-detail">• {s}</li>'
        services_by_day.append(f'<div class="service-day"><div class="service-header"><span>{d["date"]}</span><span>₹{d["earnings"]}</span></div><ul style="padding:0;">{services_list}</ul></div>')

    time_logs = parse_time_log()
    data_dict = {
        'header': header, 'stats': stats, 'labels': labels, 'earnings': earnings, 'services': services,
        'services_by_day': services_by_day, 'raw_days': days, 'time_logs': time_logs, 'complexity_stats': complexity_stats
    }
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>केसर दर्शिका | {stats['today_date']}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="dashboard_data.js"></script>
    <style>
        :root {{ --primary: #A52A2A; --success: #FFD700; --bg: #050505; --card: rgba(15, 10, 10, 0.9); --border: rgba(165, 42, 42, 0.3); --bhairavi: #FFD700; }}
        body {{ background: var(--bg); color: #f8fafc; font-family: 'Outfit', sans-serif; padding: 15px; }}
        .container {{ max-width: 600px; margin: auto; }}
        .glass-card {{ background: var(--card); backdrop-filter: blur(10px); border: 1px solid var(--border); border-radius: 20px; padding: 20px; margin-bottom: 15px; }}
        h1 {{ text-align: center; font-size: 36px; font-weight: 900; background: linear-gradient(to right, #FF9933, #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 10px 0; }}
        .stats-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
        .value {{ font-size: 24px; font-weight: 700; }}
        .progress-bar {{ height: 8px; background: rgba(255,255,255,0.05); border-radius: 10px; margin: 10px 0; overflow: hidden; }}
        .progress-fill {{ height: 100%; background: linear-gradient(to right, #A52A2A, #FFD700); transition: 1s; }}
        .service-item-detail {{ padding: 8px; background: rgba(255,255,255,0.03); border-radius: 8px; margin-bottom: 5px; border-left: 3px solid var(--primary); list-style: none; }}
        .service-header {{ display: flex; justify-content: space-between; font-weight: 700; margin-bottom: 10px; border-bottom: 1px solid var(--border); padding-bottom: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>केसर दर्शिका</h1>
        <p style="text-align:center; color:#94a3b8;">{stats['today_date']}</p>
        
        <div class="glass-card" style="background:linear-gradient(135deg, #A52A2A 0%, #800000 100%);">
            <h3>ESTIMATED END</h3>
            <div class="value">₹{stats['projected_total']}</div>
            <p style="font-size:11px; opacity:0.8;">{stats['projection_sentence']}</p>
        </div>

        <div class="glass-card">
            <h3>DAILY MISSION: {stats['recommended_today']}</h3>
            <div class="value">{stats['completed_today']} / {stats['recommended_today']}</div>
            <div class="progress-bar"><div class="progress-fill" style="width:{min(stats['completed_today']/stats['recommended_today']*100, 100)}%"></div></div>
            <p style="font-size:12px; color:#94a3b8;">{stats['explanation']}</p>
        </div>

        <div class="stats-grid">
            <div class="glass-card"><h3>TOTAL EARNED</h3><div class="value" style="color:var(--success);">₹{stats['total_earnings']}</div></div>
            <div class="glass-card"><h3>DAILY AVG</h3><div class="value">₹{stats['avg_daily']}</div></div>
        </div>

        <div class="glass-card" style="height:250px;"><canvas id="earningsChart"></canvas></div>
        <div class="glass-card" style="height:300px;"><h3>⏳ TIME ALLOCATION</h3><canvas id="timeChart"></canvas><p id="perf-insight" style="font-size:11px; font-style:italic; margin-top:5px; color:#10b981;"></p></div>
        <div class="glass-card" style="height:300px;"><h3>🧠 COMPLEXITY VS ROI</h3><canvas id="complexityChart"></canvas></div>

        <div class="glass-card" style="max-height:500px; overflow-y:auto;">
            <h3>RECENT ACTIVITY</h3>
            <div id="services-html">{''.join(services_by_day)}</div>
        </div>
    </div>

    <script>
        const data = {json.dumps(data_dict)};
        new Chart(document.getElementById('earningsChart'), {{ type: 'line', data: {{ labels: data.labels, datasets: [{{ data: data.earnings, borderColor: '#FF9933', backgroundColor: 'rgba(255, 153, 51, 0.1)', fill: true }}] }}, options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }} }});
        
        if (data.time_logs && data.time_logs.length > 0) {{
            const log = data.time_logs[data.time_logs.length-1];
            document.getElementById('perf-insight').innerText = log.note;
            new Chart(document.getElementById('timeChart'), {{ type: 'bar', data: {{ labels: log.logs.map(l=>l.activity), datasets: [{{ data: log.logs.map(l=>l.hours), backgroundColor: ['#A52A2A', '#FF4500', '#FFD700', '#800000', '#FF9933'] }}] }}, options: {{ indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }} }});
        }}

        if (data.complexity_stats) {{
            new Chart(document.getElementById('complexityChart'), {{ type: 'bar', data: {{ labels: data.complexity_stats.labels.map(l=>'Lvl '+l), datasets: [{{ label: 'Avg Earnings', data: data.complexity_stats.avg_earnings, backgroundColor: 'rgba(255, 215, 0, 0.4)', yAxisID: 'y' }}, {{ label: 'Count', data: data.complexity_stats.counts, type: 'line', borderColor: '#FF4500', yAxisID: 'y1' }}] }}, options: {{ responsive: true, maintainAspectRatio: false, scales: {{ y: {{ position: 'left' }}, y1: {{ position: 'right', grid: {{ display: false }} }} }} }} }});
        }}
    </script>
</body>
</html>"""
    
    for f_path in [os.path.join(REPORT_DIR, "dashboard", "Dashboard_Live.html"), os.path.join(REPORT_DIR, "dashboard", "Dashboard.html"), os.path.join(REPORT_DIR, "index.html")]:
        with open(f_path, 'w', encoding='utf-8') as f: f.write(html_content)
    
    data_js = f"window.dashboardData = {json.dumps(data_dict)};"
    for f_path in [os.path.join(REPORT_DIR, "dashboard", "dashboard_data.js"), os.path.join(REPORT_DIR, "dashboard_data.js")]:
        with open(f_path, 'w', encoding='utf-8') as f: f.write(data_js)

def update_readme(stats, time_logs):
    path = os.path.join(REPORT_DIR, 'README.md')
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f: content = f.read()
    sec = f"## 📉 Live Stats\n- **Total Earnings**: ₹{stats['total_earnings']}\n- **Average Daily**: ₹{stats['avg_daily']}/day\n- **Monthly Projection**: ₹{stats['projected_total']}\n"
    if time_logs:
        log = time_logs[-1]
        sec += f"\n## ⏳ Productivity Today ({log['date']})\n"
        for e in log['logs']: sec += f"- **{e['activity']}**: {e['hours']}h\n"
        sec += f"- **Note**: *{log['note']}*\n"
    sec += f"- **Last Sync**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    if "## 📉 Live Stats" in content:
        new = re.sub(r'## 📉 Live Stats\n.*?(?=\n## |$)', sec.strip() + "\n\n", content, flags=re.DOTALL)
    else: new = content.replace("## 📊 Tech Stack", sec + "\n\n## 📊 Tech Stack")
    with open(path, 'w', encoding='utf-8') as f: f.write(new)

def update_github():
    try:
        subprocess.run(["git", "add", "."], check=True)
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
        if status:
            subprocess.run(["git", "commit", "-m", f"Auto-update: {datetime.now()}"], check=True)
            subprocess.run(["git", "push"], check=True)
    except: pass

def main():
    header, days, body, prev_avg, prev_pace = parse_txt()
    stats = calculate_stats(days)
    stats['prev_avg_services'] = prev_avg
    stats['prev_recovery_pace'] = prev_pace
    time_logs = parse_time_log()
    c_stats = calculate_complexity_stats()
    update_txt(body, stats)
    update_html(header, days, stats, c_stats)
    update_readme(stats, time_logs)
    update_github()

if __name__ == "__main__":
    main()
