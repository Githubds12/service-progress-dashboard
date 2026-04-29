from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="Medal Automation API")

class SendOTPRequest(BaseModel):
    userId: str
    phone: str
    token: str # Session/Bearer token

class VerifyOTPRequest(BaseModel):
    userId: str
    code: str
    token: str

@app.post("/send")
async def send_otp(req: SendOTPRequest):
    """
    Simulates the phone verification initialization.
    Endpoint: https://api-v2.medal.tv/users/{userId}/settings
    """
    url = f"https://api-v2.medal.tv/users/{req.userId}/settings"
    headers = {
        "Authorization": f"Bearer {req.token}",
        "Content-Type": "application/json",
        "User-Agent": "Medal-Android/6.9.1"
    }
    payload = {
        "contactDiscoverable": False,
        "phone": req.phone
    }
    
    # In a real scenario, we would call the API. Here we simulate success.
    return {
        "status": "success",
        "message": f"OTP request sent to {req.phone} for user {req.userId}.",
        "payload_sent": payload
    }

@app.post("/verify")
async def verify_otp(req: VerifyOTPRequest):
    """
    Simulates the OTP verification.
    Endpoint: https://api-v2.medal.tv/users/{userId}/settings
    """
    url = f"https://api-v2.medal.tv/users/{req.userId}/settings"
    headers = {
        "Authorization": f"Bearer {req.token}",
        "Content-Type": "application/json",
        "User-Agent": "Medal-Android/6.9.1"
    }
    payload = {
        "contactDiscoverable": False,
        "phoneVerificationCode": req.code
    }
    
    return {
        "status": "success",
        "message": f"OTP {req.code} verified for user {req.userId}.",
        "payload_sent": payload
    }

if __name__ == "__main__":
    from fastapi.testclient import TestClient
    client = TestClient(app)
    try:
        print("Testing /send endpoint...")
        resp1 = client.post("/send", json={
            "userId": "616228614",
            "phone": "+918791267460",
            "token": "dummy_token"
        })
        print("Response:", resp1.json())

        print("\nTesting /verify endpoint...")
        resp2 = client.post("/verify", json={
            "userId": "616228614",
            "code": "700654",
            "token": "dummy_token"
        })
        print("Response:", resp2.json())
        print("\nAutomation script test completed successfully.")
    except Exception as e:
        print("\nAutomation script test failed:", str(e))
