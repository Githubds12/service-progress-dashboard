import requests
import json

API_BASE = "http://51.195.24.179:8092/api"
EMAIL = "deepanshu@test.com"
PASS = "deep@nshu"

def login():
    res = requests.post(f"{API_BASE}/auth/login", json={"email": EMAIL, "password": PASS})
    return res.json().get("access_token")

def list_services(token):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{API_BASE}/services", headers=headers)
    return res.json()

token = login()
services = list_services(token)
print(json.dumps(services, indent=2))
