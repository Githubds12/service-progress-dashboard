import os
import re
from datetime import datetime, date
import json
import math
import subprocess

REPORT_DIR = r"c:\Users\Gorri\Documents\Reports"
TXT_FILE = os.path.join(REPORT_DIR, "trackers", "List of Services done.txt")
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
    
    # Extract previous values
    prev_avg_services = 0.0
    prev_recovery_pace = 0.0
    
    m_avg = re.search(r'Average Daily Services:\s+([\d.]+)', old_stats_str)
    if m_avg:
        prev_avg_services = float(m_avg.group(1))
        
    m_pace = re.search(r'Recovery Pace:\s+([\d.]+)', old_stats_str)
    if m_pace:
        prev_recovery_pace = float(m_pace.group(1))
    
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
                
    today_dt = date.today()
    today_str = f"{get_ordinal(today_dt.day)} {today_dt.strftime('%B, %A')}"
    
    today_exists = False
    for d in days:
        if today_str.split(',')[0] in d['date']:
            today_exists = True
            break
            
    if not today_exists:
        new_day_block = f"\n{today_str}\nDaily Summary: 0 services, 0 rs\n----------"
        body += new_day_block
        days.append({
            'date': today_str,
            'services': [],
            'summary': 'Daily Summary: 0 services, 0 rs',
            'earnings': 0,
            'count': 0
        })

    return header, days, body, prev_avg_services, prev_recovery_pace

