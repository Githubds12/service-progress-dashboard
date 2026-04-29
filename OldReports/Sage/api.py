import requests

def send_otp(state, phone_number):
    url = "https://id.sage.com/u/mfa-phone-enrollment"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://id.sage.com",
        "Referer": f"https://id.sage.com/u/mfa-phone-enrollment?state={state}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 15; Pixel 7)"
    }
    data = {
        "state": state,
        "phone": phone_number,
        "type": "sms"
    }
    response = requests.post(url, headers=headers, data=data, allow_redirects=False)
    return response

def verify_otp(state, otp_code):
    url = "https://id.sage.com/u/mfa-sms-enrollment-verify"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://id.sage.com",
        "Referer": f"https://id.sage.com/u/mfa-sms-enrollment-verify?state={state}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 15; Pixel 7)"
    }
    data = {
        "state": state,
        "code": otp_code
    }
    response = requests.post(url, headers=headers, data=data, allow_redirects=False)
    return response

if __name__ == "__main__":
    # Sample state from HAR
    sample_state = "hKFo2SBSRFdzUUNGYlg4c3pEY1JEdjUwbldaZUdMTk9hdVlBX6Fuqm1mYS1lbnJvbGyjdGlk2SB0QTFfUzdscXptRzR3V3hrZkxNOHpwNlZ5NVNXRWMyM6NjaWTZIEsxODVlVE9aTlliemFsazZIQTFVa2N2dFV0NTVETWpi"
    sample_phone = "8791267460"
    
    print(f"[*] Sending OTP to {sample_phone}...")
    res = send_otp(sample_state, sample_phone)
    print(f"[+] Response Status: {res.status_code}")
    print(f"[+] Redirect URL: {res.headers.get('Location')}")
