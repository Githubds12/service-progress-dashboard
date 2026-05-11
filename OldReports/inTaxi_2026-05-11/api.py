import requests
import zlib
import base64
import urllib.parse
import json

class InTaxiAPI:
    def __init__(self):
        self.base_url = "https://api-intaxi.taximobile.it/appmobile"
        self.headers = {
            "User-Agent": "Dart/3.6 (dart:io)",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Accept-Encoding": "gzip",
            "Host": "api-intaxi.taximobile.it"
        }
        self.oauth = "bc4ae3d0-ca17-11e3-9c1a-0800200c9a66"
        self.device_uuid = "4ec58b222c30aecd"

    def _encode_data(self, payload):
        json_str = json.dumps(payload, separators=(',', ':'))
        compressed = zlib.compress(json_str.encode('utf-8'))
        return base64.b64encode(compressed).decode('utf-8')

    def _decode_data(self, encoded_str):
        compressed = base64.b64decode(encoded_str)
        decompressed = zlib.decompress(compressed)
        return json.loads(decompressed.decode('utf-8'))

    def get_config(self):
        print("[*] Step 1: Getting Subscription Configuration...")
        payload = {
            "tipo": "getSubscriptionConfiguration",
            "oauth": self.oauth,
            "deviceUUID": self.device_uuid,
            "device_info": {
                "isVirtual": True,
                "manufacturer": "Google",
                "model": "Pixel 7",
                "platform": "Android",
                "uuid": self.device_uuid,
                "version": "15"
            },
            "ver": "4.0.16",
            "lang": "en",
            "tipoApp": "INTAXI",
            "userdef": "INTAXI",
            "id": 66875563,
            "mittente": self.device_uuid,
            "hash": None,
            "dtm": "1778480164561",
            "cnt": 0
        }
        
        data = f"data={urllib.parse.quote(self._encode_data(payload))}"
        response = requests.post(f"{self.base_url}/getSubscriptionConfiguration", headers=self.headers, data=data)
        
        if response.status_code == 200:
            resp_json = response.json()
            decoded_resp = self._decode_data(resp_json.get('data'))
            print("[+] Config retrieved successfully.")
            return decoded_resp
        else:
            print(f"[-] Failed to get config: {response.status_code}")
            return None

    def request_sms(self, phone, magic, captcha):
        print(f"[*] Step 2: Requesting SMS for {phone}...")
        payload = {
            "tipo": "generaCodice",
            "oauth": self.oauth,
            "deviceUUID": self.device_uuid,
            "device_info": {
                "isVirtual": True,
                "manufacturer": "Google",
                "model": "Pixel 7",
                "platform": "Android",
                "uuid": self.device_uuid,
                "version": "15"
            },
            "ver": "4.0.16",
            "lang": "en",
            "tipoApp": "INTAXI",
            "userdef": "INTAXI",
            "id": 66875566,
            "username": "Deepanshu Singh",
            "mittente": phone,
            "magic": magic,
            "captcha": captcha,
            "checkToken": "",
            "tokenError": "",
            "authenticationMethod": "",
            "authenticationId": "1778480283431"
        }
        
        data = f"data={urllib.parse.quote(self._encode_data(payload))}"
        response = requests.post(f"{self.base_url}/generaCodice", headers=self.headers, data=data)
        
        if response.status_code == 200:
            resp_json = response.json()
            decoded_resp = self._decode_data(resp_json.get('data'))
            print(f"[+] SMS Request Result: {decoded_resp}")
            return decoded_resp
        else:
            print(f"[-] Failed to request SMS: {response.status_code}")
            return None

    def verify_sms(self, phone, code):
        print(f"[*] Step 3: Verifying OTP {code} for {phone}...")
        payload = {
            "tipo": "completaRegistrazione",
            "oauth": self.oauth,
            "deviceUUID": self.device_uuid,
            "device_info": {
                "isVirtual": True,
                "manufacturer": "Google",
                "model": "Pixel 7",
                "platform": "Android",
                "uuid": self.device_uuid,
                "version": "15"
            },
            "ver": "4.0.16",
            "lang": "en",
            "tipoApp": "INTAXI",
            "userdef": "INTAXI",
            "id": 66875567,
            "mittente": phone,
            "codice": code,
            "nomeCompleto": "Deepanshu Singh",
            "email": "deepanshusingh@example.com",
            "vatNumber": "",
            "yearOfBirth": "1999",
            "city": "Rome",
            "gender": "Maschio",
            "tacViewed": 1
        }
        
        data = f"data={urllib.parse.quote(self._encode_data(payload))}"
        response = requests.post(f"{self.base_url}/completaRegistrazione", headers=self.headers, data=data)
        
        if response.status_code == 200:
            resp_json = response.json()
            decoded_resp = self._decode_data(resp_json.get('data'))
            print(f"[+] Verification Result: {decoded_resp}")
            return decoded_resp
        else:
            print(f"[-] Failed to verify SMS: {response.status_code}")
            return None

if __name__ == "__main__":
    api = InTaxiAPI()
    config = api.get_config()
    if config:
        magic = config.get('parametri', {}).get('magic')
        print(f"[!] Captcha SVG: {config.get('parametri', {}).get('image')[:50]}...")
        # In a real automation, you'd solve the captcha here.
        # api.request_sms("00393720518803", magic, "1234")
