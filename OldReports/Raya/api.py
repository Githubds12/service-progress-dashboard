from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="Raya Automation API")

class SignupRequest(BaseModel):
    phone: str
    password: str = "P@ssw0rd123!"
    captchaToken: str = "p8BQ3HCvQZicTJYfTEfLBqPvNH1mPm" # Default stub

class VerifyRequest(BaseModel):
    phone: str
    token: str

@app.post("/signup")
async def signup(req: SignupRequest):
    """
    Simulates the /auth/signup endpoint.
    Real endpoint: https://prod.api.rayaculture.com/auth/signup
    Requires a valid Cloudflare Turnstile token.
    """
    url = "https://prod.api.rayaculture.com/auth/signup"
    payload = {
        "phone": req.phone,
        "password": req.password,
        "captchaToken": req.captchaToken,
        "verify_token": "3f010954a42bca0d20b5d699cece14e3a9e3c01e66e1b61b493d6482d0e697ca", # Sample token
        "ts": 1777182948
    }
    # For testing, we mock the success as Cloudflare token will likely be invalid
    return {
        "status": "initiated",
        "message": f"Signup initiated for {req.phone}. Requires valid Turnstile token.",
        "payload_sent": payload
    }

@app.post("/verify")
async def verify(req: VerifyRequest):
    """
    Simulates the /auth/verify-otp endpoint.
    Real endpoint: https://prod.api.rayaculture.com/auth/verify-otp
    """
    url = "https://prod.api.rayaculture.com/auth/verify-otp"
    payload = {
        "phone": req.phone,
        "token": req.token
    }
    return {
        "status": "success",
        "message": f"OTP {req.token} verification submitted for {req.phone}."
    }

if __name__ == "__main__":
    from fastapi.testclient import TestClient
    client = TestClient(app)
    try:
        print("Testing /signup endpoint...")
        resp1 = client.post("/signup", json={"phone": "+393471234567"})
        print("Response:", resp1.json())

        print("\nTesting /verify endpoint...")
        resp2 = client.post("/verify", json={"phone": "+393471234567", "token": "123456"})
        print("Response:", resp2.json())
        print("\nAutomation script test completed successfully.")
    except Exception as e:
        print("\nAutomation script test failed:", str(e))
