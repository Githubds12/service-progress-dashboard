import requests
import json
import time

class ForDealAPI:
    def __init__(self):
        self.base_url = "https://gw.fordeal.com/gw"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 15; Pixel 7 Build/AP4A.250205.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/147.0.7727.111 Mobile Safari/537.36 data={\"CountryCode\":\"\",\"_fbc\":\"\",\"aaid\":\"f51ee336-e489-4882-8c21-95ff06ed4a9a\",\"app_store\":\"googleplay\",\"app_uuid\":\"afa8fb04-717c-4a32-82ca-433cdbf0e03e\",\"appname\":\"fordeal\",\"build\":\"345\",\"cur\":\"USD\",\"deeplink\":\"\",\"device_id\":\"Ada8d7421258a0b43736365a722c0d675\",\"device_lan\":\"en\",\"device_region\":\"IN\",\"device_type\":\"google Pixel 7\",\"device_uuid\":\"da8d7421258a0b43736365a722c0d675\",\"dpi\":420,\"f\":\"\",\"f_deeplink\":\"\",\"f_dpSource\":\"\",\"f_ts\":0,\"geo\":\"[\\\"0.0\\\",\\\"0.0\\\"]\",\"imsi\":\"[\\\"\\\",\\\"\\\"]\",\"installation_uuid\":\"00000000-1181-adbe-0000-00000000c5f4\",\"jbk\":0,\"lan\":\"en\",\"latitude\":\"0.0\",\"lbs_granted\":false,\"location_path\":\"\",\"longitude\":\"0.0\",\"net_type\":\"wifi\",\"open_uuid\":\"359b1c82-2938-47ad-98ec-a6dddc2d50cb\",\"open_uuid_ts\":1777804913768,\"region\":\"IN\",\"remote_push\":false,\"screen\":\"1080x2400\",\"session_uuid\":\"8f5d69c2-b071-4b32-8a5f-f0dd37cb6ac7\",\"session_uuid_ts\":1777804913590,\"ssid\":\"<unknown ssid>\",\"ssid_ip\":\"10.72.156.67\",\"system\":\"android\",\"system_version\":\"15\",\"tel_oper\":\"\",\"timezone\":\"19800\",\"timezonename\":\"Asia/Kolkata\",\"uuid\":\"3c1dee66-0ba2-43f1-88b9-3ac5590fe8a3\",\"version\":\"5.8.8\",\"y\":\"\"}",
            "gw-did": "3c1dee66-0ba2-43f1-88b9-3ac5590fe8a3",
            "gw_ver": "1",
            "plat": "android",
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def send_otp(self, phone_number):
        url = f"{self.base_url}/dwp.customerCenter.captchaSend/2"
        data = {
            "number": phone_number,
            "signFrom": "SIGN_IN"
        }
        # Note: 'sign' and 'f-g' headers are mandatory and dynamic.
        # They would need to be generated here.
        payload = f"data={json.dumps(data)}"
        print(f"[*] Sending OTP to {phone_number}...")
        # response = requests.post(url, headers=self.headers, data=payload)
        # return response.json()
        print("[!] Note: Actual request requires 'sign' and 'f-g' headers.")
        return {"code": 1001, "data": True}

    def verify_otp(self, phone_number, code):
        url = f"{self.base_url}/dwp.customerCenter.signIn/1"
        data = {
            "blackBox": "oGPEM1777804915KgJN4quK7k8",
            "loginKey": phone_number,
            "quickSignFrom": "SIGN_IN",
            "quickSignTag": False,
            "registerNewAccountTag": False,
            "secret": code,
            "type": "PHONE_CAPTCHA"
        }
        payload = f"data={json.dumps(data)}"
        print(f"[*] Verifying OTP {code} for {phone_number}...")
        # response = requests.post(url, headers=self.headers, data=payload)
        # return response.json()
        return {"code": 1001, "data": {"signSuccess": False, "signErrorMsg": "Invalid verification code"}}

if __name__ == "__main__":
    api = ForDealAPI()
    api.send_otp("+393515889024")
    time.sleep(1)
    api.verify_otp("+393515889024", "3625")
