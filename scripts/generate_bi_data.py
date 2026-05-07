import os
import json
import csv
import re

def parse_service_log(file_path):
    """Parses a 'List of Services done' text file and returns a list of service entries."""
    if not os.path.exists(file_path):
        return []
    
    entries = []
    current_date = "Unknown"
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # Detect Date: "15th April, Wednesday" or "7th May, Thursday"
            date_match = re.search(r"(\d+(st|nd|rd|th)\s+[A-Za-z]+,\s+[A-Za-z]+)", line)
            if date_match:
                current_date = date_match.group(1)
                continue
            
            # Parse Service Entry: "1. [12:15] JvSpinBet - org.jvspinbet.client - 400rs"
            # or "1. Hinge - 400rs"
            time = "N/A"
            name = "Unknown"
            package = "Unknown"
            earnings = 0
            
            # Format: 1. [12:15] Name - Package - 400rs
            match_full = re.search(r"\d+\.\s*\[(.*?)\]\s*(.*?)\s*-\s*(.*?)\s*-\s*(\d+)rs", line)
            if match_full:
                time, name, package, earnings = match_full.groups()
            else:
                # Format: 1. Name - 400rs
                match_simple = re.search(r"\d+\.\s*(.*?)\s*-\s*(\d+)rs", line)
                if match_simple:
                    name, earnings = match_simple.groups()
            
            if name != "Unknown" and name != "(Reserved/Skip)":
                entries.append({
                    "name": name.strip(),
                    "date": current_date,
                    "time": time,
                    "package": package.strip(),
                    "earnings": int(earnings)
                })
    except Exception as e:
        print(f"[-] Error parsing {file_path}: {e}")
        
    return entries

