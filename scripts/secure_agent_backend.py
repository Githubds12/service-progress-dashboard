import os
import json
import http.server
import socketserver
import urllib.request
import urllib.parse
import subprocess
import shutil
from datetime import datetime

# Load PORT from Render environment (default to 10000)
PORT = int(os.environ.get("PORT", 10000))
RECON_DIR = "recon_storage"
os.makedirs(RECON_DIR, exist_ok=True)

class SecureAgentHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
        self.send_header('Access-Control-Max-Age', '86400')
        super().end_headers()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """Handle requests in a separate thread."""
    daemon_threads = True

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/agent/chat':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                payload = json.loads(post_data)
                
                api_key = os.getenv("GEMINI_API_KEY", "").replace('"', '').strip()
                if not api_key: return self.send_error_json(500, "GEMINI_API_KEY_MISSING")

                configs = [{"ver": "v1beta", "mod": "gemini-2.0-flash"}, {"ver": "v1beta", "mod": "gemini-pro-latest"}]
                for cfg in configs:
                    try:
                        v, m = cfg["ver"], cfg["mod"]
                        url = f"https://generativelanguage.googleapis.com/{v}/models/{m}:generateContent?key={api_key}"
                        req = urllib.request.Request(url, data=json.dumps({
                            "contents": [{"parts": [{"text": payload.get("message", "")}]}]
                        }).encode(), headers={'Content-Type': 'application/json'}, method='POST')
                        with urllib.request.urlopen(req, timeout=30) as res:
                            data = res.read()
                            self.send_response(200); self.send_header('Content-type', 'application/json'); self.end_headers()
                            self.wfile.write(data); return
                    except Exception as e:
                        print(f"[!] Model {cfg['mod']} failed: {e}")
                        continue
                return self.send_error_json(500, "AI_MODELS_EXHAUSTED")
            except Exception as e: return self.send_error_json(500, str(e))
        
        elif self.path == '/api/tools/save':
            try:
                content_length = int(self.headers['Content-Length'])
                payload = json.loads(self.rfile.read(content_length))
                target = payload.get('target', 'unknown').replace('/', '_').replace('\\', '_')
                tool = payload.get('tool', 'manual').replace('/', '_')
                content = payload.get('output', '')
                
                if not content.strip(): return self.send_error_json(400, "EMPTY_CONTENT")

                filename = f"{target}_{tool}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                filepath = os.path.join(RECON_DIR, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"[+] Intelligence archived: {filename}")
                self.send_response(200); self.send_header('Content-type', 'application/json'); self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "file": filename, "path": f"/recon_storage/{filename}"}).encode())
            except Exception as e: self.send_error_json(500, f"SAVE_FAILED: {str(e)}")
            return
        else:
            self.send_error_json(404, "PATH_NOT_FOUND")

    def do_GET(self):
        if self.path.startswith('/api/tools/run'):
            try:
                query = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(query)
                tool = params.get('tool', [None])[0]
                target = params.get('target', [None])[0]
                
                if not tool or not target: return self.send_error_json(400, "MISSING_PARAMS")
                
                success, output = self.run_tool(tool, target)
                self.send_response(200); self.send_header('Content-type', 'application/json'); self.end_headers()
                self.wfile.write(json.dumps({"status": "success" if success else "error", "output": output}).encode())
            except Exception as e: self.send_error_json(500, str(e))
            return
            
        elif self.path == '/api/tools/list':
            try:
                files = os.listdir(RECON_DIR)
                # Filter for txt files and ensure they exist
                files = [f for f in files if f.endswith('.txt')]
                self.send_response(200); self.send_header('Content-type', 'application/json'); self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "files": sorted(files, reverse=True)}).encode())
            except Exception as e: self.send_error_json(500, str(e))
            return
            
        # Serve static files from recon_storage
        if self.path.startswith('/recon_storage/'):
            return super().do_GET()

        return self.send_error_json(404, "NOT_FOUND")

    def run_tool(self, tool, target):
        commands = {
            "subfinder": ["subfinder", "-d", target, "-silent"],
            "dnsx": ["dnsx", "-silent"], 
            "amass": ["amass", "enum", "-passive", "-d", target],
            "assetfinder": ["assetfinder", "--subs-only", target],
            "naabu": ["naabu", "-host", target, "-s", "c", "-silent"],
            "httpx": ["httpx", "-u", target, "-silent"],
            "katana": ["katana", "-u", target, "-silent"]
        }
        
        if tool not in commands: return False, f"TOOL_UNKNOWN: {tool}"
        binary = commands[tool][0]
        binary_path = shutil.which(binary)
        if not binary_path:
            p = f"/opt/render/project/src/bin/{binary}"
            if os.path.exists(p) and os.access(p, os.X_OK): binary_path = p; commands[tool][0] = p

        if not binary_path: 
            if tool == "naabu": return True, self.run_python_port_scan(target)
            return False, f"BINARY_MISSING: {binary}"

        try:
            print(f"[*] Running {tool} on {target}...")
            stdin_data = (target + "\n") if tool == "dnsx" else None
            result = subprocess.run(commands[tool], input=stdin_data, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return True, result.stdout if result.stdout.strip() else "No results."
            
            # Handle libpcap error for Naabu
            if tool == "naabu" and "libpcap" in (result.stderr or ""):
                print("[!] Naabu libpcap error, using Python fallback.")
                return True, "[SYSTEM] LIBPCAP_MISSING: Using internal engine...\n" + self.run_python_port_scan(target)
                
            return False, result.stderr or result.stdout
        except subprocess.TimeoutExpired: return False, "TIMEOUT_300S"
        except Exception as e: return False, str(e)

    def run_python_port_scan(self, target):
        """Python-based fallback port scanner (no libpcap required)"""
        import socket
        common_ports = [80, 443, 21, 22, 25, 53, 110, 445, 3306, 3389, 5432, 8080, 8443, 9000, 9443]
        results = []
        host = target.split('://')[-1].split('/')[0]
        try:
            ip = socket.gethostbyname(host)
            for port in common_ports:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.4)
                    if s.connect_ex((ip, port)) == 0:
                        results.append(f"{ip}:{port} [OPEN]")
            return "\n".join(results) if results else "No common ports open found on " + ip
        except Exception as e:
            return f"Port scan failed: {str(e)}"

    def send_error_json(self, code, msg):
        self.send_response(code); self.send_header('Content-type', 'application/json'); self.end_headers()
        self.wfile.write(json.dumps({"error": msg, "status": "error"}).encode())

class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    server = ThreadingServer(("", PORT), SecureAgentHandler)
    print(f"[*] Gateway listening on port {PORT}")
    server.serve_forever()

