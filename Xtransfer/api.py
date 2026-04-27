import requests
import json

def request_otp(phone, captcha_output, gen_time, lot_number, pass_token, flow_id, server_grant_id):
    url = "https://g-api.xtransfer.com/api/v1/user-front/message/send"
    
    headers = {
        "Content-Type": "application/json",
        "x-server-grant-id": server_grant_id,
        "x-flow-id": flow_id,
        "x-language": "EN",
        "User-Agent": "Mozilla/5.0 (Linux; Android 15; Pixel 7 Build/AP4A.250205.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/147.0.7727.55 Mobile Safari/537.36 XTransfer(XTransfer/3.7.14)"
    }
    
    captcha_v_code = json.dumps({
        "captcha_output": captcha_output,
        "gen_time": gen_time,
        "lot_number": lot_number,
        "pass_token": pass_token
    })
    
    payload = {
        "captchaVCode": captcha_v_code,
        "mobileAreaCode": "91",
        "receiver": phone,
        "verifyType": "SMS",
        "flowId": flow_id
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def verify_otp(phone, otp, flow_id, server_grant_id):
    url = "https://g-api.xtransfer.com/api/v1/user-front/sign-up/login-name"
    
    headers = {
        "Content-Type": "application/json",
        "x-server-grant-id": server_grant_id,
        "x-flow-id": flow_id,
        "x-language": "EN",
        "User-Agent": "Mozilla/5.0 (Linux; Android 15; Pixel 7 Build/AP4A.250205.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/147.0.7727.55 Mobile Safari/537.36 XTransfer(XTransfer/3.7.14)"
    }
    
    payload = {
        "dialingCode": "91",
        "mobile": phone,
        "msgVCode": otp,
        "type": "PHONE",
        "flowId": flow_id,
        "domain": "username",
        "businessSource": "APP_Organic"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if __name__ == "__main__":
    # Example usage (placeholders)
    PHONE = "8791267460"
    FLOW_ID = "c85HuSeu7zUiYcucEcOBWhE8ah2C1v+UBOhVwH/vw3+EEX/K5lB63IJBqgbT+yfB"
    GRANT_ID = "NfANzrfXpAAk0dJ5ysIYQ+lNQM6R5AdAmEFRd2/JXqo="
    
    # In real scenario, CAPTCHA fields are obtained from GeeTest v4 solver
    # result = request_otp(PHONE, "output", "time", "lot", "token", FLOW_ID, GRANT_ID)
    # print(result)
    
    # result = verify_otp(PHONE, "440354", FLOW_ID, GRANT_ID)
    # print(result)
