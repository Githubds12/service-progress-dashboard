import os
import re
from datetime import datetime, date
import json
import math
import subprocess

REPORT_DIR = r"c:\Users\Gorri\Documents\Reports"
TXT_FILE = os.path.join(REPORT_DIR, "List of Services done.txt")
HTML_FILE = os.path.join(REPORT_DIR, "Dashboard.html")

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
    
    lines = body.split('\n')
    days = []
    current_day = None
    header = lines[0].strip() 
    
    for line in lines[1:]:
        line = line.strip()
        if not line or line == '----------':
            continue
        
        if re.match(r'^\d+(st|nd|rd|th)\s+[a-zA-Z]+,\s+[a-zA-Z]+$', line):
            current_day = {
                'date': line,
                'services': [],
                'summary': '',
                'earnings': 0,
                'count': 0
            }
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
                
    return header, days, body

def calculate_stats(days):
    total_services = sum(d['count'] for d in days)
    total_earnings = sum(d['earnings'] for d in days)
    
    start_date = date(2026, 4, 10)
    today_dt = date.today()
    days_elapsed = (today_dt - start_date).days
    if days_elapsed <= 0: days_elapsed = 1
    
    avg_daily = total_earnings / days_elapsed if days_elapsed > 0 else total_earnings
    avg_daily_services = total_services / days_elapsed if days_elapsed > 0 else total_services
    
    target = 3000
    target_total = 3000 * 30 
    remaining_target = target_total - total_earnings
    days_remaining = 30 - days_elapsed
    if days_remaining <= 0: days_remaining = 1
    
    recovery_pace_services = remaining_target / 400 / days_remaining
    total_services_needed = remaining_target / 400
    
    # Projection
    projected_total = avg_daily * 30
    
    # Baseline from Day 1
    ideal_daily_baseline = 3000 / 400 # 7.5 services
    
    # Recommendation Logic
    buffer_multiplier = 1.2 
    recommended_today = math.ceil(recovery_pace_services * buffer_multiplier)
    
    today_str_check = f"{get_ordinal(today_dt.day)} {today_dt.strftime('%B')}"
    completed_today = 0
    for d in days:
        if today_str_check in d['date']:
            completed_today = d['count']
            break

    explanation = f"To reach your monthly target of ₹90,000, you need an average of {round(recovery_pace_services, 1)} services/day for the next {days_remaining} days. A {int((buffer_multiplier-1)*100)}% buffer ({recommended_today} total) is recommended to build a safety net. Baseline was {ideal_daily_baseline} services/day."

    projection_sentence = f"At your current pace, you will reach ₹{round(projected_total, 2)} by May 10th. {'Keep it up!' if projected_total >= 90000 else 'Increase daily output to reach your ₹90,000 goal.'}"

    return {
        'total_services': total_services,
        'total_earnings': total_earnings,
        'avg_daily': round(avg_daily, 2),
        'avg_daily_services': round(avg_daily_services, 2),
        'days_elapsed': days_elapsed,
        'target': target,
        'recovery_pace_earnings': round(remaining_target / days_remaining, 2),
        'recovery_pace_services': round(recovery_pace_services, 1),
        'total_services_needed': round(total_services_needed, 1),
        'days_remaining': days_remaining,
        'recommended_today': int(recommended_today),
        'completed_today': completed_today,
        'explanation': explanation,
        'today_date': f"{get_ordinal(today_dt.day)} {today_dt.strftime('%B, %Y')}",
        'ideal_baseline': ideal_daily_baseline,
        'ideal_daily_services': ideal_daily_baseline,
        'projected_total': round(projected_total, 2),
        'projection_sentence': projection_sentence
    }

