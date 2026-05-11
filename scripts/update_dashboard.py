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

MASTERY_LOG_PATH = r"c:\Users\Gorri\Documents\Reports\data\research_heat.json"
MASTERY_JS_PATH = r"c:\Users\Gorri\Documents\Reports\dashboard\mastery_data.js"

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

            # --- HANDLE SMS HISTORY LOGS ---
            if body.startswith("APK_MSG_LOG:"):
                m_id = re.search(r'ID:\s*(.*?),', body)
                m_msg = re.search(r'Message:\s*(.*)', body, re.DOTALL)
                if m_id and m_msg:
                    tid, msg = m_id.group(1).strip(), m_msg.group(2).strip() if m_msg.lastindex >= 2 else m_msg.group(1).strip()
                    history_path = r"C:\HTB-Notes-Portal\sms_history.json"
                    history = {}
                    if os.path.exists(history_path):
                        with open(history_path, 'r', encoding='utf-8') as f: history = json.load(f)
                    
                    logs = history.get(tid, [])
                    # Avoid duplicates
                    if not logs or logs[-1].get('message') != msg:
                        logs.append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "message": msg})
                        history[tid] = logs[-20:] # Keep last 20
                        with open(history_path, 'w', encoding='utf-8') as f: json.dump(history, f, indent=4)
                        apk_updated = True # Trigger regeneration to include history
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
        if line.startswith('### 7th May') or line.startswith('### Current'):
            is_history = False
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
    
    # Calculate Total Claimed APKs
    apk_claimed_count = 0
    apk_data_path = os.path.join(REPORT_DIR, "dashboard", "apkhunter_data.js")
    if os.path.exists(apk_data_path):
        try:
            with open(apk_data_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Find the JSON part: window.apkhunterData = [...]
                match = re.search(r'window\.apkhunterData\s*=\s*(\[.*\])', content, re.DOTALL)
                if match:
                    apk_list = json.loads(match.group(1))
                    apk_claimed_count = sum(1 for item in apk_list if item.get('claimed'))
        except: pass

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
        'apk_claimed': apk_claimed_count,
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
    
    # Load Mastery Heat Data
    mastery_data = []
    if os.path.exists(MASTERY_LOG_PATH):
        try:
            with open(MASTERY_LOG_PATH, 'r', encoding='utf-8') as f:
                mastery_data = json.load(f)
        except: pass

    # Export Mastery JS for APK Hunter
    with open(MASTERY_JS_PATH, 'w', encoding='utf-8') as f:
        f.write(f"window.masteryData = {json.dumps(mastery_data)};")

    data_dict = {
        'services': days,
        'logs': time_logs,
        'today': stats['today_date_raw'],
        'stats': stats,
        'complexity': complexity_stats,
        'mastery': mastery_data
    }

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Operational Intelligence Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #030508;
            --card-bg: rgba(13, 17, 23, 0.7);
            --accent-primary: #00f2ff;
            --accent-secondary: #7000ff;
            --text-main: #e6edf3;
            --text-dim: #8b949e;
            --border-color: #30363d;
            --success: #238636;
            --danger: #da3633;
            --glass-bg: rgba(10, 10, 10, 0.8);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(circle at 50% 0%, rgba(0, 242, 255, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 0% 100%, rgba(112, 0, 255, 0.05) 0%, transparent 50%);
            color: var(--text-main);
            font-family: 'Outfit', sans-serif;
            line-height: 1.6;
            overflow-x: hidden;
            min-height: 100vh;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 30px; position: relative; z-index: 1; }}
        
        /* Background Grid */
        .grid-bg {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-image: linear-gradient(var(--border-color) 1px, transparent 1px),
                              linear-gradient(90deg, var(--border-color) 1px, transparent 1px);
            background-size: 60px 60px;
            z-index: -1; opacity: 0.05; pointer-events: none;
        }}

        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }}
        .logo {{ font-family: 'Orbitron', sans-serif; font-size: 1.5rem; color: var(--accent-primary); text-transform: uppercase; letter-spacing: 3px; text-shadow: 0 0 10px var(--accent-primary); }}
        .header-meta {{ text-align: right; font-family: 'Orbitron', sans-serif; font-size: 0.85rem; color: var(--text-dim); }}
        
        /* Dashboard Grid */
        .dashboard-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px; 
        }}
        .stat-card {{
            background: var(--card-bg);
            padding: 25px;
            border-radius: 16px;
            border: 1px solid var(--border-color);
            backdrop-filter: blur(15px);
            transition: 0.3s cubic-bezier(0.19, 1, 0.22, 1);
        }}
        .stat-card:hover {{ transform: translateY(-5px); border-color: var(--accent-primary); box-shadow: 0 10px 30px rgba(0,0,0,0.4); }}
        .stat-label {{ color: var(--text-dim); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; }}
        .stat-value {{ font-family: 'Orbitron', sans-serif; font-size: 2rem; margin: 10px 0; color: #fff; }}
        .stat-sub {{ font-size: 0.8rem; display: flex; align-items: center; gap: 5px; font-weight: 600; }}
        .up {{ color: var(--success); }}
        .down {{ color: var(--danger); }}

        /* Main Content Layout */
        .main-layout {{ display: grid; grid-template-columns: 2fr 1fr; gap: 25px; }}
        .chart-card {{
            background: var(--card-bg);
            padding: 30px;
            border-radius: 16px;
            border: 1px solid var(--border-color);
            margin-bottom: 25px;
            max-height: 700px;
            overflow-y: auto;
            backdrop-filter: blur(15px);
            scrollbar-width: thin;
            scrollbar-color: var(--border-color) transparent;
        }}
        .chart-card::-webkit-scrollbar {{ width: 6px; }}
        .chart-card::-webkit-scrollbar-thumb {{ background-color: var(--border-color); border-radius: 10px; }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            position: sticky;
            top: -30px;
            background: var(--card-bg);
            padding: 15px 0;
            z-index: 10;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        .card-title {{ font-family: 'Orbitron', sans-serif; font-size: 1rem; color: var(--accent-primary); letter-spacing: 2px; }}
        
        /* Interactive Elements */
        .controls {{ display: flex; gap: 12px; align-items: center; }}
        .btn {{
            background: rgba(48, 54, 61, 0.5);
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 10px 18px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.8rem;
            font-weight: 700;
            transition: 0.3s;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            white-space: nowrap;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .btn:hover:not(:disabled) {{ background: rgba(0, 242, 255, 0.1); border-color: var(--accent-primary); color: var(--accent-primary); box-shadow: 0 0 15px var(--accent-primary); }}
        .btn:disabled {{ opacity: 0.3; cursor: not-allowed; }}
        .btn-primary {{ background: var(--accent-primary); color: #000; border: none; }}
        .btn-primary:hover:not(:disabled) {{ background: #fff; color: #000; box-shadow: 0 0 20px #fff; }}
        
        .date-picker-wrapper {{ position: relative; }}
        .date-picker {{
            background: #000;
            color: var(--accent-primary);
            border: 1px solid var(--border-color);
            padding: 8px 12px;
            border-radius: 8px;
            font-family: 'Orbitron', sans-serif;
            font-size: 0.8rem;
            outline: none;
            transition: 0.3s;
        }}
        .date-picker:focus {{ border-color: var(--accent-primary); box-shadow: 0 0 15px var(--accent-primary); }}

        /* Activity Log Table */
        .log-table-wrapper {{ overflow-x: auto; }}
        .log-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        .log-table th {{ text-align: left; padding: 15px; border-bottom: 2px solid var(--border-color); color: var(--text-dim); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; }}
        .log-table td {{ padding: 15px; border-bottom: 1px solid var(--border-color); font-size: 0.9rem; }}
        .log-table tr:hover {{ background: rgba(255,255,255,0.02); }}
        
        /* Reflections Section */
        .ref-input-group {{ display: flex; gap: 10px; margin-top: 20px; }}
        .ref-input {{
            flex: 1;
            background: #000;
            border: 1px solid var(--border-color);
            color: #fff;
            padding: 12px 18px;
            border-radius: 10px;
            font-family: 'Outfit', sans-serif;
            font-size: 0.9rem;
            transition: 0.3s;
        }}
        .ref-input:focus {{ border-color: var(--accent-primary); outline: none; box-shadow: 0 0 15px var(--accent-primary); }}
        .ref-list {{ margin-top: 25px; list-style: none; }}
        .ref-item {{
            background: rgba(255,255,255,0.03);
            padding: 18px;
            border-radius: 12px;
            border-left: 4px solid var(--accent-secondary);
            margin-bottom: 15px;
            font-size: 0.95rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: 0.3s;
        }}
        .ref-item:hover {{ background: rgba(255,255,255,0.05); }}

        /* Heatmap Styles */
        .heatmap-container {{
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-top: 10px;
        }}
        .heatmap-grid {{
            display: grid;
            grid-template-columns: repeat(53, 1fr);
            gap: 4px;
        }}
        .heat-cell {{
            width: 14px;
            height: 14px;
            background: #161b22;
            border-radius: 3px;
            cursor: pointer;
            transition: 0.2s;
        }}
        .heat-cell:hover {{ transform: scale(1.3); z-index: 2; border: 1px solid var(--accent-primary); }}
        .heat-level-1 {{ background: #0e4429; }}
        .heat-level-2 {{ background: #006d32; }}
        .heat-level-3 {{ background: #26a641; }}
        .heat-level-4 {{ background: #39d353; box-shadow: 0 0 10px #39d353; }}
        
        /* Tip Banner */
        .tip-banner {{
            background: linear-gradient(135deg, rgba(13, 17, 23, 0.9), rgba(22, 27, 34, 0.9));
            border: 1px solid var(--border-color);
            padding: 25px;
            border-radius: 16px;
            margin-bottom: 35px;
            border-left: 5px solid var(--accent-primary);
            backdrop-filter: blur(20px);
        }}
        .tip-header {{ font-family: 'Orbitron', sans-serif; color: var(--accent-primary); font-size: 1.1rem; font-weight: 700; letter-spacing: 2px; }}

        /* Sidebar */
        .sidebar {{
            position: fixed; left: 0; top: 0; bottom: 0; width: 80px;
            background: var(--glass-bg); backdrop-filter: blur(30px);
            border-right: 1px solid var(--border-color); z-index: 1000;
            display: flex; flex-direction: column; align-items: center; padding: 30px 0;
            transition: width 0.4s cubic-bezier(0.19, 1, 0.22, 1);
            overflow: hidden;
        }}
        .sidebar:hover {{ width: 260px; box-shadow: 10px 0 50px rgba(0,0,0,0.5); }}
        .sidebar-item {{
            width: 100%; padding: 18px 30px; display: flex; align-items: center; gap: 25px;
            color: var(--text-dim); cursor: pointer; transition: 0.3s; white-space: nowrap;
            text-decoration: none; position: relative;
        }}
        .sidebar-item i {{ font-size: 22px; min-width: 30px; text-align: center; font-style: normal; opacity: 0.7; }}
        .sidebar-item span {{ opacity: 0; transition: 0.3s; font-weight: 700; font-size: 13px; letter-spacing: 1px; text-transform: uppercase; }}
        .sidebar:hover .sidebar-item span {{ opacity: 1; }}
        .sidebar-item:hover, .sidebar-item.active {{ color: var(--accent-primary); background: rgba(0, 242, 255, 0.08); }}
        .sidebar-item.active::after {{ content: ''; position: absolute; left: 0; width: 4px; height: 60%; top: 20%; background: var(--accent-primary); border-radius: 0 4px 4px 0; box-shadow: 0 0 15px var(--accent-primary); }}

        .main-content-wrapper {{ margin-left: 80px; transition: margin-left 0.4s; }}
        
        #syncStatus {{ font-size: 0.7rem; font-weight: 800; padding: 4px 10px; border-radius: 6px; text-transform: uppercase; letter-spacing: 1px; }}
        .status-ready {{ background: rgba(35, 134, 54, 0.2); color: #3fb950; border: 1px solid #3fb950; }}
        .status-syncing {{ background: rgba(112, 0, 255, 0.2); color: #a371f7; border: 1px solid #a371f7; }}
        .status-error {{ background: rgba(218, 54, 51, 0.2); color: #f85149; border: 1px solid #f85149; }}

        @media (max-width: 1100px) {{
            .main-layout {{ grid-template-columns: 1fr; }}
            .sidebar {{ display: none; }}
            .main-content-wrapper {{ margin-left: 0; }}
        }}
    </style>
    <script src="tour_guide.js"></script>
</head>
<body>
    <div class="grid-bg"></div>
    
    <div class="sidebar">
        <div class="sidebar-item active"><i>📊</i><span>OVERVIEW</span></div>
        <a href="apkhunter.html" class="sidebar-item"><i>🎯</i><span>APK HUNTER</span></a>
        <a href="apkhunter.html#diagnostics" class="sidebar-item"><i>🛡️</i><span>SYSTEM HEALTH</span></a>
        <a href="http://localhost:3000" target="_blank" class="sidebar-item"><i>🛸</i><span>DROIDPILOT</span></a>
        <div class="sidebar-item" onclick="window.startTour()" style="color: #ffd700;"><i>🎓</i><span>SITE TOUR</span></div>
        <a href="https://www.youtube.com/@HackerOneTV/videos" target="_blank" class="sidebar-item"><i>🎬</i><span>RESOURCES</span></a>
        <div class="sidebar-item" style="margin-top: auto;"><i>⚙️</i><span>SETTINGS</span></div>
    </div>

    <div class="main-content-wrapper">
    <div class="container">
        <header>
            <div class="logo">OPERATIONAL INTELLIGENCE</div>
            <div class="header-meta">
                <div>SYSTEM STATUS: <span id="syncStatus" class="status-ready">NOMINAL</span></div>
                <div style="margin-top: 8px; opacity: 0.8;">LAST SYNC: <span id="lastSyncTime">{datetime.now().strftime('%H:%M:%S')}</span></div>
            </div>
        </header>

        <div class="chart-card" style="margin-bottom: 30px;">
            <div class="card-header">
                <div class="card-title">TRAJECTORY NAVIGATOR</div>
                <div class="controls">
                    <button class="btn" onclick="window.navTrajectory('prev')">← PREV</button>
                    <div class="date-picker-wrapper">
                        <input type="date" id="dateJumpTop" class="date-picker">
                    </div>
                    <button class="btn" onclick="window.navTrajectory('next')">NEXT →</button>
                </div>
            </div>
            <h2 id="currentHeaderDate" style="text-align: center; font-family: 'Orbitron'; color: #fff; letter-spacing: 2px; margin: 10px 0;">{stats['today_date']}</h2>
        </div>

        <div class="tip-banner">
            <div class="tip-header">✨ STRATEGIC ADVISORY</div>
            <p id="projectionText" style="margin-top: 15px; font-size: 1.1rem; color: #fff; font-weight: 500;">{stats['explanation']}</p>
        </div>

        <div class="dashboard-grid">
            <div class="stat-card">
                <div class="stat-label">Total Services</div>
                <div class="stat-value">{stats['total_services']}</div>
                <div class="stat-sub up">↑ {stats['total_services'] - 12 if stats['total_services'] > 12 else 0} VS BASELINE</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Earnings</div>
                <div class="stat-value">₹{stats['total_earnings']:,}</div>
                <div class="stat-sub up">↑ {round((stats['total_earnings']/90000)*100, 1)}% OF MONTHLY GOAL</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Recovery Pace</div>
                <div class="stat-value">{stats['recovery_pace_services']}</div>
                <div class="stat-sub">SERVICES / DAY REQUIRED</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">APK Claims</div>
                <div class="stat-value">{stats['apk_claimed']}</div>
                <div class="stat-sub" style="color: var(--accent-primary)">ACTIVE RESEARCH TARGETS</div>
            </div>
        </div>

        <div class="main-layout">
            <div class="content-left">
                <div class="chart-card">
                    <div class="card-header">
                        <div class="card-title">RE MASTERY HEATMAP (BHM)</div>
                        <div class="heat-legend">
                            LESS <div class="heat-cell"></div><div class="heat-cell heat-level-1"></div><div class="heat-cell heat-level-2"></div><div class="heat-cell heat-level-3"></div><div class="heat-cell heat-level-4"></div> MORE
                        </div>
                    </div>
                    <div class="heatmap-container">
                        <div id="masteryHeatmap" class="heatmap-grid"></div>
                        <div id="masteryEvents" class="mastery-event-list">
                            <div style="color: var(--text-dim); text-align: center; padding: 20px;">SELECT A DATA NODE TO VIEW TECHNICAL WINS</div>
                        </div>
                    </div>
                </div>

                <div class="chart-card">
                    <div class="card-header">
                        <div class="card-title">REVENUE TRAJECTORY</div>
                    </div>
                    <canvas id="revenueChart" height="150"></canvas>
                </div>

                <div class="chart-card">
                    <div class="card-header">
                        <div class="card-title">OPERATIONAL LOG</div>
                    </div>
                    <div class="log-table-wrapper" id="serviceLogContainer">
                        <table class="log-table">
                            <thead>
                                <tr>
                                    <th style="width: 60px;">ID</th>
                                    <th>ACTIVITY SPECIFICATION</th>
                                </tr>
                            </thead>
                            <tbody id="serviceLogBody">
                                <!-- Dynamic Content -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="content-right">
                <div class="chart-card">
                    <div class="card-header">
                        <div class="card-title">EFFORT ALLOCATION</div>
                    </div>
                    <div style="height: 300px; position: relative;">
                        <canvas id="effortPieChart"></canvas>
                    </div>
                    <div id="noDataMessage" style="display:none; text-align:center; padding: 40px; color: var(--text-dim); font-size: 0.9rem;">NO TELEMETRY DATA FOR THIS PERIOD</div>
                </div>

                <div class="chart-card">
                    <div class="card-header">
                        <div class="card-title">STRATEGIC REFLECTIONS</div>
                    </div>
                    <div class="ref-input-group">
                        <input type="text" id="reflectionInput" class="ref-input" placeholder="RECORD OBSERVATION...">
                        <button id="saveBtn" class="btn btn-primary" onclick="window.saveReflection()">SAVE</button>
                    </div>
                    <ul id="reflectionList" class="ref-list">
                        <!-- Dynamic Content -->
                    </ul>
                </div>
            </div>
        </div>
    </div>
    </div>

    <script>
        // --- DATA HUB ---
        window.dashboardData = {json.dumps(data_dict)};
        window.state = {{
            currentDate: window.dashboardData.today,
            isSyncing: false,
            editingIdx: null
        }};

        const $ = id => document.getElementById(id);
        
        // --- MASTER RENDERER ---
        window.renderMasteryHeatmap = () => {{
            const grid = $('masteryHeatmap');
            if (!grid) return;
            grid.innerHTML = '';
            const events = window.dashboardData.mastery || [];
            const heatMap = {{}};
            events.forEach(e => {{ heatMap[e.date] = (heatMap[e.date] || 0) + e.points; }});

            const today = new Date();
            for (let i = 370; i >= 0; i--) {{
                const d = new Date();
                d.setDate(today.getDate() - i);
                const iso = d.toISOString().split('T')[0];
                const points = heatMap[iso] || 0;
                
                const cell = document.createElement('div');
                cell.className = 'heat-cell';
                if (points > 0) {{
                    const level = points >= 50 ? 4 : points >= 30 ? 3 : points >= 15 ? 2 : 1;
                    cell.classList.add(`heat-level-${{level}}`);
                }}
                cell.title = `${{iso}}: ${{points}} Mastery Points`;
                cell.onclick = () => window.showMasteryEvents(iso);
                grid.appendChild(cell);
            }}
        }};

        window.showMasteryEvents = (date) => {{
            const list = $('masteryEvents');
            const events = (window.dashboardData.mastery || []).filter(e => e.date === date);
            if (events.length === 0) {{
                list.innerHTML = `<div style="color: var(--text-dim); text-align: center; padding: 20px;">NO DATA NODES FOR ${{date}}</div>`;
                return;
            }}
            list.innerHTML = events.map(e => `
                <div class="event-item" style="padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; justify-content: space-between;">
                    <div>
                        <span style="color: var(--accent-primary); font-weight: 800; font-size: 0.75rem; margin-right: 10px;">[${{e.event_type}}]</span>
                        <span style="font-size: 0.9rem;">${{e.details}}</span>
                    </div>
                    <div style="color: var(--accent-primary); font-weight: 800;">+${{e.points}}</div>
                </div>
            `).join('');
        }};

        window.renderCharts = () => {{
            const targetDate = window.state.currentDate;
            
            // Revenue Line
            const trendCtx = $('revenueChart').getContext('2d');
            if (window.revenueChartInst) window.revenueChartInst.destroy();
            const trendDays = window.dashboardData.services.filter(d => d.iso_date).sort((a,b) => a.iso_date.localeCompare(b.iso_date));
            window.revenueChartInst = new Chart(trendCtx, {{
                type: 'line',
                data: {{
                    labels: trendDays.map(d => d.date.split(',')[0]),
                    datasets: [{{
                        label: 'REVENUE',
                        data: trendDays.map(d => d.earnings),
                        borderColor: '#00f2ff',
                        backgroundColor: 'rgba(0, 242, 255, 0.05)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3,
                        pointRadius: 0,
                        pointHoverRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#8b949e', font: {{ family: 'Orbitron', size: 10 }} }} }},
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#8b949e', font: {{ family: 'Orbitron', size: 10 }} }} }}
                    }}
                }}
            }});

            // Effort Pie
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
                            hoverOffset: 20
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{ 
                            legend: {{ position: 'bottom', labels: {{ color: '#e6edf3', font: {{ family: 'Outfit', size: 11 }}, padding: 15 }} }}
                        }},
                        cutout: '75%'
                    }}
                }});
            }}
        }};

        window.renderLogsAndReflections = () => {{
            const targetDate = window.state.currentDate;
            const serviceDay = window.dashboardData.services.find(d => d.iso_date === targetDate);
            const logBody = $('serviceLogBody');
            logBody.innerHTML = '';
            
            if (serviceDay && serviceDay.services.length) {{
                serviceDay.services.forEach(line => {{
                    const match = line.match(/^(\\d+)\\.(.*)/);
                    if (match) {{
                        logBody.insertAdjacentHTML('beforeend', `<tr><td style="font-family: 'Orbitron'; color: var(--accent-primary); font-weight: 700;">${{match[1]}}</td><td>${{match[2].trim()}}</td></tr>`);
                    }}
                }});
            }} else {{
                logBody.innerHTML = '<tr><td colspan="2" style="text-align:center; color:var(--text-dim); padding: 40px;">NO LOG ENTRIES DETECTED</td></tr>';
            }}

            const refEntry = window.dashboardData.logs.find(l => l.iso_date === targetDate);
            const refList = $('reflectionList');
            refList.innerHTML = '';
            if (refEntry && refEntry.reflections.length) {{
                refEntry.reflections.forEach((text, idx) => {{
                    refList.insertAdjacentHTML('beforeend', `
                        <li class="ref-item">
                            <span>${{text}}</span>
                            <div style="display: flex; gap: 10px;">
                                <span onclick="window.editReflection(${{idx}})" style="color: var(--accent-primary); cursor: pointer; font-size: 0.7rem; font-weight: 800;">EDIT</span>
                                <span onclick="window.deleteReflection(${{idx}})" style="color: var(--danger); cursor: pointer; font-size: 0.7rem; font-weight: 800;">DEL</span>
                            </div>
                        </li>
                    `);
                }});
            }} else {{
                refList.innerHTML = '<li style="color:var(--text-dim); font-size:0.85rem; text-align:center; padding: 20px;">NO STRATEGIC OBSERVATIONS</li>';
            }}
        }};

        window.jumpToDate = (isoDate) => {{
            if (!isoDate) return;
            window.state.currentDate = isoDate;
            $('dateJumpTop').value = isoDate;
            const serviceDay = window.dashboardData.services.find(d => d.iso_date === isoDate);
            $('currentHeaderDate').innerText = serviceDay ? serviceDay.date : isoDate;
            window.renderCharts();
            window.renderLogsAndReflections();
        }};

        window.navTrajectory = (dir) => {{
            const trendDays = window.dashboardData.services.filter(d => d.iso_date).sort((a,b) => a.iso_date.localeCompare(b.iso_date));
            const curIdx = trendDays.findIndex(d => d.iso_date === window.state.currentDate);
            let nextIdx = dir === 'prev' ? curIdx - 1 : curIdx + 1;
            if (nextIdx >= 0 && nextIdx < trendDays.length) window.jumpToDate(trendDays[nextIdx].iso_date);
        }};

        window.saveReflection = async () => {{
            const text = $('reflectionInput').value.trim();
            if (!text) return;
            const targetDate = window.state.currentDate;
            const logDateStr = targetDate.split('-').reverse().join('-');
            const isEditing = window.state.editingIdx !== null;
            
            let logEntry = window.dashboardData.logs.find(l => l.iso_date === targetDate);
            if (!logEntry) {{
                logEntry = {{ iso_date: targetDate, date: logDateStr, logs: [], reflections: [], total: 0 }};
                window.dashboardData.logs.push(logEntry);
            }}

            if (isEditing) {{
                const oldIdx = window.state.editingIdx;
                await window.pushToGitHub(`DELETE_REF: Date: ${{logDateStr}}, Index: ${{oldIdx}}`);
                logEntry.reflections.splice(oldIdx, 1);
                window.state.editingIdx = null;
                $('saveBtn').innerText = 'SAVE';
            }}
            
            logEntry.reflections.push(text);
            window.renderLogsAndReflections();
            $('reflectionInput').value = '';
            await window.pushToGitHub(`ADD_REF: Date: ${{logDateStr}}, Text: ${{text}}`);
        }};

        window.editReflection = (idx) => {{
            const logEntry = window.dashboardData.logs.find(l => l.iso_date === window.state.currentDate);
            $('reflectionInput').value = logEntry.reflections[idx];
            $('saveBtn').innerText = 'UPDATE';
            window.state.editingIdx = idx;
            $('reflectionInput').focus();
        }};

        window.deleteReflection = async (idx) => {{
            const logEntry = window.dashboardData.logs.find(l => l.iso_date === window.state.currentDate);
            const logDateStr = window.state.currentDate.split('-').reverse().join('-');
            logEntry.reflections.splice(idx, 1);
            window.renderLogsAndReflections();
            await window.pushToGitHub(`DELETE_REF: Date: ${{logDateStr}}, Index: ${{idx}}`);
        }};

        window.pushToGitHub = async (message) => {{
            const token = localStorage.getItem('github_token') || prompt("GITHUB PAT REQUIRED:");
            if (!token) return;
            localStorage.setItem('github_token', token);
            $('syncStatus').className = 'status-syncing';
            $('syncStatus').innerText = 'SYNCING';
            try {{
                const res = await fetch("https://api.github.com/repos/Githubds12/service-progress-dashboard/issues/1/comments", {{
                    method: "POST",
                    headers: {{ "Authorization": `token ${{token}}`, "Accept": "application/vnd.github.v3+json" }},
                    body: JSON.stringify({{ body: message }})
                }});
                if (res.ok) {{ $('syncStatus').className = 'status-ready'; $('syncStatus').innerText = 'NOMINAL'; return true; }}
            }} catch(e) {{ $('syncStatus').className = 'status-error'; $('syncStatus').innerText = 'ERROR'; }}
            return false;
        }};

        window.startTour = () => {{
            const tour = new TourGuide([
                {{ element: '.logo', title: 'MISSION CONTROL', content: 'Operational intelligence center. All telemetry data flows through here.' }},
                {{ element: '.dashboard-grid', title: 'CORE METRICS', content: 'Real-time tracking of revenue, pace, and research volume.' }},
                {{ element: '.heatmap-grid', title: 'MASTERY PROGRESS', content: 'Visual representation of technical breakthroughs and system research.' }},
                {{ element: '.sidebar', title: 'NAVIGATION INTERFACE', content: 'Switch between overview and deep-dive APK intelligence views.' }}
            ]);
            tour.start();
        }};

        window.addEventListener('DOMContentLoaded', () => {{
            $('dateJumpTop').onchange = (e) => window.jumpToDate(e.target.value);
            window.renderMasteryHeatmap();
            window.jumpToDate(window.dashboardData.today);
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
