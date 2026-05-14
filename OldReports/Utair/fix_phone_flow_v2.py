import requests

API_BASE = "http://51.195.24.179:8092/api"
EMAIL = "deepanshu@test.com"
PASS = "deep@nshu"
SERVICE_UUID = "7fd31965-0477-48fc-82ee-ecf87e4b825e"
SOURCE = "ru.utair.android 5.11.0"

def login():
    res = requests.post(f"{API_BASE}/auth/login", json={"email": EMAIL, "password": PASS})
    if res.status_code == 200:
        return res.json().get("access_token")
    else:
        raise Exception("Login failed: " + res.text)

def update_phone_flow():
    try:
        print("[*] Logging in...")
        token = login()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        print(f"[*] Updating phone flow status via PUT /services/{SERVICE_UUID}/claims/phone-flow...")
        payload = {
            "platform": "android",
            "source": SOURCE,
            "phone_flow": "yes"
        }
        res = requests.put(f"{API_BASE}/services/{SERVICE_UUID}/claims/phone-flow", headers=headers, json=payload)
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.text}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_phone_flow()
