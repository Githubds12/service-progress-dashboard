import os
import json
import re
from datetime import datetime

# Paths
BUG_BOUNTY_ROOT = r"c:\Users\Gorri\Documents\Bug Bounty"
REPORTS_ROOT = r"c:\Users\Gorri\Documents\Reports"
DASHBOARD_DATA_PATH = os.path.join(REPORTS_ROOT, "dashboard", "bugbounty_data.js")

CATEGORIES = {
    "API": r"api|graphql|rest|v[0-9]+",
    "Staging": r"staging|dev|test|beta|latest|internal|corp",
    "Admin": r"admin|portal|manage|gw|gateway|m-portal",
    "VPN": r"vpn|citrix|remote|pulse|globalprotect",
}

# Targets to monitor (Auto-discovery)
def discover_targets():
    found = []
    for item in os.listdir(BUG_BOUNTY_ROOT):
        dir_path = os.path.join(BUG_BOUNTY_ROOT, item)
        if os.path.isdir(dir_path):
            # Check for common naming patterns
            patterns = [
                f"{item.lower()}_subdomains.txt",
                f"MASTER_{item.lower()}.txt",
                "subdomains.txt",
                "targets.txt"
            ]
            for p in patterns:
                file_path = os.path.join(dir_path, p)
                if os.path.exists(file_path):
                    found.append({"name": item, "file": file_path})
                    break
    return found

def analyze_subdomains(file_path):
    if not os.path.exists(file_path):
        return {"total": 0, "high_value": []}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            subdomains = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[!] Error reading {file_path}: {e}")
        return {"total": 0, "high_value": []}
    
    high_value = []
    for sub in subdomains:
        for cat, pattern in CATEGORIES.items():
            if re.search(pattern, sub, re.IGNORECASE):
                # Intelligent priority
                priority = "Critical" if any(x in sub.lower() for x in ["api", "admin", "vpn", "auth", "login"]) else "High"
                high_value.append({
                    "target": sub,
                    "category": cat,
                    "priority": priority,
                    "recommendation": f"Run {cat} specific probes & Check for Auth Bypass"
                })
                break
                
    # Sort and unique
    unique_hv = {v['target']: v for v in high_value}.values()
    # Sort: Critical first, then target name
    sorted_hv = sorted(list(unique_hv), key=lambda x: (0 if x["priority"] == "Critical" else 1, x["target"]))
    
    return {
        "total": len(subdomains),
        "high_value": sorted_hv[:500] # Increased limit
    }

def main():
    print("[*] Syncing Bug Bounty Data (Universal Mode)...")
    
    targets = discover_targets()
    print(f"[*] Discovered {len(targets)} targets: {[t['name'] for t in targets]}")

    all_data = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "targets": []
    }
    
    for target in targets:
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
    
    # Sort targets alphabetically
    all_data["targets"].sort(key=lambda x: x["name"])

    # Write to JS file
    with open(DASHBOARD_DATA_PATH, "w", encoding="utf-8") as f:
        f.write(f"window.bugBountyData = {json.dumps(all_data, indent=4)};")
    
    print(f"[+] Sync Complete! Data saved to {DASHBOARD_DATA_PATH}")

if __name__ == "__main__":
    main()
