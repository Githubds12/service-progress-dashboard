import requests
import json

def test_utair_flow():
    base_url = "https://b.utair.ru"
    
    # Step 1: Handshake
    print("Step 1: OAuth Handshake...")
    handshake_url = f"{base_url}/oauth/token"
    handshake_headers = {
        "Authorization": "Basic dXRhaXJfYW5kcm9pZDpzZWNyZXQ=",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    handshake_data = "grant_type=client_credentials"
    
    response = requests.post(handshake_url, headers=handshake_headers, data=handshake_data)
    if response.status_code != 200:
        print(f"Handshake failed: {response.status_code}")
        print(response.text)
        return
    
    token = response.json().get("access_token")
    print(f"Token: {token}")

    # Step 2: Login Initiation (SMS)
    print("\nStep 2: Login Initiation (SMS)...")
    login_url = f"{base_url}/api/v1/login/"
    login_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-App-Version": "5.11.0",
        "X-Platform": "android"
    }
    login_payload = {
        "login_type": "phone",
        "login": "+393517399395",
        "confirmation_type": "standard"
    }
    
    response = requests.post(login_url, headers=login_headers, json=login_payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    test_utair_flow()
