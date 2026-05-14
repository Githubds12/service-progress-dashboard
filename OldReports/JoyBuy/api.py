import requests
import json
import time

# JoyBuy API Automation
BASE_URL = "https://color-api.joybuy.com/"
HEADERS = {
    "User-Agent": "okhttp/4.12.0",
    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    "X-Referer-Package": "com.joybuy.jdi",
    "x-api-device-token": "926eb180f3b6393f",
    "JDI-Lang": "en_GB",
    "s-countryCode": "GB"
}

def verify_account(phone_encrypted):
    url = f"{BASE_URL}?appid=joybuyAPP&functionId=user_account_verifyAccount"
    body = {
        "personalized": True,
        "verticalTag": "cn_ybxt_b2c",
        "businessTag": "cn_ybxt_b2c",
        "pickUpSiteId": "20000068",
        "userActionId": "user_account_verifyAccount"
    }
    # Note: Real implementation would need to add encrypted phone and sign parameter
    payload = f"body={json.dumps(body)}"
    print(f"[*] Verifying account...")
    response = requests.post(url, data=payload, headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    return response.json()

def get_captcha_session(mobile_encrypted):
    url = f"{BASE_URL}?appid=joybuyAPP&functionId=user_account_getCaptchaSessionId"
    body = {
        "sessionSource": "reg",
        "riskType": 2,
        "mobile": mobile_encrypted,
        "mobilePrefix": "+39"
    }
    payload = f"body={json.dumps(body)}"
    print(f"[*] Getting Captcha Session...")
    response = requests.post(url, data=payload, headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    return response.json()

def send_verify_code(identifier_encrypted, session_id, captcha_code):
    url = f"{BASE_URL}?appid=joybuyAPP&functionId=user_account_sendVerifyCode"
    body = {
        "appId": "80001",
        "riskType": 2,
        "idPrefix": "+39",
        "identifier": identifier_encrypted,
        "otpType": "2",
        "scene": "2",
        "sessionId": session_id,
        "captchaAction": "signup",
        "captchaCode": captcha_code,
        "countryCode": "GB",
        "siteCode": "UK-Site"
    }
    payload = f"body={json.dumps(body)}"
    print(f"[*] Sending Verify Code...")
    response = requests.post(url, data=payload, headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    return response.json()

def login_by_code(identifier_encrypted, otp_code, step_code):
    url = f"{BASE_URL}?appid=joybuyAPP&functionId=user_account_loginByVerifyCode"
    body = {
        "idPrefix": "+39",
        "identifier": identifier_encrypted,
        "otpType": "2",
        "scene": "2",
        "verifyCode": otp_code,
        "stepCode": step_code
    }
    payload = f"body={json.dumps(body)}"
    print(f"[*] Logging in by code...")
    response = requests.post(url, data=payload, headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    return response.json()

if __name__ == "__main__":
    # Sample encrypted values from HAR
    ENCRYPTED_MOBILE = "dbfRzlGfFW3%2F4wEuAIb7pfKnYH7lBElZZyImnxS2LA6r7ikVM%252BZyVq72208aXVOJkJ6UBQ3ZXFbL4xylRgfa8pibucGbxlYG6xdYxqJsgNI6%252FK%252BpgJ7YoFzR6IqdXIxsSGrcZ74RO3pDLYK6kFJQh%252BbY8gwxfKliNNSZbsMCwEI%253D"
    ENCRYPTED_ID = "cZSuctPX0ZIp%2BLQvIBG3NQp%2BjVV4PiUf38jBpoMFiPK6wQkXsTZSeGhOvWqKAAh4rQb1lpGbSkxK4DVs9CN9hC7ZBCZL9j41llJodoTno3ptMAqljJWWlCzPRV1rjxTMt9DFVPBluRnyGHu2Qs8Qrtn0vtmyzsVg16m9bv3Mtws%253D"
    
    verify_account(ENCRYPTED_ID)
    session = get_captcha_session(ENCRYPTED_MOBILE)
    session_id = session.get('data', {}).get('sessionId')
    
    if session_id:
        captcha = input("Enter Captcha Code (if solved) or press Enter: ")
        sms_res = send_verify_code(ENCRYPTED_ID, session_id, captcha)
        step_code = sms_res.get('data')
        
        if step_code:
            otp = input("Enter OTP: ")
            login_by_code(ENCRYPTED_ID, otp, step_code)
