# T-Business (T-Bank) - Research Report

## Metadata
- **Target URL/App**: `ru.tinkoff.sme`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-08`
- **Status**: `Completed`
- **HAR Files**: `Tbank.har`

## 1. Executive Summary
T-Bank Business (mbsme) implements a multi-step authentication flow designed for secure enterprise access. The process utilizes device fingerprinting, session-bound conversation IDs (`cid`), and a consolidated endpoint (`/auth/step`) for various authentication phases including phone number submission, OTP verification, and code resending. The application performs extensive background telemetry and event tracking to monitor session integrity. Automation feasibility is assessed as High, provided the session context (`cid` and cookies) is maintained correctly across requests.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for OTP delivery |
| **Captcha** | undefined | No visual captcha observed in the captured flow |
| **Encryption** | TLS + Fingerprinting | Standard HTTPS encryption with custom device fingerprinting in payloads |
| **Rate Limits** | Unknown | No rate limiting behavior (429) was observed during testing |
| **Endpoints Involved** | 3 | `/auth/authorize`, `/auth/step` (phone), `/auth/step` (otp) |
| **Bot Protection** | Fingerprinting | Custom device fingerprinting and session tracking via `cid` |

## 3. Flow Details

### Flow 1: Authentication (Login/Registration)

**Step 1: Initialize Authorization**
- **Endpoint**: `POST https://id.tbank.ru/auth/authorize`
- **Purpose**: Initialize the OIDC-compliant authorization flow and obtain the conversation context.
- **Request Headers**:
    ```text
    Accept: application/json
    User-Agent: mbsme-android/3.23 (Android 15; google Pixel 7)
    Content-Type: application/x-www-form-urlencoded
    Host: id.tbank.ru
    ```
- **Request Payload**:
    ```text
    client_id=mbsme&redirect_uri=mobile%3A%2F%2F&response_type=code&response_mode=json&display=json&device_id=653b5540d1afe722&client_version=14.0.2-hotfix1&vendor=tinkoff_android&claims=%7B%22id_token%22%3A%7B%22nickname%22%3Anull%2C%22email%22%3Anull%2C%22email_verified%22%3Anull%7D%7D
    ```
- **Response**:
    ```json
    {
      "authId": "YJWkaHldN6lzzStaLLT3",
      "clientId": "mbsme",
      "theme": "default",
      "action": "step",
      "step": "phone",
      "cid": "YUTFVhyVZI0kAcQ4GA0",
      "supportDarkTheme": false
    }
    ```

**Step 2: Phone Number Submission (SMS Request)**
- **Endpoint**: `POST https://id.tbank.ru/auth/step?cid=YUTFVhyVZI0kAcQ4GA0`
- **Purpose**: Submit the user's phone number to trigger the OTP delivery.
- **Request Headers**:
    ```text
    Accept: application/json
    User-Agent: mbsme-android/3.23 (Android 15; google Pixel 7)
    X-Lang: ru
    Content-Type: application/x-www-form-urlencoded
    Host: id.tbank.ru
    ```
- **Request Payload**:
    ```text
    <!-- Phone Number: +393517641332 -->
    phone=%2B393517641332&fingerprint=%7B%22appVersion%22%3A%223.23%22%2C%22clientLanguage%22%3A%22ru%22%2C%22clientTimezone%22%3A-330%2C%22timeZoneName%22%3A%22Asia%2FKolkata%22%2C%22latitude%22%3Anull%2C%22longitude%22%3Anull%7D
    ```
- **Response**:
    ```json
    {
      "authId": "YJWkaHldN6lzzStaLLT3",
      "clientId": "mbsme",
      "theme": "default",
      "action": "step",
      "step": "otp",
      "cid": "YUTFVhyVZI0kAcQ4GA0",
      "step_back_allowed": true,
      "supportDarkTheme": false,
      "token": "053ef94b13",
      "keyboard": "numeric",
      "length": 4,
      "phone": "+39 351 764-13-32",
      "resend_after_ms": 59972
    }
    ```

**Step 3: OTP Verification**
- **Endpoint**: `POST https://id.tbank.ru/auth/step?cid=YUTFVhyVZI0kAcQ4GA0`
- **Purpose**: Verify the 4-digit OTP code received via SMS.
- **Request Headers**:
    ```text
    Accept: application/json
    User-Agent: mbsme-android/3.23 (Android 15; google Pixel 7)
    Content-Type: application/x-www-form-urlencoded
    Host: id.tbank.ru
    ```
- **Request Payload**:
    ```text
    <!-- OTP Code: 2522 -->
    otp=2522&token=053ef94b13&step=otp
    ```
- **Response**:
    ```json
    {
      "authId": "YJWkaHldN6lzzStaLLT3",
      "clientId": "mbsme",
      "theme": "default",
      "action": "step",
      "step": "otp",
      "cid": "YUTFVhyVZI0kAcQ4GA0",
      "error": "invalid_request",
      "error_message": "\u041f\u0440\u043e\u0432\u0435\u0440\u044c\u0442\u0435 \u043a\u043e\u0434 \u2014 \u044d\u0442\u043e\u0442 \u043d\u0435\u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u044b\u0439",
      "token": "053ef94b13",
      "length": 4,
      "phone": "+39 351 764-13-32"
    }
    ```
- **Analysis**: The response indicates an incorrect OTP was submitted (`error_message` translates to "Check the code — this one is incorrect"). The `token` from the previous step must be included in the verification request.

## 4. Security & Reversing Notes

### Authentication Mechanisms
1. **Conversation Context (`cid`)**: All authentication steps are tied to a unique `cid` provided in the initial `authorize` response. This ID must remain constant throughout the flow.
2. **Step Token**: The phone submission response provides a `token` (e.g., `053ef94b13`) that must be included in the subsequent OTP verification request.
3. **Fingerprinting**: The phone submission request includes a `fingerprint` JSON object containing app version, language, timezone, and geolocation data.

### Bot Detection
- **Header Monitoring**: The server monitors `User-Agent` and session-specific cookies (`SSO_CONVERSATION_CSRF_YUTFV`, `__P__wuid`, `sso_uaid`).
- **Telemetry**: Extensive telemetry data is sent to `as.t-bank-app.ru/gateway/v1/events` during the auth process, likely used for behavioral risk assessment.

## 5. Conclusion

### Automation Feasibility: High (85%)

### Detailed Conclusion:
The T-Bank Business authentication flow is straightforward and lacks aggressive bot protection measures like visual captchas or complex request signing (at least in the observed initial steps). The primary requirements for automation are:
1. Maintaining the session state (cookies and `cid`).
2. Correctly capturing the `token` from the SMS request response.
3. Mimicking the fingerprinting payload (which appears static or easily replicable).

The flow is well-structured and uses standard REST/Form-encoded patterns, making it highly feasible for automated integration and security testing.

## X. Conclusion
The security reconnaissance of the T-Bank Business (mbsme) application reveals a robust yet automatable authentication framework. The platform effectively utilizes session-bound conversation IDs and multi-step verification to secure enterprise accounts. While device fingerprinting and telemetry are implemented to mitigate risk, the absence of complex cryptographic signatures or interactive captchas in the primary login flow suggests a high level of technical feasibility for automation. Security researchers should focus on the integrity of session tokens and the proper replication of device metadata to successfully interface with the authentication API.
