# XTransfer - Research Report

## Metadata
- **Target URL/App**: `com.xtapp.xtransfer`
- **Researcher**: `Security Research Team`
- **Date**: `2026-04-27`
- **Status**: `Completed`
- **HAR Files**: `Xtransfer.har (Sign-up / Login flow)`

## 1. Executive Summary
XTransfer implements a secure authentication system for its B2B financial services, primarily relying on mobile phone number verification via SMS OTP. The platform's security is anchored by GeeTest v4 (Adaptive CAPTCHA) on the OTP request endpoint and multi-layered session tracking using custom headers (`x-server-grant-id`, `x-flow-id`). The application uses React Native and integrates with Sentry and Umeng for monitoring. Automation feasibility is low to moderate, primarily gated by the requirement to solve GeeTest v4 challenges and maintain strict session/device consistency.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS OTP | Primary method for login and registration |
| **Captcha** | Yes | GeeTest v4 (Adaptive CAPTCHA) |
| **Encryption** | Yes | TLS 1.3, CSRF protection via XSRF-TOKEN, session-linked headers |
| **Rate Limits** | Yes | Enforced via GeeTest and session tracking |
| **Endpoints Involved** | 4 | /device, /message/send, /sign-up/login-name, /user-info |

## 3. Flow Details

### Flow 1: Registration / Login via OTP

**Step 1: Device Registration**
- **Endpoint**: `POST /api/v1/user-front/device`
- **Purpose**: Initialize device session and obtain a unique grant identifier
- **Notable Headers**:
    - `Content-Type`: `application/json`
- **Request Payload**:
    ```json
    {
        "appName": "XTransfer",
        "brand": "google",
        "buildNumber": "260306140",
        "bundleId": "com.xtapp.xtransfer",
        "deviceId": "panther",
        "model": "Pixel 7",
        "readableVersion": "3.7.14.260306140",
        "systemVersion": "15",
        "uniqueId": "d1170e4b172b7528",
        "version": "3.7.14"
    }
    ```
- **Response**:
    ```json
    {
        "serverGrantId": "NfANzrfXpAAk0dJ5ysIYQ+lNQM6R5AdAmEFRd2/JXqo="
    }
    ```
- **Analysis**: The `serverGrantId` is a critical session component used in the `x-server-grant-id` header for all subsequent calls.

**Step 2: Request SMS OTP (Captcha Protected)**
- **Endpoint**: `POST /api/v1/user-front/message/send`
- **Purpose**: Request SMS OTP after solving GeeTest challenge
- **Notable Headers**:
    - `x-server-grant-id`: [From Step 1]
    - `x-flow-id`: Unique session flow ID
    - `x-xsrf-token`: CSRF token from cookies
- **Request Payload**:
    ```json
    {
        "captchaVCode": "{\"captcha_output\":\"bgz9JL...\",\"gen_time\":\"1777274460\",\"lot_number\":\"929f99...\",\"pass_token\":\"96079b...\"}",
        "mobileAreaCode": "91",
        "receiver": "8791267460",
        "verifyType": "SMS",
        "authType": "user",
        "flowId": "c85HuSeu7zUiYcucEcOBWhE8ah2C1v+UBOhVwH/vw3+EEX/K5lB63IJBqgbT+yfB"
    }
    ```
- **Response**:
    ```json
    {
        "success": true
    }
    ```
- **Analysis**: The `captchaVCode` contains the serialized output of a successful GeeTest v4 challenge.

**Step 3: Verify OTP**
- **Endpoint**: `POST /api/v1/user-front/sign-up/login-name`
- **Purpose**: Submit the received OTP to complete authentication
- **Request Payload**:
    ```json
    {
        "dialingCode": "91",
        "mobile": "8791267460",
        "msgVCode": "237225",
        "type": "PHONE",
        "flowId": "c85HuSeu7zUiYcuc...",
        "domain": "username",
        "businessSource": "APP_Organic"
    }
    ```
- **Response**:
    ```json
    {
        "status": 200,
        "data": { ... }
    }
    ```
- **Analysis**: Successful verification establishes the user session, allowing access to `user-info` and `firm-info` endpoints.

## 4. Security & Reversing Notes

### Encryption/Signing Mechanisms

**1. Session Tracking Headers**
- **Header**: `x-server-grant-id` and `x-flow-id`
- **Purpose**: Binds the request to a specific device and authentication attempt.
- **Analysis**: The `serverGrantId` is generated server-side upon device registration, while `flowId` tracks the specific UI flow (e.g., registration vs. forgot password).

**2. CSRF Protection**
- **Header**: `x-xsrf-token`
- **Source**: `XSRF-TOKEN` cookie.
- **Analysis**: Standard implementation to prevent cross-site request forgery.

### Captcha Integration
- **Type**: GeeTest v4 (Adaptive CAPTCHA)
- **Token Flow**: The app initializes GeeTest via `gcaptcha4.geetest.com/load`, solves it locally, and sends the resulting tokens (`captcha_output`, `pass_token`, etc.) in the `captchaVCode` field.
- **Validation**: Server-side validation of the GeeTest result before triggering the SMS gateway.

### Bot Detection
- **GeeTest v4**: Provides sophisticated behavioral analysis and environment checks.
- **WAF**: The g-api.xtransfer.com domain is protected by Cloudflare, providing DDoS protection and TLS fingerprinting.
- **Device Fingerprinting**: Collected during the `/device` call including `uniqueId`, `brand`, and `model`.

### Key Security Features
1. **Behavioral CAPTCHA**: Mandatory for all OTP requests to prevent mass SMS flooding.
2. **Device Binding**: Authentication flows are tied to the registered device ID.
3. **Audit Trails**: Integration with Sentry and Umeng suggests heavy monitoring of client-side events.

## 5. Conclusion

### Automation Feasibility: 35%

### Critical Blockers:
1. **GeeTest v4 Integration**: Requires a specialized solver to generate valid `captchaVCode` payloads.
2. **Session Consistency**: Strict requirement to maintain `flowId`, `serverGrantId`, and CSRF tokens across multiple steps.
3. **Environment Checks**: GeeTest v4 performs extensive telemetry collection which must be accurately mimicked.
