import http.server
import socketserver
import socket
import os

PORT = 8000
DIRECTORY = r"c:\Users\Gorri\Documents\Reports"

def get_local_ip():
    try:
        # Create a dummy socket to get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    ip = get_local_ip()
    port = PORT
    httpd = None
    
    # Try finding an open port
    while port < PORT + 100:
        try:
            httpd = socketserver.TCPServer(("", port), Handler)
            break
        except OSError as e:
            if "10048" in str(e) or "address already in use" in str(e).lower():
                port += 1
            else:
                raise
                
    if not httpd:
        print("Error: Could not find an available port.")
        return

    print("\n" + "="*50)
    print("DASHBOARD SERVER IS RUNNING!")
    print("="*50)
    print(f"\nTo access on your phone (must be on same Wi-Fi):")
    print(f"-> http://{ip}:{port}/Dashboard.html\n")
    print("To access on this PC:")
    print(f"-> http://localhost:{port}/Dashboard.html\n")
    print("Press Ctrl+C to stop the server.")
    print("="*50 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        httpd.server_close()

if __name__ == "__main__":
    start_server()
