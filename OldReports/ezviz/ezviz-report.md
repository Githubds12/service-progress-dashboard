# EZVIZ - Research Report

## Metadata
- **Target URL/App**: `com.ezviz`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29 23:42`
- **Status**: `Completed`
- **HAR Files**: `ezviz.har`

## 1. Executive Summary
EZVIZ (com.ezviz) implements a robust authentication flow with regionalized API endpoints and a custom bot protection system called **Human-Computer Identify**. The registration process involves a multi-step sequence: identifying the regional domain, solving a visual captcha challenge, triggering an SMS OTP, and finally submitting user credentials. The platform uses extensive device fingerprinting via a `featureCode` and encrypts sensitive fields like passwords. Automation is complex due to the requirement of solving the custom captcha challenge and replicating the client-side encryption.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | 4-digit OTP code sent via SMS |
| **Captcha** | Custom Challenge | `human_computer_identify` system |
| **Encryption** | Custom/RSA | Encrypted password payloads in registration requests |
| **Rate Limits** | Unknown | No explicit rate limiting observed in the trace |
| **Endpoints Involved** | 5 | `/area/domain`, `/identify/verify`, `/checkcode/mt/unlogin/second`, `/regist/v3` |
| **Bot Protection** | Human-Computer Identify | Custom behavioral and visual verification system |

## 3. Flow Details

### Flow 1: Registration & SMS Verification

**Step 1: Regional Domain Discovery**
- **Endpoint**: `POST https://api.ezvizlife.com/api/area/domain`
- **Purpose**: Identify the correct regional API server (e.g., `apiiindia.ezvizlife.com`)
- **Response**:
    ```json
    {
      "domain": "apiiindia.ezvizlife.com",
      "resultCode": "0",
      "areaDomain": "apiiindia.ezvizlife.com"
    }
    ```

**Step 2: Solve Captcha Challenge**
- **Endpoint**: `GET /v3/human_computer_identify/verify`
- **Purpose**: Verify the user is human to receive a `captchaToken`
- **Notable Params**:
    - `captchaId`: `c05d25b5f9ca46fe8956f179a27e182c`
    - `y`: Encrypted behavioral data
- **Response**:
    - Returns a `captchaToken` required for the SMS request.

**Step 3: Request SMS OTP**
- **Endpoint**: `POST /v3/users/checkcode/mt/unlogin/second`
- **Purpose**: Trigger SMS delivery to the specified phone number
- **Request Payload**:
    <!-- Phone Submission -->
    ```json
    {
      "from": "393522458920",
      "bizType": "USER_REGISTRATION",
      "captchaToken": "IxeRCgrbuBpzVHYRaOAaiA==",
      "msgType": "1"
    }
    ```
- **Response**:
    ```json
    {
      "resultCode": "0",
      "resultDes": "SUCCESS"
    }
    ```

**Step 4: Verify OTP & Register**
- **Endpoint**: `POST /v3/users/regist/v3`
- **Purpose**: Submit the SMS code and complete account creation
- **Request Payload**:
    <!-- OTP Submission -->
    ```json
    {
      "phone": "393522458920",
      "smsCode": "9999",
      "password": "[ENCRYPTED_DATA]",
      "areaId": "244",
      "regType": "1",
      "featureCode": "77219bef3ecd50a6b3a215ed77d5ab75"
    }
    ```
- **Response**:
    ```json
    {
      "resultCode": "0",
      "resultDes": "Registration Successful"
    }
    ```

## 4. Security & Reversing Notes

### Human-Computer Identify
The core security mechanism is the `human_computer_identify` system. It involves loading a challenge script and submitting encrypted interaction data (`y` parameter). The resulting `captchaToken` is cryptographically bound to the session and the specific phone number.

### Password Encryption
Passwords are not sent in plaintext. They are encrypted on the client-side using a method that produces a large Base64-encoded string, likely involving RSA or a custom AES implementation tied to the `featureCode`.

### Regional Routing
EZVIZ uses a global discovery service to route users to the nearest data center. This requires an initial `/api/area/domain` call, and all subsequent authentication calls must be directed to the returned regional host.

## 5. Conclusion

### Automation Feasibility: 40% (Low)

### Detailed Conclusion:
The EZVIZ registration flow is well-protected against simple script-based automation. The primary blockers are the custom captcha system and the client-side payload encryption. Automated registration would require either a full browser-based automation (Puppeteer/Playwright) to handle the captcha or a deep reverse-engineering of the `human_computer_identify` logic and the password encryption routines. The high level of device fingerprinting (`featureCode`) also suggests that IP and device reputation are likely monitored.