def generate_bi_data(reports_root):
    output_path = os.path.join(reports_root, "dashboard", "powerbi_master_data.csv")
    old_reports_dir = os.path.join(reports_root, "OldReports")
    trackers_dir = os.path.join(reports_root, "trackers")
    
    # 1. Collect all folders in OldReports and extract technical details
    details_map = {}
    all_folders = [f for f in os.listdir(old_reports_dir) if os.path.isdir(os.path.join(old_reports_dir, f))]
    
    print(f"[*] Scanning {len(all_folders)} folders in OldReports...")
    
    for folder in all_folders:
        folder_path = os.path.join(old_reports_dir, folder)
        sheet_file = os.path.join(folder_path, "googlesheet.txt")
        details = {
            "Verification Type": "Unknown", "Captcha": "Unknown", 
            "Encryption": "Unknown", "Rate Limits": "Unknown", 
            "Endpoints Involved": "Unknown", "Bot Protection": "Unknown",
            "Service Name": folder,
            "Found Technical": "No"
        }
        
        if os.path.exists(sheet_file):
            details["Found Technical"] = "Yes"
            try:
                with open(sheet_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    fields = {
                        "Verification Type": r"Verification Type:\s*(.*)",
                        "Captcha": r"Captcha:\s*(.*)",
                        "Encryption": r"Encryption:\s*(.*)",
                        "Rate Limits": r"Rate Limits:\s*(.*)",
                        "Endpoints Involved": r"Endpoints Involved:\s*(.*)",
                        "Bot Protection": r"Bot Protection:\s*(.*)",
                        "Service Name": r"Service:\s*(.*)"
                    }
                    for field, pattern in fields.items():
                        match = re.search(pattern, content, re.IGNORECASE)
                        if match:
                            details[field] = match.group(1).strip()
            except Exception as e:
                print(f"[-] Error reading {sheet_file}: {e}")
        
        details_map[details["Service Name"].lower()] = details
        # Also map by folder name just in case
        details_map[folder.lower()] = details

    # 2. Parse Log Files
    log_files = [
        os.path.join(trackers_dir, "List of Services done.txt"),
        os.path.join(old_reports_dir, "List of Services done (10th April to 10th May).txt")
    ]
    
    all_log_entries = []
    for log_f in log_files:
        print(f"[*] Parsing log: {os.path.basename(log_f)}")
        all_log_entries.extend(parse_service_log(log_f))
    
    # 3. Merge Logged Services with Technical Details
    final_rows = []
    logged_names = set()
    
    headers = [
        "Service Name", "Date", "Time", "Earnings (RS)", "Package", "Category",
        "Verification Type", "Captcha", "Encryption", "Rate Limits", 
        "Endpoints Involved", "Bot Protection", "Complexity Index", "Status"
    ]

    def get_complexity(detail):
        score = 0
        bp = detail.get("Bot Protection", "").lower()
        if "alibaba" in bp or "awsc" in bp or "shield" in bp: score += 5
        elif "cloudflare" in bp or "akamai" in bp: score += 4
        elif "captcha" in bp: score += 2
        
        enc = detail.get("Encryption", "").lower()
        if "aes" in enc or "rsa" in enc: score += 3
        elif "base64" in enc or "custom" in enc: score += 2
        
        vt = detail.get("Verification Type", "").lower()
        if "sms" in vt and "device" in vt: score += 3
        elif "sms" in vt: score += 1
        
        return min(10, score) if score > 0 else 1

    for entry in all_log_entries:
        name = entry["name"]
        logged_names.add(name.lower())
        
        detail = details_map.get(name.lower())
        if not detail:
            # Try fuzzy match? (e.g. "JvSpinBet" vs "JvSpinBet")
            detail = {
                "Verification Type": "Unknown", "Captcha": "Unknown", 
                "Encryption": "Unknown", "Rate Limits": "Unknown", 
                "Endpoints Involved": "Unknown", "Bot Protection": "Unknown",
                "Service Name": name
            }
        
        # Category
        category = "General"
        n_lower = name.lower()
        if any(kw in n_lower for kw in ["lyft", "uber", "bolt", "grab", "yandex", "taxi", "ride", "utair", "pegasus"]): category = "Transport/Rideshare"
        elif any(kw in n_lower for kw in ["bet", "casino", "pari", "lucky", "gambling"]): category = "Gambling/Betting"
        elif any(kw in n_lower for kw in ["pay", "bank", "wallet", "crypto", "coin", "finance", "paybis", "deriv", "xtb", "luno"]): category = "Fintech/Crypto"
        elif any(kw in n_lower for kw in ["food", "eat", "delivery", "shop", "grocery", "e-gets", "klook", "daraz", "joybuy", "iherb"]): category = "Delivery/E-commerce"
        elif any(kw in n_lower for kw in ["live", "social", "chat", "meet", "poppo", "soulchill", "live.me"]): category = "Social/Live"

        final_rows.append([
            name, entry["date"], entry["time"], entry["earnings"], entry["package"], category,
            detail["Verification Type"], detail["Captcha"], detail["Encryption"],
            detail["Rate Limits"], detail["Endpoints Involved"], detail["Bot Protection"],
            get_complexity(detail), "Completed"
        ])

    # 4. Add "Orphan" Reports (Folders in OldReports not in logs)
    orphan_count = 0
    for folder_name, detail in details_map.items():
        # Only process unique folder entries
        if detail["Service Name"].lower() not in logged_names:
            orphan_count += 1
            # Try to determine category for orphans too
            category = "General"
            n_lower = detail["Service Name"].lower()
            if any(kw in n_lower for kw in ["lyft", "uber", "bolt", "grab", "yandex", "taxi", "ride"]): category = "Transport/Rideshare"
            
            final_rows.append([
                detail["Service Name"], "Inventory Only", "N/A", 0, "N/A", category,
                detail["Verification Type"], detail["Captcha"], detail["Encryption"],
                detail["Rate Limits"], detail["Endpoints Involved"], detail["Bot Protection"],
                get_complexity(detail), "Research Only"
            ])
            # Add to logged_names to avoid double entries if same name exists in detail_map twice
            logged_names.add(detail["Service Name"].lower())

    # 5. Write CSV
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(final_rows)
    
    print(f"[+] Total Rows: {len(final_rows)}")
    print(f"[+] Logged Services: {len(all_log_entries)}")
    print(f"[+] Inventory-only Services: {orphan_count}")
    print(f"[+] Power BI master data updated at: {output_path}")

if __name__ == "__main__":
    generate_bi_data(r"c:\Users\Gorri\Documents\Reports")
