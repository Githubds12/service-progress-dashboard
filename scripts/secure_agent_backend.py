import os
import json
import http.server
import socketserver
import urllib.request
from dotenv import load_dotenv

# Load local .env for development (not used on Render)
load_dotenv()

PORT = int(os.environ.get("PORT", 10000))

class SecureAgentHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/agent/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data)
            
            # 🛡️ SECURE: Pull key from the Render/Local Environment
            api_key = os.getenv("GEMINI_API_KEY")
            
            if not api_key:
                self.send_error_msg(500, "SYSTEM_ERROR: GEMINI_API_KEY not found in environment.")
                return

            try:
                # Proxy the request to Google Gemini
                gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                req = urllib.request.Request(
                    gemini_url,
                    data=json.dumps({
                        "contents": [{"parts": [{"text": payload.get("message", "")}]}]
                    }).encode('utf-8'),
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

            except Exception as e:
                self.send_error_msg(500, f"GATEWAY_ERROR: {str(e)}")
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

    # Serve static files for the dashboard
    def do_GET(self):
        # Allow cross-origin for local testing
        self.send_header('Access-Control-Allow-Origin', '*')
        return super().do_GET()

print(f"[*] SECURE AGENT BACKEND INITIALIZING ON PORT {PORT}")
with socketserver.TCPServer(("", PORT), SecureAgentHandler) as httpd:
    print(f"[*] PORTAL ACTIVE: Keys are secured in the environment.")
    httpd.serve_forever()
