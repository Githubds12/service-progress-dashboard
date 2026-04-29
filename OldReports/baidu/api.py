import requests

url_trigger = "https://edith.xiaohongshu.com/api/sns/v1/system_service/vfc_code"

headers = {
    "User-Agent": "Rednote/9.27.0 (Android; 15; Google Pixel 7)",
    "Accept": "application/json"
}

def trigger_sms(phone, zone):
    params = {
        "phone": phone,
        "zone": zone,
        "type": "login"
    }
    
    print(f"[*] Triggering SMS for {phone} (Zone {zone})...")
    try:
        response = requests.get(url_trigger, headers=headers, params=params, timeout=10)
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        if response.status_code == 403 or "captcha" in response.text.lower():
            print("[!] Blocked by Geetest Captcha.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    trigger_sms("3515868778", "39")
