# Bitget - Research Report

## Metadata
- **Target URL/App**: `com.bitget.exchange` (Bitget Crypto Exchange)
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29`
- **Status**: `Completed`
- **HAR Files**: `BitGet.har`

## 1. Executive Summary
Bitget implements a high-security authentication flow designed to prevent automated registration and API abuse. The application utilizes a proxy-based REST API architecture (`appapi.abcdstable.com`) protected by mandatory behavioral captchas (Geetest-like), encrypted request signing (`x-sign`), and server-side runtime protection (OpenRASP). The registration sequence requires stateful token management, where a `verifyKey` obtained from captcha validation is required for both SMS triggering and final OTP verification. Automation feasibility is low due to the complexity of human-behavioral challenges and proprietary header generation.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | 6-digit OTP code delivered via international channels |
| **Captcha** | Behavioral | Mandatory Geetest-style interaction challenge |
| **Encryption** | Yes | Proprietary `x-sign` header and session-bound `dy-token` |
| **Rate Limits** | Strict | Enforced via `deviceId` and `terminalCode` tracking |
| **Endpoints Involved** | 4 | get-captcha-id, check-login-name, verifyCode/send, register/pre-check |

## 3. Flow Details

### Flow 1: Registration (Mobile)

**Step 1: Get Captcha ID**
- **Endpoint**: `POST https://appapi.abcdstable.com/v1/security/policy/captcha/get-captcha-id`
- **Purpose**: Initialize the captcha challenge and obtain a `captchaId`.
- **Notable Headers**:
    - `x-sign`: EDGE-V1-1-6yuwcdZQzTXwhzLWIItQKnxuIIkJ9R0UhmiEeX3QjW0=
    - `deviceId`: a177741635452379781998816
- **Request Payload**:
    ```json
    {
      "areaCode": 39,
      "bizParam": "3522956432",
      "scene": "UserRegister"
    }
    ```
- **Response**:
    ```json
    {
      "code": "200",
      "data": {
        "captchaId": "e5f230bd177d2fa44be722d94adeb2d6",
        "captchaType": "3"
      }
    }
    ```

**Step 2: Validate Captcha (Check Login Name)**
- **Endpoint**: `POST https://appapi.abcdstable.com/v1/user/public/check-login-name`
- **Purpose**: Submit the solved captcha challenge to receive an authentication `verifyKey`.
- **Notable Headers**:
    - `dy-token`: 69f138a5jmjDCgPVEn1BtnCHWiBhgPvgtalyWMI3
    - `terminalCode`: a-18882693-1777416354786-7638746
- **Request Payload**:
    ```json
    {
      "areaCode": "39",
      "bizId": "d8abd824c0aa43cb8e1d90096527fb49",
      "captchaParam": {
        "bizId": "d8abd824c0aa43cb8e1d90096527fb49"
      },
      "captchaType": "3",
      "captchaValidate": "eyJjYXB0Y2hhX2lkIjoiZTVmMjMwYmQxNzdkMmZhNDRiZTcyMmQ5NGFkZWIyZDYiLCJsb3RfbnVtYmVyIjo..."
    }
    ```
- **Response**:
    ```json
    {
      "code": "200",
      "data": {
        "verifyKey": "hmac_CwgCEiA2REY2QkJFOTM3QUM2N0UyMTJEREJCQjEzQkNFNTgyNxoSc2VydmljZS1ncm91cC1kYXRhDBJbESS4PB5nJRYxpx8OKANhCZAiK8fnrra4Xjpk/vWd36JhMRTq8a4YjOg/o5nPiaH9Hg565LgOCKOx2NfXJlWq2XIrHJXfK5yOJ9JB+IaA97A4RLLCOfWU7zo/SA=="
      }
    }
    ```

**Step 3: Phone Number Submitting Endpoint (SMS Trigger)**
- **Endpoint**: `POST https://appapi.abcdstable.com/v1/msg/verifyCode/send`
- **Purpose**: Request the 6-digit OTP code to be sent to the user's mobile device.
- **Notable Headers**:
    - `X-Request-ID`: de11404ff54a482fb0e90908edf7c24a
    - `X-Protected-By`: OpenRASP
