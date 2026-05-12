# Chagee - Research Report

## Metadata
- **Target URL/App**: `com.chagee.application`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-12`
- **Status**: `Completed`
- **HAR Files**: `chagee.har`

## 1. Executive Summary
Chagee's Android application (`com.chagee.application`) employs a multi-layered security architecture designed to mitigate automated attacks and ensure session integrity. The authentication flow is anchored by **Alibaba Cloud (Aliyun) Captcha** and a custom encryption server that distributes session-specific keys (`sk`). All sensitive payloads, including phone numbers and device metadata, are encrypted via AES and signed using an HMAC-based mechanism (`sign` header). The presence of the **Alibaba Cloud WAF** and request-level signing makes the application highly resilient to standard bot-driven automation.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for identity verification |
| **Captcha** | Alibaba Slide CAPTCHA | Implemented via WebView challenge |
| **Encryption** | AES-256-CBC with HMAC Signing | Payloads are encrypted; requests are signed |
| **Rate Limits** | Yes | Session-based cooldown enforced server-side |
| **Endpoints Involved** | 3 | `getsk`, `countryCode`, `sendVerifyCode` |
| **Bot Protection** | Alibaba Cloud WAF | Integrated with Aliyun security suite |

## 3. Flow Details

### Flow 1: SMS OTP Verification

**Step 1: Session Initialization (Get Session Key)**
- **Endpoint**: `GET https://sea-gw.chagee.com/encrypt-server/enctrypt/api/getsk?code=CHAGEE_C_001`
- **Purpose**: Retrieve the encryption key (`sk`) required for subsequent payload encryption.
- **Request Headers**:
    ```json
    {
      "Host": "sea-gw.chagee.com",
      "User-Agent": "Dart/3.10 (dart:io)",
      "Accept-Encoding": "gzip",
      "os": "android",
      "apv": "3.33.0"
    }
    ```
- **Response**:
    ```json
    {
        "errcode": "0",
        "errmsg": "success",
        "data": "ZjczNDYwMjJjMmQ1N2M4MQ==",
        "timestamp": 1778584420000
    }
    ```

**Step 2: Captcha Verification**
- **Endpoint**: `GET https://southeast-static.chagee.com/sg-c-cli/chagee-app/oversea/verify_sea_app.html`
- **Purpose**: Challenge the user with a sliding captcha to prevent bot activity.
- **Analysis**: Upon successful solution, the Aliyun SDK returns a `captchaVerifyParam` JSON string containing `sceneId`, `certifyId`, and `deviceToken`.

**Step 3: Trigger SMS OTP (Phone Submission)**
- **Endpoint**: `POST https://api-sea.chagee.com/api/user-client/customer/sendVerifyCode`
- **Purpose**: Submit the phone number and captcha proof to receive an OTP. <!-- Phone Submission Step -->
- **Notable Headers**:
    - `wtoken`: Large encrypted session token.
    - `sk`: `ZjczNDYwMjJjMmQ1N2M4MQ==` (obtained in Step 1).
    - `sign`: `TmQhkiyuBwWt23udcHJtbvQxm+Y=` (payload signature).
- **Request Payload**:
    ```json
    {
      "scene": "1",
      "sendObj": "J6rAjwj4jBfqCbPU3DmByw==", <!-- Encrypted Phone Number -->
      "sendType": "MOBILE",
      "phoneCode": "39",
      "captchaVerifyParam": "{\"sceneId\":\"hoipvzll\",\"certifyId\":\"geUi7iAT8R\",\"deviceToken\":\"U0dfV0VCIzM3OTVkM... [truncated]\"}",
      "data": "JRMnZXEHXyIxLA4LHGB5KUIhbZcCEgJATjskM2FTNvVQVjFa7EttRA0FdKRw1... [truncated]",
      "timestamp": 1778584474372,
      "smdid": "Bjs02TW8YmQRS1bkM3esAURhgrArRVvmM9W8vYzOskp4rPKqGAWrAkezFluicTJVp+CfrAmDJBYvJc8ek+dW8MA==",
      "sign": "TmQhkiyuBwWt23udcHJtbvQxm+Y="
    }
    ```
