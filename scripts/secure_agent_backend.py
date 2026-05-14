import os
import json
import http.server
import socketserver
import urllib.request
import urllib.parse
import subprocess
import json

# Load PORT from Render environment (default to 10000)
PORT = int(os.environ.get("PORT", 10000))

class SecureAgentHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/agent/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data)
            
            # 🛡️ SECURE: Pull and Clean Key
            raw_key = os.getenv("GEMINI_API_KEY", "")
            api_key = raw_key.replace('"', '').replace("'", "").strip()
            
            if not api_key:
                self.send_error_msg(500, "SYSTEM_ERROR: GEMINI_API_KEY not found on Render.")
                return

            # Try models and versions in order (Super-Account Mapping)
            configs = [
                {"ver": "v1beta", "mod": "gemini-2.5-flash"},
                {"ver": "v1beta", "mod": "gemini-2.0-flash"},
                {"ver": "v1beta", "mod": "gemini-pro-latest"},
                {"ver": "v1", "mod": "gemini-pro-latest"}
            ]
            last_error = ""

            for cfg in configs:
                try:
                    v = cfg["ver"]
                    m = cfg["mod"]
                    gemini_url = f"https://generativelanguage.googleapis.com/{v}/models/{m}:generateContent?key={api_key}"
                    
                    req = urllib.request.Request(
                        gemini_url,
                        data=json.dumps({"contents": [{"parts": [{"text": payload.get("message", "")}]}]}).encode('utf-8'),
                        headers={'Content-Type': 'application/json'},
                        method='POST'
                    )
                    with urllib.request.urlopen(req) as response:
                        res_data = response.read()
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                        self.end_headers()
                        self.wfile.write(res_data)
                        return 

                except Exception:
                    continue
            
            self.send_error_msg(500, "AI_GATEWAY_FAILURE: All models exhausted.")
        else:
            super().do_POST()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def send_error_msg(self, code, msg):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"error": msg}).encode())

    def do_GET(self):
        if self.path.startswith('/api/adb/install'):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            tid = params.get('id', [None])[0]
            if not tid:
                self.send_error_msg(400, "Package ID is required")
                return
            
            success, message = self.install_package(tid)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success" if success else "error", "message": message}).encode())
            return

        elif self.path.startswith('/api/tools/run'):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            tool = params.get('tool', [None])[0]
            target = params.get('target', [None])[0]
            
            if not tool or not target:
                self.send_error_msg(400, "Tool and Target are required")
                return
            
            # Normalize target: lower() and check if it's a label like 'Facebook'
            domain = target.lower()
            if domain == 'facebook': domain = 'facebook.com'
            if domain == 'google': domain = 'google.com'
            
            success, output = self.run_tool(tool, domain)
            self.send_response(200) # Always 200 to let UI handle the error message
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success" if success else "error", "output": output}).encode())
            return
        return super().do_GET()

    def run_tool(self, tool, target):
        import shutil
        import os
        
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
            return False, f"UNKNOWN_TOOL: Agent '{tool}' is not registered in the gateway."
            
        binary = commands[tool][0]
        binary_path = shutil.which(binary)
        
        # Search in common Go binary locations if not in PATH
        if not binary_path:
            alt_paths = [
                os.path.expanduser(f"~/bin/{binary}"),
                os.path.expanduser(f"~/go/bin/{binary}"),
                f"/usr/local/bin/{binary}",
                f"/usr/bin/{binary}"
            ]
            for p in alt_paths:
                if os.path.exists(p):
                    binary_path = p
                    commands[tool][0] = p
                    break
        
        if not binary_path:
            return False, f"BINARY_MISSING: '{binary}' is not installed or not in PATH on the server environment (Render/Linux). Please ensure 'bash build.sh' was run."

        try:
            print(f"[*] Executing {tool} on {target}...")
            result = subprocess.run(commands[tool], capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                return True, result.stdout if result.stdout.strip() else f"Execution finished. No results found for {target}."
            else:
                return False, f"TOOL_ERROR: {result.stderr or result.stdout}"
        except subprocess.TimeoutExpired:
            return False, "TIMEOUT: The agent execution exceeded the 300s limit."
        except Exception as e:
            return False, f"SYSTEM_ERROR: {str(e)}"

    def install_package(self, tid):
        try:
            # 1. Search Aptoide for exact package
            search_url = f"https://ws75.aptoide.com/api/7/apps/search?query={tid}"
            with urllib.request.urlopen(search_url) as response:
                data = json.loads(response.read().decode())
                apps = data.get("datalist", {}).get("list", [])
                
                # Filter for exact package name match
                app = next((a for a in apps if a.get("package") == tid), None)
                if not app and apps: app = apps[0] # Fallback to first result
                
                if not app:
                    return False, f"Package {tid} not found on Aptoide."
                
                download_url = app.get("file", {}).get("path")
                if not download_url:
                    return False, "Download URL not found."
                
                # 2. Download to local temp
                temp_apk = f"temp_{tid}.apk"
                print(f"[*] Downloading {tid}...")
                urllib.request.urlretrieve(download_url, temp_apk)
                
                # 3. ADB Install
                print(f"[*] Installing {tid} via ADB...")
                cmd = ["adb", "install", "-r", temp_apk]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                # Cleanup
                if os.path.exists(temp_apk):
                    os.remove(temp_apk)
                
                if result.returncode == 0:
                    return True, f"Successfully installed {tid} on device."
                else:
                    return False, f"ADB Error: {result.stderr or result.stdout}"
                    
        except Exception as e:
            return False, f"Bridge Error: {str(e)}"

with socketserver.TCPServer(("", PORT), SecureAgentHandler) as httpd:
    print(f"[*] SECURE PORTAL ACTIVE ON PORT {PORT}")
    print(f"[*] ADB INSTALL BRIDGE ENABLED")
    httpd.serve_forever()
