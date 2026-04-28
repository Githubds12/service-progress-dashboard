import requests

url = "https://api.vshowapi.com/user/login"

def login_test():
    params = {
        "type": "phone",
        "phone": "+39 351 857 9897",
        "ext_token": "333333",
        "c": "poppo",
        "v": "534",
        "uuid": "217daab874cc196f"
    }
    
    print("[*] Attempting Login to Poppo Live...")
    try:
        response = requests.post(url, params=params, timeout=10)
        print("Status Code:", response.status_code)
        print("Response:", response.text)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    login_test()
