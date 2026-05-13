import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from dotenv import load_dotenv

# Load your local .env
load_dotenv()

class SecretBridgeHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.end_headers()

    def do_GET(self):
        if self.path == '/sync-keys':
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Pack the keys to send to your local dashboard
            keys = {
                "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
                "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
                "GH_PAT": os.getenv("GH_PAT")
            }
            self.wfile.write(json.dumps(keys).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_bridge():
    port = 9999
    server_address = ('', port)
    httpd = HTTPServer(server_address, SecretBridgeHandler)
    print(f"🚀 INTELLIGENCE BRIDGE ACTIVE ON PORT {port}")
    print("Dashboard will now automatically pull keys from your .env file.")
    httpd.serve_forever()

if __name__ == "__main__":
    run_bridge()
