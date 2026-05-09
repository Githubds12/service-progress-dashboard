import os
import re
from datetime import datetime, date
import json
import math
import subprocess
import csv
import requests
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

REPORT_DIR = r"c:\Users\Gorri\Documents\Reports"
TXT_FILE = os.path.join(REPORT_DIR, "trackers", "List of Services done.txt")
TIME_LOG_FILE = os.path.join(REPORT_DIR, "trackers", "Time Log.txt")
HTML_FILE = os.path.join(REPORT_DIR, "dashboard", "Dashboard.html")

def process_remote_reflections():
    token = os.getenv("GITHUB_TOKEN")
    if not token: return
    
    # Check Issue Comments (DB)
    url = "https://api.github.com/repos/Githubds12/service-progress-dashboard/issues/1/comments"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200: return
        
        comments = response.json()
        if not comments: return
        
        log_path = TIME_LOG_FILE
        if not os.path.exists(log_path): return
        
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        new_reflections = []
        deletions = []
        for comment in comments:
            body = comment['body'].strip()
            if body.startswith("DELETE_REF:"):
                deletions.append(body)
            else:
                new_reflections.append(body)
            requests.delete(comment['url'], headers=headers)
            
        if not new_reflections and not deletions: return
        
        # Process Deletions
        if deletions:
            for d_cmd in deletions:
                try:
                    m_date = re.search(r'Date:\s*(.*?)(?:,|$)', d_cmd)
                    m_idx = re.search(r'Index:\s*(\d+)', d_cmd)
                    if not m_date or not m_idx: continue
                    
                    target_date = m_date.group(1).strip()
                    target_idx = int(m_idx.group(1))
                    
                    for i, line in enumerate(lines):
                        if line.startswith("Date:") and target_date in line:
                            for j in range(i + 1, len(lines)):
                                if lines[j].startswith("Date:"): break
                                if lines[j].strip().startswith("Reflections:"):
                                    content = lines[j].split("Reflections:")[1].strip()
                                    items = re.split(r'\s*\d+\.\s*', content)
                                    items = [it.strip() for it in items if it.strip()]
                                    
                                    if 0 <= target_idx < len(items):
                                        items.pop(target_idx)
                                        if items:
                                            lines[j] = "Reflections: " + " ".join([f"{k+1}. {it}" for k, it in enumerate(items)]) + "\n"
                                        else:
                                            lines[j] = "Reflections:\n"
                                    break
                            break
                except: continue

        # Process Additions
        if new_reflections:
            for ref_cmd in new_reflections:
                target_date = ""
                text = ref_cmd
                if ref_cmd.startswith("ADD_REF:"):
                    m_date = re.search(r'Date:\s*(.*?),\s*Text:\s*(.*)', ref_cmd, re.DOTALL)
                    if m_date:
                        target_date = m_date.group(1).strip()
                        text = m_date.group(2).strip()
                
                # Find target date section or default to latest
                target_idx = -1
                if target_date:
                    for i, line in enumerate(lines):
                        if line.startswith("Date:") and target_date in line:
                            target_idx = i
                            break
                if target_idx == -1:
                    for i, line in enumerate(lines):
                        if line.startswith("Date:"): target_idx = i
                
                if target_idx != -1:
                    ref_line_idx = -1
                    insert_pos = -1
                    for j in range(target_idx + 1, len(lines)):
                        if lines[j].startswith("Date:"):
                            insert_pos = j
                            break
                        if lines[j].strip().startswith("Reflections:"):
                            ref_line_idx = j
                            break
                    
                    if ref_line_idx != -1:
                        content = lines[ref_line_idx].split("Reflections:")[1].strip()
                        items = re.split(r'\s*\d+\.\s*', content)
                        items = [it.strip() for it in items if it.strip()]
                        items.append(text)
                        lines[ref_line_idx] = "Reflections: " + " ".join([f"{k+1}. {it}" for k, it in enumerate(items)]) + "\n"
                    else:
                        lines.insert(target_idx + 1, f"Reflections: 1. {text}\n")

        with open(log_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
            
        print(f"Synced {len(new_reflections)} additions and {len(deletions)} deletions.")
    except Exception as e:
        print(f"Error syncing remote reflections: {e}")

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
            m_date = re.match(r'^(\d+)(?:st|nd|rd|th)\s+([a-zA-Z]+)', line)
            day_num = int(m_date.group(1))
            month_name = m_date.group(2)
            # Support mapping month name to month number (assuming 2026)
            try: month_num = datetime.strptime(month_name, '%B').month
            except: month_num = 5
            iso_date = f"2026-{month_num:02d}-{day_num:02d}"
            current_day = {'date': line, 'iso_date': iso_date, 'services': [], 'summary': '', 'earnings': 0, 'count': 0, 'is_history': is_history}
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
        days.append({'date': today_str, 'iso_date': today_dt.strftime('%Y-%m-%d'), 'services': [], 'summary': 'Daily Summary: 0 services, 0 rs', 'earnings': 0, 'count': 0})
    return header, days, body, prev_avg_services, prev_recovery_pace

def parse_time_log():
    if not os.path.exists(TIME_LOG_FILE): return []
    try:
        with open(TIME_LOG_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        days = []
        # Support both 'Date:' and 'Date: ' formats
        entries = re.split(r'Date:\s*', content)
        for entry in entries:
            if not entry.strip() or '###' in entry[:10]: continue
            lines = entry.strip().split('\n')
            date_str = lines[0].strip()
            logs = []
            total_h = 0.0
            for line in lines:
                line = line.strip()
                if line.startswith('-'):
                    # Match activity and hours (supports 2h, 1.5h, etc.)
                    match = re.search(r'-\s*(.*?):\s*(\d+\.?\d*)\s*h', line, re.IGNORECASE)
                    if match:
                        act, h = match.groups()
                        logs.append({'activity': act.strip(), 'hours': float(h)})
                        total_h += float(h)
            
            # Extract Reflections
            ref_match = re.search(r'Reflections:\s*(.*?)(?=\nDate:|$)', entry, re.DOTALL | re.IGNORECASE)
            ref_raw = ref_match.group(1).strip() if ref_match else ""
            
            # Parse numbered list: "1. A 2. B" -> ["A", "B"]
            ref_items = re.split(r'\s*\d+\.\s*', ref_raw)
            ref_items = [it.strip() for it in ref_items if it.strip()]

            if logs or ref_items:
                days.append({'date': date_str, 'logs': logs, 'total': total_h, 'reflections': ref_items})
        return days
    except Exception as e:
        print(f"Error parsing time log: {e}")
        return []

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
        prompt = f"Analyze progress: {total_earnings}/90000. Completed today: {completed_today}/{recommended_today}. Write 1-2 sentence tip with Sanskrit header."
        response = client.models.generate_content(model='gemini-flash-latest', contents=prompt)
        if response and response.text: explanation = response.text.strip().replace('"', '')
    except: pass

    return {
        'total_services': total_services, 'total_earnings': total_earnings,
        'avg_daily': round(avg_daily, 2), 'avg_daily_services': round(avg_daily_services, 2),
        'days_elapsed': days_elapsed, 'recovery_pace_services': round(recovery_pace_services, 1),
        'days_remaining': days_remaining, 'recommended_today': int(recommended_today),
        'completed_today': completed_today, 'explanation': explanation,
        'projected_total': round(projected_total, 2),
        'today_date': f"{get_ordinal(today_dt.day)} {today_dt.strftime('%B, %Y')}",
        'today_date_raw': f"{get_ordinal(today_dt.day)} {today_dt.strftime('%B')}",
        'projection_sentence': explanation
    }

def update_txt(body, stats):
    new_stats = f"\nDashboard Stats:\n- Total Services: {stats['total_services']}\n- Total Earnings: {stats['total_earnings']} rs\n- Average Daily Earning: {stats['avg_daily']} rs/day\n- Average Daily Services: {stats['avg_daily_services']} services/day\n- Recovery Pace: {stats['recovery_pace_services']} Services / day\n- Projected Monthly Total: ₹{stats['projected_total']}\n"
    with open(TXT_FILE, 'w', encoding='utf-8') as f:
        f.write(body + "\n\n" + new_stats.strip() + "\n")

def update_html(header, days, stats, complexity_stats=None):
    # Sort days chronologically for charts
    days.sort(key=lambda x: x['iso_date'])
    
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
    <style>
        :root {{
            --primary: #800000;
            --accent: #D4AF37;
            --bg-dark: #070707;
            --card-bg: rgba(10, 10, 10, 0.45); /* Increased Transparency */
            --border: rgba(212, 175, 55, 0.25);
            --text-main: #FFFFFF;
            --text-dim: #94A3B8;
            --glow: rgba(212, 175, 55, 0.35);
        }}
        
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ 
            background: var(--bg-dark); color: var(--text-main); font-family: 'Outfit', sans-serif; padding: 15px; 
            overflow-x: hidden; min-height: 100vh;
        }}
        
        /* Animated Gradient Background with Bhairavi Aura */
        .bg-glow {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;
            background: 
                radial-gradient(circle at 10% 10%, rgba(139, 0, 0, 0.25) 0%, transparent 40%),
                radial-gradient(circle at 90% 90%, rgba(212, 175, 55, 0.15) 0%, transparent 40%),
                url('dashboard/bhairavi_texture_real.jpg');
            background-size: 100% 100%, 100% 100%, cover;
            opacity: 0.6; /* Increased for visibility */
            animation: bgPulse 20s infinite alternate ease-in-out;
        }}
        @keyframes bgPulse {{
            0% {{ transform: scale(1); opacity: 0.8; }}
            100% {{ transform: scale(1.1); opacity: 1; }}
        }}

        .container {{ max-width: 1100px; margin: auto; position: relative; z-index: 1; padding: 0 10px; }}
        
        @media (max-width: 1000px) {{
            .pie-section-content {{ flex-direction: column !important; align-items: center !important; }}
            .chart-container {{ flex: 0 0 auto !important; width: 100% !important; max-width: 450px !important; }}
            #pieLegend {{ width: 100% !important; margin-top: 20px; }}
        }}
        
        .header {{ text-align: center; padding: 40px 0; animation: fadeInDown 1.2s cubic-bezier(0.22, 1, 0.36, 1); position: relative; }}
        
        /* Linga Bhairavi Sacred Banner */
        .bhairavi-banner {{
            width: 100%;
            height: 400px;
            background: url('dashboard/bhairavi_banner_real.jpg') no-repeat center center;
            background-size: cover;
            position: relative;
            margin-top: -15px;
            margin-bottom: -120px;
            z-index: 0;
            mask-image: linear-gradient(to bottom, black 60%, transparent 95%);
            -webkit-mask-image: linear-gradient(to bottom, black 60%, transparent 95%);
            filter: brightness(0.8) contrast(1.1);
        }}
        
        .header h1 {{ 
            font-size: 56px; font-weight: 900; letter-spacing: -3px;
            background: linear-gradient(135deg, #D4AF37 0%, #FFF 50%, #B8860B 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 20px var(--glow));
            margin-bottom: 5px;
        }}
        .header .subtitle {{ color: var(--text-dim); font-size: 11px; text-transform: uppercase; letter-spacing: 7px; font-weight: 800; opacity: 0.9; }}
        
        .glass-card {{
            background: var(--card-bg); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px); 
            border: 1px solid var(--border);
            border-radius: 32px; padding: 30px; margin-bottom: 25px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.4);
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            animation: fadeInUp 1s ease-out backwards;
            position: relative; overflow: hidden;
        }}
        .glass-card:hover {{ 
            transform: translateY(-10px) scale(1.02); 
            border-color: var(--accent); 
            box-shadow: 0 30px 60px rgba(212, 175, 55, 0.2); 
        }}
        
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(40px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .stats-hero {{ border-top: 8px solid var(--accent); }}
        .hero-label {{ font-size: 12px; color: var(--accent); text-transform: uppercase; letter-spacing: 3px; font-weight: 900; margin-bottom: 10px; }}
        .hero-value {{ font-size: 52px; font-weight: 900; color: #FFF; line-height: 1; text-shadow: 0 0 30px rgba(212, 175, 55, 0.2); }}
        
        .stats-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px; }}
        .stat-box {{ padding: 25px; border-radius: 28px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); text-align: center; }}
        .stat-box h4 {{ font-size: 11px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px; }}
        .stat-box .value {{ font-size: 28px; font-weight: 950; color: var(--accent); text-shadow: 0 0 15px var(--glow); }}
        
        .progress-container {{ margin-top: 35px; }}
        .progress-header {{ display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 15px; font-weight: 900; color: #FFF; }}
        .progress-bar {{ height: 12px; background: rgba(255,255,255,0.05); border-radius: 20px; overflow: hidden; border: 1px solid rgba(255,255,255,0.08); }}
        .progress-fill {{ 
            height: 100%; background: linear-gradient(90deg, var(--primary), var(--accent), #FFF); 
            transition: 3s cubic-bezier(0.34, 1.56, 0.64, 1); 
            box-shadow: 0 0 20px var(--accent);
            position: relative;
        }}
        .progress-fill::after {{
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            animation: progressFlow 2s infinite linear;
        }}
        @keyframes progressFlow {{ 0% {{ transform: translateX(-100%); }} 100% {{ transform: translateX(100%); }} }}
        @keyframes blink {{ 0%, 100% {{ opacity: 1; filter: brightness(1.2); }} 50% {{ opacity: 0.4; filter: brightness(0.8); }} }}
        
        .section-title {{ 
            font-size: 15px; font-weight: 950; color: #FFF; text-transform: uppercase; 
            letter-spacing: 3px; margin-bottom: 25px; display: flex; align-items: center; gap: 15px;
            flex-wrap: wrap;
        }}
        .section-title::after {{ content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, var(--accent), transparent); opacity: 0.4; min-width: 50px; }}
        
        .chart-container {{ height: 320px; position: relative; padding: 10px; }}
        
        .legend-item {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 12px 18px; background: rgba(255,255,255,0.03);
            border: 1px solid var(--border); border-radius: 16px; margin-bottom: 10px;
            transition: all 0.3s ease;
        }}
        .legend-item:hover {{ background: rgba(255,255,255,0.07); transform: translateX(5px); }}
        .legend-color {{ width: 12px; height: 12px; border-radius: 4px; margin-right: 12px; }}
        
        #pieLegend::-webkit-scrollbar {{ width: 4px; }}
        #pieLegend::-webkit-scrollbar-thumb {{ background: var(--accent); border-radius: 10px; }}
        
        .day-group {{ margin-bottom: 40px; }}
        .day-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-weight: 900; font-size: 18px; color: #FFF; border-left: 6px solid var(--accent); padding-left: 18px; }}
        .service-link {{ display: block; margin-bottom: 15px; outline: none; }}
        .service-entry {{ 
            background: rgba(255,255,255,0.03); border: 1px solid var(--border); padding: 22px 28px; 
            border-radius: 24px; display: flex; justify-content: space-between; align-items: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); cursor: pointer;
        }}
        .service-entry:hover {{ 
            background: rgba(212, 175, 55, 0.12); 
            border-color: var(--accent); 
            transform: translateX(10px) scale(1.02);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(212, 175, 55, 0.2);
        }}
        .service-info {{ display: flex; flex-direction: column; gap: 6px; }}
        .service-name {{ font-weight: 800; font-size: 17px; color: #FFF; }}
        .service-pkg {{ font-size: 12px; color: var(--text-dim); font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }}
        .service-price {{ font-weight: 1000; color: var(--accent); font-size: 20px; text-shadow: 0 0 15px rgba(212, 175, 55, 0.4); }}
        
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-thumb {{ background: var(--accent); border-radius: 10px; }}
    </style>
</head>
<body>
    <div class="bhairavi-banner"></div>
    <div class="bg-glow"></div>
    <div class="container">
        <div class="header">
            <div class="subtitle">Neural Operations Hub</div>
            <h1>केसर दर्शिका</h1>
            <div id="header-date" style="font-size: 18px; color: var(--accent); font-weight: 900; letter-spacing: 2px; margin-top: 8px; text-shadow: 0 0 15px var(--glow);">
                {stats['today_date']}
            </div>
            <div style="margin-top: 15px; display: flex; align-items: center; justify-content: center; gap: 10px;">
                <div style="width: 8px; height: 8px; background: #00FF00; border-radius: 50%; box-shadow: 0 0 10px #00FF00; animation: blink 1.5s infinite;"></div>
                <span style="font-size: 10px; font-weight: 800; letter-spacing: 2px; color: #00FF00; text-transform: uppercase;">System Operational</span>
            </div>
        </div>

        <div class="glass-card stats-hero" style="animation-delay: 0.1s;">
            <div class="hero-label">Terminal Revenue Prediction</div>
            <div class="hero-value">₹{stats['projected_total']}</div>
            <p style="margin-top: 18px; color: var(--text-dim); font-size: 15px; line-height: 1.7; font-weight: 600;">{stats['projection_sentence']}</p>
            
            <div class="progress-container">
                <div class="progress-header">
                    <span>MISSION LOAD</span>
                    <span style="color: var(--accent); text-shadow: 0 0 15px var(--glow); font-weight: 1000;">{stats['completed_today']} / {stats['recommended_today']} UNITS</span>
                </div>
                <div class="progress-bar"><div class="progress-fill" id="mission-fill" style="width: 0%"></div></div>
            </div>
        </div>

        <div class="stats-grid">
            <div class="glass-card stat-box" style="margin-bottom: 0; animation-delay: 0.2s;">
                <h4>TOTAL HARVEST</h4>
                <div class="value">₹{stats['total_earnings']}</div>
            </div>
            <div class="glass-card stat-box" style="margin-bottom: 0; animation-delay: 0.3s;">
                <h4>EFFICIENCY</h4>
                <div class="value">₹{stats['avg_daily']}</div>
            </div>
            <div class="glass-card stat-box" style="margin-bottom: 0; animation-delay: 0.4s;">
                <h4>AVG SERVICES</h4>
                <div class="value">{stats['avg_daily_services']}</div>
            </div>
            <div class="glass-card stat-box" style="margin-bottom: 0; animation-delay: 0.5s;">
                <h4>TOTAL UNITS</h4>
                <div class="value">{stats['total_services']}</div>
            </div>
        </div>

        <div class="glass-card" style="animation-delay: 0.4s;">
            <div class="section-title">Revenue Trajectory</div>
            <div class="chart-container"><canvas id="trendChart"></canvas></div>
        </div>

        <div class="glass-card" style="animation-delay: 0.5s;">
            <div class="section-title" style="display: flex; align-items: center; gap: 15px; flex-wrap: wrap;">
                <span>Daily Focus Distribution</span>
                <span id="pieTotalHours" style="font-size: 11px; color: #FFF; background: rgba(255,255,255,0.05); padding: 4px 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);"></span>
                <div style="flex: 1; display: flex; justify-content: flex-end; align-items: center; gap: 12px; min-width: 300px;">
                    <button onclick="navigatePie(-1)" style="background: var(--accent); border: none; color: #000; padding: 6px 12px; border-radius: 8px; cursor: pointer; font-weight: 900; display: inline-block !important;">&lt;</button>
                    <span id="pieViewedDate" style="font-size: 12px; color: var(--accent); font-weight: 800; text-transform: uppercase;"></span>
                    <button onclick="navigatePie(1)" style="background: var(--accent); border: none; color: #000; padding: 6px 12px; border-radius: 8px; cursor: pointer; font-weight: 900; display: inline-block !important;">&gt;</button>
                    <input type="date" id="pieDateJump" style="background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 12px; padding: 8px 12px; color: #FFF; cursor: pointer; color-scheme: dark;">
                </div>
            </div>
            <div class="pie-section-content" style="display: flex; gap: 30px; align-items: flex-start; margin-top: 10px;">
                <div class="chart-container" style="flex: 0 0 450px; height: 450px;">
                    <canvas id="pieChart"></canvas>
                </div>
                <div id="pieLegend" style="flex: 1; max-height: 450px; overflow-y: auto; padding-right: 15px;">
                    <!-- Legend dynamic content -->
                </div>
            </div>
        </div>

        <div class="glass-card" id="reflectionsCard" style="animation-delay: 0.6s;">
            <div class="section-title" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <span>Daily Reflections</span>
                <div style="flex: 1; display: flex; justify-content: flex-end; align-items: center; gap: 12px; min-width: 300px;">
                    <button onclick="navigateRef(-1)" style="background: var(--accent); border: none; color: #000; padding: 6px 12px; border-radius: 8px; cursor: pointer; font-weight: 900;">&lt;</button>
                    <span id="refViewedDate" style="font-size: 12px; color: var(--accent); font-weight: 800; text-transform: uppercase;"></span>
                    <button onclick="navigateRef(1)" style="background: var(--accent); border: none; color: #000; padding: 6px 12px; border-radius: 8px; cursor: pointer; font-weight: 900;">&gt;</button>
                    <input type="date" id="refDateJump" style="background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 12px; padding: 8px 12px; color: #FFF; cursor: pointer; color-scheme: dark;">
                </div>
            </div>
            
            <div id="reflectionInputArea" style="margin-bottom: 30px; background: rgba(255,255,255,0.02); padding: 25px; border-radius: 28px; border: 1px solid var(--border); box-shadow: inset 0 0 20px rgba(0,0,0,0.2);">
                <label id="refInputLabel" style="display: block; font-size: 11px; color: var(--accent); text-transform: uppercase; letter-spacing: 2px; font-weight: 900; margin-bottom: 12px;">New Insight for Today</label>
                <textarea id="newReflectionText" placeholder="Type your reflections for today here..." 
                    style="width: 100%; background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.05); color: #FFF; font-family: 'Outfit'; font-size: 15px; min-height: 120px; outline: none; resize: vertical; padding: 15px; border-radius: 16px; line-height: 1.6;"></textarea>
                <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px;">
                    <button onclick="copyReflection()" style="background: var(--accent); border: none; color: #000; padding: 10px 25px; border-radius: 12px; font-weight: 950; cursor: pointer; font-size: 12px; letter-spacing: 1px; transition: all 0.3s ease; box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);">SAVE TO DATABASE</button>
                </div>
            </div>

            <div style="padding: 0 10px;">
                <label style="display: block; font-size: 11px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 2px; font-weight: 900; margin-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 10px;">Logged Reflections</label>
                <div id="reflectionsText" style="color: var(--text-dim); font-size: 15px; line-height: 1.8; font-weight: 600;"></div>
            </div>
        </div>

        <div class="glass-card" style="animation-delay: 0.7s;">
            <div class="section-title" style="margin-bottom: 25px;">
                <span>Operational Intelligence Log</span>
                <span id="log-header-date" style="font-size: 13px; color: var(--accent); margin-left: auto; letter-spacing: 2px; font-weight: 900;">[ {stats['today_date']} ]</span>
            </div>
            <div style="margin-bottom: 25px; display: flex; gap: 15px; flex-wrap: wrap;">
                <input type="text" id="logSearch" placeholder="SEARCH NEURAL RECORDS..." 
                    style="flex: 1; min-width: 250px; background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 16px; padding: 15px 20px; color: #FFF; font-family: 'Outfit'; font-weight: 700; letter-spacing: 1px; outline: none; transition: all 0.3s ease;">
                <input type="date" id="dateJump" 
                    style="background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 16px; padding: 15px 20px; color: #FFF; font-family: 'Outfit'; font-weight: 700; outline: none; transition: all 0.3s ease; cursor: pointer; color-scheme: dark;">
            </div>
            <div id="log-html"></div>
        </div>
    </div>

    <script>
        const data = {json.dumps(data_dict)};
        
        function initDashboard(data) {{
            // Animate Units
            setTimeout(() => {{
                const pct = Math.min((data.stats.completed_today / data.stats.recommended_today) * 100, 100);
                document.getElementById('mission-fill').style.width = pct + '%';
                
                // Update dates dynamically
                if (data.stats.today_date) {{
                    document.getElementById('header-date').innerText = data.stats.today_date;
                    document.getElementById('log-header-date').innerText = `[ ${{data.stats.today_date}} ]`;
                    document.title = `केसर दर्शिका | ${{data.stats.today_date}}`;
                }}
            }}, 600);

            Chart.defaults.color = 'rgba(255,255,255,0.7)';
            Chart.defaults.font.family = "'Outfit', sans-serif";
            Chart.defaults.font.weight = '600';

            const commonOptions = {{
                responsive: true,
                maintainAspectRatio: false,
                animation: {{ duration: 2500, easing: 'easeOutQuart' }},
                plugins: {{ 
                    legend: {{ display: false }},
                    tooltip: {{ 
                        backgroundColor: 'rgba(5, 5, 5, 0.98)', titleColor: '#D4AF37',
                        bodyColor: '#FFF', borderColor: '#D4AF37', borderWidth: 1,
                        padding: 15, cornerRadius: 16, displayColors: false,
                        titleFont: {{ size: 16, weight: 800 }}, bodyFont: {{ size: 14 }}
                    }}
                }}
            }};

            // 1. Line Chart
            new Chart(document.getElementById('trendChart'), {{
                type: 'line',
                data: {{
                    labels: data.labels,
                    datasets: [{{
                        data: data.earnings,
                        borderColor: '#D4AF37',
                        borderWidth: 5,
                        backgroundColor: (ctx) => {{
                            const gradient = ctx.chart.ctx.createLinearGradient(0, 0, 0, 350);
                            gradient.addColorStop(0, 'rgba(212, 175, 55, 0.3)');
                            gradient.addColorStop(1, 'transparent');
                            return gradient;
                        }},
                        tension: 0.45, fill: true, pointRadius: 7, pointHoverRadius: 10,
                        pointBackgroundColor: '#FFF', pointBorderColor: '#D4AF37', pointBorderWidth: 4
                    }}]
                }},
                options: {{
                    ...commonOptions,
                    scales: {{ 
                        y: {{ 
                            grid: {{ color: 'rgba(255,255,255,0.05)' }}, 
                            ticks: {{ padding: 10, color: '#94A3B8', font: {{ weight: 600 }} }} 
                        }},
                        x: {{ 
                            grid: {{ display: false }}, 
                            ticks: {{ 
                                padding: 10, color: '#94A3B8', font: {{ weight: 600 }},
                                maxRotation: 45, minRotation: 45,
                                autoSkip: true, maxTicksLimit: 10
                            }} 
                        }}
                    }}
                }}
            }});

            // 2. Pie Chart (Task Distribution)
            // 3. Task Distribution & Reflections Engine (Synchronized)
            let currentPage = 1;
            const pageSize = 1;
            window.currentSyncDate = data.stats.today_date_raw;
            let pieChart;

            function updateDashboardDate(targetDate) {{
                if (!targetDate) return;
                window.currentSyncDate = targetDate;
                renderPieChart(targetDate);
                renderReflections(targetDate);
                
                // Update all date pickers
                const parts = targetDate.split('-');
                if (parts.length === 3) {{
                    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
                    const monthIdx = monthNames.indexOf(parts[1]);
                    if (monthIdx !== -1) {{
                        const isoDate = `${{parts[2]}}-${{(monthIdx + 1).toString().padStart(2, '0')}}-${{parts[0].padStart(2, '0')}}`;
                        if (document.getElementById('pieDateJump')) document.getElementById('pieDateJump').value = isoDate;
                        if (document.getElementById('refDateJump')) document.getElementById('refDateJump').value = isoDate;
                        if (document.getElementById('dateJump')) document.getElementById('dateJump').value = isoDate;
                    }}
                }}

                // Sync the Log Section
                const allDays = [...data.raw_days].reverse();
                const dayIdx = allDays.findIndex(d => {{
                    const dObj = new Date(d.iso_date);
                    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
                    const dStr = `${{dObj.getDate().toString().padStart(2, '0')}}-${{monthNames[dObj.getMonth()]}}-${{dObj.getFullYear()}}`;
                    return dStr === targetDate;
                }});
                if (dayIdx !== -1) {{
                    currentPage = dayIdx + 1;
                    renderLog();
                }}
            }}

            window.navigatePie = (dir) => {{
                const allDatesInLogs = data.time_logs.map(l => l.date);
                if (!allDatesInLogs.includes(data.stats.today_date_raw)) allDatesInLogs.push(data.stats.today_date_raw);
                
                allDatesInLogs.sort((a,b) => {{
                    const parse = (s) => {{
                        const p = s.split('-');
                        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
                        return new Date(p[2], monthNames.indexOf(p[1]), p[0]);
                    }};
                    return parse(a) - parse(b);
                }});

                let idx = allDatesInLogs.indexOf(currentSyncDate);
                if (idx === -1) idx = allDatesInLogs.length - 1;
                const newIdx = Math.max(0, Math.min(allDatesInLogs.length - 1, idx + dir));
                updateDashboardDate(allDatesInLogs[newIdx]);
            }};

            window.navigateRef = window.navigatePie;

            function renderPieChart(targetDate) {{
                document.getElementById('pieViewedDate').innerText = targetDate;
                const log = data.time_logs.find(l => l.date === targetDate);
                const ctx = document.getElementById('pieChart').getContext('2d');
                const legend = document.getElementById('pieLegend');
                
                if (pieChart) pieChart.destroy();
                
                if (!log || !log.logs || log.logs.length === 0) {{
                    document.getElementById('pieTotalHours').innerText = 'NO DATA FOR THIS DATE';
                    legend.innerHTML = '<div style=\"text-align: center; color: var(--text-dim); padding: 20px;\">[ NO_LOG_ENTRIES ]</div>';
                    return;
                }}
                
                document.getElementById('pieTotalHours').innerText = `${{log.total.toFixed(1)}} HOURS LOGGED`;
                
                const colors = ['#D4AF37', '#800000', '#4A0404', '#B8860B', '#DAA520', '#8B4513', '#5D4037', '#795548'];
                
                pieChart = new Chart(ctx, {{
                    type: 'doughnut',
                    data: {{
                        labels: log.logs.map(l => l.activity),
                        datasets: [{{
                            data: log.logs.map(l => l.hours),
                            backgroundColor: colors.map(c => c + '99'),
                            borderWidth: 2,
                            borderColor: 'rgba(5,5,5,0.5)'
                        }}]
                    }},
                    options: {{
                        ...commonOptions,
                        cutout: '75%',
                        plugins: {{
                            ...commonOptions.plugins,
                            legend: {{ display: false }}
                        }}
                    }}
                }});

                legend.innerHTML = log.logs.map((l, i) => `
                    <div class="legend-item">
                        <div style="display: flex; align-items: center;">
                            <div class="legend-color" style="background: ${{colors[i % colors.length]}}"></div>
                            <span style="font-weight: 800; font-size: 13px;">${{l.activity}}</span>
                        </div>
                        <span style="font-weight: 1000; color: var(--accent);">${{l.hours.toFixed(1)}}h</span>
                    </div>
                `).join('');
            }}

            function renderReflections(targetDate) {{
                document.getElementById('refViewedDate').innerText = targetDate;
                const log = data.time_logs.find(l => l.date === targetDate);
                const area = document.getElementById('reflectionsText');
                
                if (!log || !log.reflections || log.reflections.length === 0) {{
                    area.innerHTML = '<div style=\"padding: 20px; text-align: center; color: var(--text-dim); opacity: 0.5;\">[ NO_REFLECTIONS_RECORDED ]</div>';
                }} else {{
                    area.innerHTML = '<ol style=\"padding-left: 20px; list-style-type: decimal;\">' + 
                        log.reflections.map((ref, idx) => `
                            <li style=\"margin-bottom: 12px; padding-left: 10px;\">
                                <div style=\"display: flex; justify-content: space-between; align-items: flex-start; gap: 15px;\">
                                    <span style=\"flex: 1;\">${{ref}}</span>
                                    <button onclick=\"deleteReflection('${{targetDate}}', ${{idx}})\" 
                                        title=\"Delete Reflection\"
                                        style=\"background: rgba(255,68,68,0.1); border: 1px solid rgba(255,68,68,0.2); color: #FF4444; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; cursor: pointer; font-weight: 800; transition: all 0.3s; flex-shrink: 0; font-size: 16px; line-height: 1;\">×</button>
                                </div>
                            </li>
                        `).join('') + '</ol>';
                }}
                
                const label = document.getElementById('refInputLabel');
                label.innerText = (targetDate === data.stats.today_date_raw) ? 'New Insight for Today' : 'Add Insight for ' + targetDate;
            }}

            const dateJumpHandler = (e) => {{
                const d = new Date(e.target.value);
                const day = d.getDate();
                const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
                const month = monthNames[d.getMonth()];
                const dateStr = `${{day.toString().padStart(2, '0')}}-${{month}}-${{d.getFullYear()}}`;
                updateDashboardDate(dateStr);
            }};

            document.getElementById('pieDateJump').addEventListener('change', dateJumpHandler);
            document.getElementById('refDateJump').addEventListener('change', dateJumpHandler);

            // Initial render
            updateDashboardDate(currentSyncDate);



            // 4. Operational Log Rendering Engine

            function renderLog(filter = '') {{
                const query = filter.toLowerCase();
                const allDays = [...data.raw_days].reverse(); // Show latest first
                const filteredDays = allDays.filter(d => {{
                    if (!query) return true;
                    return d.date.toLowerCase().includes(query) || d.services.some(s => s.toLowerCase().includes(query));
                }});

                const totalPages = Math.ceil(filteredDays.length / pageSize);
                if (currentPage > totalPages) currentPage = Math.max(1, totalPages);

                const start = (currentPage - 1) * pageSize;
                const pagedDays = filteredDays.slice(start, start + pageSize);

                const logHtml = pagedDays.map((d, idx) => {{
                    const actualIdx = start + idx;
                    const isExpanded = true; // Always expand in single-day view
                    return `
                        <div class="day-group" id="day-${{actualIdx}}">
                            <div class="day-header" onclick="toggleDay(${{actualIdx}})" style="cursor: pointer; user-select: none;">
                                <div style="display: flex; align-items: center; gap: 15px;">
                                    <span class="toggle-icon" id="icon-${{actualIdx}}" style="font-size: 14px; color: var(--accent); transition: 0.3s;">${{isExpanded ? '▼' : '▶'}}</span>
                                    <span>${{d.date}}</span>
                                    <span style="font-size: 11px; color: var(--text-dim); background: rgba(255,255,255,0.05); padding: 4px 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); letter-spacing: 1px;">[ ${{d.count}} UNITS ]</span>
                                </div>
                                <span style="color: var(--accent); text-shadow: 0 0 10px var(--glow);">₹${{d.earnings}}</span>
                            </div>
                            <div class="service-log" id="log-${{actualIdx}}" style="display: ${{isExpanded ? 'block' : 'none'}}">
                                ${{(query ? d.services.filter(s => s.toLowerCase().includes(query)) : d.services).map(s => {{
                                    const m = s.match(/^\\d+\\.\\s+\\[(\\d\\d:\\d\\d)\\]\\s+(.*?)\\s+-\\s+(.*?)\\s+-\\s+(\\d+)rs/);
                                    if (m) {{
                                        const name = m[2].trim();
                                        const pkg = m[3].trim();
                                        const uuidMap = {{
                                            'utair': '7fd31965-0477-48fc-82ee-ecf87e4b825e',
                                            'lyft': 'cff30feb-2ec7-4cc1-b5fb-04815c3cb497',
                                            'viya lite': '51b1efb3-13a1-4bdd-82dc-103c69b93ea2',
                                            'jvspinbet': '31742461-826a-4934-89c0-681585257982',
                                            'opentable': 'c34dfb4d-3d83-4176-ba7d-3919b5f07e73'
                                        }};
                                        const uuid = uuidMap[name.toLowerCase()];
                                        const link = uuid ? `http://51.195.24.179:3000/services/${{uuid}}` : `http://51.195.24.179:3000/services?search=${{encodeURIComponent(name)}}`;
                                        
                                        return `
                                        <a href="${{link}}" target="_blank" class="service-link" style="text-decoration: none;">
                                            <div class="service-entry">
                                                <div class="service-info">
                                                    <span class="service-name">${{name}}</span>
                                                    <span class="service-pkg">${{pkg}}</span>
                                                </div>
                                                <div class="service-price">₹${{m[4]}}</div>
                                            </div>
                                        </a>`;
                                    }}
                                    return `<div class="service-entry"><span class="service-name">${{s}}</span></div>`;
                                }}).join('') }}
                            </div>
                        </div>
                    `;
                }}).join('');

                const paginationHtml = totalPages > 1 ? 
                    '<div style="display: flex; justify-content: center; align-items: center; gap: 20px; margin-top: 30px; padding: 20px; border-top: 1px solid var(--border);">' +
                        '<button onclick="changePage(1)" ' + (currentPage === totalPages ? 'disabled' : '') + ' ' +
                            'style="background: rgba(255,255,255,0.05); border: 1px solid var(--border); color: #FFF; padding: 10px 20px; border-radius: 12px; cursor: pointer; font-weight: 700; transition: all 0.3s ease; opacity: ' + (currentPage === totalPages ? '0.3' : '1') + '">PREV</button>' +
                        '<span style="font-weight: 800; letter-spacing: 2px; color: var(--text-dim); font-size: 14px;">DAY ' + currentPage + ' / ' + totalPages + '</span>' +
                        '<button onclick="changePage(-1)" ' + (currentPage === 1 ? 'disabled' : '') + ' ' +
                            'style="background: rgba(255,255,255,0.05); border: 1px solid var(--border); color: #FFF; padding: 10px 20px; border-radius: 12px; cursor: pointer; font-weight: 700; transition: all 0.3s ease; opacity: ' + (currentPage === 1 ? '0.3' : '1') + '">NEXT</button>' +
                    '</div>' : '';

                document.getElementById('log-html').innerHTML = logHtml + paginationHtml || '<div style="text-align:center; padding: 40px; color: var(--text-dim); font-weight: 700;">[ NO_RECORDS_FOUND ]</div>';
            }}

            window.toggleDay = (idx) => {{
                const el = document.getElementById('log-' + idx);
                const icon = document.getElementById('icon-' + idx);
                const isVisible = el.style.display !== 'none';
                el.style.display = isVisible ? 'none' : 'block';
                icon.innerText = isVisible ? '▶' : '▼';
            }};

            window.changePage = (dir) => {{
                currentPage += dir;
                renderLog(document.getElementById('logSearch').value);
                
                // Sync rest of dashboard
                const allDays = [...data.raw_days].reverse();
                const day = allDays[currentPage - 1];
                if (day) {{
                    const dateObj = new Date(day.iso_date);
                    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
                    const dateStr = `${{dateObj.getDate().toString().padStart(2, '0')}}-${{monthNames[dateObj.getMonth()]}}-${{dateObj.getFullYear()}}`;
                    window.currentSyncDate = dateStr;
                    renderPieChart(dateStr);
                    renderReflections(dateStr);
                    
                    // Update all date pickers
                    const iso = day.iso_date;
                    if (document.getElementById('pieDateJump')) document.getElementById('pieDateJump').value = iso;
                    if (document.getElementById('refDateJump')) document.getElementById('refDateJump').value = iso;
                    if (document.getElementById('dateJump')) document.getElementById('dateJump').value = iso;
                }}
                
                document.getElementById('logSearch').scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }};

            document.getElementById('logSearch').addEventListener('input', (e) => {{
                currentPage = 1;
                renderLog(e.target.value);
            }});

            document.getElementById('dateJump').addEventListener('change', (e) => {{
                const selectedDate = e.target.value;
                const foundIdx = data.raw_days.findIndex(d => d.iso_date === selectedDate);
                if (foundIdx !== -1) {{
                    currentPage = Math.floor(foundIdx / pageSize) + 1;
                    renderLog();
                    document.getElementById('logSearch').scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}
            }});
            
            // Initial render
            renderLog();
        }}

        function copyReflection() {{
            const text = document.getElementById('newReflectionText').value;
            if (!text) return;
            
            // 1. Immediate UI update
            const logArea = document.getElementById('reflectionsText');
            let list = logArea.querySelector('ol');
            if (!list) {{
                logArea.innerHTML = `<ol style=\"padding-left: 20px; list-style-type: decimal;\"></ol>`;
                list = logArea.querySelector('ol');
            }}
            const li = document.createElement('li');
            li.style.marginBottom = '12px';
            li.style.paddingLeft = '10px';
            li.style.opacity = '0.7';
            li.innerHTML = `
                <div style=\"display: flex; justify-content: space-between; align-items: flex-start; gap: 15px;\">
                    <span style=\"flex: 1;\">${{text}} <small style=\"color: var(--accent); opacity: 0.8; margin-left: 5px;\">(Sync Pending...)</small></span>
                    <button style=\"background: rgba(255,255,255,0.05); border: 1px solid var(--border); color: var(--text-dim); border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; cursor: not-allowed; font-weight: 800; font-size: 16px; line-height: 1;\">×</button>
                </div>
            `;
            list.appendChild(li);

            // 2. Save to "Database" (GitHub Issue)
            saveToRemoteDatabase(text, window.currentSyncDate);
            
            // 3. UI Feedback on button
            const btn = document.querySelector('[onclick=\"copyReflection()\"]');
            const oldText = btn.innerText;
            btn.innerText = 'SAVED TO DB!';
            btn.style.background = '#00FF00';
            btn.style.color = '#000';
            setTimeout(() => {{
                btn.innerText = oldText;
                btn.style.background = '';
                btn.style.color = '';
                document.getElementById('newReflectionText').value = '';
            }}, 2000);
        }}

        async function saveToRemoteDatabase(text, date) {{
            let token = localStorage.getItem('gh_token');
            if (!token) {{
                token = prompt('Please enter your GitHub PAT (repo scope) to save to DB:');
                if (token) localStorage.setItem('gh_token', token);
            }}
            if (!token) return;

            const url = 'https://api.github.com/repos/Githubds12/service-progress-dashboard/issues/1/comments';
            try {{
                const command = `ADD_REF: Date: ${{date}}, Text: ${{text}}`;
                const res = await fetch(url, {{
                    method: 'POST',
                    headers: {{
                        'Authorization': `token ${{token}}`,
                        'Accept': 'application/vnd.github.v3+json',
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{ body: command }})
                }});
                if (res.ok) console.log('Successfully saved to remote DB');
                else if (res.status === 401) localStorage.removeItem('gh_token');
            }} catch (e) {{
                console.error('Save to DB failed:', e);
            }}
        }}

        async function deleteReflection(date, index) {{
            if (!confirm('Are you sure you want to delete this reflection?')) return;
            
            let token = localStorage.getItem('gh_token');
            if (!token) {{
                token = prompt('Please enter your GitHub PAT (repo scope) to authorize deletion:');
                if (token) localStorage.setItem('gh_token', token);
            }}
            if (!token) return;

            const command = `DELETE_REF: Date: ${{date}}, Index: ${{index}}`;
            const url = 'https://api.github.com/repos/Githubds12/service-progress-dashboard/issues/1/comments';
            
            try {{
                const res = await fetch(url, {{
                    method: 'POST',
                    headers: {{
                        'Authorization': `token ${{token}}`,
                        'Accept': 'application/vnd.github.v3+json',
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{ body: command }})
                }});
                if (res.ok) {{
                    alert('Deletion request sent. It will be removed in the next sync (15 mins).');
                    // Visually remove it for the current session
                    const area = document.getElementById('reflectionsText');
                    const items = area.querySelectorAll('li');
                    if (items[index]) items[index].style.opacity = '0.3';
                }}
            }} catch (e) {{
                console.error('Delete request failed:', e);
            }}
        }}

        initDashboard(data);
    </script>
</body>
</html>"""
    
    # Save files
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
        if 'note' in log and log['note']:
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
