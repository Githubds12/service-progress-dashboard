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
    
    time_logs = parse_time_log()
    data_dict = {
        'header': header, 'stats': stats, 'labels': labels, 'earnings': earnings, 'services': services,
        'raw_days': days, 'time_logs': time_logs, 'complexity_stats': complexity_stats
    }
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>केसर दर्शिका | {stats['today_date']}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="dashboard_data.js"></script>
    <style>
        :root {{
            --primary: #800000;
            --accent: #D4AF37;
            --bg-dark: #0A0A0A;
            --card-bg: rgba(20, 20, 20, 0.9);
            --border: rgba(212, 175, 55, 0.2);
            --text-main: #E2E8F0;
            --text-dim: #94A3B8;
        }}
        
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ 
            background: var(--bg-dark); color: var(--text-main); font-family: 'Outfit', sans-serif; padding: 15px; 
            background-image: 
                radial-gradient(circle at 0% 0%, rgba(128, 0, 0, 0.2) 0%, transparent 50%),
                radial-gradient(circle at 100% 100%, rgba(212, 175, 55, 0.1) 0%, transparent 50%);
            min-height: 100vh;
        }}
        .container {{ max-width: 600px; margin: auto; }}
        
        .header {{ text-align: center; padding: 30px 0; }}
        .header h1 {{ 
            font-size: 44px; font-weight: 900; letter-spacing: -1px;
            background: linear-gradient(135deg, #D4AF37 0%, #FFF 50%, #B8860B 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .header .subtitle {{ color: var(--text-dim); font-size: 12px; text-transform: uppercase; letter-spacing: 5px; font-weight: 600; margin-bottom: 5px; }}
        
        .glass-card {{
            background: var(--card-bg); backdrop-filter: blur(25px); border: 1px solid var(--border);
            border-radius: 24px; padding: 25px; margin-bottom: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        }}
        
        .stats-hero {{ border-top: 5px solid var(--accent); }}
        .hero-label {{ font-size: 11px; color: var(--accent); text-transform: uppercase; letter-spacing: 2px; font-weight: 700; margin-bottom: 5px; }}
        .hero-value {{ font-size: 44px; font-weight: 900; color: #FFF; line-height: 1; }}
        
        .stats-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }}
        .stat-box {{ padding: 20px; border-radius: 20px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); }}
        .stat-box h4 {{ font-size: 10px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
        .stat-box .value {{ font-size: 24px; font-weight: 800; color: var(--accent); }}
        
        .progress-container {{ margin-top: 25px; }}
        .progress-header {{ display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 10px; font-weight: 700; }}
        .progress-bar {{ height: 8px; background: rgba(255,255,255,0.05); border-radius: 10px; overflow: hidden; }}
        .progress-fill {{ height: 100%; background: linear-gradient(90deg, #800000, #D4AF37); transition: 2s cubic-bezier(0.4, 0, 0.2, 1); }}
        
        .section-title {{ 
            font-size: 14px; font-weight: 800; color: #FFF; text-transform: uppercase; 
            letter-spacing: 2px; margin-bottom: 20px; display: flex; align-items: center; gap: 12px;
        }}
        .section-title::after {{ content: ""; flex: 1; height: 1px; background: var(--border); }}
        
        .chart-container {{ height: 280px; position: relative; }}
        
        .day-group {{ margin-bottom: 30px; }}
        .day-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; font-weight: 800; font-size: 16px; border-left: 4px solid var(--accent); padding-left: 12px; }}
        .service-entry {{ 
            padding: 15px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05);
            border-radius: 16px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;
            transition: all 0.3s ease;
        }}
        .service-entry:hover {{ background: rgba(212, 175, 55, 0.08); border-color: rgba(212, 175, 55, 0.3); transform: translateX(5px); }}
        .service-info {{ display: flex; flex-direction: column; gap: 4px; }}
        .service-name {{ font-weight: 700; font-size: 15px; color: #FFF; }}
        .service-pkg {{ font-size: 11px; color: var(--text-dim); }}
        .service-price {{ font-weight: 900; color: var(--accent); font-size: 16px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="subtitle">Mission Intelligence</div>
            <h1>केसर दर्शिका</h1>
            <div style="font-size: 15px; color: var(--accent); font-weight: 700; letter-spacing: 1px; margin-top: 5px;">{stats['today_date']}</div>
        </div>

        <div class="glass-card stats-hero">
            <div class="hero-label">Projected Month End</div>
            <div class="hero-value">₹{stats['projected_total']}</div>
            <p style="margin-top: 12px; color: var(--text-dim); font-size: 13px; line-height: 1.5;">{stats['projection_sentence']}</p>
            
            <div class="progress-container">
                <div class="progress-header">
                    <span>Target Fulfillment</span>
                    <span style="color: var(--accent);">{stats['completed_today']} / {stats['recommended_today']} Services</span>
                </div>
                <div class="progress-bar"><div class="progress-fill" id="mission-fill" style="width: 0%"></div></div>
            </div>
        </div>

        <div class="stats-grid">
            <div class="glass-card stat-box" style="margin-bottom: 0;">
                <h4>Net Revenue</h4>
                <div class="value">₹{stats['total_earnings']}</div>
            </div>
            <div class="glass-card stat-box" style="margin-bottom: 0;">
                <h4>Performance Index</h4>
                <div class="value">₹{stats['avg_daily']}</div>
            </div>
        </div>

        <div class="glass-card">
            <div class="section-title">Revenue Velocity</div>
            <div class="chart-container"><canvas id="earningsChart"></canvas></div>
        </div>

        <div class="glass-card">
            <div class="section-title">Focus Distribution</div>
            <div class="chart-container" style="height: 320px;"><canvas id="timeChart"></canvas></div>
        </div>

        <div class="glass-card">
            <div class="section-title">Profitability Analysis</div>
            <div class="chart-container" style="height: 320px;"><canvas id="complexityChart"></canvas></div>
        </div>

        <div class="glass-card">
            <div class="section-title" style="margin-bottom: 25px;">Mission Records</div>
            <div id="services-html"></div>
        </div>
    </div>

    <script>
        const data = {json.dumps(data_dict)};
        
        function renderUI(data) {{
            setTimeout(() => {{
                const pct = Math.min((data.stats.completed_today / data.stats.recommended_today) * 100, 100);
                document.getElementById('mission-fill').style.width = pct + '%';
            }}, 300);

            const commonOptions = {{
                responsive: true, maintainAspectRatio: false,
                plugins: {{ 
                    legend: {{ display: false }},
                    tooltip: {{ 
                        backgroundColor: 'rgba(10,10,10,0.9)', titleFont: {{ size: 14 }},
                        bodyFont: {{ size: 12 }}, borderColor: 'rgba(212,175,55,0.3)', borderWidth: 1
                    }}
                }},
                scales: {{ 
                    y: {{ grid: {{ color: 'rgba(255,255,255,0.08)' }}, ticks: {{ color: '#94A3B8', font: {{ size: 11 }} }} }},
                    x: {{ grid: {{ display: false }}, ticks: {{ color: '#94A3B8', font: {{ size: 11 }} }} }}
                }}
            }};

            // Trend Chart
            new Chart(document.getElementById('earningsChart'), {{
                type: 'line',
                data: {{
                    labels: data.labels,
                    datasets: [{{
                        data: data.earnings,
                        borderColor: '#D4AF37',
                        borderWidth: 3,
                        backgroundColor: 'rgba(212, 175, 55, 0.1)',
                        tension: 0.4, fill: true, pointRadius: 4, pointHoverRadius: 6,
                        pointBackgroundColor: '#FFF', pointBorderColor: '#D4AF37'
                    }}]
                }},
                options: commonOptions
            }});

            // Time Chart (Horizontal + Multi-color)
            if (data.time_logs && data.time_logs.length > 0) {{
                const log = data.time_logs[data.time_logs.length-1];
                new Chart(document.getElementById('timeChart'), {{
                    type: 'bar',
                    data: {{
                        labels: log.logs.map(l => l.activity),
                        datasets: [{{
                            data: log.logs.map(l => l.hours),
                            backgroundColor: ['#800000', '#B8860B', '#D4AF37', '#A52A2A', '#5C0000', '#F1D382'],
                            borderRadius: 6
                        }}]
                    }},
                    options: {{ ...commonOptions, indexAxis: 'y' }}
                }});
            }}

            // Complexity Chart (Dual Axis)
            if (data.complexity_stats) {{
                new Chart(document.getElementById('complexityChart'), {{
                    type: 'bar',
                    data: {{
                        labels: data.complexity_stats.labels.map(l => 'Lvl ' + l),
                        datasets: [{{
                            label: 'Avg ROI (₹)',
                            data: data.complexity_stats.avg_earnings,
                            backgroundColor: 'rgba(212, 175, 55, 0.6)',
                            borderRadius: 6,
                            yAxisID: 'y'
                        }}, {{
                            label: 'Volume',
                            data: data.complexity_stats.counts,
                            type: 'line',
                            borderColor: '#800000',
                            borderWidth: 3,
                            yAxisID: 'y1',
                            tension: 0.3,
                            pointRadius: 4
                        }}]
                    }},
                    options: {{
                        ...commonOptions,
                        scales: {{
                            y: {{ position: 'left', grid: {{ color: 'rgba(255,255,255,0.08)' }} }},
                            y1: {{ position: 'right', grid: {{ display: false }}, ticks: {{ color: '#800000' }} }},
                            x: {{ grid: {{ display: false }} }}
                        }}
                    }}
                }});
            }}

            // Render Log
            const html = data.raw_days.map(d => `
                <div class="day-group">
                    <div class="day-header">
                        <span>${{d.date}}</span>
                        <span style="color: var(--accent);">₹${{d.earnings}}</span>
                    </div>
                    <div class="service-log">
                        ${{d.services.map(s => {{
                            const m = s.match(/^\\d+\\.\\s+\\[(\\d\\d:\\d\\d)\\]\\s+(.*?)\\s+-\\s+(.*?)\\s+-\\s+(\\d+)rs/);
                            if (m) return `
                                <div class="service-entry">
                                    <div class="service-info">
                                        <span class="service-name">${{m[2]}}</span>
                                        <span class="service-pkg">${{m[3]}}</span>
                                    </div>
                                    <div class="service-price">₹${{m[4]}}</div>
                                </div>`;
                            return `<div class="service-entry"><span class="service-name">${{s}}</span></div>`;
                        }}).join('')}}
                    </div>
                </div>
            `).join('');
            document.getElementById('services-html').innerHTML = html;
        }}

        renderUI(data);
    </script>
</body>
</html>"""
    
    for f_path in [os.path.join(REPORT_DIR, "dashboard", "Dashboard_Live.html"), os.path.join(REPORT_DIR, "dashboard", "Dashboard.html"), os.path.join(REPORT_DIR, "index.html")]:
        with open(f_path, 'w', encoding='utf-8') as f: f.write(html_content)
    
    data_js = f"window.dashboardData = {json.dumps(data_dict)};"
    for f_path in [os.path.join(REPORT_DIR, "dashboard", "dashboard_data.js"), os.path.join(REPORT_DIR, "dashboard_data.js")]:
        with open(f_path, 'w', encoding='utf-8') as f: f.write(data_js)
    
    for f_path in [os.path.join(REPORT_DIR, "dashboard", "Dashboard_Live.html"), os.path.join(REPORT_DIR, "dashboard", "Dashboard.html"), os.path.join(REPORT_DIR, "index.html")]:
        with open(f_path, 'w', encoding='utf-8') as f: f.write(html_content)
    
    data_js = f"window.dashboardData = {json.dumps(data_dict)};"
    for f_path in [os.path.join(REPORT_DIR, "dashboard", "dashboard_data.js"), os.path.join(REPORT_DIR, "dashboard_data.js")]:
        with open(f_path, 'w', encoding='utf-8') as f: f.write(data_js)
    
    for f_path in [os.path.join(REPORT_DIR, "dashboard", "Dashboard_Live.html"), os.path.join(REPORT_DIR, "dashboard", "Dashboard.html"), os.path.join(REPORT_DIR, "index.html")]:
        with open(f_path, 'w', encoding='utf-8') as f: f.write(html_content)
    
    data_js = f"window.dashboardData = {json.dumps(data_dict)};"
    for f_path in [os.path.join(REPORT_DIR, "dashboard", "dashboard_data.js"), os.path.join(REPORT_DIR, "dashboard_data.js")]:
        with open(f_path, 'w', encoding='utf-8') as f: f.write(data_js)
    
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
