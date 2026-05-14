# ViYa Lite - Research Report

## Metadata
- **Target URL/App**: `com.kinkey.vgolite`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-07`
- **Status**: `Completed`
- **HAR Files**: `ViyaLite.har`

## 1. Executive Summary
ViYa Lite implements a standard OTP-based authentication flow with integrated bot protection via Alibaba Bot Manager (AWSC). The application utilizes sophisticated device fingerprinting and behavioral telemetry collection, including mouse movements and system signals, which are transmitted as base64-encoded payloads. The SMS request process is gated by a captcha challenge, and the authentication state is managed through custom session headers. Automation feasibility is medium-low due to the requirement of valid captcha tickets and complex telemetry data.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for account authentication |
| **Captcha** | Alibaba Slide CAPTCHA | Utilizes Alibaba Bot Manager (AWSC) with a silent fallback mechanism |
| **Encryption** | Base64 Telemetry | Telemetry data (cola, mouse, signal) is base64 encoded |
| **Rate Limits** | Unknown | No explicit rate limiting behavior was observed during capture |
| **Endpoints Involved** | 5 | `/auth/account/checkAccount`, `/auth/security/getWebToken`, `/auth/account/getAuthSms`, `/auth/account/login` |
| **Bot Protection** | Alibaba Bot Manager | Integration with `g.alicdn.com/AWSC/AWSC/awsc.js` |

## 3. Flow Details

### Flow 1: SMS Authentication

**Step 1: Account Check**
- **Endpoint**: `POST https://api.salamyo.com/auth/account/checkAccount`
- **Purpose**: Verifies the account status and initializes the login flow.
- **Request**:
    ```json
    {
      "request": {
        "mobile": "+393519139022" <!-- Phone Number -->
      },
      "requestId": "187056824",
      "userEnv": {
        "appBuild": 453,
        "appId": "com.kinkey.vgolite",
        "appVersion": "1.2.6",
        "deviceId": "116158d944b4fe395afe34ee12a569a0764a436a"
      }
    }
    ```
- **Response**:
    ```json
    {
      "code": 0,
      "status": "Success",
      "result": {
        "isRegister": true
      },
      "success": true
    }
    ```

**Step 2: Get Captcha Settings**
- **Endpoint**: `POST https://web.kinkey.tech/h5-api/auth/account/getCaptchaSetting`
- **Purpose**: Determines which captcha provider to use.
- **Request**:
    ```json
    {
      "request": {
        "mobile": "+393519139022"
      }
    }
    ```
- **Response**:
    ```json
    {
      "code": 0,
      "status": "Success",
      "result": {
        "provider": "fallback",
        "captchaTicket": "9a2a0969-b1f3-4972-9352-532d7bf35fa2"
      },
      "success": true
    }
    ```

**Step 3: Request SMS OTP (Phone Submitting Endpoint)**
- **Endpoint**: `POST https://api.salamyo.com/auth/account/getAuthSms`
- **Purpose**: Triggers the delivery of a verification code to the user's mobile device.
- **Request**:
    ```json
    {
      "request": {
        "captchaTicket": "{\"captchaValue\":\"9a2a0969-b1f3-4972-9352-532d7bf35fa2\",\"captchaType\":\"fallback\"}",
        "mobile": "+393519139022" <!-- Phone Number -->
      },
      "requestId": "187056826",
      "userEnv": {
        "cola": "h8bJs/Uc1aFS8fCV...",
        "mouse": "wBJHgKGxCngZrLC2...",
        "signal": "{\"uuId\":\"W0O02byR...\"}"
      }
    }
    ```
- **Response**:
    ```json
    {
      "result": null,
      "code": 10020,
      "success": false,
      "status": "BusinessException"
    }
    ```
    *Note: The response indicates a business exception, likely due to environment validation or session expiration during capture.*

**Step 4: Submit OTP for Login**
- **Endpoint**: `POST https://api.salamyo.com/auth/account/login`
- **Purpose**: Authenticates the user using the received SMS code.
- **Request**:
    ```json
    {
      "request": {
        "authType": 2,
        "mobile": "+393519139022", <!-- Phone Number -->
        "smsCode": "362598" <!-- OTP Code -->
      },
      "requestId": "187056827",
      "userEnv": {
        "deviceId": "116158d944b4fe395afe34ee12a569a0764a436a",
        "mouse": "wBJHgKGxCngZrLC2...",
        "signal": "{\"uuId\":\"iZkM5xWZI...\"}"
      }
    }
    ```
- **Response**:
    ```json
    {
      "code": 20002,
      "status": "BusinessException",
      "message": "手机验证码校验失败",
      "success": false
    }
    ```
    *Note: "手机验证码校验失败" translates to "Mobile verification code validation failed".*

## 4. Security & Reversing Notes

### Telemetry and Fingerprinting
The application collects three main types of telemetry data in the `userEnv` object:
1. **`cola`**: Application-level state or encrypted constants.
2. **`mouse`**: Behavioral data, likely recording touch/mouse coordinates and timing.
3. **`signal`**: System-level signals, device identifiers, and environmental checks (e.g., `uuId`, `param`).

These fields are essential for passing the server-side bot protection checks.

### Captcha Integration
ViYa Lite uses a dual-layered captcha approach. It first checks for a `provider` (in this case, `fallback`). It also loads Alibaba's `awsc.js`, indicating that it can trigger more advanced challenges if the initial risk assessment fails.

## 5. Conclusion

### Automation Feasibility: Low (35%)
The automation of the ViYa Lite authentication flow is hindered by the mandatory inclusion of valid captcha tickets and complex behavioral telemetry. Generating the `mouse` and `signal` payloads requires either reverse-engineering the underlying encryption/obfuscation logic or using a headless browser environment to satisfy the Alibaba Bot Manager.

### Summary
The platform demonstrates a high level of awareness regarding automated attacks by implementing:
- Behavioral telemetry collection.
- Context-aware captcha challenges.
- Encrypted/Obfuscated device environments.
- Structured request signatures (inferred from `requestId` and `userEnv`).

Recommendations for further research include decrypting the `userEnv` payloads to understand the specific device checks being performed.
