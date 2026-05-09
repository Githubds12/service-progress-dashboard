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

def sync_github_commands():
    token = os.getenv("GITHUB_TOKEN")
    if not token: return
    
    url = "https://api.github.com/repos/Githubds12/service-progress-dashboard/issues/1/comments"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200: return
        
        comments = response.json()
        if not comments: return
        
        # Load Logs for reflections
        log_path = TIME_LOG_FILE
        lines = []
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        
        # Load APK DB
        apk_db_path = r"C:\HTB-Notes-Portal\apk_local_database.json"
        apk_db = None
        if os.path.exists(apk_db_path):
            with open(apk_db_path, 'r', encoding='utf-8') as f:
                apk_db = json.load(f)

        processed_count = 0
        apk_updated = False
        
        for comment in comments:
            body = comment['body'].strip()
            
            # --- HANDLE APK UPDATES ---
            if body.startswith("APK_UPDATE:"):
                if apk_db:
                    m_id = re.search(r'ID:\s*(.*?),', body)
                    m_field = re.search(r'Field:\s*(.*?),', body)
                    m_val = re.search(r'Value:\s*(.*)', body)
                    if m_id and m_field and m_val:
                        tid, field, val_str = m_id.group(1).strip(), m_field.group(1).strip(), m_val.group(1).strip()
                        val = True if val_str.lower() == 'true' else False if val_str.lower() == 'false' else val_str
                        if field == 'note': apk_db.setdefault('notes', {})[tid] = val
                        elif field == 'claimed': apk_db.setdefault('claimed', {})[tid] = val
                        elif field == 'root_detected': apk_db.setdefault('root_detected', {})[tid] = val
                        elif field == 'not_found': apk_db.setdefault('not_found', {})[tid] = val
                        apk_db.setdefault('last_updated', {})[tid] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        apk_updated = True
                requests.delete(comment['url'], headers=headers)
                processed_count += 1
                continue

            # --- HANDLE REFLECTION DELETIONS ---
            if body.startswith("DELETE_REF:"):
                try:
                    m_date = re.search(r'Date:\s*(.*?)(?:,|$)', body)
                    m_idx = re.search(r'Index:\s*(\d+)', body)
                    if m_date and m_idx:
                        target_date, target_idx = m_date.group(1).strip(), int(m_idx.group(1))
                        for i, line in enumerate(lines):
                            if line.startswith("Date:") and target_date in line:
                                for j in range(i + 1, len(lines)):
                                    if lines[j].startswith("Date:"): break
                                    if lines[j].strip().startswith("Reflections:"):
                                        content = lines[j].split("Reflections:")[1].strip()
                                        items = [it.strip() for it in re.split(r'\s*\d+\.\s*', content) if it.strip()]
                                        if 0 <= target_idx < len(items):
                                            items.pop(target_idx)
                                            lines[j] = "Reflections: " + " ".join([f"{k+1}. {it}" for k, it in enumerate(items)]) + "\n" if items else "Reflections:\n"
                                        break
                                break
                except: pass
                requests.delete(comment['url'], headers=headers)
                processed_count += 1
                continue

            # --- HANDLE REFLECTION ADDITIONS (Default) ---
            target_date, text = "", body
            if body.startswith("ADD_REF:"):
                m_date = re.search(r'Date:\s*(.*?),\s*Text:\s*(.*)', body, re.DOTALL)
                if m_date: target_date, text = m_date.group(1).strip(), m_date.group(2).strip()
            
            target_idx = -1
            if target_date:
                for i, line in enumerate(lines):
                    if line.startswith("Date:") and target_date in line:
                        target_idx = i; break
            if target_idx == -1:
                for i, line in enumerate(lines):
                    if line.startswith("Date:"): target_idx = i
            
            if target_idx != -1:
                ref_line_idx = -1
                for j in range(target_idx + 1, len(lines)):
                    if lines[j].startswith("Date:"): break
                    if lines[j].strip().startswith("Reflections:"): ref_line_idx = j; break
                
                if ref_line_idx != -1:
                    content = lines[ref_line_idx].split("Reflections:")[1].strip()
                    items = [it.strip() for it in re.split(r'\s*\d+\.\s*', content) if it.strip()]
                    items.append(text)
                    lines[ref_line_idx] = "Reflections: " + " ".join([f"{k+1}. {it}" for k, it in enumerate(items)]) + "\n"
                else:
                    lines.insert(target_idx + 1, f"Reflections: 1. {text}\n")
            else:
                lines.append(f"\nDate: {target_date if target_date else datetime.now().strftime('%d-%m-%Y')}\n")
                lines.append(f"Reflections: 1. {text}\n")
            
            requests.delete(comment['url'], headers=headers)
            processed_count += 1

        # Save Changes
        if lines:
            with open(log_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        if apk_updated and apk_db:
            with open(apk_db_path, 'w', encoding='utf-8') as f:
                json.dump(apk_db, f, indent=4)
            # Re-generate the APK JS data
            import sys
            subprocess.run([sys.executable, os.path.join(REPORT_DIR, "scripts", "sync_apkhunter.py")])

        print(f"Synced {processed_count} commands from GitHub.")
    except Exception as e:
        print(f"Error syncing GitHub commands: {e}")


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
                    match = re.search(r'-\s*(.*?):\s*(\d+\.?\d*)\s*h', line, re.IGNORECASE)
                    if match:
                        act, h = match.groups()
                        logs.append({'activity': act.strip(), 'hours': float(h)})
                        total_h += float(h)
            
            ref_match = re.search(r'Reflections:\s*(.*?)(?=\nDate:|$)', entry, re.DOTALL | re.IGNORECASE)
            ref_raw = ref_match.group(1).strip() if ref_match else ""
            
            ref_items = re.split(r'\s*\d+\.\s*', ref_raw)
            ref_items = [it.strip() for it in ref_items if it.strip()]

            if logs or ref_items:
                iso_date = ""
                m_iso = re.search(r'(\d{2})-(\d{2})-(\d{4})', date_str)
                if m_iso: iso_date = f"{m_iso.group(3)}-{m_iso.group(2)}-{m_iso.group(1)}"
                days.append({'date': date_str, 'iso_date': iso_date, 'logs': logs, 'total': total_h, 'reflections': ref_items})
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
        'today_date_raw': today_dt.strftime('%Y-%m-%d'),
        'projection_sentence': explanation
    }

