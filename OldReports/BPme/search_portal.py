import requests
import json

API_BASE = "http://51.195.24.179:8092/api"
EMAIL = "deepanshu@test.com"
PASS = "deep@nshu"

def login():
    res = requests.post(f"{API_BASE}/auth/login", json={"email": EMAIL, "password": PASS})
    return res.json().get("access_token")

def search_service(token, name):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{API_BASE}/services?search={name}", headers=headers)
    return res.json()

token = login()
results = search_service(token, "BPme")
print(json.dumps(results, indent=2))
