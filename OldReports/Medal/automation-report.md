# Medal Automation Report

## 1. Automation Logic
The automation script `api.py` for Medal targets the user settings endpoint which handles both phone linking and verification.

### Flow Documentation:
1.  **Request OTP (`/send`)**:
    -   Endpoint: `POST https://api-v2.medal.tv/users/{userId}/settings`
    -   Requires: A valid session token (`Bearer`) and the user's `userId`.
    -   Payload: `{"contactDiscoverable": false, "phone": "+91XXXXXXXXXX"}`
    -   This triggers the SMS delivery to the specified phone number.

2.  **Verify OTP (`/verify`)**:
    -   Endpoint: `POST https://api-v2.medal.tv/users/{userId}/settings`
    -   Requires: The same session token and `userId`.
    -   Payload: `{"contactDiscoverable": false, "phoneVerificationCode": "XXXXXX"}`
    -   This completes the phone verification process.

## 2. Testing Proofs

### /send Endpoint Test:
-   **Request**: `POST /send`
-   **Response**:
    ```json
    {
        "status": "success",
        "message": "OTP request sent to +918791267460 for user 616228614.",
        "payload_sent": {
            "contactDiscoverable": false,
            "phone": "+918791267460"
        }
    }
    ```

### /verify Endpoint Test:
-   **Request**: `POST /verify`
-   **Response**:
    ```json
    {
        "status": "success",
        "message": "OTP 700654 verified for user 616228614.",
        "payload_sent": {
            "contactDiscoverable": false,
            "phoneVerificationCode": "700654"
        }
    }
    ```

## 3. Conclusion
The Medal automation flow is straightforward once a valid user session is established. The lack of CAPTCHA and additional request signing makes it a highly reliable target for automation. The `userId` must be known beforehand, which can be retrieved from the `/users/auth` callback or profile data.
