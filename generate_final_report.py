import json
import os

# Paths
JSON_PATH = r"c:\Users\Gorri\Documents\Reports\recon_storage\recon_replit.com_1778865804.json"
REPORT_PATH = r"c:\Users\Gorri\Documents\Reports\FULL_RECON_REPORT_REPLIT_COMPLETE.md"

def generate():
    if not os.path.exists(JSON_PATH):
        print("JSON data not found!")
        return

    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    with open(REPORT_PATH, "w", encoding='utf-8') as f:
        f.write(f"# 🛡️ COMPLETE RECONNAISSANCE REPORT: {data['target']}\n")
        f.write(f"Generated: 2026-05-16\n\n")
        
        f.write("## 📊 EXECUTIVE SUMMARY\n")
        f.write(f"- **Subdomains Found:** {len(data['subdomains'])}\n")
        f.write(f"- **Live Web Servers:** {len(data['live_hosts'])}\n")
        f.write(f"- **Open Ports Detected:** {len(data['open_ports'])}\n\n")

        f.write("## 🌐 1. FULL SUBDOMAIN INVENTORY (520)\n")
        for i, sub in enumerate(data['subdomains'], 1):
            f.write(f"{i}. {sub}\n")
        
        f.write("\n## ⚡ 2. FULL LIVE HOSTS CATALOG (81)\n")
        f.write("| URL | Status | Title |\n")
        f.write("| --- | --- | --- |\n")
        for host in data['live_hosts']:
            f.write(f"| {host.get('url')} | {host.get('status-code')} | {host.get('title', 'N/A')} |\n")

        f.write("\n## 🔌 3. FULL PORT MAP (271)\n")
        for port in data['open_ports']:
            f.write(f"- `{port}`\n")

    print(f"Complete report generated at: {REPORT_PATH}")

if __name__ == "__main__":
    generate()
