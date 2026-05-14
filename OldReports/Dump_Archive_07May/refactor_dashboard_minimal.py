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
        services_list = "".join(f"<li>• {s}</li>" for s in d['services'])
        services_html += f"""
        <div class="service-day">
            <h3><span>{d['date']}</span><span style="color:#1877f2;">₹{d['earnings']}</span></h3>
            <ul class="service-list">
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ box-sizing: border-box; }}
        html, body {{ background: #f0f2f5; color: #1c1e21; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 4px; font-size: 12px; }}
        .container {{ max-width: 600px; margin: auto; padding: 0; }}
        .header {{ background: #fff; padding: 8px; border-radius: 6px; margin-bottom: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); text-align: center; }}
        .header h1 {{ color: #1877f2; font-size: 16px; margin: 0 0 2px 0; font-weight: bold; letter-spacing: -0.2px; }}
        .header p {{ color: #606770; font-size: 11px; margin: 0; }}
        
        .stats-container {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-bottom: 6px; }}
        .stat-box {{ background: #fff; padding: 6px 8px; border-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); }}
        .stat-box h2 {{ margin: 0; font-size: 10px; color: #606770; text-transform: uppercase; }}
        .stat-box p {{ margin: 2px 0 0 0; font-size: 14px; font-weight: bold; color: #1c1e21; }}
        .goal-text {{ font-size: 10px; color: #8a8d91; margin-top: 2px; }}
        
        .chart-container {{ background: #fff; padding: 8px; border-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); margin-bottom: 6px; height: 140px; width: 100%; }}
        .services-list-container {{ background: #fff; padding: 8px; border-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); margin-bottom: 6px; }}
        .services-list-container h2 {{ color: #1c1e21; margin: 0 0 8px 0; font-size: 14px; font-weight: bold; border-bottom: 1px solid #e4e6eb; padding-bottom: 4px; }}
        
        .service-day {{ margin-bottom: 6px; padding-bottom: 6px; border-bottom: 1px solid #e4e6eb; }}
        .service-day:last-child {{ border-bottom: none; margin-bottom: 0; padding-bottom: 0; }}
        .service-day h3 {{ margin: 0 0 4px 0; color: #1c1e21; font-size: 12px; font-weight: bold; display:flex; justify-content: space-between; }}
        .service-list {{ list-style-type: none; padding: 0; margin: 0; }}
        .service-list li {{ padding: 2px 0; color: #4b4f56; font-size: 11px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Dashboard</h1>
            <p id="period-header">Billing Period</p>
        </div>
        
        <div class="stats-container">
            <div class="stat-box">
                <h2>Total Services</h2>
                <p id="total-services"></p>
            </div>
            <div class="stat-box">
                <h2>Total Earnings</h2>
                <p id="total-earnings" style="color:#1877f2;"></p>
            </div>
            <div class="stat-box">
                <h2>Avg Daily Earning</h2>
                <p id="avg-daily"></p>
                <div id="avg-target" class="goal-text"></div>
            </div>
            <div class="stat-box">
                <h2>Recovery Pace</h2>
                <p id="pace-services"></p>
                <div id="pace-earnings" class="goal-text"></div>
            </div>
            <div class="stat-box">
                <h2>Services to Goal</h2>
                <p id="services-to-goal" style="color:#fa383e;"></p>
                <div class="goal-text">Target: 225 Total</div>
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

            document.getElementById('period-header').innerText = data.header;
            document.getElementById('total-services').innerText = data.stats.total_services;
            document.getElementById('total-earnings').innerText = '₹' + data.stats.total_earnings;
            document.getElementById('avg-daily').innerText = '₹' + data.stats.avg_daily;
            document.getElementById('avg-target').innerText = 'Target: ₹' + data.stats.target + '/d';
            document.getElementById('pace-services').innerText = data.stats.recovery_pace_services + '/d';
            document.getElementById('pace-earnings').innerText = '(₹' + data.stats.recovery_pace_earnings + ' for ' + data.stats.days_remaining + 'd)';
            document.getElementById('services-to-goal').innerText = data.stats.total_services_needed;
            document.getElementById('services-html').innerHTML = data.services_html;

            const dates = data.labels;
            const earnings = data.earnings;
            const services = data.services;

            const dailyGoal = dates.map(() => 3000);

            Chart.defaults.color = '#606770';
            Chart.defaults.font.family = '-apple-system, sans-serif';
            Chart.defaults.borderColor = '#e4e6eb';
            Chart.defaults.font.size = 9;

            if (earningsChart) {{ earningsChart.destroy(); }}
            const ctx1 = document.getElementById('earningsChart').getContext('2d');

            earningsChart = new Chart(ctx1, {{
                type: 'line',
                data: {{
                    labels: dates,
                    datasets: [{{
                        label: 'Earnings',
                        data: earnings,
                        borderColor: '#1877f2',
                        backgroundColor: 'rgba(24,119,242,0.1)',
                        borderWidth: 1.5,
                        tension: 0,
                        fill: true,
                        pointRadius: 1
                    }}, {{
                        label: 'Target',
                        data: dailyGoal,
                        borderColor: '#fa383e',
                        borderWidth: 1,
                        borderDash: [2, 2],
                        pointRadius: 0,
                        tension: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        title: {{ display: true, text: 'Earnings', font: {{ size: 11, weight: 'bold' }}, color: '#1c1e21', padding: {{top: 0, bottom: 2}} }},
                        legend: {{ display: false }}
                    }},
                    scales: {{
                        x: {{ ticks: {{ maxTicksLimit: 6 }}, grid: {{ display: false }} }},
                        y: {{ beginAtZero: true, ticks: {{ maxTicksLimit: 4 }} }}
                    }}
                }}
            }});

            if (servicesChart) {{ servicesChart.destroy(); }}
            const ctx2 = document.getElementById('servicesChart').getContext('2d');

            servicesChart = new Chart(ctx2, {{
                type: 'bar',
                data: {{
                    labels: dates,
                    datasets: [{{
                        label: 'Services',
                        data: services,
                        backgroundColor: '#42b72a',
                        borderRadius: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        title: {{ display: true, text: 'Services', font: {{ size: 11, weight: 'bold' }}, color: '#1c1e21', padding: {{top: 0, bottom: 2}} }},
                        legend: {{ display: false }}
                    }},
                    scales: {{
                        x: {{ ticks: {{ maxTicksLimit: 6 }}, grid: {{ display: false }} }},
                        y: {{ beginAtZero: true, ticks: {{ stepSize: 1, maxTicksLimit: 4 }} }}
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
