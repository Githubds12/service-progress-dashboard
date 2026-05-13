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
    token = os.getenv("GH_PAT")
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

def calculate_stats(days, mastery_data=None):
    current_days = [d for d in days if not d.get('is_history', False)]
    total_services = sum(len(d['services']) for d in current_days)
    total_earnings = sum(d['earnings'] for d in current_days)
    
    # Operational Cycle: Starts 7th May 2026
    cycle_start = date(2026, 5, 7)
    today_dt = date.today()
    
    # Days elapsed in cycle
    days_elapsed = max((today_dt - cycle_start).days + 1, 1) 
    days_remaining = max(31 - days_elapsed, 1) # 31 day cycle
    
    # Cycle Earnings
    cycle_earnings = sum(d['earnings'] for d in current_days if datetime.strptime(d['iso_date'], '%Y-%m-%d').date() >= cycle_start)
    
    # Cycle Mastery Points
    cycle_points = 0
    if mastery_data:
        for entry in mastery_data:
            try:
                entry_date = datetime.strptime(entry['date'], '%Y-%m-%d').date()
                if entry_date >= cycle_start:
                    cycle_points += entry['points']
            except: continue

    avg_daily = cycle_earnings / days_elapsed if days_elapsed > 0 else 0
    avg_daily_services = total_services / days_elapsed if days_elapsed > 0 else 0
    
    # Calculate Total Claimed APKs
    apk_claimed_count = 0
    apk_data_path = os.path.join(REPORT_DIR, "dashboard", "apkhunter_data.js")
    if os.path.exists(apk_data_path):
        try:
            with open(apk_data_path, 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search(r'window\.apkhunterData\s*=\s*(\[.*\])', content, re.DOTALL)
                if match:
                    apk_list = json.loads(match.group(1))
                    apk_claimed_count = sum(1 for item in apk_list if item.get('claimed'))
        except: pass

    target_total = 90000
    remaining_target = target_total - cycle_earnings
    recovery_pace_services = remaining_target / 400 / days_remaining
    projected_total = avg_daily * 31
    recommended_today = math.ceil(recovery_pace_services * 1.2)
    
    today_str_check = f"{get_ordinal(today_dt.day)} {today_dt.strftime('%B')}"
    completed_today = next((len(d['services']) for d in days if today_str_check in d['date']), 0)

    explanation = f"Target: ₹90,000. Cycle Day {days_elapsed}/31. Pace: {round(recovery_pace_services, 1)} services/day."
    try:
        prompt = f"Analyze progress for Cycle (Start: May 7): {cycle_earnings}/90000. Points: {cycle_points}. Day {days_elapsed}/31. Write 1-2 sentence tip with Sanskrit header."
        response = client.models.generate_content(model='gemini-flash-latest', contents=prompt)
        if response and response.text: explanation = response.text.strip().replace('"', '')
    except: pass

    return {
        'total_services': total_services, 
        'total_earnings': total_earnings,
        'cycle_earnings': cycle_earnings,
        'cycle_points': cycle_points,
        'cycle_day': days_elapsed,
        'cycle_remaining': days_remaining,
        'apk_claimed': apk_claimed_count,
        'avg_daily': round(avg_daily, 2), 
        'avg_daily_services': round(avg_daily_services, 2),
        'days_elapsed': days_elapsed, 
        'recovery_pace_services': round(recovery_pace_services, 1),
        'days_remaining': days_remaining, 
        'recommended_today': int(recommended_today),
        'completed_today': completed_today, 
        'explanation': explanation,
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
    # Load token from environment
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        print("[!] Warning: GITHUB_TOKEN not found. Remote sync features will be disabled.")
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
        .main-layout {{ 
            display: grid; 
            grid-template-columns: minmax(0, 2fr) minmax(0, 1fr); 
            gap: 25px; 
        }}
        .chart-card {{
            background: var(--card-bg);
            padding: 30px;
            border-radius: 16px;
            border: 1px solid var(--border-color);
            margin-bottom: 25px;
            max-height: 700px;
            overflow-y: auto;
            overflow-x: hidden; /* Prevent horizontal expansion */
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
            overflow-x: auto;
            padding-bottom: 10px;
            scrollbar-width: thin;
            scrollbar-color: var(--border-color) transparent;
        }}
        .heatmap-container::-webkit-scrollbar {{ height: 6px; }}
        .heatmap-container::-webkit-scrollbar-thumb {{ background: var(--border-color); border-radius: 10px; }}
        .heatmap-grid {{
            display: grid;
            grid-template-columns: repeat(53, 1fr);
            gap: 4px;
            min-width: 950px;
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
        .heat-level-1 {{ background: #0e4429 !important; }}
        .heat-level-2 {{ background: #006d32 !important; }}
        .heat-level-3 {{ background: #26a641 !important; }}
        .heat-level-4 {{ background: #39d353 !important; }}

        /* New Heatmap Meta Styles */
        .heatmap-wrapper {{ display: flex; gap: 10px; min-width: 980px; }}
        .heatmap-axis-labels {{ 
            display: grid; 
            grid-template-rows: repeat(7, 14px); 
            gap: 4px; 
            padding-top: 25px; /* Alignment with month labels */
            font-size: 0.65rem; 
            color: var(--text-dim); 
            font-family: 'Orbitron';
        }}
        .heatmap-month-labels {{ 
            display: grid; 
            grid-template-columns: repeat(53, 1fr); 
            gap: 4px; 
            margin-bottom: 5px; 
            margin-left: 35px; /* Offset for day labels */
            font-size: 0.65rem; 
            color: var(--text-dim); 
            font-family: 'Orbitron';
            min-width: 950px;
        }}
        .heatmap-footer {{ 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-top: 15px; 
            padding: 0 5px;
        }}
        .heatmap-legend {{ 
            display: flex; 
            align-items: center; 
            gap: 5px; 
            font-size: 0.7rem; 
            color: var(--text-dim); 
            font-family: 'Outfit';
        }}
        .legend-box {{ width: 10px; height: 10px; border-radius: 2px; }}
        
        .heatmap-stats {{
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        .h-stat {{ flex: 1; }}
        .h-stat-label {{ font-size: 0.6rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 1px; }}
        .h-stat-value {{ font-family: 'Orbitron'; font-size: 1rem; color: var(--accent-primary); margin-top: 5px; }}
        /* Settings Modal */
        .modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.85);
            backdrop-filter: blur(15px);
            z-index: 20000;
            display: none;
            align-items: center;
            justify-content: center;
        }}
        .modal-content {{
            background: #0d1117;
            border: 1px solid var(--accent-primary);
            border-radius: 20px;
            width: 90%;
            max-width: 500px;
            padding: 35px;
            box-shadow: 0 0 50px rgba(0, 242, 255, 0.15);
            position: relative;
        }}
        .modal-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            padding-bottom: 15px;
        }}
        .modal-title {{ font-family: 'Orbitron'; font-size: 1.2rem; color: var(--accent-primary); letter-spacing: 2px; }}
        .close-modal {{ color: var(--text-dim); cursor: pointer; font-size: 1.5rem; transition: 0.3s; }}
        .close-modal:hover {{ color: var(--danger); }}
        .setting-row {{ margin-bottom: 20px; }}
        .setting-label {{ display: block; color: var(--text-dim); font-size: 0.8rem; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 1px; }}
        .setting-input {{
            width: 100%;
            background: #000;
            border: 1px solid var(--border-color);
            color: #fff;
            padding: 12px;
            border-radius: 10px;
            font-family: 'Outfit';
            outline: none;
            transition: 0.3s;
        }}
        .setting-input:focus {{ border-color: var(--accent-primary); box-shadow: 0 0 15px rgba(0, 242, 255, 0.2); }}

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

        .main-content-wrapper {{ 
            margin-left: 80px; 
            width: calc(100% - 80px);
            transition: margin-left 0.4s; 
            overflow-x: hidden;
        }}
        
        #syncStatus {{ font-size: 0.7rem; font-weight: 800; padding: 4px 10px; border-radius: 6px; text-transform: uppercase; letter-spacing: 1px; }}
        .status-ready {{ background: rgba(35, 134, 54, 0.2); color: #3fb950; border: 1px solid #3fb950; }}
        .status-syncing {{ background: rgba(112, 0, 255, 0.2); color: #a371f7; border: 1px solid #a371f7; }}
        .status-error {{ background: rgba(218, 54, 51, 0.2); color: #f85149; border: 1px solid #f85149; }}

        @media (max-width: 1300px) {{
            .main-layout {{ grid-template-columns: 1fr; }}
        }}

        @media (max-width: 768px) {{
            .sidebar {{ display: none; }}
            .main-content-wrapper {{ 
                margin-left: 0; 
                width: 100%;
            }}
        }}
    </style>
    <script src="tour_guide.js"></script>
</head>
<body>
    <div id="settingsModal" class="modal-overlay">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">⚙️ SYSTEM SETTINGS</div>
                <div class="close-modal" onclick="window.closeSettings()">×</div>
            </div>
            <div class="setting-row">
                <label class="setting-label">GitHub Personal Access Token (PAT)</label>
                <input type="password" id="githubTokenInput" class="setting-input" placeholder="ghp_xxxxxxxxxxxx">
            </div>
            <div class="setting-row">
                <label class="setting-label">DroidPilot Intel Port</label>
                <input type="number" id="droidPilotPortInput" class="setting-input" placeholder="7777">
            </div>
            <div class="setting-row">
                <label class="setting-label">Display Preference</label>
                <select id="displayPref" class="setting-input" style="background:#000;">
                    <option value="cyber">CYBERPUNK (DEFAULT)</option>
                    <option value="minimal">MINIMALIST</option>
                </select>
            </div>
            <div style="margin-top: 30px; display: flex; gap: 15px;">
                <button class="btn btn-primary" style="flex:1" onclick="window.saveSettings()">SAVE CONFIGURATION</button>
            </div>
        </div>
    </div>

    <div class="grid-bg"></div>
    
    <div class="sidebar">
        <div class="sidebar-item active"><i>📊</i><span>OVERVIEW</span></div>
        <a href="apkhunter.html" class="sidebar-item"><i>🎯</i><span>APK HUNTER</span></a>
        <a href="apkhunter.html#diagnostics" class="sidebar-item"><i>🛡️</i><span>SYSTEM HEALTH</span></a>
        <a href="http://localhost:7777" target="_blank" class="sidebar-item"><i>🛸</i><span>DROIDPILOT</span></a>
        <div class="sidebar-item" onclick="window.startTour()" style="color: #ffd700;"><i>🎓</i><span>SITE TOUR</span></div>
        <a href="https://www.youtube.com/@HackerOneTV/videos" target="_blank" class="sidebar-item"><i>🎬</i><span>RESOURCES</span></a>
        <div class="sidebar-item" onclick="window.showSettings()" style="margin-top: auto;"><i>⚙️</i><span>SETTINGS</span></div>
    </div>

    <div class="main-content-wrapper">
    <div class="container">
        <header>
            <div class="logo">OPERATIONAL INTELLIGENCE <span style="font-size: 0.7rem; color: var(--accent-secondary); vertical-align: middle; margin-left: 10px; opacity: 0.8;">[OPERATIONAL CYCLE: MAY 7th - JUNE 6th, 2026]</span></div>
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

        <div class="section-divider" style="margin: 40px 0 20px 0; border-bottom: 2px solid var(--accent-secondary); width: fit-content; padding-right: 20px;">
            <h3 style="font-family: 'Orbitron'; color: var(--accent-primary); letter-spacing: 2px; font-size: 0.9rem;">OPERATIONAL CYCLE INTELLIGENCE (MTD)</h3>
        </div>

        <div class="dashboard-grid" style="margin-bottom: 30px;">
            <div class="stat-card" style="border-color: var(--accent-secondary);" title="Current day within the 31-day operational window (Starts May 7th).">
                <div class="stat-label">Cycle Progress</div>
                <div class="stat-value">Day {stats['cycle_day']}</div>
                <div class="stat-sub">{stats['cycle_remaining']} DAYS REMAINING</div>
            </div>
            <div class="stat-card" style="border-color: var(--accent-secondary);" title="Total revenue generated since the May 7th reset.">
                <div class="stat-label">Cycle Revenue</div>
                <div class="stat-value">₹{stats['cycle_earnings']:,}</div>
                <div class="stat-sub">TARGET: ₹90,000</div>
            </div>
            <div class="stat-card" style="border-color: var(--accent-secondary);" title="Total research intensity points earned since May 7th. Reflects volume of deep technical analysis.">
                <div class="stat-label">Cycle Mastery</div>
                <div class="stat-value">{stats['cycle_points']} Pts</div>
                <div class="stat-sub">RESEARCH INTENSITY</div>
                <div style="font-size: 0.6rem; color: var(--text-dim); margin-top: 5px; line-height: 1.2;">Cumulative research effort since cycle reset.</div>
            </div>
            <div class="stat-card" style="border-color: var(--accent-secondary);" title="Ratio of actual earnings vs. required earnings for the current day to hit ₹90k. 100% = On Track.">
                <div class="stat-label">Survival Index</div>
                <div class="stat-value">{round((stats['cycle_earnings'] / (90000/31 * stats['cycle_day'])) * 100, 1) if stats['cycle_day'] > 0 else 0}%</div>
                <div class="stat-sub">OUTPUT VS PROJECTED</div>
                <div style="font-size: 0.6rem; color: var(--text-dim); margin-top: 5px; line-height: 1.2;">Earnings vs. required pace for today.</div>
            </div>
        </div>

        <div class="main-layout">
            <div class="content-left">
                <div class="chart-card" id="masteryCard">
                    <div class="card-header">
                        <div class="card-title">RE MASTERY HEATMAP (BHM)</div>
                    </div>
                    <div class="heatmap-stats">
                        <div class="h-stat">
                            <div class="h-stat-label">Total Mastery</div>
                            <div id="totalMasteryPoints" class="h-stat-value">0</div>
                        </div>
                        <div class="h-stat">
                            <div class="h-stat-label">Current Streak</div>
                            <div id="currentStreak" class="h-stat-value">0 Days</div>
                        </div>
                        <div class="h-stat">
                            <div class="h-stat-label">Peak Intensity</div>
                            <div id="peakIntensity" class="h-stat-value">0 Pts</div>
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 15px; padding: 15px; background: rgba(0, 242, 255, 0.03); border-radius: 10px; border: 1px solid rgba(0, 242, 255, 0.1);">
                        <p style="font-size: 0.85rem; color: var(--text-dim); line-height: 1.6;">
                            <strong style="color: var(--accent-primary);">CORE INTELLIGENCE:</strong> This heatmap tracks your deep research activity. Darker cells indicate higher technical intensity.
                            <span id="heatmapStatusMsg" style="color: var(--danger); font-weight: 700; margin-left: 10px;"></span>
                        </p>
                    </div>

                    <div id="heatmapMonthLabels" class="heatmap-month-labels">
                        <!-- Generated via JS -->
                    </div>
                    <div class="heatmap-container">
                        <div class="heatmap-wrapper">
                            <div class="heatmap-axis-labels">
                                <div></div><div>Mon</div><div></div><div>Wed</div><div></div><div>Fri</div><div></div>
                            </div>
                            <div id="masteryHeatmap" class="heatmap-grid">
                                <!-- Cells generated via JS -->
                            </div>
                        </div>
                    </div>
                    <div class="heatmap-footer">
                        <div style="font-size: 0.7rem; color: var(--text-dim);">LAST 370 DAYS OF RECONNAISSANCE</div>
                        <div class="heatmap-legend">
                            <span>Less</span>
                            <div class="legend-box" style="background: rgba(255,255,255,0.05);"></div>
                            <div class="legend-box heat-level-1"></div>
                            <div class="legend-box heat-level-2"></div>
                            <div class="legend-box heat-level-3"></div>
                            <div class="legend-box heat-level-4"></div>
                            <span>More</span>
                        </div>
                    </div>

                    <div id="masteryEvents" style="margin-top: 20px; max-height: 200px; overflow-y: auto;">
                        <div style="color: var(--text-dim); text-align: center; padding: 20px; font-size: 0.8rem;">SELECT A DATA NODE TO VIEW ACTIVITY SPECIFICATIONS</div>
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
                        <div class="controls">
                            <button class="btn btn-sm" style="padding: 4px 10px; font-size: 0.6rem;" onclick="window.navTrajectory('prev')">← PREV</button>
                            <span id="localLogDate" style="font-family: 'Orbitron'; font-size: 0.7rem; color: var(--accent-primary); margin: 0 5px; font-weight: 800;"></span><button class="btn btn-sm" style="padding: 4px 10px; font-size: 0.6rem;" onclick="window.navTrajectory('next')">NEXT →</button>
                        </div>
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
                        <div class="card-title">EFFORT ALLOCATION <span id="localEffortDate" style="font-family: 'Orbitron'; font-size: 0.7rem; color: #f0f; margin-left: 10px; font-weight: 800; opacity: 0.8;"></span></div>
                        <div class="controls">
                            <button class="btn btn-sm" style="padding: 4px 10px; font-size: 0.6rem;" onclick="window.navTrajectory('prev')">← PREV</button>
                            <button class="btn btn-sm" style="padding: 4px 10px; font-size: 0.6rem;" onclick="window.navTrajectory('next')">NEXT →</button>
                        </div>
                    </div>
                    <div style="height: 300px; position: relative;">
                        <canvas id="effortPieChart"></canvas>
                    </div>
                    <div id="noDataMessage" style="display:none; text-align:center; padding: 40px; color: var(--text-dim); font-size: 0.9rem;">NO TELEMETRY DATA FOR THIS PERIOD</div>
                </div>

                <div class="chart-card">
                    <div class="card-header">
                        <div class="card-title">STRATEGIC REFLECTIONS</div>
                        <div class="controls">
                            <button class="btn btn-sm" style="padding: 4px 10px; font-size: 0.6rem;" onclick="window.navTrajectory('prev')">← PREV</button>
                            <span id="localRefDate" style="font-family: 'Orbitron'; font-size: 0.7rem; color: var(--accent-secondary); margin: 0 5px; font-weight: 800;"></span><button class="btn btn-sm" style="padding: 4px 10px; font-size: 0.6rem;" onclick="window.navTrajectory('next')">NEXT →</button>
                        </div>
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
            const monthLabels = $('heatmapMonthLabels');
            if (!grid) return;
            
            grid.innerHTML = '';
            monthLabels.innerHTML = '';
            
            const events = window.dashboardData.mastery || [];
            const msgEl = $('heatmapStatusMsg');
            if (events.length === 0) {{
                msgEl.innerText = "⚠ NO RESEARCH LOG DETECTED";
            }} else {{
                msgEl.innerText = "✅ SYSTEM ONLINE";
            }}
            
            const heatMap = {{}};
            let totalPoints = 0;
            let peakPoints = 0;
            events.forEach(e => {{ 
                heatMap[e.date] = (heatMap[e.date] || 0) + e.points;
                totalPoints += e.points;
                if (heatMap[e.date] > peakPoints) peakPoints = heatMap[e.date];
            }});

            // Stats Update
            $('totalMasteryPoints').innerText = totalPoints.toLocaleString();
            $('peakIntensity').innerText = peakPoints + ' Pts';
            
            // Streak Calculation
            let streak = 0;
            let checkDate = new Date();
            while (true) {{
                const iso = checkDate.toISOString().split('T')[0];
                if (heatMap[iso]) {{
                    streak++;
                    checkDate.setDate(checkDate.getDate() - 1);
                }} else {{
                    break;
                }}
            }}
            $('currentStreak').innerText = streak + ' Days';

            const today = new Date();
            const dayOfWeek = today.getDay(); // 0 is Sun
            
            // Adjust to start from a Sunday 371 days ago to fill 53 weeks
            const startDate = new Date();
            startDate.setDate(today.getDate() - 370);
            while (startDate.getDay() !== 0) startDate.setDate(startDate.getDate() - 1);

            const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            let lastMonth = -1;

            // Generate 53 weeks (columns)
            for (let w = 0; w < 53; w++) {{
                // Month Label logic
                const weekDate = new Date(startDate);
                weekDate.setDate(startDate.getDate() + (w * 7));
                const currentMonth = weekDate.getMonth();
                
                const mLabel = document.createElement('div');
                if (currentMonth !== lastMonth && w < 52) {{
                    mLabel.innerText = months[currentMonth];
                    lastMonth = currentMonth;
                }}
                monthLabels.appendChild(mLabel);

                // Week Column
                const col = document.createElement('div');
                col.style.display = 'grid';
                col.style.gridTemplateRows = 'repeat(7, 14px)';
                col.style.gap = '4px';

                for (let d = 0; d < 7; d++) {{
                    const currentDate = new Date(weekDate);
                    currentDate.setDate(weekDate.getDate() + d);
                    const iso = currentDate.toISOString().split('T')[0];
                    const points = heatMap[iso] || 0;
                    
                    const cell = document.createElement('div');
                    cell.className = 'heat-cell';
                    if (points > 0) {{
                        const level = points >= 50 ? 4 : points >= 30 ? 3 : points >= 15 ? 2 : 1;
                        cell.classList.add(`heat-level-${{level}}`);
                    }}
                    
                    // Don't show future dates
                    if (currentDate > today) {{
                        cell.style.opacity = '0';
                        cell.style.pointerEvents = 'none';
                    }}

                    cell.title = `${{iso}}: ${{points}} Mastery Points`;
                    cell.onclick = () => window.showMasteryEvents(iso);
                    col.appendChild(cell);
                }}
                grid.appendChild(col);
            }}

            // Fix grid layout for columns
            grid.style.display = 'flex';
            grid.style.gap = '4px';
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
            
            const finalLabels = (logEntry && logEntry.logs.length) ? logEntry.logs.map(l => l.activity) : ['DORMANT'];
            const finalData = (logEntry && logEntry.logs.length) ? logEntry.logs.map(l => l.hours) : [1];
            const finalColors = (logEntry && logEntry.logs.length) ? ['#00f2ff', '#7000ff', '#3fb950', '#f85149', '#db6d28', '#e3b341'] : ['rgba(255, 255, 255, 0.05)'];

            $('effortPieChart').style.display = 'block';
            $('noDataMessage').style.display = 'none';

            window.pieChartInst = new Chart(pieCtx, {{
                type: 'doughnut',
                data: {{
                    labels: finalLabels,
                    datasets: [{{
                        data: finalData,
                        backgroundColor: finalColors,
                        borderWidth: 0,
                        hoverOffset: (logEntry && logEntry.logs.length) ? 20 : 0
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
        }};

        window.renderLogsAndReflections = () => {{
            const targetDate = window.state.currentDate;
            const serviceDay = window.dashboardData.services.find(d => d.iso_date === targetDate);
            
            // Update local date labels
            const dateLabel = serviceDay ? serviceDay.date.split(',')[0].toUpperCase() : targetDate;
            if ($('localLogDate')) $('localLogDate').innerText = dateLabel;
            if ($('localRefDate')) $('localRefDate').innerText = dateLabel;
            if ($('localEffortDate')) $('localEffortDate').innerText = '[ ' + dateLabel + ' ]';

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
            const steps = [
                {{ 
                    element: ".logo", 
                    title: "🛸 OPERATIONAL COMMAND", 
                    content: "Welcome to your primary intelligence hub. This dashboard aggregates telemetry from all active research sectors. The interface is optimized for high-density data visualization and rapid decision making." 
                }},
                {{ 
                    element: ".header-meta", 
                    title: "📡 SYSTEM STATUS", 
                    content: "This monitor tracks your global connectivity. \\\"NOMINAL\\\" means all local data feeds, GitHub sync, and research logs are perfectly synchronized. Red indicators signal a sync failure or missing data source." 
                }},
                {{ 
                    element: ".sidebar", 
                    title: "🛰️ NAVIGATION ARRAY", 
                    content: "This is your primary navigation hub. It contains specialized portals for different operational tasks. Let's explore them." 
                }},
                {{ 
                    element: ".sidebar-item:nth-child(1)", 
                    title: "📊 OVERVIEW HUB", 
                    content: "Your current location. Provides a high-level summary of earnings, recovery pace, and overall research momentum." 
                }},
                {{ 
                    element: 'a[href*="apkhunter"]', 
                    title: "🛡️ APK HUNTER PORTAL", 
                    content: "Deep-dive into specific research targets. This portal handles thousands of services, categorizing them by complexity (Easy, Medium, Hard) and tracking claim status via UUID/Slug matching." 
                }},
                {{ 
                    element: 'a[href*="diagnostics"]', 
                    title: "🛸 SYSTEM HEALTH", 
                    content: "Diagnostic monitor for background services. Verifies that your data parsers, API endpoints, and Render deployment engines are running at peak performance." 
                }},
                {{ 
                    element: 'a[href*="7777"]', 
                    title: "🎓 DROIDPILOT INTEL", 
                    content: "Direct link to your local AI Agent interface. DroidPilot manages autonomous reconnaissance and background data gathering for the research board." 
                }},
                {{ 
                    element: ".sidebar-item:last-child", 
                    title: "⚙️ SYSTEM CONFIGURATION", 
                    content: "Critical settings hub. Here you can configure your GitHub PAT (Personal Access Token) for secure syncing and adjust ports for your local intelligence tools." 
                }},
                {{ 
                    element: ".stat-card:nth-child(1)", 
                    title: "💰 REVENUE METRICS", 
                    content: "Real-time tracking of your total earnings (₹). The bottom indicator compares your current performance against the baseline from the previous sync period." 
                }},
                {{ 
                    element: ".stat-card:nth-child(2)", 
                    title: "📈 RECOVERY PROJECTOR", 
                    content: "Calculates your trajectory toward the ₹90,000 monthly target. It projects your end-of-month earnings based on your current recovery pace." 
                }},
                {{ 
                    element: ".stat-card:nth-child(3)", 
                    title: "🏃 RECOVERY PACE", 
                    content: "The most critical metric. It tells you exactly how many services you need to complete PER DAY to hit your goals. This number turns green when you are ahead of schedule." 
                }},
                {{ 
                    element: "#masteryCard", 
                    title: "🧠 RE MASTERY HEATMAP (BHM)", 
                    content: "Behavorial Heat Map of your technical analysis. Each node tracks 53 weeks of history. Darker green = Higher research output. CLICK A NODE below to see specific activity logs for that day." 
                }},
                {{ 
                    element: "#revenueChart", 
                    title: "📉 REVENUE TRAJECTORY", 
                    content: "Chronological trend of your financial growth. Use this to identify peak productivity patterns and research milestones over time." 
                }},
                {{ 
                    element: ".log-viewer", 
                    title: "📋 OPERATIONAL LOG", 
                    content: "Granular view of daily activity. Includes time-stamped entries, activity specifications, and service IDs. This is the raw telemetry behind your revenue stats." 
                }},
                {{ 
                    element: ".ref-input-group", 
                    title: "🧠 STRATEGIC REFLECTIONS", 
                    content: "Your professional journal. Record critical hurdles, breakthroughs, or technical observations here. These entries help train your research intuition over time." 
                }}
            ];
            new TourGuide(steps).start();
        }};

        window.showSettings = () => {{
            $('githubTokenInput').value = localStorage.getItem('github_token') || '';
            $('droidPilotPortInput').value = localStorage.getItem('droidpilot_port') || '7777';
            $('settingsModal').style.display = 'flex';
        }};

        window.closeSettings = () => {{
            $('settingsModal').style.display = 'none';
        }};

        window.saveSettings = () => {{
            const token = $('githubTokenInput').value.trim();
            const port = $('droidPilotPortInput').value.trim() || '7777';
            localStorage.setItem('github_token', token);
            localStorage.setItem('droidpilot_port', port);
            alert("Settings saved. Some changes may require page refresh.");
            window.closeSettings();
            location.reload(); // Refresh to apply port changes etc
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
        content = html_content.replace('href="apkhunter.html"', 'href="dashboard/apkhunter.html"')
        content = content.replace('href="apkhunter.html#diagnostics"', 'href="dashboard/apkhunter.html#diagnostics"')
        f.write(content)
    
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
    
    # Load Mastery Data early for stats
    mastery_data = []
    if os.path.exists(MASTERY_LOG_PATH):
        try:
            with open(MASTERY_LOG_PATH, 'r', encoding='utf-8') as f:
                mastery_data = json.load(f)
        except: pass

    header, days, body, prev_avg, prev_pace = parse_txt()
    stats = calculate_stats(days, mastery_data)
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
