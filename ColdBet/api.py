import requests
import json

url = "https://andind2022.com/Account/v1/SendCode"

headers = {
    "User-Agent": "org.coldbet.client-user-agent/coldbet-v253.0.2",
    "Content-Type": "application/json; charset=UTF-8",
    "AppGuid": "737844568a148476_2",
    "X-Message-Id": "kwlgDGPE33C"
}

def trigger_sms(guid, token):
    payload = {
        "Data": {},
        "Auth": {
            "Guid": guid,
            "Token": token
        }
    }
    
    print(f"[*] Attempting to trigger SMS for Guid: {guid}...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print("Status Code:", response.status_code)
        print("Response:", response.text)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    # These are session-specific and would need to be fetched from /Registration first
    trigger_sms("a110b6eb-ac3e-4802-986b-f7305337fff8", "251F1C17F6424133B65A9239D97A652B")
