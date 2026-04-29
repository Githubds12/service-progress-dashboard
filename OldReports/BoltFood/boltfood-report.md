# Bolt Food - Research Report

## Metadata
- **Target URL/App**: `com.bolt.deliveryclient`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-26`
- **Status**: `Completed`
- **HAR Files**: `BoltFood.har`

## 1. Executive Summary
Bolt Food implements a standard OTP-based authentication flow with SMS as the primary verification channel. The application utilizes Google reCAPTCHA v2 for bot protection during the registration/login process. The traffic analysis reveals a clean three-step flow: phone number submission, OTP verification, and profile completion. While the API payloads are in plaintext JSON, the platform is protected by Cloudflare and implements device-specific tracking using session identifiers and session UUIDs. Automation feasibility is medium-high, contingent on successful reCAPTCHA solving.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for OTP |
| **Captcha** | reCAPTCHA v2 Image Challenge (Google) | Observed reCAPTCHA scripts and endpoints |
| **Encryption** | None | Plaintext JSON payloads over HTTPS |
| **Rate Limits** | Unknown | No rate limiting behavior was explicitly observed during testing |
| **Endpoints Involved** | 3 | `/profile/verification/start`, `/profile/verification/confirm`, `/profile/registration/complete` |
| **Bot Protection** | Cloudflare & Google reCAPTCHA | Cloudflare edge protection and Google reCAPTCHA v2 |

## 3. Flow Details

### Flow 1: Authentication & Registration

**Step 1: Request OTP (Phone Number Submission)**
- **Endpoint**: `POST https://deliveryuser.live.boltsvc.net/profile/verification/start`
- **Purpose**: Submit phone number to trigger SMS OTP
- **Notable Headers**:
    - `User-Agent`: `okhttp/4.12.0`
    - `Content-Type`: `application/json`
- **Request Payload**:
    ```json
    {
      "phone_number": "+918791267460",
      "phone_uuid": "8a06caa4-f8aa-413a-bc65-888cf5fc9697",
      "type": "phone",
      "last_known_state": {}
    }
    ```
- **Response**:
    ```json
    {
      "code": 0,
      "message": "OK",
      "data": {
        "state": "pending_phone_verification",
        "phone": "+918791267460",
        "resend_confirmation_interval_ms": 20000,
        "ui_content": {
          "title": "Verify phone number",
          "text": "We sent a verification code to +918791267460"
        }
      }
    }
    ```
- **Analysis**: The `phone_uuid` appears to be a client-side generated UUID for tracking the session.

**Step 2: Verify OTP**
- **Endpoint**: `POST https://deliveryuser.live.boltsvc.net/profile/verification/confirm`
- **Purpose**: Verify the 4-digit OTP received via SMS
- **Request Payload**:
    ```json
    {
      "phone_number": "+918791267460",
      "phone_uuid": "8a06caa4-f8aa-413a-bc65-888cf5fc9697",
      "code": "5613",
      "type": "phone",
      "last_known_state": {}
    }
    ```
- **Response**:
    ```json
    {
      "code": 0,
      "message": "OK",
      "data": {
        "state": "pending_signup",
        "ui_content": {
          "title": "Complete profile",
          "text": "Please enter your personal details to complete your profile"
        }
      }
    }
    ```
- **Analysis**: Successful verification transitions the state to `pending_signup`.

**Step 3: Complete Registration**
- **Endpoint**: `POST https://deliveryuser.live.boltsvc.net/profile/registration/complete`
- **Purpose**: Submit user details to finish account creation
- **Request Payload**:
    ```json
    {
      "phone_number": "+918791267460",
      "phone_uuid": "8a06caa4-f8aa-413a-bc65-888cf5fc9697",
      "first_name": "Deepanshu ",
      "last_name": "Singh ",
      "email": "deepanshusinghdigitalheroes@gmail.com",
      "type": "email",
      "last_known_state": {}
    }
    ```
- **Response**:
    ```json
    {
      "code": 0,
      "message": "OK",
      "data": {
        "state": "complete",
        "auth": {
          "id": 310418470,
          "phone": "+918791267460",
          "auth_token": "c0JFd3SpP5Vm6PMC17SUZaYm90I1lNiG9fDv9aIznHpVDj94ZZPrxnICyrFtpJhWR2uRJw8J6PWKa4y3JKbXUgka77bOPasVSqY16RxVXVMbulHUiIp3jjds23elLjYIXw5Qr61bKLA92P0BM8GFToJ6TiYoyI089SiF8DsTvGtkOp5v4uk8Vti9xrObwcLQS6vvE20nP7WXGpUmjNjAgD19XfaApvUEnQfEtKhdH5KM40OFonCTsWoFMqsIi9Yg"
        }
      }
    }
    ```
- **Analysis**: Returns the `auth_token` required for authenticated requests.

## 4. Security & Reversing Notes
- **Bot Protection**: The presence of `www.recaptcha.net` in the HAR indicates that Google reCAPTCHA v2 is used. It is likely triggered based on risk analysis or frequency.
- **Session Tracking**: Uses `phone_uuid` and `session_id` query parameters across all endpoints to maintain flow state.
- **Cloudflare Integration**: Endpoints are served via Cloudflare, providing protection against DDoS and simple bot patterns.

## 5. Conclusion

### Automation Feasibility: 75% (High)

### Detailed Conclusion
The Bolt Food authentication API is straightforward and uses standard RESTful patterns with JSON payloads. There is no heavy payload encryption or custom header signing involved, which significantly lowers the barrier for automation. The primary hurdle is the Google reCAPTCHA v2 implementation, which can be bypassed using automated solvers or behavioral mimicking. The flow is predictable and consistent across the analyzed traces.
