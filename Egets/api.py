import requests
import time

def send_sms(mobile, area_code="00856"):
    url = "https://uni.e-gets.com/api/user/app/1.3/captcha/send"
    params = {
        "area_code": area_code,
        "business_type": "1",
        "mobile": mobile,
        "type": "1",
        "captcha_type": "1",
        "fallback": "0",
        "verify": "1777451042-a9h5CxgMyGbq9CwuWor7dTe+d25rv/UPda6Ch65r2iU="
    }
    
    headers = {
        "User-Agent": "E-GetS/4.6.5.20260424.1 (Linux; Android 15; google/Pixel 7) NetType/WiFi Lang/en_us LLD/la scale/2.625",
        "x-client-type": "5",
        "x-locale": "en_us",
        "x-request-id": "69dc8991-fbfe-a817-77d4-d5ad9909d95d",
        "x-device-uuid": "8564b63f-ffd2-465a-aebd-f2466dcafa35",
        "x-currency": "LAK",
        "x-channel": "google",
        "x-lld": "la",
        "x-region-code": "134283520",
        "x-tz": "+0530",
        "x-risk-hmv": "1",
        "x-app-id": "So4uyYkyIwadg70dBA5nTwlwwO9uUS1X",
        "x-timestamp": "1777451042173", # Replaying EXACT timestamp from HAR
        "x-version": "1.0.0",
        "x-sign": "MDUwMmM4OGMzZWUyNzA4N2YwZDg0ZmFhNzJmYjE2MmJmYzY3Y2M1ZDYzNjM3ZTE0ZGI0MThiN2U5ZDJlMmIyYw==",
        "x-sign-type": "S2",
        "x-encrypt-type": "E1",
        "Host": "uni.e-gets.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

    try:
        # Replaying the exact request to see if it works or gives a different error
        response = requests.get(url, params=params, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code, response.text
    except Exception as e:
        print(f"Error: {e}")
        return None, str(e)

if __name__ == "__main__":
    send_sms("973736132")
