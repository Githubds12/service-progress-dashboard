import os
import json
import csv
import re

def generate_bi_data(reports_root):
    output_path = os.path.join(reports_root, "dashboard", "powerbi_master_data.csv")
    old_reports_dir = os.path.join(reports_root, "OldReports")
    
    # 1. Load data from dashboard_data.json
    dashboard_json = os.path.join(reports_root, "dashboard", "dashboard_data.json")
    if not os.path.exists(dashboard_json):
        print(f"[-] Dashboard data not found at {dashboard_json}")
        return

    with open(dashboard_json, "r", encoding="utf-8") as f:
        dashboard_data = json.load(f)
    
    raw_days = dashboard_data.get("raw_days", [])
    
    # 2. Map of detailed info from OldReports/googlesheet.txt
    details_map = {}
    for folder in os.listdir(old_reports_dir):
        folder_path = os.path.join(old_reports_dir, folder)
        if os.path.isdir(folder_path):
            sheet_file = os.path.join(folder_path, "googlesheet.txt")
            if os.path.exists(sheet_file):
                details = {}
                with open(sheet_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    fields = {
                        "Verification Type": r"Verification Type:\s*(.*)",
                        "Captcha": r"Captcha:\s*(.*)",
                        "Encryption": r"Encryption:\s*(.*)",
                        "Rate Limits": r"Rate Limits:\s*(.*)",
                        "Endpoints Involved": r"Endpoints Involved:\s*(.*)",
                        "Bot Protection": r"Bot Protection:\s*(.*)"
                    }
                    for field, pattern in fields.items():
                        match = re.search(pattern, content, re.IGNORECASE)
                        details[field] = match.group(1).strip() if match else "Unknown"
                
                service_name_match = re.search(r"Service:\s*(.*)", content, re.IGNORECASE)
                service_name = service_name_match.group(1).strip() if service_name_match else folder
                details_map[service_name.lower()] = details

    # 3. Flatten Data
    headers = [
        "Service Name", "Date", "Time", "Earnings (RS)", "Package", "Category",
        "Verification Type", "Captcha", "Encryption", "Rate Limits", 
        "Endpoints Involved", "Bot Protection"
    ]
    
    final_rows = []
    
    for day in raw_days:
        day_date = day.get("date", "Unknown")
        services = day.get("services", [])
        
        for s_str in services:
            # Parse string: "1. [12:15] JvSpinBet - org.jvspinbet.client - 400rs"
            # or simpler: "1. Hinge - 400rs"
            
            time = "Unknown"
            name = "Unknown"
            package = "Unknown"
            earnings = 400
            
            # Regex for standard format: [12:15] Name - Package - 400rs
            match_full = re.search(r"\[(.*?)\]\s*(.*?)\s*-\s*(.*?)\s*-\s*(\d+)rs", s_str)
            if match_full:
                time, name, package, earnings = match_full.groups()
            else:
                # Fallback for simple format: Name - 400rs
                match_simple = re.search(r"\d+\.\s*(.*?)\s*-\s*(\d+)rs", s_str)
                if match_simple:
                    name, earnings = match_simple.groups()
            
            # Get details
            detail = details_map.get(name.lower(), {
                "Verification Type": "Unknown", "Captcha": "Unknown", 
                "Encryption": "Unknown", "Rate Limits": "Unknown", 
                "Endpoints Involved": "Unknown", "Bot Protection": "Unknown"
            })
            
            # Category
            category = "General"
            n_lower = name.lower()
            if any(kw in n_lower for kw in ["lyft", "uber", "bolt", "grab", "yandex", "taxi", "ride"]): category = "Transport/Rideshare"
            elif any(kw in n_lower for kw in ["bet", "casino", "pari", "lucky"]): category = "Gambling/Betting"
            elif any(kw in n_lower for kw in ["pay", "bank", "wallet", "crypto", "coin", "finance"]): category = "Fintech/Crypto"
            elif any(kw in n_lower for kw in ["food", "eat", "delivery", "shop", "grocery"]): category = "Delivery/E-commerce"
            elif any(kw in n_lower for kw in ["live", "social", "chat", "meet"]): category = "Social/Live"

            final_rows.append([
                name, day_date, time, earnings, package, category,
                detail.get("Verification Type"),
                detail.get("Captcha"),
                detail.get("Encryption"),
                detail.get("Rate Limits"),
                detail.get("Endpoints Involved"),
                detail.get("Bot Protection")
            ])

    # 4. Write CSV
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(final_rows)
    
    print(f"[+] Power BI master data generated at: {output_path}")

if __name__ == "__main__":
    generate_bi_data(r"c:\Users\Gorri\Documents\Reports")
