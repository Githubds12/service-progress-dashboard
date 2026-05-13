import os
import json
import re
from datetime import datetime

# Paths
BUG_BOUNTY_ROOT = r"c:\Users\Gorri\Documents\Bug Bounty"
REPORTS_ROOT = r"c:\Users\Gorri\Documents\Reports"
DASHBOARD_DATA_PATH = os.path.join(REPORTS_ROOT, "dashboard", "bugbounty_data.js")

# Targets to monitor
TARGETS = [
    {"name": "Facebook", "file": os.path.join(BUG_BOUNTY_ROOT, "Facebook", "facebook_subdomains.txt")},
]

CATEGORIES = {
    "API": r"api|graphql|rest|v[0-9]+",
    "Staging": r"staging|dev|test|beta|latest|internal|corp",
    "Admin": r"admin|portal|manage|gw|gateway|m-portal",
    "VPN": r"vpn|citrix|remote|pulse|globalprotect",
}

def analyze_subdomains(file_path):
    if not os.path.exists(file_path):
        return {"total": 0, "high_value": []}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        subdomains = [line.strip() for line in f if line.strip()]
    
    high_value = []
    for sub in subdomains:
        for cat, pattern in CATEGORIES.items():
            if re.search(pattern, sub, re.IGNORECASE):
                priority = "Critical" if "api" in sub.lower() or "admin" in sub.lower() else "High"
                high_value.append({
                    "target": sub,
                    "category": cat,
                    "priority": priority,
                    "recommendation": f"Run {cat} specific probes"
                })
                break
                
    # Sort and unique
    unique_hv = {v['target']: v for v in high_value}.values()
    sorted_hv = sorted(list(unique_hv), key=lambda x: x["priority"])
    
    return {
        "total": len(subdomains),
        "high_value": sorted_hv[:200] # Limit for JS size
    }

def main():
    print("[*] Syncing Bug Bounty Data...")
    
    all_data = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "targets": []
    }
    
    for target in TARGETS:
        print(f"[*] Processing {target['name']}...")
        analysis = analyze_subdomains(target['file'])
        all_data["targets"].append({
            "name": target["name"],
            "stats": {
                "total": analysis["total"],
                "high_value_count": len(analysis["high_value"])
            },
            "findings": analysis["high_value"]
        })
    
    # Write to JS file
    with open(DASHBOARD_DATA_PATH, "w", encoding="utf-8") as f:
        f.write(f"window.bugBountyData = {json.dumps(all_data, indent=4)};")
    
    print(f"[+] Sync Complete! Data saved to {DASHBOARD_DATA_PATH}")

if __name__ == "__main__":
    main()
