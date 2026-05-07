import requests
import json
import base64
import urllib.parse

def test_lyft_auth():
    session = requests.Session()
    phone = "+393518831002"
    
    # Common Headers
    headers = {
        "User-Agent": "lyft:android:15:2026.16.3.1777447561",
        "Accept-Language": "en_IN",
        "X-Session": "eyJhIjoiMTQ2OGYwYmY1ZGIxOGI3YyIsImgiOnRydWUsImsiOiI1YTdjZWM4OC01YTBhLTQ2ZmItYWI4My04ZmU0NDM3Y2ZkNDgifV0=",
        "X-Client-Session-Id": "1bced0dd-a3b2-425a-9570-133232d0c94d"
    }
    
    # Step 1: Get Initial Access Token
    url_token = "https://api.lyft.com/oauth2/access_token"
    token_headers = headers.copy()
    token_headers["Authorization"] = "Basic ZVNhdDctaXU5ZG9NOlp0dkxEejBuMS1rSlZ3a0l2eEM0aVNKMHlNdkp5ZFBx"
    token_headers["Content-Type"] = "application/x-www-form-urlencoded"
    
    print(f"[*] Requesting Client Access Token...")
    res_token = session.post(url_token, headers=token_headers, data="grant_type=client_credentials")
    print(f"Status: {res_token.status_code}")
    
    if res_token.status_code != 200:
        print("[-] Failed to get client token.")
        return
        
    access_token = res_token.json().get("access_token")
    print(f"[+] Token: {access_token[:20]}...")
    
    # Step 2: Request Phone Auth (SMS)
    url_phone = "https://api.lyft.com/v1/phoneauth"
    phone_headers = headers.copy()
    phone_headers["Authorization"] = f"Bearer {access_token}"
    phone_headers["Content-Type"] = "application/json;messageType=pb.api.endpoints.v1.phone_auth.CreatePhoneAuthRequest"
    phone_headers["X-Session"] = "eyJhIjoiMTQ2OGYwYmY1ZGIxOGI3YyIsImYiOiJmNTFlZTMzNi1lNDg5LTQ4ODItOGMyMS05NWZmMDZlZDRhOWEiLCJoIjp0cnVlLCJrIjoiNWE3Y2VjODgtNWEwYS00NmZiLWFiODMtOGZlNDQzN2NmZDQ4In0="
    
    payload = {
        "phone_number": phone,
        "voice_verification": False,
        "message_format": "sms_android_retriever",
        "client_configuration": "release"
    }
    
    print(f"[*] Requesting OTP for {phone}...")
    res_phone = session.post(url_phone, headers=phone_headers, json=payload)
    print(f"Status: {res_phone.status_code}")
    print(f"Response: {res_phone.text}")
    
    if res_phone.status_code in [200, 202]:
        print("[+] OTP Request Successful!")
        
        # Step 3: Verify OTP (Simulated with the captured failure code for completeness)
        otp_code = "258899"
        print(f"[*] Verifying OTP: {otp_code}...")
        
        verify_headers = headers.copy()
        verify_headers["Authorization"] = "Basic ZVNhdDctaXU5ZG9NOlp0dkxEejBuMS1rSlZ3a0l2eEM0aVNKMHlNdkp5ZFBx"
        verify_headers["Content-Type"] = "application/x-www-form-urlencoded"
        
        verify_payload = {
            "grant_type": "urn:lyft:oauth2:grant_type:phone",
            "phone_number": phone,
            "phone_code": otp_code,
            "identifiers": "W3sidHlwZSI6ImFuZHJvaWRfYmFja3VwX3Rva2VuIiwic291cmNlIjoibHlmdF9hbmRyb2lkX2FwcCIsIm5hbWUiOiI1YTdjZWM4OC01YTBhLTQ2ZmItYWI4My04ZmU0NDM3Y2ZkNDgifV0="
        }
        
        encoded_payload = urllib.parse.urlencode(verify_payload)
        res_verify = session.post(url_token, headers=verify_headers, data=encoded_payload)
        print(f"Status: {res_verify.status_code}")
        print(f"Response: {res_verify.text}")
        
    else:
        print("[-] OTP Request Failed.")

if __name__ == "__main__":
    test_lyft_auth()
