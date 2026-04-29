import requests

url = "https://my.eneba.com/oauth/token"

headers = {
    "User-Agent": "Eneba/1.9.34 (Android; 15; Google Pixel 7)",
    "Content-Type": "application/x-www-form-urlencoded"
}

def login_test():
    # Example payload from HAR (simplified)
    data = {
        "grant_type": "password",
        "client_id": "875b7ca2-6022-11...",
        "username": "test_user",
        "password": "test_password"
    }
    
    print("[*] Attempting Login to Eneba (Expect Cloudflare Block)...")
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        print("Status Code:", response.status_code)
        if response.status_code == 403:
            print("[!] Blocked by Cloudflare WAF.")
        else:
            print("Response:", response.text[:500])
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    login_test()
