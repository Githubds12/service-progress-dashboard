import requests

url_send = "https://abakan.taximaxim.ru/0000/Services/Public.svc/api/v2/login/code/sms/send"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Taxsee/3.17.2 (Android; 15; Google Pixel 7)"
}

def trigger_sms(phone):
    params = {
        "city": "18",
        "platform": "CLAPP_ANDROID",
        "udid": "3974a226932ff5cf",
        "sig": "A4D97A93D3144822A8CD980D4792A26B"
    }
    payload = {"locale":"en","phone":phone,"type":"sms","smstoken":"vEMdSjfFO6R"}
    try:
        res = requests.post(url_send, headers=headers, params=params, json=payload, timeout=10)
        print("Status:", res.status_code)
        print("Response:", res.text)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    trigger_sms("393519061133")
