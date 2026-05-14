
# Weltrade - Research Report

## Metadata
- **Target URL/App**: `secure.weltrade.app` / `com.weltrade.appterminal`
- **Researcher**: `Security Research Team`
- **Date**: `2026-04-26`
- **Status**: `Completed`
- **HAR Files**: `WellTrade.har`

## 1. Executive Summary
Weltrade (com.weltrade.appterminal) uses a web-view based architecture for its Android application, routing most critical actions through `secure.weltrade.app`. The security model involves a two-stage registration and verification process: initial account creation via Email (protected by Google reCAPTCHA) followed by mandatory phone verification via SMS OTP. Post-registration sessions are managed using standard JWT Bearer tokens. Automation feasibility is moderate, primarily constrained by the reCAPTCHA requirement during the registration step.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | Email + SMS | Email for registration, SMS for phone binding/verification |
| **Captcha** | reCAPTCHA v2 Image Challenge (Google) | reCAPTCHA v2 Image Challenge (Google) |
| **Encryption** | Standard | HTTPS with JWT Bearer tokens for session auth |
| **Rate Limits** | Unknown | No rate limiting behavior was observed during testing |
| **Endpoints Involved** | 3 | `/app/api/v1/`, `/app/api/v2/`, `recaptcha/api2/userverify` |

## 3. Flow Details

### Flow 1: Registration and Email Confirmation

**Step 1: Registration Request**
- **Endpoint**: `POST https://secure.weltrade.app/app/api/v1/`
- **Action**: `terminal.registration`
- **Request Payload**:
    ```json
    [
      {
        "action": "terminal.registration",
        "data": {
          "EMAIL": "user@example.com",
          "PERSONAL_COUNTRY": "IL",
          "UF_TIMEZONE": 5.5,
          "agreement": true,
          "RECAPTCHA": "0cAFcWeA6EuWQFZ7o3-DJNA3A5Bh8YC04F8AoN9L0fQ...",
          "PASSWORD": "hashed_or_plain_password",
          "FINGERPRINT": "d2ed623ef1e2f523d0eb1c1ec077d777",
          "ACCOUNT_TYPE": "PRO"
        }
      }
    ]
    ```

**Step 2: Confirm Registration (Email Hash)**
- **Endpoint**: `POST https://secure.weltrade.app/app/api/v1/`
- **Action**: `token.confirmRegistration`
- **Purpose**: Validates the email verification link clicked by the user.
- **Request Payload**:
    ```json
    [
      {
        "action": "token.confirmRegistration",
        "data": {
          "HASH": "7dbff79bb5ecb204127e97acac9ec59ea77b0e75",
          "FINGERPRINT": "d2ed623ef1e2f523d0eb1c1ec077d777"
        }
      }
    ]
    ```

### Flow 2: Phone Verification

**Step 1: Set Initial Phone**
- **Endpoint**: `POST https://secure.weltrade.app/app/api/v2/`
- **Action**: `client.setPhoneFirst`
- **Authorization**: `Bearer <JWT_TOKEN>`
- **Request Payload**:
    ```json
    [
      {
        "action": "client.setPhoneFirst",
        "data": {
          "PERSONAL_PHONE": "+918791267460"
        }
      }
    ]
    ```

**Step 2: Send SMS OTP**
- **Endpoint**: `POST https://secure.weltrade.app/app/api/v2/`
- **Action**: `client.sendSms`
- **Request Payload**:
    ```json
    [
      {
        "action": "client.sendSms",
        "data": {
          "phone": "+918791267460"
        }
      }
    ]
    ```

**Step 3: Verify SMS Code**
- **Endpoint**: `POST https://secure.weltrade.app/app/api/v2/`
- **Action**: `client.checkSmsCode`
- **Request Payload**:
    ```json
    [
      {
        "action": "client.checkSmsCode",
        "data": {
          "code": "4971"
        }
      }
    ]
    ```

## 4. Security & Reversing Notes

### Authentication Mechanism
Weltrade utilizes a JSON-based RPC interface where multiple actions can be batched in a single request. 
- **API v1**: Used for unauthenticated or initial session setup (registration, login, confirmation).
- **API v2**: Used for authenticated client actions, requiring a `Authorization: Bearer` header.

### Bot Protection
- **reCAPTCHA**: The `terminal.registration` action is strictly protected by reCAPTCHA v2. The token is obtained from `www.recaptcha.net` and must be included in the registration payload.
- **Fingerprinting**: A `FINGERPRINT` field (MD5-like hash) is consistently used in authentication-related actions to track the client device.

### Session Management
Once the registration is confirmed or the user logs in, the server issues a JWT. This token is used in subsequent requests to the `/api/v2/` endpoints.

## 5. Conclusion

### Automation Feasibility: 40%

### Critical Blockers:
1. **reCAPTCHA v2**: High hurdle for fully automated registration. Requires either manual intervention or integrated solver services.
2. **Email Hash**: The flow requires extracting a unique hash from a verification email sent to the user's inbox.
3. **SMS Verification**: Standard OTP verification blocker.

### Success Criteria for Automation:
- Functional reCAPTCHA solving mechanism.
- Automated email polling to retrieve the registration hash.
- Consistent device fingerprinting implementation.
