import re
import json
import os
from datetime import datetime

def generate_html():
    file_path = 'List of Services done.txt'
    if not os.path.exists(file_path):
        print(f"File not found: {{file_path}}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse blocks
    blocks = content.split('----------')
    
    dates = []
    services_count = []
    earnings = []
    
    for block in blocks:
        date_match = re.search(r'(\d+[a-z]{2}\s+[A-Za-z]+,\s+[A-Za-z]+)', block)
        summary_match = re.search(r'Daily Summary:\s*(\d+)\s*services,\s*(\d+)\s*rs', block)
        
        if date_match and summary_match:
            dates.append(date_match.group(1).split(',')[0].strip())
            services_count.append(int(summary_match.group(1)))
            earnings.append(int(summary_match.group(2)))

    # Total Earnings
    total_earnings_match = re.search(r'Total Earnings:\s*(\d+)\s*rs', content)
    total_earnings = int(total_earnings_match.group(1)) if total_earnings_match else sum(earnings)
    
    # Calculate days elapsed (From April 10, 2026)
    start_date = datetime(2026, 4, 10)
    today = datetime.now()
    days_elapsed = (today - start_date).days + 1
    
    # Cap days elapsed at 31
    if days_elapsed > 31:
        days_elapsed = 31
    elif days_elapsed < 1:
        days_elapsed = 1
        
    avg_earnings = round(total_earnings / days_elapsed, 2)
    
    # Pace Calculations
    total_days = 31
    target_average = 3000
    total_target = total_days * target_average
    remaining_earnings = total_target - total_earnings
    remaining_days = total_days - days_elapsed
    
    if remaining_days > 0 and remaining_earnings > 0:
        required_daily = remaining_earnings / remaining_days
        required_services = required_daily / 400
        pace_text = f"{required_services:.1f} Services / day"
        pace_subtext = f"(₹{int(required_daily)}/day for {remaining_days} days)"
        pace_color = "#e74c3c" # Red, needs work
    elif remaining_earnings <= 0:
        pace_text = "Goal Reached!"
        pace_subtext = "You hit the monthly target."
        pace_color = "#27ae60" # Green
    else:
        pace_text = "Period Ended"
        pace_subtext = "Billing cycle is over."
        pace_color = "#7f8c8d"

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Progress Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            html, body {{ background-color: #f4f7f6 !important; color: #333 !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; }}
            .container {{ max-width: 1000px; margin: auto; }}
            .header {{ text-align: center; margin-bottom: 40px; }}
            .header h1 {{ color: #2c3e50; font-size: 2.5em; margin-bottom: 10px; }}
            .header p {{ color: #7f8c8d; font-size: 1.2em; }}
            .stats-container {{ display: flex; justify-content: space-around; margin-bottom: 40px; flex-wrap: wrap; gap: 20px; }}
            .stat-box {{ background: #ffffff !important; padding: 20px 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; flex: 1; min-width: 200px; }}
            .stat-box h2 {{ margin: 0; font-size: 1.0em; color: #7f8c8d; text-transform: uppercase; letter-spacing: 1px; }}
            .stat-box p {{ margin: 10px 0 0 0; font-size: 2.2em; font-weight: bold; color: #27ae60; }}
            .goal-text {{ font-size: 0.9em; color: #7f8c8d; margin-top: 5px; font-weight: bold; }}
            .chart-container {{ background: #ffffff !important; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 40px; position: relative; height: 400px; width: 100%; box-sizing: border-box; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Freelance Progress Dashboard</h1>
                <p>Billing Period: 10th April to 10th May</p>
            </div>
            
            <div class="stats-container">
                <div class="stat-box">
                    <h2>Total Services</h2>
                    <p style="color: #2980b9;">{sum(services_count)}</p>
                </div>
                <div class="stat-box">
                    <h2>Total Earnings</h2>
                    <p>₹{total_earnings}</p>
                </div>
                <div class="stat-box">
                    <h2>Avg Daily Earning</h2>
                    <p style="color: #e67e22;">₹{avg_earnings}</p>
                    <div class="goal-text" style="color: #e74c3c;">Target: ₹3000 / day</div>
                </div>
                <div class="stat-box">
                    <h2>Recovery Pace</h2>
                    <p style="color: {pace_color}; font-size: 1.8em;">{pace_text}</p>
                    <div class="goal-text">{pace_subtext}</div>
                </div>
            </div>
            
            <div class="chart-container">
                <canvas id="earningsChart"></canvas>
            </div>
            
            <div class="chart-container">
                <canvas id="servicesChart"></canvas>
            </div>
        </div>

        <script>
            const dates = {json.dumps(dates)};
            const earnings = {json.dumps(earnings)};
            const services = {json.dumps(services_count)};

            // Cumulative earnings calculation
            let cumulativeEarnings = [];
            let currentTotal = 0;
            for(let e of earnings) {{
                currentTotal += e;
                cumulativeEarnings.push(currentTotal);
            }}

            // Daily goal array
            const dailyGoal = dates.map(() => 3000);

            Chart.defaults.color = '#333';
            Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";

            const ctx1 = document.getElementById('earningsChart').getContext('2d');
            new Chart(ctx1, {{
                type: 'line',
                data: {{
                    labels: dates,
                    datasets: [{{
                        label: 'Daily Earnings (₹)',
                        data: earnings,
                        borderColor: '#27ae60',
                        backgroundColor: 'rgba(39, 174, 96, 0.2)',
                        borderWidth: 3,
                        tension: 0.4,
                        fill: true,
                        yAxisID: 'y'
                    }}, {{
                        label: 'Target Average (₹3000)',
                        data: dailyGoal,
                        borderColor: '#e74c3c',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        pointRadius: 0,
                        tension: 0,
                        yAxisID: 'y'
                    }}, {{
                        label: 'Cumulative Earnings (₹)',
                        data: cumulativeEarnings,
                        borderColor: '#2980b9',
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
                        title: {{ display: true, text: 'Earnings Progression', font: {{ size: 18 }}, color: '#2c3e50' }}
                    }},
                    scales: {{
                        x: {{ ticks: {{ color: '#333' }}, grid: {{ color: '#eee' }} }},
                        y: {{ type: 'linear', display: true, position: 'left', title: {{ display: true, text: 'Daily Earnings', color: '#333' }}, ticks: {{ color: '#333' }}, grid: {{ color: '#eee' }} }},
                        y1: {{ type: 'linear', display: true, position: 'right', grid: {{ drawOnChartArea: false }}, title: {{ display: true, text: 'Total Earnings', color: '#333' }}, ticks: {{ color: '#333' }} }}
                    }}
                }}
            }});

            const ctx2 = document.getElementById('servicesChart').getContext('2d');
            new Chart(ctx2, {{
                type: 'bar',
                data: {{
                    labels: dates,
                    datasets: [{{
                        label: 'Services Completed',
                        data: services,
                        backgroundColor: '#8e44ad',
                        borderRadius: 5
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        title: {{ display: true, text: 'Daily Services Completed', font: {{ size: 18 }}, color: '#2c3e50' }},
                        legend: {{ display: false }}
                    }},
                    scales: {{
                        x: {{ ticks: {{ color: '#333' }}, grid: {{ display: false }} }},
                        y: {{ beginAtZero: true, ticks: {{ stepSize: 1, color: '#333' }}, grid: {{ color: '#eee' }} }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    out_file = 'Dashboard.html'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Successfully generated {{out_file}}!")
        
if __name__ == '__main__':
    generate_html()
