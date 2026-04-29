import requests
import json
import time

base_url = "https://acs-m.daraz.com.bd/gw"

headers = {
    "x-appkey": "24937026",
    "x-app-ver": "9.34.0",
    "x-sign": "INVALID_SIGNATURE_TEST",
    "x-mini-wua": "INVALID_WUA",
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "x-t": str(int(time.time())),
    "user-agent": "MTOPSDK/3.1.1.7 (Android;15;Google;Pixel 7)"
}

def send_sms():
    url = f"{base_url}/mtop.lazada.member.user.biz.sendverificationsms/1.0/"
    
    # Missing the 'wua' token in the payload intentionally to demonstrate mtop blocking
    payload = 'data={"bizScene":"MyAccountTab","checkRisk":"true","deliveryType":"sms","enablePhoneRegisterConvertLogin":"false","lzdAppVersion":"1.6","pageSource":"welcome_page","phone":"1331745359","phonePrefixCode":"880","platform":"android","resend":"false","sendCodeTemplate":"default","type":"OTP_LOGIN"}'

    print("[*] Attempting to trigger SMS without valid x-sign and wua token...")
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        print("Status Code:", response.status_code)
        print("Response:", response.text)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    send_sms()