def update_txt(body, stats):
    new_stats = f"""
Dashboard Stats:
- Total Services: {stats['total_services']}
- Total Earnings: {stats['total_earnings']} rs
- Average Daily Earning (over {stats['days_elapsed']} days since Apr 10): {stats['avg_daily']} rs/day
- Average Daily Services: {stats['avg_daily_services']} services/day
- Target: {stats['target']} rs / day
- Recovery Pace: {stats['recovery_pace_services']} Services / day ({stats['recovery_pace_earnings']} rs/day for {stats['days_remaining']} days)
- Services Needed to Goal: {stats['total_services_needed']}
- Recommended for Today (inc. buffer): {stats['recommended_today']} services
- Projected Monthly Total: ₹{stats['projected_total']}
"""
    with open(TXT_FILE, 'w', encoding='utf-8') as f:
        f.write(body + "\n\n" + new_stats.strip() + "\n")

def update_html(header, days, stats):
    labels = [d['date'].split(',')[0] for d in days]
    earnings = [d['earnings'] for d in days]
    services = [d['count'] for d in days]
    
    services_html = ''
    for d in reversed(days):
        services_list = "".join(f"<li>• {s}</li>" for s in d['services'])
        services_html += f"""
        <div class="service-day">
            <h3>
                <span>{d['date']} <small style="font-weight:normal; color:#8a8d91;">({d['count']} services)</small></span>
                <span style="color:#1877f2;">₹{d['earnings']}</span>
            </h3>
            <ul class="service-list">
                {services_list}
            </ul>
        </div>
        """

    data_dict = {
        'header': header,
        'stats': stats,
        'labels': labels,
        'earnings': earnings,
        'services': services,
        'services_html': services_html
    }
    
    with open('c:/Users/Gorri/Documents/Reports/dashboard_data.js', 'w', encoding='utf-8') as f:
        f.write(f"window.dashboardData = {json.dumps(data_dict)};")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Live Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        :root {{
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.5);
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --bg-dark: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --border: rgba(255, 255, 255, 0.1);
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        
        body {{ 
            background: var(--bg-dark);
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.1) 0px, transparent 50%);
            color: #f8fafc; 
            font-family: 'Outfit', sans-serif; 
            padding: 10px;
            min-height: 100vh;
            overflow-x: hidden;
        }}

        @keyframes pulse {{
            0% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.1); opacity: 0.7; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}

        .live-indicator {{
            display: inline-flex; align-items: center; gap: 6px;
            background: rgba(239, 68, 68, 0.1);
            color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.2);
            padding: 4px 10px; border-radius: 20px; font-size: 10px; font-weight: 700;
            text-transform: uppercase; letter-spacing: 1px;
        }}
        .live-dot {{ width: 6px; height: 6px; background: #ef4444; border-radius: 50%; animation: pulse 1.5s infinite; }}

        .container {{ max-width: 600px; margin: auto; }}
        
        .glass-card {{
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}

        .header {{ text-align: center; margin-bottom: 20px; }}
        .header h1 {{ font-size: 32px; font-weight: 900; letter-spacing: -1px; margin: 10px 0; background: linear-gradient(to right, #fff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}

        .stats-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 15px; }}
        .stat-card {{ padding: 15px; position: relative; overflow: hidden; }}
        .stat-card h3 {{ font-size: 10px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
        .stat-card .value {{ font-size: 24px; font-weight: 700; color: #fff; }}
        .stat-card .subtext {{ font-size: 10px; color: #64748b; margin-top: 4px; }}

        .projection-card {{ 
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
            color: white; border: none;
            display: flex; justify-content: space-between; align-items: center;
        }}
        .proj-val {{ font-size: 28px; font-weight: 900; }}

        .progress-section {{ text-align: center; }}
        .progress-bar-bg {{ height: 10px; background: rgba(255,255,255,0.1); border-radius: 10px; margin: 15px 0; overflow: hidden; }}
        .progress-bar-fill {{ height: 100%; background: var(--success); width: 0%; transition: width 1s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 0 15px var(--success); }}

        .chart-container {{ height: 180px; }}
        
        .recent-activity h2 {{ font-size: 18px; margin-bottom: 15px; font-weight: 700; }}
        .service-item {{ padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }}
        .service-item:last-child {{ border-bottom: none; }}
        .service-header {{ display: flex; justify-content: space-between; font-weight: 600; margin-bottom: 5px; }}
        .service-list {{ list-style: none; color: #94a3b8; font-size: 11px; }}
        .service-list li {{ margin: 3px 0; }}

        #celebration {{ display: none; text-align: center; margin-top: 15px; }}
        .trophy {{ width: 80px; filter: drop-shadow(0 0 20px var(--success)); margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="live-indicator"><span class="live-dot"></span> LIVE</div>
            <h1 id="today-badge">Dashboard</h1>
            <p style="color: #64748b; font-weight: 500;" id="period-header"></p>
        </div>

        <div class="glass-card projection-card">
            <div>
                <h3>ESTIMATED MONTHLY END</h3>
                <div id="projected-val" class="proj-val">₹0</div>
                <p id="projection-text" style="font-size: 11px; opacity: 0.9; margin-top: 5px;"></p>
            </div>
            <img src="financial_growth_graphic_1777206994999.png" style="width: 70px; opacity: 0.8;" alt="Growth">
        </div>

        <div class="glass-card progress-section" id="recommendation-card">
            <h3>DAILY MISSION: <span id="target-count">0</span> SERVICES</h3>
            <div style="display: flex; justify-content: center; align-items: baseline; gap: 8px; margin: 10px 0;">
                <span id="completed-count" style="font-size: 42px; font-weight: 900;">0</span>
                <span style="color: #64748b; font-size: 18px;">/ <span id="target-count-2">0</span></span>
            </div>
            <div class="progress-bar-bg">
                <div id="progress-fill" class="progress-bar-fill"></div>
            </div>
            <p id="explanation-text" style="font-size: 11px; color: #94a3b8; line-height: 1.4;"></p>
            
            <div id="celebration">
                <img src="goal_achievement_icon_1777206977639.png" class="trophy" alt="Goal">
                <h2 style="color: var(--success);">TARGET ACHIEVED! 🚀</h2>
            </div>
        </div>

        <div class="stats-grid">
            <div class="glass-card stat-card">
                <h3>TOTAL EARNED</h3>
                <div id="total-earnings" class="value" style="color: var(--success);">₹0</div>
                <div class="subtext">Across <span id="total-services">0</span> services</div>
            </div>
            <div class="glass-card stat-card">
                <h3>DAILY AVERAGE</h3>
                <div id="avg-daily" class="value">₹0</div>
                <div id="avg-target" class="subtext">Target: ₹3000/d</div>
            </div>
            <div class="glass-card stat-card">
                <h3>RECOVERY PACE</h3>
                <div id="pace-services" class="value" style="color: var(--warning);">0/d</div>
                <div id="pace-earnings" class="subtext">Needed for ₹90k</div>
            </div>
            <div class="glass-card stat-card">
                <h3>TO GOAL</h3>
                <div id="services-to-goal" class="value" style="color: var(--danger);">0</div>
                <div class="subtext">Services remaining</div>
            </div>
        </div>

        <div class="glass-card chart-container">
            <canvas id="earningsChart"></canvas>
        </div>

        <div class="glass-card recent-activity">
            <h2>Recent Activity</h2>
            <div id="services-html"></div>
        </div>

        <p style="text-align: center; color: #475569; font-size: 10px; margin-bottom: 20px;">
            Last update: <span id="last-updated"></span>
        </p>
    </div>

    <script>
        let earningsChart = null;
        let lastDataStr = "";
        let confettiTriggered = false;

        function renderUI(data) {{
            const dataStr = JSON.stringify(data);
            if (dataStr === lastDataStr) return; 
            lastDataStr = dataStr;

            document.getElementById('period-header').innerText = data.header;
            document.getElementById('total-services').innerText = data.stats.total_services;
            document.getElementById('total-earnings').innerText = '₹' + data.stats.total_earnings;
            document.getElementById('avg-daily').innerText = '₹' + data.stats.avg_daily;
            document.getElementById('avg-target').innerText = 'Goal: ₹' + data.stats.target + '/d';
            
            document.getElementById('pace-services').innerText = data.stats.recovery_pace_services + '/d';
            document.getElementById('pace-earnings').innerText = '₹' + data.stats.recovery_pace_earnings + '/d';
            document.getElementById('services-to-goal').innerText = Math.ceil(data.stats.total_services_needed);
            document.getElementById('services-html').innerHTML = data.services_html.replace(/service-day/g, 'service-item').replace(/<h3>/g, '<div class="service-header">').replace(/<\/h3>/g, '</div>');
            
            document.getElementById('target-count').innerText = data.stats.recommended_today;
            document.getElementById('target-count-2').innerText = data.stats.recommended_today;
            document.getElementById('completed-count').innerText = data.stats.completed_today;
            document.getElementById('explanation-text').innerText = data.stats.explanation;
            
            const now = new Date();
            document.getElementById('last-updated').innerText = now.toLocaleTimeString();
            document.getElementById('projected-val').innerText = '₹' + data.stats.projected_total;
            document.getElementById('projection-text').innerText = data.stats.projection_sentence;

            const progress = Math.min((data.stats.completed_today / data.stats.recommended_today) * 100, 100);
            document.getElementById('progress-fill').style.width = progress + '%';

            if (data.stats.completed_today >= data.stats.recommended_today) {{
                document.getElementById('celebration').style.display = 'block';
                if (!confettiTriggered) {{
                    confetti({{ particleCount: 150, spread: 70, origin: {{ y: 0.6 }}, colors: ['#6366f1', '#10b981', '#f59e0b'] }});
                    confettiTriggered = true;
                }}
            }} else {{
                document.getElementById('celebration').style.display = 'none';
                confettiTriggered = false;
            }}

            // Chart
            if (earningsChart) earningsChart.destroy();
            const ctx = document.getElementById('earningsChart').getContext('2d');
            earningsChart = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: data.labels,
                    datasets: [{{
                        label: 'Earnings',
                        data: data.earnings,
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        borderWidth: 3,
                        tension: 0.4,
                        fill: true,
                        pointRadius: 4,
                        pointBackgroundColor: '#6366f1'
                    }}, {{
                        label: 'Target',
                        data: data.labels.map(() => 3000),
                        borderColor: 'rgba(239, 68, 68, 0.5)',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        pointRadius: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#64748b', font: {{ size: 10 }} }} }},
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#64748b', font: {{ size: 10 }} }} }}
                    }}
                }}
            }});
        }}

        function refreshData() {{
            let script = document.createElement('script');
            script.src = 'dashboard_data.js?t=' + new Date().getTime();
            script.onload = () => {{ if (window.dashboardData) renderUI(window.dashboardData); script.remove(); }};
            document.head.appendChild(script);
        }}
        refreshData();
        setInterval(refreshData, 3000);
    </script>
</body>
</html>"""
    with open('c:/Users/Gorri/Documents/Reports/Dashboard_Live.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    with open('c:/Users/Gorri/Documents/Reports/Dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

def update_github():
    print("Updating GitHub...")
    try:
        # Add all changed files
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        
        # Check if there are changes to commit
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
        if not status:
            print("No changes to commit to GitHub.")
            return

        # Commit changes
        commit_msg = f"Auto-update dashboard: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True, capture_output=True)
        
        # Push changes
        subprocess.run(["git", "push"], check=True, capture_output=True)
        print("GitHub updated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e.stderr.decode() if e.stderr else str(e)}")
    except Exception as e:
        print(f"An error occurred while updating GitHub: {e}")

def main():
    header, days, body = parse_txt()
    stats = calculate_stats(days)
    update_txt(body, stats)
    update_html(header, days, stats)
    print("Dashboard updated with Avg Daily Services!")
    update_github()

if __name__ == "__main__":
    main()