- **Request Payload**:
    ```json
    {
      "areaCode": "39",
      "bizType": "REGISTER_MOBILE",
      "address": "<!-- 3522956432 -->",
      "sendType": "SMS",
      "templateParams": {
        "login_address": "",
        "sys_ip": "",
        "device": ""
      },
      "verifyKey": "hmac_CwgCEiA2REY2QkJFOTM3QUM2N0UyMTJEREJCQjEzQkNFNTgyNxoSc2VydmljZS1ncm91cC1kYXRhDBJbESS4PB5nJRYxpx8OKANhCZAiK8fnrra4Xjpk/vWd36JhMRTq8a4YjOg/o5nPiaH9Hg565LgOCKOx2NfXJlWq2XIrHJXfK5yOJ9JB+IaA97A4RLLCOfWU7zo/SA==",
      "retry": 1
    }
    ```
- **Response**:
    ```json
    {
      "code": "200",
      "data": {
        "countdown": 60,
        "expireTime": 10,
        "sent": true,
        "status": 1,
        "supportTypes": ["EMAIL", "SMS", "VOICE"],
        "verifyKey": "hmac_CwgCEiAyNEU2MUU0QzhCMDI3NUQyRjM4NzcwRjZEN0UxOUMzNxoSc2VydmljZS1ncm91cC1kYXRhDBJboFHbRDXshv36EP/73Co+s60UDDe2tgdD+EKvOxUCo7TNGmYhPIupcFp+hKdAlng4Bt0YKybwmy2X6Mr8eIWNl31nFVX2tu/3RyUWVLLFabtkhTKO5eHWq25pdQ=="
      }
    }
    ```

**Step 4: Submit SMS OTP (Pre-Check)**
- **Endpoint**: `POST https://appapi.abcdstable.com/v1/user/register/pre-check`
- **Purpose**: Verify the OTP code received by the user to proceed with account creation.
- **Notable Headers**:
    - `uhti`: a177741646451534623991922
    - `tm`: 1777416464028
- **Request Payload**:
    ```json
    {
      "account": "<!-- 3522956432 -->",
      "accountType": "mobile",
      "areaCode": "39",
      "verifyCode": "<!-- 362514 -->",
      "verifyCodeKey": "hmac_CwgCEiAyNEU2MUU0QzhCMDI3NUQyRjM4NzcwRjZEN0UxOUMzNxoSc2VydmljZS1ncm91cC1kYXRhDBJboFHbRDXshv36EP/73Co+s60UDDe2tgdD+EKvOxUCo7TNGmYhPIupcFp+hKdAlng4Bt0YKybwmy2X6Mr8eIWNl31nFVX2tu/3RyUWVLLFabtkhTKO5eHWq25pdQ=="
    }
    ```
- **Response (Invalid Code Case)**:
    ```json
    {
      "code": "20409",
      "flag": true,
      "group": "user",
      "msg": "Your mobile verification code is incorrect.",
      "requestTime": 1777416464945
    }
    ```

## 4. Security & Reversing Notes

### Encryption & Signing
- **x-sign Header**: A dynamic signature generated for each request. It likely incorporates the payload, timestamp, and a hardware-bound secret.
- **Session Tokens**: Use of `dy-token` and `verifyKey` (HMAC-based) ensures that requests cannot be replayed outside of the active session.

### Captcha Integration
- **Type**: Behavioral interaction challenge.
- **Implementation**: The challenge solution is encoded in the `captchaValidate` parameter. It requires high-fidelity interaction data to be accepted by the backend.

### Bot Detection & Protection
- **OpenRASP**: Server-side runtime protection is active, monitoring for suspicious API usage patterns and automated replay attacks.
- **Device Fingerprinting**: Hardware details (model, manufacturer) and unique identifiers (`deviceId`, `terminalCode`) are strictly validated.

## 5. Conclusion

### Automation Feasibility: 10%

### Critical Blockers:
1. **Proprietary Signing**: Bypassing the `x-sign` header requires deep reverse engineering of the native Android library.
2. **Behavioral Captcha**: Requires human interaction or advanced simulation of mouse/touch events.
3. **Session Binding**: Every step is strictly linked to a dynamic `verifyKey` and hardware fingerprint, preventing cross-device or cross-session replay.
4. **WAF/RASP Monitoring**: High-frequency or non-standard request patterns are immediately flagged and blocked by OpenRASP.
