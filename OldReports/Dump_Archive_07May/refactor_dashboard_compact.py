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
        services_list = "".join(f"<li style='padding: 4px 0; color: #cbd5e1; font-size: 0.8rem; border-bottom: 1px dashed rgba(255,255,255,0.05);'>{s}</li>" for s in d['services'])
        services_html += f"""
        <div class="service-day" style="margin-bottom: 8px; background: rgba(15, 23, 42, 0.5); padding: 8px; border-radius: 6px; border-left: 3px solid #3b82f6;">
            <h3 style="margin: 0 0 6px 0; color: #f8fafc; font-size: 0.85rem; font-weight: 600; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 4px; display:flex; justify-content: space-between;">
                <span>{d['date']}</span>
                <span style="color:#10b981; font-size: 0.9rem; font-weight: 700;">₹{d['earnings']}</span>
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; }}
        html, body {{ background: #0f172a; color: #f8fafc; font-family: 'Inter', sans-serif; margin: 0; padding: 5px; min-height: 100vh; font-size: 14px; }}
        .container {{ max-width: 800px; margin: auto; padding: 5px; }}
        .header {{ text-align: center; margin-bottom: 15px; }}
        .header h1 {{ color: #f8fafc; font-size: 1.4rem; margin-bottom: 2px; font-weight: 700; letter-spacing: -0.5px; }}
        .header p {{ color: #94a3b8; font-size: 0.8rem; margin: 0; }}
        
        .stats-container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 8px; margin-bottom: 15px; }}
        .stat-box {{ 
            background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255, 255, 255, 0.05); 
            padding: 10px; border-radius: 8px; text-align: center;
        }}
        .stat-box h2 {{ margin: 0; font-size: 0.65rem; color: #94a3b8; text-transform: uppercase; font-weight: 600; }}
        .stat-box p {{ margin: 4px 0 0 0; font-size: 1.2rem; font-weight: 700; line-height: 1.2; }}
        .goal-text {{ font-size: 0.65rem; color: #94a3b8; margin-top: 2px; font-weight: 500; }}
        
        .chart-container {{ 
            background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255, 255, 255, 0.05); 
            padding: 10px; border-radius: 8px; margin-bottom: 15px; height: 220px; width: 100%; 
        }}
        .services-list-container {{ 
            background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255, 255, 255, 0.05); 
            padding: 12px; border-radius: 8px; margin-bottom: 15px; 
        }}
        .services-list-container h2 {{ color: #f8fafc; margin: 0 0 10px 0; font-size: 1rem; font-weight: 600; }}
        
        @media (max-width: 400px) {{
            .stats-container {{ grid-template-columns: 1fr 1fr; }}
            .chart-container {{ height: 180px; }}
            html, body {{ font-size: 12px; }}
        }}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {{ width: 6px; }}
        ::-webkit-scrollbar-track {{ background: #0f172a; }}
        ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 3px; }}
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
                <p id="total-services" style="color: #38bdf8;"></p>
            </div>
            <div class="stat-box">
                <h2>Total Earnings</h2>
                <p id="total-earnings" style="color: #f8fafc;"></p>
            </div>
            <div class="stat-box">
                <h2>Avg Daily Earning</h2>
                <p id="avg-daily" style="color: #fbbf24;"></p>
                <div id="avg-target" class="goal-text" style="color: #ef4444;"></div>
            </div>
            <div class="stat-box">
                <h2>Recovery Pace</h2>
                <p id="pace-services" style="color: #ef4444; font-size: 1.1rem;"></p>
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
            document.getElementById('pace-earnings').innerText = '(₹' + data.stats.recovery_pace_earnings + '/d for ' + data.stats.days_remaining + 'd)';
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
            Chart.defaults.font.size = 10;

            if (earningsChart) {{ earningsChart.destroy(); }}
            const ctx1 = document.getElementById('earningsChart').getContext('2d');
            
            let gradient = ctx1.createLinearGradient(0, 0, 0, 200);
            gradient.addColorStop(0, 'rgba(16, 185, 129, 0.4)');
            gradient.addColorStop(1, 'rgba(16, 185, 129, 0.0)');

            earningsChart = new Chart(ctx1, {{
                type: 'line',
                data: {{
                    labels: dates,
                    datasets: [{{
                        label: 'Earnings',
                        data: earnings,
                        borderColor: '#10b981',
                        backgroundColor: gradient,
                        borderWidth: 2,
                        tension: 0.4,
                        fill: true,
                        yAxisID: 'y'
                    }}, {{
                        label: 'Target',
                        data: dailyGoal,
                        borderColor: '#ef4444',
                        borderWidth: 1,
                        borderDash: [3, 3],
                        pointRadius: 0,
                        tension: 0,
                        yAxisID: 'y'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {{ mode: 'index', intersect: false }},
                    plugins: {{
                        title: {{ display: true, text: 'Earnings', font: {{ size: 12, weight: 600 }}, color: '#f8fafc', padding: {{top: 0, bottom: 5}} }},
                        legend: {{ position: 'top', labels: {{ boxWidth: 10, padding: 5 }} }}
                    }},
                    scales: {{
                        x: {{ ticks: {{ maxTicksLimit: 7 }} }},
                        y: {{ type: 'linear', display: true, position: 'left' }}
                    }}
                }}
            }});

            if (servicesChart) {{ servicesChart.destroy(); }}
            const ctx2 = document.getElementById('servicesChart').getContext('2d');
            
            let barGradient = ctx2.createLinearGradient(0, 0, 0, 200);
            barGradient.addColorStop(0, '#8b5cf6');
            barGradient.addColorStop(1, '#6366f1');

            servicesChart = new Chart(ctx2, {{
                type: 'bar',
                data: {{
                    labels: dates,
                    datasets: [{{
                        label: 'Services',
                        data: services,
                        backgroundColor: barGradient,
                        borderRadius: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        title: {{ display: true, text: 'Services Completed', font: {{ size: 12, weight: 600 }}, color: '#f8fafc', padding: {{top: 0, bottom: 5}} }},
                        legend: {{ display: false }}
                    }},
                    scales: {{
                        x: {{ ticks: {{ maxTicksLimit: 7 }}, grid: {{ display: false }} }},
                        y: {{ beginAtZero: true, ticks: {{ stepSize: 1 }} }}
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
