import requests
import json

API_BASE = "http://51.195.24.179:8092/api"
EMAIL = "deepanshu@test.com"
PASS = "deep@nshu"

def login():
    res = requests.post(f"{API_BASE}/auth/login", json={"email": EMAIL, "password": PASS})
    if res.status_code == 200:
        return res.json().get("access_token")
    else:
        raise Exception("Login failed: " + res.text)

def search_service(token, query):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{API_BASE}/services", headers=headers, params={"search": query})
    if res.status_code == 200:
        return res.json()
    else:
        print(f"Error searching: {res.text}")
        return []

token = login()
results = search_service(token, "YandexEats")
print(json.dumps(results, indent=2))

results_go = search_service(token, "Yandex")
print(json.dumps(results_go, indent=2))
