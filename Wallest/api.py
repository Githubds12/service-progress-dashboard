import requests

def send_otp(phone_number):
    url = "https://api-auth.wallester.com/v1/sign-up"
    headers = {
        "Host": "api-auth.wallester.com",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": '"Android"',
        "User-Agent": "Mozilla/5.0 (Linux; Android 15; Pixel 7 Build/AP4A.250205.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/147.0.7727.137 Mobile Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": '"Android WebView";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        "Content-Type": "application/json",
        "Origin": "https://client.wallester.com",
        "X-Requested-With": "com.wallester.whitelabel",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Language": "en,en-IN;q=0.9,en-GB;q=0.8,fil-PH;q=0.7,fil;q=0.6,en-US;q=0.1"
    }
    
    payload = {
        "mobile": phone_number,
        "locale": "en",
        "timezone_name": "Asia/Calcutta"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    print(response.status_code)
    print(response.text)

if __name__ == "__main__":
    send_otp("+393720513805")
