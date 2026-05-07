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

def update_claim():
    try:
        print("[*] Logging in...")
        token = login()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Try both "Yes" and "True" to see what works
        print(f"[*] Re-submitting claim with phone_flow='Yes'...")
        payload = {
            "platform": "android",
            "source": SOURCE,
            "phone_flow": "Yes"
        }
        res = requests.post(f"{API_BASE}/services/{SERVICE_UUID}/claim", headers=headers, json=payload)
        print(f"Claim Status Code: {res.status_code}")
        print(f"Claim Response: {res.text}")

        # Also try marking the project specifically if that helps
        # The project ID was 29e7e239-a351-47e9-8eb0-e60119abc638
        PROJECT_ID = "29e7e239-a351-47e9-8eb0-e60119abc638"
        print(f"[*] Updating project {PROJECT_ID} with phone_flow='Yes'...")
        res_proj = requests.put(f"{API_BASE}/projects/{PROJECT_ID}", headers=headers, json={"phone_flow": "Yes"})
        print(f"Project Update Status: {res_proj.status_code}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_claim()
