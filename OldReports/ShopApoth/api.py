import requests
import uuid

# Configuration
BASE_URL = "https://api.sa-tech.de"
CLIENT_ID = "android-app" # Placeholder based on typical patterns

class ShopApothekeAPI:
    def __init__(self, bearer_token=None):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "okhttp/4.11.0",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-request-id": str(uuid.uuid4())
        }
        if bearer_token:
            self.headers["Authorization"] = f"Bearer {bearer_token}"
        self.session.headers.update(self.headers)

    def register(self, email, password, first_name, last_name, dob):
        """
        Flow 1: Registration
        """
        url = f"{BASE_URL}/auth/v2/com/register"
        payload = {
            "dateOfBirth": dob,
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "newsletterAccepted": False,
            "password": password,
            "preferredLanguage": "de",
            "registrationOrigin": "app",
            "salutation": "mr",
            "tosAccepted": True
        }
        response = self.session.post(url, json=payload)
        return response

    def check_erx_status(self, customer_id):
        """
        Flow 2: Check E-Prescription Status
        """
        url = f"{BASE_URL}/session/v1/com/erx-session-status/{customer_id}"
        response = self.session.get(url)
        return response

    def record_nfc_position(self, x, y, z):
        """
        Flow 2: Record NFC Card Position for Prescription
        """
        url = f"{BASE_URL}/nfc-health-card-position/api/v1/nfc-position"
        payload = {"x": x, "y": y, "z": z}
        response = self.session.post(url, json=payload)
        return response

    def request_phone_otp(self, customer_id, phone_number):
        """
        Flow 3: Request Phone Verification OTP
        """
        url = f"{BASE_URL}/customer/v1/com/mfa/{customer_id}/phone-verification/request"
        payload = {"phoneNumber": phone_number}
        response = self.session.post(url, json=payload)
        return response

    def verify_phone_otp(self, customer_id, code):
        """
        Flow 3: Confirm Phone Verification OTP
        """
        url = f"{BASE_URL}/customer/v1/com/mfa/{customer_id}/phone-verification/confirmation"
        payload = {"code": code}
        response = self.session.post(url, json=payload)
        return response

if __name__ == "__main__":
    # Example usage (needs valid token/ID)
    api = ShopApothekeAPI()
    print("API Client Initialized")
