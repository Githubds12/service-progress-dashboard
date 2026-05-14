import requests
import json
import time

class YaahlanAPI:
    def __init__(self, phone, country_code="IT", area_code="39"):
        self.phone = phone
        self.country_code = country_code
        self.area_code = area_code
        self.session = requests.Session()
        self.base_url = "https://gw-api.yaahlan.fun/yaahlan"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Linux; Android 15; Pixel 7 Build/AP3A.240617.008; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.203 Mobile Safari/537.36",
            "Host": "gw-api.yaahlan.fun",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        self.mmuid = "fcd1feb4e5fbe62d3ded48eb1e8b136c8698e054"
        self.mmuidv3 = "55d64301426dec7e419b365364873f1661383ca15fcc20c282260df10193f0006f"

    def send_verify_code(self):
        url = f"{self.base_url}/mdp-user/login/sendVerifyCode"
        params = {
            "area": "",
            "ext": json.dumps({"a": str(int(time.time() * 1000)), "b": "wifi", "c": "Asia/Kolkata"}),
            "innerVersion": "1",
            "country": "SG",
            "appVersion": "2.4.8",
            "mmuid": self.mmuid,
            "mmuidv3": self.mmuidv3,
            "os": "android",
            "ip": "10.238.129.42",
            "userId": "",
            "appVersionCode": "375",
            "deviceId": "83e9eee0ec75cfdf",
            "rom": "15",
            "osVersion": "Pixel 7",
            "channelKey": "primary",
            "appId": "2005",
            "osType": "android",
            "model": "Pixel 7",
            "lang": "en"
        }
        
        payload = {
            "areaCode": self.area_code,
            "mmuid": self.mmuid,
            "mmuidv3": self.mmuidv3,
            "riskType": "0",
            "mobile": self.phone,
            "countryAreaCode": self.country_code,
            "scene": "login"
        }
        
        print(f"[*] Requesting verification code for {self.phone}...")
        response = self.session.post(url, params=params, data=payload, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ec") == 200:
                print(f"[+] Request successful: {data.get('em')}")
                if data.get("data", {}).get("needUpVerify") == 1:
                    print(f"[!] UpVerify required!")
                    print(f"    Receiver: {data['data']['upVerifyUrl'].split('receiver=')[1].split('&')[0]}")
                    print(f"    Content: {data['data']['upVerifyUrl'].split('content=')[1].split('&')[0]}")
                return True
            else:
                print(f"[-] API Error: {data.get('em')} (Code: {data.get('ec')})")
                return False
        else:
            print(f"[-] HTTP Error: {response.status_code}")
            print(response.text)
            return False

if __name__ == "__main__":
    # Test with captured phone number
    test_phone = "3720517038"
    api = YaahlanAPI(test_phone)
    api.send_verify_code()
