import requests
import json
import time

# Target: Soul (com.soul.android.international)
# Version: 2.73.1

def send_otp(phone, area="39"):
    url = f"https://api-global.soulapp.me/account/smsCode/deliver?bi=%5B%2219e05b3dc9b%22%2C-1%2C%22google%22%2C%22Android%22%2C35%2C15%2C%22Pixel7%22%2C%22Google%22%2C420%2C%221080*2400%22%2C%22soul%22%2C%22WIFI%22%2C%22en%22%5D&bik=32755"
    
    headers = {
        "api-sign": "54DD6C74D5CF5520EF07126A417A4113CD9BC673",
        "os": "android",
        "api-sign-version": "v7",
        "device-id": "UGl4ZWwgNzdEW3WeeVn2BQ__a4997475a26662c643ac76acd3544177",
        "request-nonce": "0a4bb194ceb34fdfb37f61f963a6a335",
        "app-id": "20000010",
        "app-version": "2.73.1",
        "app-time": "1778212134046",
        "aid": "20000010",
        "av": "2.73.1",
        "at": "1778212134046",
        "sdi": "UGl4ZWwgNzdEW3WeeVn2BQ__a4997475a26662c643ac76acd3544177",
        "language": "en",
        "region": "IT",
        "User-Agent": "M1NJUkdYODFRclcxQkQwbml2ZGNLYVcyWnBub3lBQW9nQXlJVVhjRERYZi9MbWdoeHFEdmZZbGx2ajlvNDBwUg==",
        "cs": "028fc0d9792de056006f00579414175300ac",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "area": area,
        "phone": phone,
        "type": "REGISTER"
    }
    
    response = requests.post(url, headers=headers, data=data)
    return response.json()

if __name__ == "__main__":
    test_phone = "3720517396"
    print(f"Testing OTP delivery for {test_phone}...")
    result = send_otp(test_phone)
    print(json.dumps(result, indent=2))
