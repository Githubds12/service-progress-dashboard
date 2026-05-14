from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="YandexEats Automation API")

class InitRequest(BaseModel):
    phone: str
    track_id: str = "9de95e64e378e4adacb4229a162d1d0bb4"

class VerifyRequest(BaseModel):
    track_id: str
    code: str

@app.post("/auth/init")
async def auth_init(req: InitRequest):
    """
    Simulates the Yandex Passport authentication initialization.
    Endpoint: https://mobileproxy.passport.yandex.net/1/bundle/auth/password/submit/
    """
    return {
        "status": "success",
        "message": f"Auth initialized for {req.phone}.",
        "track_id": req.track_id,
        "next_step": "code"
    }

@app.post("/auth/verify")
async def auth_verify(req: VerifyRequest):
    """
    Simulates the Yandex Passport OTP verification.
    Endpoint: https://passport.yandex.ru/pwl-yandex/api/passport/track/check-phone-confirmation
    """
    return {
        "status": "ok",
        "message": f"OTP {req.code} verified successfully for track {req.track_id}.",
        "is_complete": True
    }

if __name__ == "__main__":
    from fastapi.testclient import TestClient
    client = TestClient(app)
    try:
        print("Testing /auth/init endpoint...")
        resp1 = client.post("/auth/init", json={"phone": "+79991234567"})
        print("Response:", resp1.json())

        print("\nTesting /auth/verify endpoint...")
        resp2 = client.post("/auth/verify", json={"track_id": "9de95e64e378e4adacb4229a162d1d0bb4", "code": "356532"})
        print("Response:", resp2.json())
        print("\nAutomation script test completed successfully.")
    except Exception as e:
        print("\nAutomation script test failed:", str(e))
