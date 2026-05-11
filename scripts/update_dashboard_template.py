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
        .heat-level-1 {{ background: #0e4429; }}
        .heat-level-2 {{ background: #006d32; }}
        .heat-level-3 {{ background: #26a641; }}
        .heat-level-4 {{ background: #39d353; }}
        
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

        @media (max-width: 1100px) {{
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
