import requests
import time

base_url = "https://m.eapeakwealth.com"

def send_sms():
    url = f"{base_url}/user/info/send/regist/sms"
    payload = {
        "t": str(int(time.time() * 1000)),
        "deviceId": "f51ee336-e489-4882-8c21-95ff06ed4a9a",
        "sourceId": "12",
        "device": "1",
        "v": "1.3.7.53",
        "market": "googleplay",
        "exchangeId": "7",
        "timeZoneOffset": "19800",
        "remoteLoginTips": "1",
        "currency": "EUR",
        "language": "en-US",
        "telCode": "39",
        "username": "3513093982",
        "auth": "af92cc915d6e95951db569be74d8d30b" # Static auth for test
    }
    
    print(f"[*] Triggering SMS for ehamarkets...")
    try:
        response = requests.post(url, data=payload, timeout=10)
        print("Status Code:", response.status_code)
        print("Response:", response.text)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    send_sms()
