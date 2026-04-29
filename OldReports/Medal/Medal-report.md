# Medal - Research Report

## Metadata
- **Target App**: `Medal (tv.medal.recorder)`
- **Version**: `6.9.1`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-26`
- **Host**: `api-v2.medal.tv`

## 1. Executive Summary
Medal is a gaming clip sharing platform. The application uses social login (Google/Facebook) and allows users to link their phone number for verification. The phone verification process involves sending an OTP via SMS and subsequently submitting the code to the user settings endpoint. The flow is protected by standard session-based authentication following a social login. No explicit CAPTCHA challenge was observed during the phone linking process in the captured trace.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | primary channel for phone verification |
| **Captcha** | undefined | No captcha was observed during the phone linking flow |
| **Encryption** | None | Data is transmitted in plaintext JSON over standard HTTPS |
| **Rate Limits** | Unknown | No rate limiting response (HTTP 429) was observed during testing |
| **Endpoints Involved** | 1 | `/users/{userId}/settings` (used for both sending and verifying) |
| **Bot Protection** | None | No specific bot protection was identified on the phone verification endpoints |

## 3. Flow Details

### Step 1: Phone Number Submission (Send OTP)
- **Endpoint**: `POST https://api-v2.medal.tv/users/{userId}/settings`
- **Purpose**: Submit phone number to trigger OTP SMS.
- **Notable Headers**:
    - `User-Agent`: `Medal-Android/6.9.1 ...`
    - `Authorization`: `[Bearer Token]`
- **Request Payload**:
    ```json
    {
      "contactDiscoverable": false,
      "phone": "<!-- Phone Number Highlight --> <mark>+918791267460</mark>"
    }
    ```
- **Response Payload**:
    ```json
    {
      "userId": "616228614",
      "displayName": "deepdude61",
      "phone": "+918791267460",
      ...
    }
    ```

### Step 2: Verify OTP
- **Endpoint**: `POST https://api-v2.medal.tv/users/{userId}/settings`
- **Purpose**: Submit the verification code received via SMS.
- **Request Payload**:
    ```json
    {
      "contactDiscoverable": false,
      "phoneVerificationCode": "<!-- OTP Highlight --> <mark>700654</mark>"
    }
    ```
- **Response Payload**:
    ```json
    {
      "userId": "616228614",
      "displayName": "deepdude61",
      ...
    }
    ```

## 4. Conclusion

### Automation Feasibility: High (80%)

### Detailed Conclusion:
Medal's phone verification flow is highly automatable as it relies on a single endpoint for both triggering the SMS and verifying the code. The primary requirement for automation is a valid authentication token (obtained via social login or existing session). There are no complex cryptographic signings or CAPTCHAs implemented on these specific endpoints, making it a low-friction target for automated verification once the initial session is established.

**Strengths**:
- Simple RESTful API structure.
- No CAPTCHA observed in the verification flow.

**Weaknesses**:
- Relies solely on session tokens for authorization without additional per-request integrity checks for phone linking.

**Recommendations**:
Automation should focus on maintaining a valid session token. The `userId` is dynamic and must be extracted from the session initialization or user profile endpoint before calling the settings endpoint.
