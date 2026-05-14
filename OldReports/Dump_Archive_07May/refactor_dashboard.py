import os

filepath = 'c:/Users/Gorri/Documents/Reports/update_dashboard.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

prefix = content[:content.find('def update_html(header, days, stats):')]

new_func = r'''def update_html(header, days, stats):
    labels = [d['date'].split(',')[0] for d in days]
    earnings = [d['earnings'] for d in days]
    services = [d['count'] for d in days]
    
    services_html = ''
    for d in reversed(days):
        services_list = "".join(f"<li style='padding: 8px 0; color: #cbd5e1; font-size: 0.85em; border-bottom: 1px dashed rgba(255,255,255,0.05);'>{s}</li>" for s in d['services'])
        services_html += f"""
        <div class="service-day" style="margin-bottom: 15px; background: rgba(15, 23, 42, 0.4); padding: 15px; border-radius: 8px; border-left: 4px solid #3b82f6; transition: transform 0.2s;">
            <h3 style="margin: 0 0 10px 0; color: #f8fafc; font-size: 0.9em; font-weight: 600; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 8px; display:flex; justify-content: space-between;">
                <span>{d['date']}</span>
                <span style="color:#10b981; font-size: 1.05em; font-weight: 800;">₹{d['earnings']}</span>
            </h3>
            <ul class="service-list" style="list-style-type: none; padding: 0; margin: 0;">
                {services_list}
            </ul>
        </div>
        """

    import json
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Progress Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        html, body {{ background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; font-family: 'Inter', sans-serif; margin: 0; padding: 10px; min-height: 100vh; }}
        .container {{ max-width: 1000px; margin: auto; padding: 10px; }}
        .header {{ text-align: center; margin-bottom: 25px; animation: fadeIn 1s ease-out; }}
        .header h1 {{ color: #f8fafc; font-size: 1.8em; margin-bottom: 5px; font-weight: 800; letter-spacing: -0.5px; text-shadow: 0 2px 10px rgba(0,0,0,0.5); }}
        .header p {{ color: #94a3b8; font-size: 0.9em; font-weight: 400; }}
        
        .stats-container {{ display: flex; justify-content: space-around; margin-bottom: 25px; flex-wrap: wrap; gap: 15px; }}
        .stat-box {{ 
            background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); 
            padding: 15px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); text-align: center; flex: 1; min-width: 180px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .stat-box:hover {{ transform: translateY(-3px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.4); border-color: rgba(255,255,255,0.15); }}
        .stat-box h2 {{ margin: 0; font-size: 0.75em; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }}
        .stat-box p {{ margin: 8px 0 0 0; font-size: 1.6em; font-weight: 800; }}
        .goal-text {{ font-size: 0.75em; color: #94a3b8; margin-top: 5px; font-weight: 600; }}
        
        .chart-container {{ 
            background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); 
            padding: 15px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); margin-bottom: 25px; position: relative; height: 320px; width: 100%; box-sizing: border-box; 
        }}
        .services-list-container {{ 
            background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); 
            padding: 20px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); margin-bottom: 25px; 
        }}
        .services-list-container h2 {{ color: #f8fafc; margin-top: 0; margin-bottom: 15px; text-align: center; font-size: 1.2em; font-weight: 600; letter-spacing: -0.5px; }}
        
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(-10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        
        @media (max-width: 768px) {{
            .stat-box {{ min-width: 100%; }}
            .chart-container {{ height: 280px; padding: 10px; }}
            .header h1 {{ font-size: 1.4em; }}
        }}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: #0f172a; }}
        ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #475569; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Freelance Dashboard</h1>
            <p id="period-header">Billing Period: </p>
        </div>
        
        <div class="stats-container">
            <div class="stat-box">
                <h2>Total Services</h2>
                <p id="total-services" style="color: #38bdf8; text-shadow: 0 0 10px rgba(56,189,248,0.3);"></p>
            </div>
            <div class="stat-box">
                <h2>Total Earnings</h2>
                <p id="total-earnings" style="color: #f8fafc;"></p>
            </div>
            <div class="stat-box">
                <h2>Avg Daily Earning</h2>
                <p id="avg-daily" style="color: #fbbf24; text-shadow: 0 0 10px rgba(251,191,36,0.3);"></p>
                <div id="avg-target" class="goal-text" style="color: #ef4444;"></div>
            </div>
            <div class="stat-box">
                <h2>Recovery Pace</h2>
                <p id="pace-services" style="color: #ef4444; font-size: 1.3em; text-shadow: 0 0 10px rgba(239,68,68,0.3);"></p>
                <div id="pace-earnings" class="goal-text"></div>
            </div>
        </div>
        
        <div class="chart-container">
            <canvas id="earningsChart"></canvas>
        </div>
        
        <div class="chart-container">
            <canvas id="servicesChart"></canvas>
        </div>
        
        <div class="services-list-container">
            <h2>Completed Services</h2>
            <div id="services-html"></div>
        </div>
    </div>

    <script>
        let earningsChart = null;
        let servicesChart = null;
        let lastDataStr = "";

        function renderUI(data) {{
            const dataStr = JSON.stringify(data);
            if (dataStr === lastDataStr) return; // Prevent unnecessary re-rendering
            lastDataStr = dataStr;

            document.getElementById('period-header').innerText = 'Billing Period: ' + data.header;
            document.getElementById('total-services').innerText = data.stats.total_services;
            document.getElementById('total-earnings').innerText = '₹' + data.stats.total_earnings;
            document.getElementById('avg-daily').innerText = '₹' + data.stats.avg_daily;
            document.getElementById('avg-target').innerText = 'Target: ₹' + data.stats.target + ' / day';
            document.getElementById('pace-services').innerText = data.stats.recovery_pace_services + ' / day';
            document.getElementById('pace-earnings').innerText = '(₹' + data.stats.recovery_pace_earnings + '/day for ' + data.stats.days_remaining + ' days)';
            document.getElementById('services-html').innerHTML = data.services_html;

            const dates = data.labels;
            const earnings = data.earnings;
            const services = data.services;

            let cumulativeEarnings = [];
            let currentTotal = 0;
            for(let e of earnings) {{
                currentTotal += e;
                cumulativeEarnings.push(currentTotal);
            }}

            const dailyGoal = dates.map(() => 3000);

            Chart.defaults.color = '#94a3b8';
            Chart.defaults.font.family = "'Inter', sans-serif";
            Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.05)';

            if (earningsChart) {{ earningsChart.destroy(); }}
            const ctx1 = document.getElementById('earningsChart').getContext('2d');
            
            let gradient = ctx1.createLinearGradient(0, 0, 0, 400);
            gradient.addColorStop(0, 'rgba(16, 185, 129, 0.4)');
            gradient.addColorStop(1, 'rgba(16, 185, 129, 0.0)');

            earningsChart = new Chart(ctx1, {{
                type: 'line',
                data: {{
                    labels: dates,
                    datasets: [{{
                        label: 'Daily Earnings (₹)',
                        data: earnings,
                        borderColor: '#10b981',
                        backgroundColor: gradient,
                        borderWidth: 3,
                        tension: 0.4,
                        fill: true,
                        yAxisID: 'y'
                    }}, {{
                        label: 'Target Average (₹3000)',
                        data: dailyGoal,
                        borderColor: '#ef4444',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        pointRadius: 0,
                        tension: 0,
                        yAxisID: 'y'
                    }}, {{
                        label: 'Cumulative Earnings (₹)',
                        data: cumulativeEarnings,
                        borderColor: '#38bdf8',
                        borderWidth: 3,
                        borderDash: [5, 5],
                        tension: 0.4,
                        yAxisID: 'y1'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {{ mode: 'index', intersect: false }},
                    plugins: {{
                        title: {{ display: true, text: 'Earnings Progression', font: {{ size: 14, weight: 600 }}, color: '#f8fafc' }},
                        legend: {{ position: 'top', labels: {{ color: '#cbd5e1', font: {{ size: 11 }} }} }}
                    }},
                    scales: {{
                        x: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }}, grid: {{ color: 'rgba(255,255,255,0.05)' }} }},
                        y: {{ type: 'linear', display: true, position: 'left', title: {{ display: false }}, ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }}, grid: {{ color: 'rgba(255,255,255,0.05)' }} }},
                        y1: {{ type: 'linear', display: true, position: 'right', grid: {{ drawOnChartArea: false }}, title: {{ display: false }}, ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }} }}
                    }}
                }}
            }});

            if (servicesChart) {{ servicesChart.destroy(); }}
            const ctx2 = document.getElementById('servicesChart').getContext('2d');
            
            let barGradient = ctx2.createLinearGradient(0, 0, 0, 400);
            barGradient.addColorStop(0, '#8b5cf6');
            barGradient.addColorStop(1, '#6366f1');

            servicesChart = new Chart(ctx2, {{
                type: 'bar',
                data: {{
                    labels: dates,
                    datasets: [{{
                        label: 'Services Completed',
                        data: services,
                        backgroundColor: barGradient,
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        title: {{ display: true, text: 'Daily Services Completed', font: {{ size: 14, weight: 600 }}, color: '#f8fafc' }},
                        legend: {{ display: false }}
                    }},
                    scales: {{
                        x: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }}, grid: {{ display: false }} }},
                        y: {{ beginAtZero: true, ticks: {{ stepSize: 1, color: '#94a3b8', font: {{ size: 10 }} }}, grid: {{ color: 'rgba(255,255,255,0.05)' }} }}
                    }}
                }}
            }});
        }}

        function refreshData() {{
            let script = document.createElement('script');
            script.src = 'dashboard_data.js?t=' + new Date().getTime();
            script.onload = () => {{
                if (window.dashboardData) {{
                    renderUI(window.dashboardData);
                }}
                script.remove();
            }};
            document.head.appendChild(script);
        }}

        refreshData();
        setInterval(refreshData, 3000);
    </script>
</body>
</html>"""
    with open('c:/Users/Gorri/Documents/Reports/Dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    header, days, body = parse_txt()
    stats = calculate_stats(days)
    update_txt(body, stats)
    update_html(header, days, stats)
    print("Dashboard and text file updated successfully!")

if __name__ == "__main__":
    main()
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(prefix + new_func)

print('Updated update_dashboard.py')
