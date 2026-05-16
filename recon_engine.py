import os
import json
import subprocess
import time
from datetime import datetime

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RECON_DIR = os.path.join(SCRIPT_DIR, "recon_storage")
DATA_FILE = os.path.join(SCRIPT_DIR, "dashboard_data.js")
os.makedirs(RECON_DIR, exist_ok=True)

class ReconEngine:
    def __init__(self, target):
        self.target = target
        self.timestamp = int(time.time())
        self.results = {
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "subdomains": [],
            "live_hosts": [],
            "open_ports": [],
            "crawled_urls": []
        }

    def log(self, message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def run_command(self, cmd, input_data=None, timeout=300):
        try:
            binary = cmd[0]
            local_bin = os.path.join(SCRIPT_DIR, "bin", f"{binary}.exe")
            
            if os.path.exists(local_bin):
                cmd[0] = local_bin
            elif not any(os.path.exists(os.path.join(p, binary)) for p in os.environ["PATH"].split(os.pathsep)):
                render_bin = f"/opt/render/project/src/bin/{binary}"
                if os.path.exists(render_bin):
                    cmd[0] = render_bin
                else:
                    self.log(f"Warning: Binary {binary} not found. Skipping...")
                    return ""

            self.log(f" > Running {' '.join(cmd)}...")
            result = subprocess.run(
                cmd, 
                input=input_data if input_data else None,
                capture_output=True, 
                text=True,
                timeout=timeout
            )
            return result.stdout
        except subprocess.TimeoutExpired:
            self.log(f" ! Timeout expired for {cmd[0]}")
            return ""
        except Exception as e:
            self.log(f" ! Error running {cmd[0]}: {e}")
            return ""

    def execute(self):
        self.log(f"Starting FULL 7-TOOL reconnaissance for {self.target}")
        
        # 1. Subdomain Discovery (3 Tools)
        sub_list = []
        
        # Subfinder
        out = self.run_command(["subfinder", "-d", self.target, "-silent"])
        if out: sub_list.extend(out.splitlines())
        
        # Assetfinder
        out = self.run_command(["assetfinder", "--subs-only", self.target])
        if out: sub_list.extend(out.splitlines())
        
        # Amass
        out = self.run_command(["amass", "enum", "-passive", "-d", self.target, "-silent"])
        if out: sub_list.extend(out.splitlines())
        
        unique_subs = sorted(list(set([s.strip().lower() for s in sub_list if s.strip()])))
        self.results["subdomains"] = unique_subs
        self.log(f"Phase 1 Complete: {len(unique_subs)} subdomains found from 3 sources.")

        # 2. DNS Verification (dnsx)
        dns_out = self.run_command(["dnsx", "-silent"], input_data="\n".join(unique_subs))
        verified_subs = [s.strip() for s in dns_out.splitlines() if s.strip()]
        self.log(f"Phase 2 Complete: {len(verified_subs)} active subdomains.")

        # 3. HTTP Probing (httpx)
        httpx_out = self.run_command(["httpx", "-silent", "-title", "-status-code", "-json"], input_data="\n".join(verified_subs))
        live_data = []
        for line in httpx_out.splitlines():
            try: live_data.append(json.loads(line))
            except: pass
        self.results["live_hosts"] = live_data
        self.log(f"Phase 3 Complete: {len(live_data)} live web hosts.")

        # 4. Port Scanning (naabu)
        naabu_out = self.run_command(["naabu", "-top-ports", "100", "-silent"], input_data="\n".join(verified_subs))
        if naabu_out: 
            self.results["open_ports"] = [p.strip() for p in naabu_out.splitlines() if p.strip()]
        self.log(f"Phase 4 Complete: {len(self.results['open_ports'])} open ports.")

        # 5. Web Crawling (katana)
        # We only crawl the main domain and 2-3 live subdomains to keep it fast
        targets_to_crawl = [self.target] + [h.get('url') for h in live_data[:2] if h.get('url')]
        katana_out = self.run_command(["katana", "-list", ",".join(targets_to_crawl), "-silent", "-d", "1"])
        if katana_out:
            self.results["crawled_urls"] = [u.strip() for u in katana_out.splitlines() if u.strip()]
        self.log(f"Phase 5 Complete: {len(self.results['crawled_urls'])} URLs discovered via Katana.")

        # Finalize
        self.save_results()
        self.generate_report()
        self.update_dashboard_data()
        self.log("Reconnaissance engine finished.")
        return self.results

    def generate_report(self):
        report_path = os.path.join(RECON_DIR, f"report_{self.target}_{self.timestamp}.md")
        with open(report_path, "w", encoding='utf-8') as f:
            f.write(f"# 🛡️ FULL 7-TOOL Recon Report: {self.target}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 📊 Summary Statistics\n")
            f.write(f"- **Total Subdomains:** {len(self.results['subdomains'])}\n")
            f.write(f"- **Live Web Hosts:** {len(self.results['live_hosts'])}\n")
            f.write(f"- **Open Ports Found:** {len(self.results['open_ports'])}\n")
            f.write(f"- **Crawled URLs:** {len(self.results['crawled_urls'])}\n\n")
            
            f.write("## 🌐 Live Infrastructure\n")
            f.write("| URL | Status | Title |\n")
            f.write("| --- | --- | --- |\n")
            for item in self.results['live_hosts'][:100]:
                f.write(f"| {item.get('url')} | {item.get('status-code')} | {item.get('title', 'N/A')} |\n")
            
            if self.results['open_ports']:
                f.write("\n## 🔌 Open Ports (Top 100)\n")
                for port in self.results['open_ports'][:50]:
                    f.write(f"- `{port}`\n")

            if self.results['crawled_urls']:
                f.write("\n## 🕷️ Sample Crawled URLs\n")
                for url in self.results['crawled_urls'][:50]:
                    f.write(f"- {url}\n")
                    
        self.log(f"Report generated: {report_path}")

    def save_results(self):
        filepath = os.path.join(RECON_DIR, f"recon_{self.target}_{self.timestamp}.json")
        with open(filepath, "w") as f:
            json.dump(self.results, f, indent=4)
        self.log(f"JSON Results saved to {filepath}")

    def update_dashboard_data(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as f:
                    content = f.read()
                    data = json.loads(content.replace("const dashboardData = ", "").rstrip(";"))
            else: data = []
        except: data = []

        data.insert(0, self.results)
        with open(DATA_FILE, "w") as f:
            f.write(f"const dashboardData = {json.dumps(data[:10], indent=4)};")
        self.log("Dashboard data updated.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python recon_engine.py <domain>")
        sys.exit(1)
    
    engine = ReconEngine(sys.argv[1])
    engine.execute()