def calculate_stats(days):
    total_services = sum(len(d['services']) for d in days)
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
            completed_today = len(d['services'])
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
- Average Daily Services: {stats['prev_avg_services']} -> {stats['avg_daily_services']} services/day
- Target: {stats['target']} rs / day
- Recovery Pace: {stats['prev_recovery_pace']} -> {stats['recovery_pace_services']} Services / day ({stats['recovery_pace_earnings']} rs/day for {stats['days_remaining']} days)
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
    
    services_by_day = []
    for d in days:
        services_list = ""
        for s in d['services']:
            # Parse format: 98. [12:45] Urban Outfitters - com.urbanoutfitters.android - 400rs
            match = re.search(r'^\d+\.\s+\[(\d\d:\d\d)\]\s+(.*?)\s+-\s+(.*?)\s+-\s+(\d+)rs', s)
            if match:
                time, name, pkg, price = match.groups()
                item_html = f"""
                <li class="service-item-detail">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; color:#f8fafc; font-size:13px;">{name}</span>
                        <span style="font-size:10px; color:var(--primary); font-weight:600;">{time}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:2px;">
                        <span style="font-size:9px; color:#64748b; font-family:monospace;">{pkg}</span>
                        <span style="font-size:10px; color:var(--success); font-weight:700;">₹{price}</span>
                    </div>
                </li>"""
                services_list += item_html
            else:
                services_list += f"<li class='service-item-detail'>• {s}</li>"

        day_html = f"""
        <div class="service-day">
            <div class="service-header">
                <span>{d['date']} <small style="font-weight:normal; color:#8a8d91;">({d['count']} services)</small></span>
                <span style="color: var(--primary);">₹{d['earnings']}</span>
            </div>
            <ul class="service-list" style="padding-left:0;">
                {services_list}
            </ul>
        </div>
        """
        services_by_day.append(day_html)

    data_dict = {
        'header': header,
        'stats': stats,
        'labels': labels,
        'earnings': earnings,
        'services': services,
        'services_by_day': services_by_day
    }
    
    with open('c:/Users/Gorri/Documents/Reports/dashboard/dashboard_data.js', 'w', encoding='utf-8') as f:
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
            --card-bg: rgba(30, 41, 59, 0.6);
            --border: rgba(255, 255, 255, 0.08);
            --accent-glow: rgba(99, 102, 241, 0.3);
        }}

        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}

        @keyframes shimmer {{
            0% {{ background-position: -200% 0; }}
            100% {{ background-position: 200% 0; }}
        }}

        @keyframes rainbow {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        .rainbow-text {{
            background: linear-gradient(to right, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #8f00ff);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: rainbow 3s linear infinite;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; outline: none; }}
        
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
            margin-bottom: 10px;
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
            position: relative;
        }}

        .glass-card::after {{
            content: '';
            position: absolute;
            inset: -1px;
            border-radius: 20px;
            padding: 1px;
            background: linear-gradient(45deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #8f00ff);
            background-size: 300% 300%;
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            opacity: 0.5;
            animation: rainbow 6s ease infinite;
            pointer-events: none;
        }}

        .header {{ text-align: center; margin-bottom: 20px; }}
        .header h1 {{ font-size: 40px; font-weight: 900; letter-spacing: -2px; margin: 10px 0; background: linear-gradient(to right, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #8f00ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-size: 200% auto; animation: rainbow 3s linear infinite; filter: drop-shadow(0 0 15px rgba(255,255,255,0.2)); }}

        .banner-container {{
            width: 100%; height: 120px; border-radius: 20px; overflow: hidden; margin-bottom: 20px;
            position: relative; box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            animation: float 6s ease-in-out infinite;
        }}
        .banner-img {{ width: 100%; height: 100%; object-fit: cover; opacity: 0.8; filter: brightness(0.8) contrast(1.2); }}
        .banner-overlay {{ position: absolute; inset: 0; background: linear-gradient(to top, var(--bg-dark), transparent); }}

        .quote-card {{
            background: url('quote_bg.png'); background-size: cover; background-position: center;
            border: none; position: relative; overflow: hidden; min-height: 100px;
            display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;
            padding: 25px; color: #fff; text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        }}
        .quote-card::before {{ content: ''; position: absolute; inset: 0; background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(2px); }}
        .quote-text {{ position: relative; font-size: 16px; font-weight: 600; font-style: italic; line-height: 1.5; margin-bottom: 5px; }}
        .quote-author {{ position: relative; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; color: var(--primary); }}

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
        .progress-bar-fill {{ height: 100%; background: linear-gradient(to right, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #8f00ff); background-size: 200% auto; animation: rainbow 2s linear infinite, reach 3s ease-in-out infinite; width: var(--p-width, 0%); transition: width 1s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 0 15px var(--success); position: relative; transform-origin: left; }}
        
        @keyframes reach {{
            0%, 100% {{ width: var(--p-width); filter: brightness(1); }}
            50% {{ width: var(--n-width); filter: brightness(1.3); box-shadow: 0 0 25px var(--success); }}
        }}

        .chart-container {{ height: 180px; }}
        
        .recent-activity h2 {{ font-size: 18px; margin-bottom: 15px; font-weight: 700; position: sticky; top: 0; background: var(--card-bg); z-index: 10; padding-bottom: 10px; }}
        .recent-activity {{ 
            max-height: 500px; 
            overflow-y: auto; 
            padding-right: 10px;
        }}
        
        /* Custom Scrollbar for Recent Activity */
        .recent-activity::-webkit-scrollbar {{ width: 6px; }}
        .recent-activity::-webkit-scrollbar-track {{ background: rgba(255,255,255,0.05); border-radius: 10px; }}
        .recent-activity::-webkit-scrollbar-thumb {{ background: linear-gradient(to bottom, var(--primary), #10b981); border-radius: 10px; }}
        
        .service-item {{ padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }}
        
        .pagination-controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 15px;
            gap: 10px;
        }}
        .pager-btn {{
            background: rgba(255,255,255,0.05);
            border: 1px solid var(--border);
            color: #fff;
            padding: 8px 15px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 600;
            transition: all 0.3s ease;
            flex: 1;
        }}
        .pager-btn:hover:not(:disabled) {{
            background: var(--primary);
            box-shadow: 0 0 15px var(--primary-glow);
            transform: translateY(-2px);
        }}
        .pager-btn:disabled {{
            opacity: 0.3;
            cursor: not-allowed;
        }}
        .page-info {{
            font-size: 11px;
            color: #94a3b8;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .service-item:last-child {{ border-bottom: none; }}
        .service-header {{ display: flex; justify-content: space-between; font-weight: 600; margin-bottom: 5px; }}
        .service-list {{ list-style: none; color: #94a3b8; font-size: 11px; }}
        .service-list li {{ margin: 3px 0; }}
        .service-item-detail {{
            padding: 8px 10px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
            margin-bottom: 8px !important;
            border-left: 3px solid var(--primary);
        }}

        #celebration {{ display: none; text-align: center; margin-top: 15px; }}
        .trophy {{ width: 80px; filter: drop-shadow(0 0 20px var(--success)); margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="live-indicator"><span class="live-dot"></span> LIVE</div>
            <p style="font-size: 14px; color: var(--primary); font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px;">{stats['today_date']}</p>
            <h1 id="today-badge">Dashboard</h1>
            <p style="color: #64748b; font-weight: 500;" id="period-header"></p>
        </div>

        <div class="banner-container">
            <img src="dashboard/productivity_banner.png" class="banner-img" alt="Productivity">
            <div class="banner-overlay"></div>
        </div>

        <div class="glass-card quote-card">
            <div class="quote-text" id="random-quote"></div>
            <div class="quote-author" id="quote-author"></div>
        </div>

        <div class="glass-card projection-card">
            <div>
                <h3>ESTIMATED MONTHLY END</h3>
                <div id="projected-val" class="proj-val">₹0</div>
                <p id="projection-text" style="font-size: 11px; opacity: 0.9; margin-top: 5px;"></p>
            </div>
            <img src="dashboard/financial_growth_graphic_1777206994999.png" style="width: 70px; opacity: 0.8;" alt="Growth">
        </div>

        <div class="glass-card progress-section" id="recommendation-card">
            <h3>DAILY MISSION: <span id="target-count">0</span> SERVICES</h3>
            <div style="display: flex; justify-content: center; align-items: baseline; gap: 8px; margin: 10px 0;">
                <span id="completed-count" style="font-size: 42px; font-weight: 900;">0</span>
                <span style="color: #64748b; font-size: 18px;">/ <span id="target-count-2">0</span></span>
            </div>
            <div class="progress-bar-bg" style="position: relative;">
                <div id="progress-fill" class="progress-bar-fill"></div>
            </div>
            <p id="explanation-text" style="font-size: 11px; color: #94a3b8; line-height: 1.4;"></p>
            
            <div id="celebration">
                <img src="dashboard/goal_achievement_icon_1777206977639.png" class="trophy" alt="Goal">
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
                <div id="avg-services" class="subtext" style="color: var(--primary); font-weight: 700; margin-bottom: 4px;">0 services/day</div>
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
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h2 style="margin: 0;">Recent Activity</h2>
                <span class="page-info" id="page-indicator">Page 1 of 1</span>
            </div>
            <div id="services-html"></div>
            
            <div class="pagination-controls">
                <button class="pager-btn" id="prev-btn" onclick="changePage(-1)">← PREVIOUS</button>
                <button class="pager-btn" id="next-btn" onclick="changePage(1)">NEXT →</button>
            </div>
        </div>

        <p style="text-align: center; color: #475569; font-size: 10px; margin-bottom: 20px;">
            Last update: <span id="last-updated"></span>
        </p>
    </div>

    <script>
        let earningsChart = null;
        let lastDataStr = "";
        let confettiTriggered = false;
        let currentPage = 0;
        let totalPages = 0;
        let serviceData = [];

        const quotes = [
            {{ text: "Success is not final, failure is not fatal: it is the courage to continue that counts.", author: "Winston Churchill" }},
            {{ text: "The only way to do great work is to love what you do.", author: "Steve Jobs" }},
            {{ text: "Don't watch the clock; do what it does. Keep going.", author: "Sam Levenson" }},
            {{ text: "Your limit is only your imagination.", author: "Inspiration" }},
            {{ text: "Push yourself, because no one else is going to do it for you.", author: "Motivation" }},
            {{ text: "Great things never come from comfort zones.", author: "Growth" }},
            {{ text: "Dream it. Wish it. Do it.", author: "Success" }},
            {{ text: "Stay focused. Be kind. Work hard.", author: "Vision" }},
            {{ text: "The future depends on what you do today.", author: "Mahatma Gandhi" }},
            {{ text: "It always seems impossible until it's done.", author: "Nelson Mandela" }}
        ];

        function updateQuote() {{
            const quote = quotes[Math.floor(Math.random() * quotes.length)];
            document.getElementById('random-quote').innerText = `"${{quote.text}}"`;
            document.getElementById('quote-author').innerText = `— ${{quote.author}}`;
        }}
        updateQuote();
        setInterval(updateQuote, 10000);

        function changePage(delta) {{
            currentPage = Math.max(0, Math.min(currentPage + delta, totalPages - 1));
            renderPage();
        }}

        function renderPage() {{
            if (serviceData && serviceData.length > 0) {{
                document.getElementById('services-html').innerHTML = serviceData[currentPage];
                const isLastPage = currentPage === totalPages - 1;
                const pageLabel = isLastPage ? `PAGE ${{currentPage + 1}} (TODAY)` : `PAGE ${{currentPage + 1}}`;
                document.getElementById('page-indicator').innerText = `${{pageLabel}} OF ${{totalPages}}`;
                document.getElementById('prev-btn').disabled = currentPage === 0;
                document.getElementById('next-btn').disabled = currentPage === totalPages - 1;
            }}
        }}

        function renderUI(data) {{
            const dataStr = JSON.stringify(data);
            if (dataStr === lastDataStr) return; 
            const isFirstLoad = lastDataStr === "";
            lastDataStr = dataStr;

            serviceData = data.services_by_day;
            totalPages = serviceData.length;
            if (isFirstLoad || currentPage >= totalPages) currentPage = totalPages - 1;
            renderPage();

            document.getElementById('period-header').innerText = data.header;
            document.getElementById('total-services').innerText = data.stats.total_services;
            document.getElementById('total-earnings').innerText = '₹' + data.stats.total_earnings;
            document.getElementById('avg-daily').innerText = '₹' + data.stats.avg_daily;
            document.getElementById('avg-services').innerText = data.stats.prev_avg_services + ' -> ' + data.stats.avg_daily_services + ' services/day';
            document.getElementById('avg-target').innerText = 'Goal: ₹' + data.stats.target + '/d';
            
            document.getElementById('pace-services').innerText = data.stats.prev_recovery_pace + ' -> ' + data.stats.recovery_pace_services + '/d';
            document.getElementById('pace-earnings').innerText = '₹' + data.stats.recovery_pace_earnings + '/d';
            document.getElementById('services-to-goal').innerText = Math.ceil(data.stats.total_services_needed);
            
            document.getElementById('target-count').innerText = data.stats.recommended_today;
            document.getElementById('target-count-2').innerText = data.stats.recommended_today;
            document.getElementById('completed-count').innerText = data.stats.completed_today;
            document.getElementById('explanation-text').innerText = data.stats.explanation;
            
            const now = new Date();
            document.getElementById('last-updated').innerText = now.toLocaleTimeString();
            document.getElementById('projected-val').innerText = '₹' + data.stats.projected_total;
            document.getElementById('projection-text').innerText = data.stats.projection_sentence;

            const progress = Math.min((data.stats.completed_today / data.stats.recommended_today) * 100, 100);
            const nextProgress = Math.min(((data.stats.completed_today + 0.8) / data.stats.recommended_today) * 100, 100);
            
            const fill = document.getElementById('progress-fill');
            fill.style.setProperty('--p-width', progress + '%');
            fill.style.setProperty('--n-width', nextProgress + '%');
            fill.style.width = progress + '%';

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
            script.src = 'dashboard/dashboard_data.js?t=' + new Date().getTime();
            script.onload = () => {{ if (window.dashboardData) renderUI(window.dashboardData); script.remove(); }};
            document.head.appendChild(script);
        }}
        refreshData();
        setInterval(refreshData, 3000);
    </script>
</body>
</html>"""
    with open('c:/Users/Gorri/Documents/Reports/dashboard/Dashboard_Live.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    with open('c:/Users/Gorri/Documents/Reports/dashboard/Dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    with open('c:/Users/Gorri/Documents/Reports/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

def update_readme(stats):
    readme_path = 'c:/Users/Gorri/Documents/Reports/README.md'
    if not os.path.exists(readme_path):
        return
        
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    stats_section = f"## 📉 Live Stats\n" \
                    f"- **Total Services**: {stats['total_services']}\n" \
                    f"- **Total Earnings**: ₹{stats['total_earnings']}\n" \
                    f"- **Average Daily Services**: {stats['prev_avg_services']:.2f} -> {stats['avg_daily_services']:.2f} services/day\n" \
                    f"- **Average Daily Earnings**: ₹{stats['avg_daily']:.2f}/day\n" \
                    f"- **Recovery Pace**: {stats['prev_recovery_pace']:.1f} -> {stats['recovery_pace_services']:.1f} services/day\n" \
                    f"- **Monthly Projection**: ₹{stats['projected_total']:.2f}\n" \
                    f"- **Last Sync**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    if "## 📉 Live Stats" in content:
        # Improved regex to handle the section replacement more reliably
        new_content = re.sub(r'## 📉 Live Stats\n.*?(?=\n## |$)', stats_section.strip() + "\n", content, flags=re.DOTALL)
    else:
        new_content = content.replace("## 📊 Tech Stack", stats_section + "\n## 📊 Tech Stack")
        
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

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
    header, days, body, prev_avg_services, prev_recovery_pace = parse_txt()
    stats = calculate_stats(days)
    stats['prev_avg_services'] = prev_avg_services
    stats['prev_recovery_pace'] = prev_recovery_pace
    update_txt(body, stats)
    update_html(header, days, stats)
    update_readme(stats)
    print("Dashboard and README updated with Avg Daily Services!")
    update_github()

if __name__ == "__main__":
    main()