def update_txt(body, stats):
    new_stats = f"\nDashboard Stats:\n- Total Services: {stats['total_services']}\n- Total Earnings: {stats['total_earnings']} rs\n- Average Daily Earning: {stats['avg_daily']} rs/day\n- Average Daily Services: {stats['avg_daily_services']} services/day\n- Recovery Pace: {stats['recovery_pace_services']} Services / day\n- Projected Monthly Total: ₹{stats['projected_total']}\n"
    with open(TXT_FILE, 'w', encoding='utf-8') as f:
        f.write(body + "\n\n" + new_stats.strip() + "\n")

def update_html(header, days, stats, complexity_stats=None):
    # Load .env manually if not in environment
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        env_path = os.path.join(os.getcwd(), ".env")
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith("GITHUB_TOKEN="):
                        token = line.split("=", 1)[1].strip()
                        os.environ["GITHUB_TOKEN"] = token
    time_logs = parse_time_log()
    
    # Sort days by date for charts
    chart_days = sorted([d for d in days if d['iso_date']], key=lambda x: x['iso_date'])
    trend_labels = [d['date'].split(',')[0] for d in chart_days]
    trend_earnings = [d['earnings'] for d in chart_days]
    trend_counts = [d['count'] for d in chart_days]
    
    data_dict = {
        'services': days,
        'logs': time_logs,
        'today': stats['today_date_raw'],
        'stats': stats,
        'complexity': complexity_stats
    }

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Operational Intelligence Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #05070a;
            --card-bg: #0d1117;
            --accent-primary: #00f2ff;
            --accent-secondary: #7000ff;
            --text-main: #e6edf3;
            --text-dim: #8b949e;
            --border-color: #30363d;
            --success: #238636;
            --danger: #da3633;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            overflow-x: hidden;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 30px;
        }}
        .logo {{ font-family: 'Orbitron', sans-serif; font-size: 1.5rem; color: var(--accent-primary); text-transform: uppercase; letter-spacing: 2px; }}
        .header-meta {{ text-align: right; font-family: 'Orbitron', sans-serif; font-size: 0.9rem; color: var(--text-dim); }}
        
        /* Dashboard Grid */
        .dashboard-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px; 
        }}
        .stat-card {{
            background: var(--card-bg);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            transition: transform 0.2s;
        }}
        .stat-card:hover {{ transform: translateY(-5px); border-color: var(--accent-primary); }}
        .stat-label {{ color: var(--text-dim); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }}
        .stat-value {{ font-family: 'Orbitron', sans-serif; font-size: 1.8rem; margin: 10px 0; color: var(--accent-primary); }}
        .stat-sub {{ font-size: 0.85rem; display: flex; align-items: center; gap: 5px; }}
        .up {{ color: #3fb950; }}
        .down {{ color: #f85149; }}

        /* Main Content Layout */
        .main-layout {{ display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }}
        .chart-card {{
            background: var(--card-bg);
            padding: 25px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            margin-bottom: 20px;
            max-height: 600px;
            overflow-y: auto;
            scrollbar-width: thin;
            scrollbar-color: var(--border-color) transparent;
        }}
        .chart-card::-webkit-scrollbar {{ width: 6px; }}
        .chart-card::-webkit-scrollbar-thumb {{ background-color: var(--border-color); border-radius: 10px; }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            position: sticky;
            top: -25px;
            background: var(--card-bg);
            padding: 10px 0;
            z-index: 10;
        }}
        .card-title {{ font-family: 'Orbitron', sans-serif; font-size: 1.1rem; color: var(--accent-primary); }}
        
        /* Interactive Elements */
        .controls {{ display: flex; gap: 10px; flex-wrap: wrap; }}
        .btn {{
            background: #21262d;
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            transition: 0.2s;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            white-space: nowrap;
        }}
        .btn:hover:not(:disabled) {{ background: #30363d; border-color: var(--accent-primary); }}
        .btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}
        .btn-primary {{ background: var(--accent-primary); color: #000; border: none; font-weight: 600; }}
        .btn-primary:hover:not(:disabled) {{ background: #00d8e6; }}
        
        .date-picker {{
            background: #0d1117;
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 5px 10px;
            border-radius: 6px;
            font-family: 'Inter', sans-serif;
        }}

        /* Activity Log Table */
        .log-table-wrapper {{ overflow-x: auto; }}
        .log-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; min-width: 400px; }}
        .log-table th {{ text-align: left; padding: 12px; border-bottom: 2px solid var(--border-color); color: var(--text-dim); font-size: 0.85rem; }}
        .log-table td {{ padding: 12px; border-bottom: 1px solid var(--border-color); font-size: 0.9rem; }}
        .log-table tr:hover {{ background: #161b22; }}
        
        /* Reflections Section */
        .ref-input-group {{ display: flex; gap: 10px; margin-top: 20px; }}
        .ref-input {{
            flex: 1;
            background: #0d1117;
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 10px;
            border-radius: 6px;
            font-family: 'Inter', sans-serif;
            min-width: 0;
        }}
        .ref-list {{ margin-top: 20px; list-style: none; }}
        .ref-item {{
            background: #161b22;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-left: 3px solid var(--accent-secondary);
            gap: 10px;
        }}
        .ref-item span:first-child {{ flex: 1; word-break: break-word; }}
        .ref-actions {{ display: flex; gap: 10px; }}
        .ref-edit {{ color: var(--accent-primary); cursor: pointer; opacity: 0.7; font-size: 0.8rem; white-space: nowrap; }}
        .ref-delete {{ color: var(--danger); cursor: pointer; opacity: 0.7; font-size: 0.8rem; white-space: nowrap; }}
        .ref-edit:hover, .ref-delete:hover {{ opacity: 1; }}

        /* Tip of the day */
        .tip-banner {{
            background: linear-gradient(90deg, #0d1117, #161b22);
            border: 1px solid var(--border-color);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 30px;
            border-left: 4px solid var(--accent-primary);
        }}
        .tip-header {{ font-family: 'Orbitron', sans-serif; color: var(--accent-primary); margin-bottom: 5px; display: flex; align-items: center; gap: 10px; }}
        
        #syncStatus {{ font-size: 0.75rem; font-weight: bold; padding: 2px 8px; border-radius: 10px; }}
        .status-ready {{ background: var(--success); color: #fff; }}
        .status-syncing {{ background: var(--accent-secondary); color: #fff; }}
        .status-error {{ background: var(--danger); color: #fff; }}

        /* Mobile Adjustments */
        @media (max-width: 1000px) {{
            .main-layout {{ grid-template-columns: 1fr; }}
            .container {{ padding: 15px; }}
        }}
        @media (max-width: 600px) {{
            header {{ flex-direction: column; align-items: flex-start; gap: 15px; }}
            .header-meta {{ text-align: left; }}
            .stat-value {{ font-size: 1.5rem; }}
            .tip-header {{ font-size: 0.9rem; }}
            .logo {{ font-size: 1.2rem; }}
            .ref-input-group {{ flex-direction: column; }}
            .btn {{ width: 100%; justify-content: center; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">Operational Intelligence <a href="apkhunter.html" style="margin-left: 20px; font-size: 0.8rem; text-decoration: none; color: var(--accent-primary); border: 1px solid var(--accent-primary); padding: 4px 10px; border-radius: 4px; vertical-align: middle;">APK HUNTER</a></div>
            <div class="header-meta">
                <div>DATE: <span id="currentHeaderDate">{stats['today_date']}</span></div>
                <div style="margin-top: 5px;"><span id="syncStatus" class="status-ready">READY</span></div>
            </div>
        </header>

        <div class="tip-banner">
            <div class="tip-header">✨ {stats['explanation'].split(' ')[0] if ' ' in stats['explanation'] else 'ADVICE'}</div>
            <p id="projectionText">{stats['explanation']}</p>
        </div>

        <div class="dashboard-grid">
            <div class="stat-card">
                <div class="stat-label">Total Services</div>
                <div class="stat-value">{stats['total_services']}</div>
                <div class="stat-sub up">↑ {stats['total_services'] - 12} vs last sync</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Earnings</div>
                <div class="stat-value">₹{stats['total_earnings']:,}</div>
                <div class="stat-sub up">↑ Current: ₹{stats['total_earnings']}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Pace Required</div>
                <div class="stat-value">{stats['recovery_pace_services']}</div>
                <div class="stat-sub">Monthly Target: ₹90,000</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Recommendation</div>
                <div class="stat-value">{stats['recommended_today']}</div>
                <div class="stat-sub">Services to complete today</div>
            </div>
        </div>

        <div class="main-layout">
            <div class="content-left">
                <div class="chart-card">
                    <div class="card-header">
                        <div class="card-title">REVENUE TRAJECTORY</div>
                        <div class="controls">
                            <input type="date" id="dateJump" class="date-picker">
                            <button class="btn" onclick="window.navTrajectory('prev')">PREVIOUS TRAJECTORY</button>
                        </div>
                    </div>
                    <canvas id="revenueChart" height="150"></canvas>
                </div>

                <div class="chart-card">
                    <div class="card-header">
                        <div class="card-title">OPERATIONAL INTELLIGENCE LOG</div>
                        <div class="controls">
                            <input type="date" id="logDateJump" class="date-picker">
                        </div>
                    </div>
                    <div class="log-table-wrapper" id="serviceLogContainer">
                        <table class="log-table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Activity / Task</th>
                                </tr>
                            </thead>
                            <tbody id="serviceLogBody">
                                <!-- Dynamic -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="content-right">
                <div class="chart-card">
                    <div class="card-header">
                        <div class="card-title">EFFORT DISTRIBUTION</div>
                        <div class="controls">
                            <input type="date" id="pieDateJump" class="date-picker">
                        </div>
                    </div>
                    <canvas id="effortPieChart" height="250"></canvas>
                    <div id="noDataMessage" style="display:none; text-align:center; padding: 20px; color: var(--text-dim);">No time logs for this date</div>
                </div>

                <div class="chart-card">
                    <div class="card-header">
                        <div class="card-title">STRATEGIC REFLECTIONS</div>
                    </div>
                    <div class="ref-input-group">
                        <input type="text" id="reflectionInput" class="ref-input" placeholder="Add observation...">
                        <button id="saveBtn" class="btn btn-primary" onclick="window.saveReflection()">SAVE</button>
                    </div>
                    <ul id="reflectionList" class="ref-list">
                        <!-- Dynamic -->
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <script>
        // --- GLOBAL DATA & STATE ---
        window.dashboardData = {json.dumps(data_dict)};
        window.state = {{
            currentDate: window.dashboardData.today,
            isSyncing: false,
            editingIdx: null
        }};

        // --- UTILS ---
        const $ = id => document.getElementById(id);
        const formatLongDate = iso => {{
            const d = new Date(iso);
            return d.toLocaleDateString('en-GB', {{ day:'numeric', month:'long', year:'numeric', weekday:'long' }});
        }};

        // --- UI RENDERERS ---
        window.renderCharts = () => {{
            const targetDate = window.state.currentDate;
            
            // 1. Revenue Trend Chart (Full History)
            const trendCtx = $('revenueChart').getContext('2d');
            if (window.revenueChartInst) window.revenueChartInst.destroy();
            
            const trendDays = window.dashboardData.services.filter(d => d.iso_date).sort((a,b) => a.iso_date.localeCompare(b.iso_date));
            window.revenueChartInst = new Chart(trendCtx, {{
                type: 'line',
                data: {{
                    labels: trendDays.map(d => d.date.split(',')[0]),
                    datasets: [{{
                        label: 'Earnings (RS)',
                        data: trendDays.map(d => d.earnings),
                        borderColor: '#00f2ff',
                        backgroundColor: 'rgba(0, 242, 255, 0.1)',
                        fill: true,
                        tension: 0.4
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{ grid: {{ color: '#30363d' }}, ticks: {{ color: '#8b949e' }} }},
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#8b949e' }} }}
                    }}
                }}
            }});

            // 2. Effort Pie Chart (Selected Date)
            const pieCtx = $('effortPieChart').getContext('2d');
            if (window.pieChartInst) window.pieChartInst.destroy();
            
            const logEntry = window.dashboardData.logs.find(l => l.iso_date === targetDate);
            if (!logEntry || !logEntry.logs.length) {{
                $('effortPieChart').style.display = 'none';
                $('noDataMessage').style.display = 'block';
            }} else {{
                $('effortPieChart').style.display = 'block';
                $('noDataMessage').style.display = 'none';
                
                window.pieChartInst = new Chart(pieCtx, {{
                    type: 'doughnut',
                    data: {{
                        labels: logEntry.logs.map(l => l.activity),
                        datasets: [{{
                            data: logEntry.logs.map(l => l.hours),
                            backgroundColor: ['#00f2ff', '#7000ff', '#3fb950', '#f85149', '#db6d28', '#e3b341'],
                            borderWidth: 0,
                            hoverOffset: 15
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{ 
                            legend: {{ 
                                position: 'bottom', 
                                labels: {{ 
                                    color: '#e6edf3', 
                                    padding: 20,
                                    font: {{ size: 12 }}
                                }} 
                            }} 
                        }},
                        cutout: '70%'
                    }}
                }});
            }}
        }};

        window.renderLogsAndReflections = () => {{
            const targetDate = window.state.currentDate;
            
            // Render Service Logs
            const serviceDay = window.dashboardData.services.find(d => d.iso_date === targetDate);
            const logBody = $('serviceLogBody');
            logBody.innerHTML = '';
            
            if (serviceDay && serviceDay.services.length) {{
                serviceDay.services.forEach(line => {{
                    const match = line.match(/^(\d+)\.(.*)/);
                    if (match) {{
                        const row = `<tr><td>${{match[1]}}</td><td>${{match[2].trim()}}</td></tr>`;
                        logBody.insertAdjacentHTML('beforeend', row);
                    }}
                }});
            }} else {{
                logBody.innerHTML = '<tr><td colspan="2" style="text-align:center; color:var(--text-dim);">No services recorded for this date</td></tr>';
            }}

            // Render Reflections
            const refEntry = window.dashboardData.logs.find(l => l.iso_date === targetDate);
            const refList = $('reflectionList');
            refList.innerHTML = '';
            
            if (refEntry && refEntry.reflections.length) {{
                refEntry.reflections.forEach((text, idx) => {{
                    const li = document.createElement('li');
                    li.className = 'ref-item';
                    li.innerHTML = `<span>${{text}}</span>
                                   <div class="ref-actions">
                                       <span class="ref-edit" onclick="window.editReflection(${{idx}})">EDIT</span>
                                       <span class="ref-delete" onclick="window.deleteReflection(${{idx}})">DELETE</span>
                                   </div>`;
                    refList.appendChild(li);
                }});
            }} else {{
                refList.innerHTML = '<li style="color:var(--text-dim); font-size:0.9rem;">No reflections yet. Add your first one above.</li>';
            }}
        }};

        window.jumpToDate = (isoDate) => {{
            if (!isoDate) return;
            window.state.currentDate = isoDate;
            
            // Sync all jump inputs
            $('dateJump').value = isoDate;
            $('logDateJump').value = isoDate;
            $('pieDateJump').value = isoDate;
            
            // Update Header
            const serviceDay = window.dashboardData.services.find(d => d.iso_date === isoDate);
            $('currentHeaderDate').innerText = serviceDay ? serviceDay.date : formatLongDate(isoDate);
            
            window.renderCharts();
            window.renderLogsAndReflections();
        }};

        window.navTrajectory = (dir) => {{
            const trendDays = window.dashboardData.services.filter(d => d.iso_date).sort((a,b) => a.iso_date.localeCompare(b.iso_date));
            const curIdx = trendDays.findIndex(d => d.iso_date === window.state.currentDate);
            let nextIdx = dir === 'prev' ? curIdx - 1 : curIdx + 1;
            
            if (nextIdx >= 0 && nextIdx < trendDays.length) {{
                window.jumpToDate(trendDays[nextIdx].iso_date);
            }}
        }};

        // --- GITHUB SYNC LOGIC ---
        window.updateSyncStatus = (status) => {{
            const el = $('syncStatus');
            el.className = '';
            if (status === 'syncing') {{ el.innerText = 'SYNCING...'; el.classList.add('status-syncing'); }}
            else if (status === 'error') {{ el.innerText = 'SYNC ERROR'; el.classList.add('status-error'); }}
            else {{ el.innerText = 'READY'; el.classList.add('status-ready'); }}
        }};

        window.pushToGitHub = async (message) => {{
            const token = localStorage.getItem('github_token');
            if (!token) {{
                const t = prompt("Enter GitHub PAT for Sync:");
                if (t) localStorage.setItem('github_token', t);
                else return false;
            }}
            
            window.state.isSyncing = true;
            window.updateSyncStatus('syncing');
            $('saveBtn').disabled = true;

            try {{
                const response = await fetch("https://api.github.com/repos/Githubds12/service-progress-dashboard/issues/1/comments", {{
                    method: "POST",
                    headers: {{ "Authorization": `token ${{token}}`, "Accept": "application/vnd.github.v3+json" }},
                    body: JSON.stringify({{ body: message }})
                }});
                if (response.ok) {{
                    window.updateSyncStatus('ready');
                    return true;
                }} else {{ throw new Error("API Failure"); }}
            }} catch (e) {{
                window.updateSyncStatus('error');
                console.error(e);
                return false;
            }} finally {{
                window.state.isSyncing = false;
                $('saveBtn').disabled = false;
            }}
        }};

        window.editReflection = (idx) => {{
            const targetDate = window.state.currentDate;
            const logEntry = window.dashboardData.logs.find(l => l.iso_date === targetDate);
            if (!logEntry) return;

            $('reflectionInput').value = logEntry.reflections[idx];
            $('saveBtn').innerText = 'UPDATE';
            window.state.editingIdx = idx;
            $('reflectionInput').focus();
        }};

        window.saveReflection = async () => {{
            const text = $('reflectionInput').value.trim();
            if (!text) return;
            
            const targetDate = window.state.currentDate;
            const logDateStr = targetDate.split('-').reverse().join('-'); // DD-MM-YYYY
            const isEditing = window.state.editingIdx !== null;
            const oldIdx = window.state.editingIdx;

            // Optimistic Update
            let logEntry = window.dashboardData.logs.find(l => l.iso_date === targetDate);
            if (!logEntry) {{
                logEntry = {{ iso_date: targetDate, date: logDateStr, logs: [], reflections: [], total: 0 }};
                window.dashboardData.logs.push(logEntry);
            }}

            if (isEditing) {{
                // Delete old, then add new
                const deleteCmd = `DELETE_REF: Date: ${{logDateStr}}, Index: ${{oldIdx}}`;
                logEntry.reflections.splice(oldIdx, 1);
                
                // Add new at the same place or end? Let's add at end for simplicity
                logEntry.reflections.push(text);
                
                window.renderLogsAndReflections();
                $('reflectionInput').value = '';
                $('saveBtn').innerText = 'SAVE';
                window.state.editingIdx = null;

                await window.pushToGitHub(deleteCmd);
                const addCmd = `ADD_REF: Date: ${{logDateStr}}, Text: ${{text}}`;
                await window.pushToGitHub(addCmd);
            }} else {{
                logEntry.reflections.push(text);
                window.renderLogsAndReflections();
                $('reflectionInput').value = '';

                const cmd = `ADD_REF: Date: ${{logDateStr}}, Text: ${{text}}`;
                await window.pushToGitHub(cmd);
            }}
        }};

        window.deleteReflection = async (idx) => {{
            const targetDate = window.state.currentDate;
            const logEntry = window.dashboardData.logs.find(l => l.iso_date === targetDate);
            if (!logEntry) return;

            const logDateStr = targetDate.split('-').reverse().join('-');
            
            // Optimistic Delete
            logEntry.reflections.splice(idx, 1);
            window.renderLogsAndReflections();

            // Remote Sync
            const cmd = `DELETE_REF: Date: ${{logDateStr}}, Index: ${{idx}}`;
            await window.pushToGitHub(cmd);
        }};

        // --- INITIALIZATION ---
        window.addEventListener('DOMContentLoaded', () => {{
            const today = window.dashboardData.today;
            $('dateJump').value = today;
            $('logDateJump').value = today;
            $('pieDateJump').value = today;
            
            // Bind input changes
            $('dateJump').onchange = (e) => window.jumpToDate(e.target.value);
            $('logDateJump').onchange = (e) => window.jumpToDate(e.target.value);
            $('pieDateJump').onchange = (e) => window.jumpToDate(e.target.value);

            window.jumpToDate(today);
        }});
    </script>
</body>
</html>"""
    
    # Save files
    # Save dashboard files
    for f_path in [os.path.join(REPORT_DIR, "dashboard", "Dashboard_Live.html"), os.path.join(REPORT_DIR, "dashboard", "Dashboard.html")]:
        with open(f_path, 'w', encoding='utf-8') as f: f.write(html_content)
    
    # Save root index file with adjusted path
    index_path = os.path.join(REPORT_DIR, "index.html")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content.replace('href="apkhunter.html"', 'href="dashboard/apkhunter.html"'))
    
    data_js = f"window.GH_TOKEN_INJECTED = '';\nwindow.dashboardData = {json.dumps(data_dict)};"
    for f_path in [os.path.join(REPORT_DIR, "dashboard", "dashboard_data.js"), os.path.join(REPORT_DIR, "dashboard_data.js")]:
        with open(f_path, 'w', encoding='utf-8') as f: f.write(data_js)

def update_readme(stats, time_logs):
    path = os.path.join(REPORT_DIR, 'README.md')
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f: content = f.read()
    sec = f"## 📉 Live Stats\n- **Total Earnings**: ₹{stats['total_earnings']}\n- **Average Daily**: ₹{stats['avg_daily']}/day\n- **Monthly Projection**: ₹{stats['projected_total']}\n"
    if time_logs:
        # Find today's log or last log
        log = next((l for l in time_logs if l['iso_date'] == stats['today_date_raw']), time_logs[-1] if time_logs else None)
        if log:
            sec += f"\n## ⏳ Productivity Today ({log['date']})\n"
            for e in log['logs']: sec += f"- **{e['activity']}**: {e['hours']}h\n"
            if 'reflections' in log and log['reflections']:
                sec += f"- **Latest Reflection**: *{log['reflections'][-1]}*\n"
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
    # Sync first to pick up any remote changes
    sync_github_commands()
    
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
    print("Dashboard updated successfully.")

if __name__ == "__main__":
    main()
