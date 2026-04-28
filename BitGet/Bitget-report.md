# Bitget - Research Report

## Metadata
- **Target URL/App**: `com.bitget.exchange` (Bitget Crypto Exchange)
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29`
- **Status**: `Completed`
- **HAR Files**: `BitGet.har`

## 1. Executive Summary
Bitget implements a high-security authentication flow featuring mandatory captcha verification and encrypted request signing. The application utilizes a proxy-based API architecture under the `appapi.abcdstable.com` domain. The registration process requires a successful captcha validation (`check-login-name`) to obtain a `verifyKey`, which is then passed to the SMS trigger (`verifyCode/send`) and the final verification (`register/pre-check`) endpoints. Automation is highly difficult due to the mandatory behavioral captcha and the complex custom headers (`x-sign`, `dy-token`, `mini-wua`) required for every request.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | 6-digit OTP code |
| **Captcha** | Behavioral (Geetest-like) | Mandatory before SMS trigger |
| **Encryption** | Advanced | Encrypted request signing (`x-sign`) and proprietary headers |
| **Rate Limits** | Strict | Managed via `deviceId`, `terminalCode`, and session keys |
| **Endpoints Involved** | 4 | `get-captcha-id`, `check-login-name`, `verifyCode/send`, `register/pre-check` |
| **Bot Protection** | High | Custom Captcha + WAF (OpenRASP) + Request Signing |

## 3. Flow Details

### Flow 1: Registration Flow

**Step 1: Captcha Validation (check-login-name)**
- **Endpoint**: `POST https://appapi.abcdstable.com/v1/user/public/check-login-name`
- **Request Headers**:
    ```text
    User-Agent: Mozilla/5.0 (Linux; Android 15; Pixel 7 Build/AP4A.250205.002; wv) ...
    x-sign: EDGE-V1-1-6yuwcdZQzTXwhzLWIItQKnxuIIkJ9R0UhmiEeX3QjW0=
    deviceId: a177741635452379781998816
    Host: appapi.abcdstable.com
    ```
- **Request Body**:
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
- **Response Body**:
    ```json
    {
      "code": "200",
      "data": {
        "verifyKey": "hmac_CwgCEiA2REY2QkJFOTM3QUM2N0UyMTJEREJCQjEzQkNFNTgyNxoSc2VydmljZS1ncm91cC1kYXRhDBJb..."
      }
    }
    ```

**Step 2: Phone Number Submitting Endpoint (SMS Trigger)**
- **Endpoint**: `POST https://appapi.abcdstable.com/v1/msg/verifyCode/send`
- **Request Headers**:
    ```text
    User-Agent: Mozilla/5.0 (Linux; Android 15; Pixel 7 Build/AP4A.250205.002; wv) ...
    Content-Type: application/json; charset=utf-8
    ```
- **Request Body**:
    ```json
    {
      "areaCode": "39",
      "bizType": "REGISTER_MOBILE",
      "address": "<!-- 3522956432 -->",
      "sendType": "SMS",
      "verifyKey": "hmac_CwgCEiA2REY2QkJFOTM3QUM2N0UyMTJEREJCQjEzQkNFNTgyNxoSc2VydmljZS1ncm91cC1kYXRhDBJb...",
      "retry": 1
    }
    ```
- **Response Headers**:
    ```text
    X-Request-ID: de11404ff54a482fb0e90908edf7c24a
    X-Protected-By: OpenRASP
    ```
- **Response Body**:
    ```json
    {
      "code": "200",
      "data": {
        "countdown": 60,
        "expireTime": 10,
        "sent": true,
        "verifyKey": "hmac_CwgCEiAyNEU2MUU0QzhCMDI3NUQyRjM4NzcwRjZEN0UxOUMzNxoSc2VydmljZS1ncm91cC1kYXRhDBJb..."
      }
    }
    ```

**Step 3: Submit SMS OTP (Verification)**
- **Endpoint**: `POST https://appapi.abcdstable.com/v1/user/register/pre-check`
- **Request Headers**:
    ```text
    dy-token: 69f138a5jmjDCgPVEn1BtnCHWiBhgPvgtalyWMI3
    tm: 1777416464028
    ```
- **Request Body**:
    ```json
    {
      "account": "<!-- 3522956432 -->",
      "accountType": "mobile",
      "areaCode": "39",
      "verifyCode": "<!-- 362514 -->",
      "verifyCodeKey": "hmac_CwgCEiA2REY2QkJFOTM3QUM2N0UyMTJEREJCQjEzQkNFNTgyNxoSc2VydmljZS1ncm91cC1kYXRhDBJb..."
    }
    ```
- **Response Body (Invalid Case)**:
    ```json
    {
      "code": "20409",
      "flag": true,
      "msg": "Your mobile verification code is incorrect."
    }
    ```

## 4. Security & Reversing Notes

### Encrypted Request Signing (`x-sign`)
- Every critical request is signed with an `x-sign` header. This signature is generated using the request parameters and a secret key stored in the native library.
- The `dy-token` and `uhti` headers provide additional layers of session-based verification.

### Behavioral Captcha (Geetest)
- The app integrates a behavioral captcha that must be solved before an SMS can be triggered. The `captchaValidate` token is mandatory for the `check-login-name` endpoint.

### OpenRASP & WAF
- The presence of the `X-Protected-By: OpenRASP` header indicates server-side runtime protection, which actively monitors for malicious patterns and automated abuse.

## 5. Conclusion
Bitget employs a top-tier security stack that makes automated registration extremely difficult. The combination of mandatory behavioral captchas, complex request signing, and server-side RASP protection effectively blocks most automated tools. Bypassing these defenses would require sophisticated reverse engineering of the native signing logic and high-fidelity browser/device orchestration to satisfy the behavioral verification requirements.
