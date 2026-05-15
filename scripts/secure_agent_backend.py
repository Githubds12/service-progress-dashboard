import os
import json
import http.server
import socketserver
import urllib.request
import urllib.parse
import subprocess
import shutil

# Load PORT from Render environment (default to 10000)
PORT = int(os.environ.get("PORT", 10000))

class SecureAgentHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/agent/chat':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                payload = json.loads(post_data)
                
                api_key = os.getenv("GEMINI_API_KEY", "").replace('"', '').strip()
                if not api_key:
                    return self.send_error_json(500, "GEMINI_API_KEY_MISSING")

                configs = [
                    {"ver": "v1beta", "mod": "gemini-2.0-flash"},
                    {"ver": "v1beta", "mod": "gemini-pro-latest"}
                ]

                for cfg in configs:
                    try:
                        v, m = cfg["ver"], cfg["mod"]
                        url = f"https://generativelanguage.googleapis.com/{v}/models/{m}:generateContent?key={api_key}"
                        req = urllib.request.Request(
                            url,
                            data=json.dumps({"contents": [{"parts": [{"text": payload.get("message", "")}]}]}).encode(),
                            headers={'Content-Type': 'application/json'},
                            method='POST'
                        )
                        with urllib.request.urlopen(req, timeout=30) as res:
                            data = res.read()
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            self.wfile.write(data)
                            return
                    except: continue
                return self.send_error_json(500, "AI_MODELS_EXHAUSTED")
            except Exception as e:
                return self.send_error_json(500, str(e))
        else:
            super().do_POST()

    def do_GET(self):
        if self.path.startswith('/api/tools/run'):
            try:
                query = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(query)
                tool = params.get('tool', [None])[0]
                target = params.get('target', [None])[0]
                
                if not tool or not target:
                    return self.send_error_json(400, "MISSING_PARAMS")
                
                success, output = self.run_tool(tool, target)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success" if success else "error", "output": output}).encode())
            except Exception as e:
                self.send_error_json(500, str(e))
            return
        return super().do_GET()

    def run_tool(self, tool, target):
        commands = {
            "subfinder": ["subfinder", "-d", target, "-silent"],
            "dnsx": ["dnsx", "-d", target, "-silent"],
            "amass": ["amass", "enum", "-d", target, "-passive"],
            "assetfinder": ["assetfinder", "--subs-only", target],
            "naabu": ["naabu", "-host", target, "-silent"],
            "httpx": ["httpx", "-u", target, "-silent"],
            "katana": ["katana", "-u", target, "-silent"]
        }
        
        if tool not in commands:
            return False, f"TOOL_UNKNOWN: {tool}"
            
        binary = commands[tool][0]
        binary_path = shutil.which(binary)
        
        if not binary_path:
            # Check Render Project Bin
            p = f"/opt/render/project/src/bin/{binary}"
            if os.path.exists(p) and os.access(p, os.X_OK):
                binary_path = p
                commands[tool][0] = p

        if not binary_path:
            return False, f"BINARY_MISSING: {binary}"

        try:
            print(f"[*] Running {tool} on {target}...")
            # Use a longer timeout for recon tools
            result = subprocess.run(commands[tool], capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                return True, result.stdout if result.stdout.strip() else "No results."
            return False, result.stderr or result.stdout
        except subprocess.TimeoutExpired:
            return False, "TIMEOUT_300S"
        except Exception as e:
            return False, str(e)

    def send_error_json(self, code, msg):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": msg, "status": "error"}).encode())

class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    server = ThreadingServer(("", PORT), SecureAgentHandler)
    print(f"[*] Gateway listening on port {PORT}")
    server.serve_forever()
