# Raya Automation Report

## 1. Automation Logic
The automation script `api.py` for Raya is built using FastAPI to simulate the authentication flow identified in the HAR analysis. 

### Flow Documentation:
1.  **Signup Initialization (`/signup`)**:
    -   Maps to the real endpoint: `https://prod.api.rayaculture.com/auth/signup`.
    -   **Requirement**: A valid `captchaToken` (Cloudflare Turnstile Managed) and a `verify_token`.
    -   The script takes the user's phone and password, then submits the payload with a Turnstile token.
    -   In a real-world scenario, a third-party Turnstile solver would be needed to generate the `captchaToken`.

2.  **OTP Verification (`/verify`)**:
    -   Maps to the real endpoint: `https://prod.api.rayaculture.com/auth/verify-otp`.
    -   Submits the phone number and the OTP code received by the user.

## 2. Testing Proofs

### Signup Request Simulation:
-   **Method**: `POST`
-   **Endpoint**: `/signup`
-   **Payload**:
    ```json
    {
        "phone": "+393471234567",
        "password": "P@ssw0rd123!",
        "captchaToken": "p8BQ3HCvQZicTJYfTEfLBqPvNH1mPm",
        "verify_token": "3f010954a42bca0d20b5d699cece14e3a9e3c01e66e1b61b493d6482d0e697ca",
        "ts": 1777182948
    }
    ```
-   **Response**:
    ```json
    {
        "status": "initiated",
        "message": "Signup initiated for +393471234567. Requires valid Turnstile token.",
        "payload_sent": { ... }
    }
    ```

### OTP Verification Simulation:
-   **Method**: `POST`
-   **Endpoint**: `/verify`
-   **Payload**:
    ```json
    {
        "phone": "+393471234567",
        "token": "123456"
    }
    ```
-   **Response**:
    ```json
    {
        "status": "success",
        "message": "OTP 123456 verification submitted for +393471234567."
    }
    ```

## 3. Conclusion
The automation script successfully simulates the identified flow. The primary challenge for full automation is the real-time solving of Cloudflare Turnstile CAPTCHA. The endpoints and payload structures are well-defined and verifiable based on the HAR trace.
