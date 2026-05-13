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

            # Try models in order of efficiency
            models = ["gemini-1.5-flash", "gemini-pro"]
            last_error = ""

            for model in models:
                try:
                    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
                    print(f"[*] Attempting AI Request using model: {model}")
                    
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
                        self.end_headers()
                        self.wfile.write(res_data)
                        return # Success!

                except Exception as e:
                    last_error = str(e)
                    print(f"[!] Model {model} failed: {last_error}")
                    continue
            
            self.send_error_msg(500, f"AI_GATEWAY_FAILURE: Tried all models. Last error: {last_error}")
        else:
            super().do_POST()

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
