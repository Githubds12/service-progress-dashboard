import os
import json
import http.server
import socketserver
import urllib.request

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

            # Try models and versions in order (Master Mapping)
            configs = [
                {"ver": "v1beta", "mod": "gemini-1.5-flash-latest"},
                {"ver": "v1beta", "mod": "gemini-1.5-flash"},
                {"ver": "v1", "mod": "gemini-1.5-pro"},
                {"ver": "v1", "mod": "gemini-pro"}
            ]
            last_error = ""

            for cfg in configs:
                try:
                    v = cfg["ver"]
                    m = cfg["mod"]
                    gemini_url = f"https://generativelanguage.googleapis.com/{v}/models/{m}:generateContent?key={api_key}"
                    print(f"[*] Trying: {v}/{m}")
                    
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

                except urllib.error.HTTPError as e:
                    err_body = e.read().decode('utf-8')
                    print(f"[!] Google API Error ({e.code}): {err_body}")
                    last_error = f"Google_{e.code}: {err_body}"
                    continue
                except Exception as e:
                    last_error = str(e)
                    print(f"[!] System Error: {last_error}")
                    continue
            
            self.send_error_msg(500, f"AI_GATEWAY_FAILURE: {last_error}")
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
        return super().do_GET()

with socketserver.TCPServer(("", PORT), SecureAgentHandler) as httpd:
    print(f"[*] SECURE PORTAL ACTIVE ON PORT {PORT}")
    httpd.serve_forever()
