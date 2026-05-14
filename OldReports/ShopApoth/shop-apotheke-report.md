# Shop Apotheke - Research Report

## Metadata
- **Target URL/App**: `shop.shop_apotheke.com.shopapotheke`
- **Researcher**: `Security Research Team`
- **Date**: `2026-04-27`
- **Status**: `Completed`
- **HAR Files**: `ShopApoth.har (Flows: Register, NFC Card Positioning, Phone MFA)`

## 1. Executive Summary
Shop Apotheke (Redcare) implements a secure onboarding flow for its European pharmacy platform. The app utilizes JWT-based authentication (Bearer tokens) and integrates a specialized "CardLink" flow for e-prescription redemption via NFC health cards. The registration process is straightforward, but the subsequent MFA step for phone verification adds a layer of security. Analysis reveals that while core flows are functional, there are opportunities to improve rate-limiting on MFA endpoints and app attestation checks.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS OTP | 6-digit code for phone verification |
| **Captcha** | undefined | No visual captcha observed in the analyzed flows |
| **Encryption** | SSL/TLS | Standard HTTPS with SSL Pinning and Root Detection |
| **Rate Limits** | Low | No strict cooldown observed on SMS OTP requests |
| **Endpoints Involved** | 5 | register, erx-session-status, nfc-position, mfa-request, mfa-confirmation |

## 3. Flow Details

### Flow 1: Signup (Registration)
- **Endpoint**: `POST https://api.sa-tech.de/auth/v2/com/register`
- **Purpose**: Create a new customer account
- **Notable Headers**:
    - `User-Agent`: `okhttp/4.11.0`
    - `Content-Type`: `application/json`
- **Request Payload**:
    ```json
    {
      "dateOfBirth": "1998-04-15",
      "email": "deepanshusinghdigitalheroes@gmail.com",
      "firstName": "Deepanshu",
      "lastName": "Singh",
      "newsletterAccepted": false,
      "password": "Facebook@ds12,",
      "preferredLanguage": "de",
      "registrationOrigin": "app",
      "salutation": "mr",
      "tosAccepted": true
    }
    ```
- **Response**:
    ```json
    {
      "tokenType": "bearer",
      "token": "eyJraWQiOiJmMjI3MGU4OS1iOGJjLTQ1ODAtOTA2MC01OTBmMTNiYjkyMjEiLCJhbGciOiJSUzM4NCJ9..."
    }
    ```
- **Analysis**: Registration returns a Bearer token used for all subsequent authenticated requests.

---

### Flow 2: E-Prescription Redemption (NFC)
**Step 1: Check Session Status**
- **Endpoint**: `GET https://api.sa-tech.de/session/v1/com/erx-session-status/2514629848`
- **Purpose**: Check if an e-prescription session is already active for the user.
- **Response (404)**: Indicates no active session.

**Step 2: NFC Card Position**
- **Endpoint**: `POST https://api.sa-tech.de/nfc-health-card-position/api/v1/nfc-position`
- **Purpose**: Retrieve precise NFC antenna location for the user's device model to ensure successful card reading.
- **Request Payload**:
    ```json
    {
      "manufacturer": "Google",
      "marketingName": "Pixel 7",
      "modelName": "Pixel 7",
      "os": "Android"
    }
    ```
- **Response**:
    ```json
    {
      "nfcPos": {
        "x0": 0.35, "y0": 0.25, "x1": 0.65, "y1": 0.4
      },
      "found": true
    }
    ```

---

### Flow 3: Phone MFA Verification
**Step 1: Request OTP**
- **Endpoint**: `POST https://api.sa-tech.de/customer/v1/com/mfa/2514629848/phone-verification/request`
- **Purpose**: Trigger a 6-digit OTP SMS to the provided phone number.
- **Request Payload**:
    ```json
    {
      "phoneNumber": "+491765550123"
    }
    ```
- **Response**: `204 No Content`

**Step 2: Verify OTP**
- **Endpoint**: `POST https://api.sa-tech.de/customer/v1/com/mfa/2514629848/phone-verification/confirmation`
- **Purpose**: Submit the received 6-digit code.
- **Request Payload**:
    ```json
    {
      "code": "222222"
    }
    ```
- **Response (400)**: `erx.phone_verification.password_rejected` (due to invalid code).

---

## 4. Security & Reversing Notes

### Authentication Mechanism
- **JWT Tokens**: The app uses standard JSON Web Tokens.
- **Session Tracking**: Authenticated via `Authorization: Bearer {token}`.

### CardLink (NFC) Security
- The NFC flow relies on server-side positioning data to guide the user.
- The actual prescription data exchange happens over a secure NFC channel (not fully captured in this API-level HAR).

### Bot Detection & Anti-Fraud
- **SSL Pinning**: Active on `api.sa-tech.de`.
- **Root Detection**: App checks for rooted devices during initialization.
- **App Attestation**: Currently missing strict Play Integrity/SafetyNet checks on registration.

---

## 5. Conclusion

### Automation Feasibility: 75%

### Critical Blockers:
1. **SSL Pinning**: Requires dynamic instrumentation (Frida) to bypass for traffic analysis.
2. **NFC Physicality**: Automating the e-prescription redemption requires physical NFC interaction or hardware emulation.
3. **SMS OTP**: Requires a reliable SMS reception and parsing system.
