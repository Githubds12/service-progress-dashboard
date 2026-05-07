import os
import json
import pandas as pd
import re

# --- CONFIGURATION ---
REPORTS_ROOT = r"c:\Users\Gorri\Documents\Reports"
DASHBOARD_JSON = os.path.join(REPORTS_ROOT, "dashboard", "dashboard_data.json")
OLD_REPORTS_DIR = os.path.join(REPORTS_ROOT, "OldReports")

def get_dataset():
    if not os.path.exists(DASHBOARD_JSON):
        return pd.DataFrame()

    # 1. Load Core Data
    with open(DASHBOARD_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    raw_days = data.get("raw_days", [])
    
    # 2. Extract Details from OldReports
    details_map = {}
    if os.path.exists(OLD_REPORTS_DIR):
        for folder in os.listdir(OLD_REPORTS_DIR):
            sheet_path = os.path.join(OLD_REPORTS_DIR, folder, "googlesheet.txt")
            if os.path.exists(sheet_path):
                with open(sheet_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    d = {
                        "BotProtection": re.search(r"Bot Protection:\s*(.*)", content, re.I),
                        "RateLimits": re.search(r"Rate Limits:\s*(.*)", content, re.I),
                        "Verification": re.search(r"Verification Type:\s*(.*)", content, re.I)
                    }
                    details_map[folder.lower()] = {k: (v.group(1).strip() if v else "Standard") for k, v in d.items()}

    # 3. Build Flat List
    rows = []
    for day in raw_days:
        date = day.get("date", "Unknown")
        for s_str in day.get("services", []):
            match = re.search(r"\[(.*?)\]\s*(.*?)\s*-\s*(.*?)\s*-\s*(\d+)rs", s_str)
            if match:
                time, name, pkg, earn = match.groups()
                detail = details_map.get(name.lower(), details_map.get(folder.lower(), {}))
                
                # Complexity Logic
                bp = detail.get("BotProtection", "Standard")
                complexity = 1
                if any(x in bp.lower() for x in ["cloudflare", "akamai", "datadome"]): complexity = 3
                elif any(x in bp.lower() for x in ["captcha", "hcaptcha", "recaptcha"]): complexity = 2
                
                rows.append({
                    "Date": date,
                    "Time": time,
                    "Service": name,
                    "Package": pkg,
                    "Earnings": int(earn),
                    "BotProtection": bp,
                    "ComplexityIndex": complexity,
                    "RateLimits": detail.get("RateLimits", "Unknown"),
                    "Verification": detail.get("Verification", "SMS")
                })
    
    return pd.DataFrame(rows)

# Power BI expects the final dataframe to be in a variable
dataset = get_dataset()
print(dataset.head())
