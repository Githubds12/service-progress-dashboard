import requests
import json

def test_galarm_auth():
    session = requests.Session()
    phone = "3720511560"
    
    # Common Headers
    headers = {
        "User-Agent": "okhttp/4.10.0",
        "Content-Type": "application/json; charset=utf-8",
        "Host": "us-central1-migrateto3.cloudfunctions.net",
        "Connection": "Keep-Alive"
    }

    # Step 1: Send Verification Code
    # Note: reCAPTCHA token and cipher are captured from HAR and will likely be expired
    url_send = "https://us-central1-migrateto3.cloudfunctions.net/sendVerificationCodeHttps"
    send_payload = {
        "data": {
            "cipher": "U2FsdGVkX19U72Zk01JcEWYqI/I4QiUfvxe1yWPoRGaOEDgDhzlzvmujKfhGBfvrd6UJvM6OLVyc4GAtWsDpsquRTN+//O2/pwgCUGS/4y5gSrNgZ5Da6ZlEa9EWNuR46t94U2Jxfx7U+qk3oqbWD/OBoSOwEjWFJTnHVnbkXwFI=",
            "apiVersion": "v2",
            "os": "android",
            "fromUid": None,
            "mobileNumber": phone,
            "countryCode": "39",
            "ip": "49.43.161.81",
            "token": "0cAFcWeA7CXfMqB_Vxdw-SIbKz4SdDDGvXfEfpn65p6QcOFXGjirFe3kfbqpVsGBOgZJMkqeRUJGbuNEJ-imvFlNIdnAgIcpXayfjAOpgLwv7waL3-H50W_sE5-YmWmLR4GkBxvezg5K0TAurs7s37lNummpTsY1pnQXZjtPJBglZhYt3VH9Q7J_dFRyJKIJMt4lM8wPJL1TGDl8OKz6PzTk_9RIMqarUDb1-4trk_dtThQ3y30S0NPZD4XzVGlr6VWTkV1ZmnVwYdxzV-y7qKFv6VTX8pGt2UkRAr7891cFdr5wrS4WlUqcjYw_fqsz2w6RdSUuCt-wXcYXT7qoYPOG-WlWBT6kROURdk38-tgdOjlsttPd1geVrOFaSvrBKY-dtzSKSvmxdmJnpgHT92B1OiNIMZFTbCw14XjG14ASStnHjsfZxpvt9HA1vSqE2S6MZ_0DCKPYn9yfxtYzY7xmvT7nIrabG0kZJKcpMB7rolaZvxK2YymOvbQLF4YgNhgCWPKnDFKc6JHfkAp3fnXGblKagdG9VB03c0PeWNNwaHikQ7xFALnF7WxW7PoorF2a2pSP6yMNuG2Fjd3LwITIHEvjpkOYZ1WjfqhhwCFhMiENFcv0Ta5War736SkDnm_na6Qtrga0LSfP1w1SgpI11w0HKGKV7QGbd01MAignlWXq-1W9sY8LQSmkn-OuIhJbCJqHk81s4I7ItvTclzq_15XICO0CsIJEfodRM2NOnNfghybOGiaAJaFJwYQSNEoplj81KtEE5XMv1TGlgw19WNTyTRpjQvqPnMq1QtF6PQqL6X3KnhejmV-IMiG8DY72MihcJNvxdirLL6xN6cAuIaXJJhdG7DXsztTABzJKysDemCkDSEoGgDvarOv8q6ilcC3H4VpO39TGGuqELTmkmRjrZHi82fueCHV7ciigwjSXcPxiTydnWV6XdkF2WJ3SMZ21ofno16wlSuphzzXHlvcYJ3gnbRjLvAHuzACYrfTjOrj1c13c7Zvk66iEsUygzrdynGH6hTwy3bA92R8fa7KR0xSVx9Pl1Jpcv_eChtK2ogn_Jsh9TjpP0aFeVMP7yZ6bMCdaRbXiLAVGIEe54jWGHa0QkyQpx5BoxKeJH2ut6sQezxs5t5gFgly_mQWySlZkfByjSUn4LxRx1dDbsSzfg3Nk8BhpIqoLBguKbdQL--CtHq4s8ooNHg5bYYCMvkD3OtO9LvgAEuvsJLVKOb_jcFe3rfizUhaD-x4aeiwLC3dLTVnyIR7rgWmUaCj3De4dtbv03vVueajFTuJzAGWcVuAc9uXAU7xdTQ9MZJF6SpnKq4Pw-Mu7dfVYI0ZXDbgVkoL1-t87O1wlU29V5PDP_9MaBucttiZOCQL_Q26hH8-4bcgE4zUBFI_LLjhUiAzwSnDKPAbSVe1bRGZxlk6hdHj27vGAMnMHY-8_Wt8T1cGMuDVtlfYPRSJWqQeQb8EJQLb2Xo9fgG3_GnDxMFKmhLmH2tPuqVdeEL4lR3RmD92-hPhZe25TTluY6LYqiYtzpr226l7QaNZG4dYCZTtKV4RzYF_5dAXJqlRejkVfG4Tp4qCrYYutd3N24cIpOgQ-xhw9d9IVUrfbtkrcO7-wSzRieqL3Jjub7vooB0A03SD68lCOrAfZv9CQ2b6aPtgywjY4Aa2kLucYZxn5VQLY4rEIxyybq8WKKAiklJAItoyNpFWkfkLD5cgGhBPukX2157zyM5YRGVZkmLmz4mnwPNN_g3WM-LVX0hoYFB9X_dKoWrerlckvqLFuWJQWFHW22dk2DBCo2UVNgkyEZGnBurNANS0LtwGgWxF7-lERmC2nCDvJtTBPdOMSlo-zIG1S6nl5hyD81x_626jy1Q1lRFa80sfvPuxy5b5NMqnYicusFVA9sFUrryiaYMoAbVVDApuAdhaPn2APhW0KZqwfgv4PL5Foqv8srPalbJ5GOJ8fITcdfvMs1vM6-ArkxhlrLpE9wQx38v5j0a7EyZDhGLDVMW0yduxaCF9_0ZuQvTdRWE4bTvIB7lKS1bA0n0VKTgOUVMF61Yb5Oq8bGBMD9tYa-tliNlcO7A4AtSkZKRUUzKwK_Cs1RHbfs8QJPgmua2aaaFZYLpQuQAwKcUYqw8X4oX82_ZrrIhFITlCPwCC9AkT3Q3QYgxqlUk1aiLMd_SjCr1HkcZNGa4Vc2Sgs2eMgnYsjv50LesuelAU4RKjfvrKrRx901q8EZ-RqJYvf441KU5qzeCnKnQKAqMi6MG861X18A"
        }
    }
    
    print(f"[*] Requesting OTP for {phone}...")
    res_send = session.post(url_send, headers=headers, json=send_payload)
    print(f"Status: {res_send.status_code}")
    print(f"Response: {res_send.text}")
    
    if "success" not in res_send.text:
        print("[-] OTP Request failed (likely expired token/cipher).")
        return

    result = res_send.json().get("result", {}).get("result", {})
    request_id = result.get("requestId")
    print(f"[+] OTP Requested! Request ID: {request_id}")

    # Step 2: Verify Code
    url_verify = "https://us-central1-migrateto3.cloudfunctions.net/verifyCodeHttps"
    verify_payload = {
        "data": {
            "cipher": "U2FsdGVkX18fDHn6zaBEcWR+l3iWcV6wbs/KG2W5VkikyohPRR0wR/HIiJ+jMQIfppmNTSJWOA26rVRyTSd5wysA1aAtT0Vu2iR6NDiTU/UFeXv7g/FPAfBnb0wbR0Abelqhb6r0WgoRYisnWUurZa/yGSHqefOHe7dZkNJQVgU=",
            "code": "1234",
            "os": "android",
            "mobileNumber": phone,
            "ip": "49.43.161.81",
            "phoneId": "819dbd62-4722-4863-b0ca-a0e0dbe445e2",
            "source": "checkmobi",
            "apiVersion": "v2",
            "fromUid": None,
            "requestId": request_id,
            "countryCode": "39",
            "cca2": "IT"
        }
    }
    
    print(f"[*] Verifying OTP: 1234...")
    res_verify = session.post(url_verify, headers=headers, json=verify_payload)
    print(f"Status: {res_verify.status_code}")
    print(f"Response: {res_verify.text}")

if __name__ == "__main__":
    test_galarm_auth()
