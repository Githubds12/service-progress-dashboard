import requests

API_BASE = "http://51.195.24.179:8092/api"
EMAIL = "deepanshu@test.com"
PASS = "deep@nshu"
PROJECT_ID = "29e7e239-a351-47e9-8eb0-e60119abc638"

def login():
    res = requests.post(f"{API_BASE}/auth/login", json={"email": EMAIL, "password": PASS})
    if res.status_code == 200:
        return res.json().get("access_token")
    else:
        raise Exception("Login failed: " + res.text)

def mark_received():
    try:
        print("[*] Logging in...")
        token = login()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        print(f"[*] Marking message received for project {PROJECT_ID}...")
        payload = {"message_received": "yes", "message_note": ""}
        res = requests.put(f"{API_BASE}/projects/{PROJECT_ID}/message-received", headers=headers, json=payload)
        
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    mark_received()
