import requests
import json

API_BASE = "http://51.195.24.179:8092/api"
EMAIL = "deepanshu@test.com"
PASS = "deep@nshu"
SERVICE_UUID = "c34dfb4d-3d83-4176-ba7d-3919b5f07e73"

def get_token():
    res = requests.post(f"{API_BASE}/auth/login", json={"email": EMAIL, "password": PASS})
    return res.json().get("access_token")

try:
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{API_BASE}/projects", headers=headers)
    if res.status_code == 200:
        projects = res.json()
        match = next((p for p in projects if p.get('linked_service_id') == SERVICE_UUID), None)
        if match:
            print(f"PROJECT_ID:{match.get('id')}")
        else:
            print("PROJECT_NOT_FOUND")
except Exception as e:
    print(f"ERROR:{e}")
