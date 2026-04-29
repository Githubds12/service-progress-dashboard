import requests

def verify_phone(auth_id, phone_number):
    url = "https://energyid.bp.com/am/json/realms/root/realms/bravo/authenticate?authIndexType=service&authIndexValue=Registration&realm=%2Fbravo&locale=en"
    headers = {
        "Content-Type": "application/json",
        "X-Requested-With": "com.bp.app.bpme.global.pl"
    }
    payload = {
        "authId": auth_id,
        "callbacks": [
            {
                "type": "StringAttributeInputCallback",
                "input": [
                    {
                        "name": "IDToken3",
                        "value": phone_number
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def verify_otp(auth_id, otp_code):
    url = "https://energyid.bp.com/am/json/realms/root/realms/bravo/authenticate?authIndexType=service&authIndexValue=Registration&realm=%2Fbravo&locale=en"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "authId": auth_id,
        "callbacks": [
            {
                "type": "StringAttributeInputCallback",
                "input": [
                    {
                        "name": "IDToken4",
                        "value": otp_code
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
