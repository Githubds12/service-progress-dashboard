
# JvSpinBet - Research Report

## Metadata
- **Target URL/App**: `https://andind2022.com/` / `JvSpinBet`
- **Researcher**: `Gorri`
- **Date**: `2026-05-06`
- **Status**: `In Progress`
- **HAR Files**: `JVSPINBet.har`

## 1. Executive Summary
JvSpinBet (package: `org.jvspinbet.client`) is a betting platform utilizing a multi-stage registration and verification flow. The system requires solving a captcha during the initial registration phase, which then initiates an SMS-based verification process. All primary authentication traffic is routed through the domain `andind2022.com`. The application uses session-bound `Guid` and `Token` identifiers to track the verification state across requests.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | `Sms` code type is enforced after registration submission. |
| **Captcha** | Visual | Required in the `/Registration` endpoint (`CaptchaId` and `ImageText`). |
| **Encryption** | HTTPS | Standard TLS encryption for API traffic; JSON payloads are used. |
| **Rate Limits** | 300s | `RAS: 300` observed in `/SendCode` response suggests a 5-minute cooldown. |
| **Endpoints Involved** | 4 | `GetRegistrationFields`, `Registration`, `SendCode`, `CheckCode` |

## 3. Flow Details

### Flow 1: Registration & SMS Verification

**Step 1: Get Registration Fields**
- **Endpoint**: `GET /Account/v1/Mb/Register/GetRegistrationFields?Partner=238&Group=1287&Language=en_GB&Whence=22&fcountry=71`
- **Purpose**: Retrieves the required input fields for different registration types (Phone, Email, Full, One-click).
- **Response Analysis**: Returns a schema for `RegType: 2` (Phone registration) including `Phone`, `CurrencyId`, `Birthday`, etc.

**Step 2: Submit Registration (Captcha Required)**
- **Endpoint**: `POST /Account/v1.1/Mb/Register/Registration`
- **Purpose**: Submits user data and solves the initial captcha challenge.
- **Request Payload**:
    ```json
    {
        "CaptchaId": "65f82c04-615e-42d6-8820-f071bd3c97a0",
        "ImageText": "...",
        "Data": {
            "RegType": 2,
            "CountryId": 71,
            "CurrencyId": 99,
            "Phone": "7990158524",
            "Birthday": "1998-05-05",
            "RulesConfirmation": 1,
            "SharePersonalDataConfirmation": 1
        }
    }
    ```
- **Response**:
    ```json
    {
        "Success": true,
        "Value": {
            "Auth": {
                "CodeType": "Sms",
                "Guid": "053693f2-767d-4bab-8f31-bf77d3970d6e",
                "Token": "B9EA94C56BD74F89A5ED55D31F500E44",
                "Hash": "053693f2-767d-4bab-8f31-bf77d3970d6e|B9EA94C56BD74F89A5ED55D31F500E44"
            },
            "CodeTypes": ["Sms"]
        }
    }
    ```

**Step 3: Trigger SMS Code**
- **Endpoint**: `POST /Account/v1/SendCode`
- **Purpose**: Requests the server to send the SMS verification code to the registered phone number.
- **Request Payload**:
    ```json
    {
        "Data": {},
        "Auth": {
            "Guid": "053693f2-767d-4bab-8f31-bf77d3970d6e",
            "Token": "B9EA94C56BD74F89A5ED55D31F500E44"
        }
    }
    ```
- **Response**:
    ```json
    {
        "Success": true,
        "Value": {
            "RAS": 300,
            "Auth": {
                "Guid": "053693f2-767d-4bab-8f31-bf77d3970d6e",
                "Token": "8E1D8E9F6FBB43519C178865AEE2760A",
                "Hash": "..."
            }
        }
    }
    ```
- **Note**: The `Token` is updated in each successful step, maintaining session state.

**Step 4: Verify SMS Code**
- **Endpoint**: `POST /Account/v1/CheckCode`
- **Purpose**: Validates the 6-digit code received via SMS.
- **Request Payload**:
    ```json
    {
        "Data": { "Code": "252525" },
        "Auth": {
            "Guid": "053693f2-767d-4bab-8f31-bf77d3970d6e",
            "Token": "8E1D8E9F6FBB43519C178865AEE2760A"
        }
    }
    ```
- **Response (Invalid Code)**:
    ```json
    {
        "Success": false,
        "Error": "Verification code is incorrect.",
        "ErrorCode": 100371
    }
    ```

## 4. Security & Reversing Notes

### Authentication Mechanisms
1.  **Session Tracking**: The `Auth` object (containing `Guid` and `Token`) is central to the flow. Each request must provide the `Token` returned by the previous step.
2.  **Captcha**: The registration endpoint requires a `CaptchaId` and `ImageText`. This suggests a visual captcha is presented to the user before the SMS flow begins.
3.  **App Identification**: Headers include `X-BundleId: org.jvspinbet.client` and `Version: jvspinbet-v253.0.1`, which are used by the server to identify the client application.
4.  **Logging**: Exception logs are sent to `https://andind2022.com/log/Android`, which provides insight into server-side error messages (e.g., "Verification code is incorrect").

## 5. Conclusion
### Automation Feasibility: 40%
The primary blocker for automation is the **Initial Captcha** required during registration. Once the captcha is solved (or bypassed via OCR/manual input), the subsequent SMS triggering and verification steps are straightforward JSON requests with session tokens. The 300-second rate limit (`RAS`) also necessitates careful timing in automated tests.

