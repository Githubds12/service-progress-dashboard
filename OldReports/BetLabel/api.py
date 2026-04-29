from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="BetLabel Automation API")

class RegistrationRequest(BaseModel):
    phone: str
    captcha_text: str
    captcha_id: str = "d0821b02-60dc-4555-8279-20e3c1c77edd"

class SendCodeRequest(BaseModel):
    guid: str
    token: str

class CheckCodeRequest(BaseModel):
    guid: str
    token: str
    code: str

@app.post("/register")
async def register(req: RegistrationRequest):
    """
    Simulates the registration phase.
    Endpoint: https://andind2022.com/Account/v1.1/Mb/Register/Registration
    """
    return {
        "Success": True,
        "Value": {
            "Auth": {
                "Guid": "752c5099-3f38-42ae-a409-24280f0125a1",
                "Token": "E49DBA053FDD465C8510AC25D425EE0E"
            }
        }
    }

@app.post("/send-code")
async def send_code(req: SendCodeRequest):
    """
    Simulates sending the OTP code.
    Endpoint: https://andind2022.com/Account/v1/SendCode
    """
    return {
        "Success": True,
        "Value": {
            "RAS": 300,
            "Auth": {
                "Guid": req.guid,
                "Token": "771C57FBCE624BE2A9B89283AC2DEA60"
            }
        }
    }

@app.post("/verify-code")
async def verify_code(req: CheckCodeRequest):
    """
    Simulates verifying the OTP code.
    Endpoint: https://andind2022.com/Account/v1/CheckCode
    """
    return {
        "Success": True,
        "Message": f"Code {req.code} verified successfully."
    }

if __name__ == "__main__":
    from fastapi.testclient import TestClient
    client = TestClient(app)
    try:
        print("Testing /register endpoint...")
        resp1 = client.post("/register", json={"phone": "8791267460", "captcha_text": "12345"})
        print("Response:", resp1.json())
        
        guid = resp1.json()["Value"]["Auth"]["Guid"]
        token = resp1.json()["Value"]["Auth"]["Token"]

        print("\nTesting /send-code endpoint...")
        resp2 = client.post("/send-code", json={"guid": guid, "token": token})
        print("Response:", resp2.json())
        
        token = resp2.json()["Value"]["Auth"]["Token"]

        print("\nTesting /verify-code endpoint...")
        resp3 = client.post("/verify-code", json={"guid": guid, "token": token, "code": "92617"})
        print("Response:", resp3.json())
        print("\nAutomation script test completed successfully.")
    except Exception as e:
        print("\nAutomation script test failed:", str(e))
