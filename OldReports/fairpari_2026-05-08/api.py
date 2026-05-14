import requests
import json
import time

def test_fairpari_auth():
    session = requests.Session()
    phone = "3720514700"
    
    # Common Headers
    headers = {
        "User-Agent": "org.fairpari.client-user-agent/fairpari-v253.0.2",
        "Version": "fairpari-v253.0.2",
        "X-BundleId": "org.fairpari.client",
        "AppGuid": "aa96c36dff5e61fd_2",
        "X-Language": "en_GB",
        "X-Whence": "22",
        "X-Referral": "339",
        "X-Group": "2059",
        "X-FCountry": "71",
        "Content-Type": "application/json; charset=UTF-8",
        "Host": "andind2022.com"
    }

    # Step 1: Submit Registration (This includes Phone and solved Captcha)
    # Note: X-Sign and ImageText are captured from HAR and may be expired/session-bound
    url_reg = "https://andind2022.com/Account/v1.1/Mb/Register/Registration"
    reg_headers = headers.copy()
    reg_headers["X-Sign"] = "N7lEADA0FFP5L1M1WAgFbEt8d3f6D9o5/+5szLbrLcBTEZH1dIBeUuvoMWz0FBc+x+tbv4h1PtayY2WQb6krlyO5HHSQKRhvKjUbq2G+mnlORhr1YlIyV7x1kWtc1y4yo0761gbXknu5PZjCn3o9BF3TbiQpalkkwhGmBz9vVu7mkkQoVNLAyL46R+6IhQIVMJ53af0ga6TqCw1lQoOEA05KDiIjqx9VtaYUmu80mJL6AqXy+WAW7whbeyU9R9G4oZtLjmu2tKWOKbtuFjuUJB+z0gsxm2lhn2a5y/EZyKDnQaR9Q86AS8JAs3YJY8m9exLM7LCUpypcLEpfX2lq9JUoJpX6_LVQXC1gQ4bV3okoRsiw/MnqG8acbHaOoJz4iwSxbVtCTTKl5u0oRV+C8Cj2arcG2Q7LNkKuIABTUIMCKOHLplwz1Mp36xxuCjt893VuSyKcFT9udU78NdIiCpNds+lBqaOSv+8NDL7sP4gHqkaeZ8igNVf3ojEtBhwDEZN9KkNAOiur6WwiMID"
    
    reg_payload = {
        "CaptchaId": "60b9e81b-b4b3-4879-b9dd-35cf31c2608c",
        "ImageText": "Hg9M1VXO5tCf9pViUbvXcKrQc0EZO4Kn4XBdteaS342V--JUOKSkSh8RzfOTXC2lcYZ8fn3fv9cY1PDvrLnWbNJJ25V5aBHNKjNLxMHUWIVMuJfr02FQFjJXtIionW8opTjuOGgsdVUWndgSALG8bckJTkk0iP4cfH5J-w8v6X0nTKPeUEWtynm7tBOLI1Q83GqLYan33IjPIlIiD1oVxS2enpn7pZwmzzKIQmZY0_GYEQnWZPNULZu5YA4XamXbd5Szbd7bRGK0s_WtlzNiAFOscq2zRd4DAJRyudS-tokTj9Q-1qzedMkq5zV0g_HUUKO_MDbbt060zfrT5v0Eqe8-IZGxAScqGokeoCN6V5p0u5vP_iLGLMlDQgUzCO2xKq8f6T1BERWbxANmo2I8pqb6-66gtT6Cy_jd9wXX_Fqn6qfChFlzxSC7VFvQWiK3uu3GZ5gxnfdhl6XlvcBTBF0mlHktb8h8nfzMx3gjPrLdeQ7GJDPZZO8bVFGHHYd-jCCR2pBrs_7jDHwKfrAYOuMUsWtW13jBzjX955JmnFQiy2LQvKlPAXVc6AmDGdG5l8IfmUJ3NRr3lbu7c4FI-vPUuHdZYGsz197g9XlBvnRoHbAFE7XugU_1tTQQk3Zu_naCp7_Qy53vsUq77jJ-9QbQzmVd1yWR7EBHM2hCXva1MHD-8UemBYXH",
        "Data": {
            "RegType": 2,
            "CountryId": 79,
            "CurrencyId": 12,
            "Phone": phone,
            "RulesConfirmation": 1,
            "SharePersonalDataConfirmation": 1,
            "TimeZone": "5.3"
        }
    }
    
    print(f"[*] Submitting Registration for {phone}...")
    res_reg = session.post(url_reg, headers=reg_headers, json=reg_payload)
    print(f"Status: {res_reg.status_code}")
    print(f"Response: {res_reg.text}")
    
    if not res_reg.json().get("Success"):
        print("[-] Registration failed (likely due to expired Captcha/X-Sign).")
        return

    auth_val = res_reg.json().get("Value", {}).get("Auth", {})
    guid = auth_val.get("Guid")
    token = auth_val.get("Token")
    
    print(f"[+] Registration Success! GUID: {guid}, Token: {token[:10]}...")

    # Step 2: Send Code
    url_send = "https://andind2022.com/Account/v1/SendCode"
    send_payload = {
        "Data": {},
        "Auth": {
            "Guid": guid,
            "Token": token
        }
    }
    
    print(f"[*] Requesting OTP...")
    res_send = session.post(url_send, headers=headers, json=send_payload)
    print(f"Status: {res_send.status_code}")
    print(f"Response: {res_send.text}")
    
    if not res_send.json().get("Success"):
        print("[-] Failed to send OTP.")
        return
        
    new_token = res_send.json().get("Value", {}).get("Auth", {}).get("Token")
    print(f"[+] OTP Sent! New Token: {new_token[:10]}...")

    # Step 3: Check Code
    url_check = "https://andind2022.com/Account/v1/CheckCode"
    otp_code = "123456" # Placeholder
    check_payload = {
        "Data": {"Code": otp_code},
        "Auth": {
            "Guid": guid,
            "Token": new_token
        }
    }
    
    print(f"[*] Verifying OTP: {otp_code}...")
    res_check = session.post(url_check, headers=headers, json=check_payload)
    print(f"Status: {res_check.status_code}")
    print(f"Response: {res_check.text}")

if __name__ == "__main__":
    test_fairpari_auth()
