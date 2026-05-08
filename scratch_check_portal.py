import requests
import json

API_BASE = "http://51.195.24.179:8092/api"
EMAIL = "deepanshu@test.com"
PASS = "deep@nshu"
PROJECT_ID = "2582f9bc-1f6b-419c-8c98-42b8dda1583d"

def login():
    res = requests.post(f"{API_BASE}/auth/login", json={"email": EMAIL, "password": PASS})
    if res.status_code == 200:
        return res.json().get("access_token")
    return None

token = login()
if token:
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{API_BASE}/projects/{PROJECT_ID}", headers=headers)
    if res.status_code == 200:
        print(json.dumps(res.json(), indent=2))
    else:
        print(f"Failed to fetch project: {res.status_code}")
        print(res.text)