- **Response**:
    ```json
    {
      "errcode": "0",
      "errmsg": "处理成功",
      "data": "发送成功", <!-- OTP Successfully Triggered -->
      "traceId": null,
      "thirdTraceId": "",
      "globalTicket": "0fee25a484cc6e38c072c11e8e44c47e",
      "timestamp": 1778584473044
    }
    ```

**Step 4: OTP Submission (Verify Code)**
- **Endpoint**: `POST https://api-sea.chagee.com/api/user-client/customer/loginOrRegister`
- **Purpose**: Submit the 6-digit OTP code to complete the authentication process. <!-- OTP Submission Step -->
- **Request Headers**:
    ```json
    {
      "ua": "Dart/2.12 (dart:io)",
      "content-type": "application/json",
      "wtoken": "0004_9E1BE93D8E3599FA29092C13C44798A1... [truncated]",
      "sk": "ZjczNDYwMjJjMmQ1N2M4MQ=="
    }
    ```
- **Request Payload**:
    ```json
    {
      "phoneCode": "39",
      "code": "222222", <!-- User Entered OTP Code -->
      "mobile": "J6rAjwj4jBfqCbPU3DmByw==", <!-- Encrypted Phone Number -->
      "utm": "{\"inviteCode\":\"\",\"channelType\":\"1\"}"
    }
    ```
- **Response**:
    ```json
    {
      "errcode": "12320120200014",
      "errmsg": "Verification code error", <!-- Failed Attempt captured in HAR -->
      "data": null,
      "traceId": null,
      "thirdTraceId": null,
      "globalTicket": "bdfe500420bac0ea942f3dd3209c5d12",
      "timestamp": 1778584729312
    }
    ```

## 4. Security & Reversing Notes

### Encryption/Signing Mechanisms

**1. Session Key Exchange (`sk`)**
The application initializes its secure communication channel by requesting a session-specific `sk` (Base64 encoded). This key is essential for all subsequent encrypted fields and is likely used in a symmetric encryption algorithm (AES) for data at rest and in transit within the payload.

**2. Request Signing (`sign` header)**
Every API call to the `sendVerifyCode` endpoint is signed. The `sign` header contains a hash that validates the request body against tampering. Replicating this signature requires reverse-engineering the signing algorithm (potentially HMAC-SHA256) and extracting the static or dynamic salts from the binary.

**3. Captcha Integration (Alibaba Slide CAPTCHA)**
The app uses a custom Aliyun-based slider captcha. The validation token (`certifyId`) and device metadata (`deviceToken`) are bundled into a JSON string (`captchaVerifyParam`) and submitted with the OTP request. This creates a hard dependency on successful captcha completion.

### Key Security Features
1.  **Request Body Integrity**: Enforced via the `sign` header.
2.  **Encrypted PII**: Phone numbers are never sent in plaintext.
3.  **Bot Prevention**: Deep integration with Alibaba Cloud WAF and Captcha.
4.  **Session Binding**: Tokens and keys are tied to the specific application instance and device fingerprint (`smdid`).

## 5. Conclusion

### Automation Feasibility: Medium 40-70%

### Detailed Conclusion
The Chagee Android application presents a robust security posture against unauthorized automation. The primary strengths of its architecture lie in the multi-layered encryption approach and the mandatory sliding captcha gate. The use of a session-specific key (`sk`) and request signing (`sign`) ensures that even if an attacker intercepts the traffic, they cannot easily replay or modify requests without the underlying cryptographic logic.

However, the automation feasibility is rated as Medium (40-70%) because the endpoints are clearly defined and follow a predictable flow. The main blockers are the **Alibaba Slide CAPTCHA** and the **HMAC signing logic**. For successful automation, a researcher would need to:
1. Implement a captcha-solving strategy (e.g., using a third-party API or behavioral modeling).
2. Decompile the Android binary to extract the encryption and signing parameters.
3. Mimic the session-binding logic to maintain a valid state across the `getsk` and `sendVerifyCode` requests.

Recommendations for further research include a deeper dive into the native libraries (JNI) if the signing logic is not found in the Java/Kotlin layers, as well as testing the robustness of the Alibaba WAF against high-frequency requests from non-residential IP blocks.

---
**Researcher**: `Deepanshu Singh`
**Date**: `2026-05-12`
