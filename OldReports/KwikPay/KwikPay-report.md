# KwikPay - Research Report

## Metadata
- **Target URL/App**: `com.kwikpay.transfers`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-03`
- **Status**: `Completed`
- **HAR Files**: `KwikPay.har`

## 1. Executive Summary
KwikPay (com.kwikpay.transfers) implements a secure mobile authentication flow primarily utilizing SMS OTP for user verification. The security architecture is characterized by a multi-step initialization process involving server time synchronization, dynamic signing key acquisition, and bot protection via Yandex SmartCaptcha. Each critical request is protected by a custom cryptographic signature (`X-Signature`) and a non-standard timestamp header (`X-Signature-Date`). While the core API logic is straightforward, the integration of Yandex SmartCaptcha and the proprietary signing mechanism provides a significant barrier to simple automation.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for OTP |
| **Captcha** | Yandex SmartCaptcha Invisible | Used to protect the user registration/login endpoint |
| **Encryption** | Custom Request Signing | `X-Signature` header (SHA-256) based on server-provided keys |
| **Rate Limits** | 180s Cooldown | Enforced via `repeat_delay` in the API response |
| **Endpoints Involved** | 4 | `time/now`, `sign`, `v4/users`, `v2/users/confirmation` |
| **Bot Protection** | Yandex SmartCaptcha | Implemented on the phone submission step |

## 3. Flow Details

### Flow 1: User Authentication (Login/Signup)

**Step 1: Get Server Time**
- **Endpoint**: `GET /ru/api/v1/time/now`
- **Host**: `mob.kwikpay.ru`
- **Purpose**: Synchronize client time with server for signature validation.
- **Request Headers**:
    ```text
    X-App-Version: 3.31.0
    X-App-Platform: android
    User-Agent: okhttp/4.12.0
    Host: mob.kwikpay.ru
    ```
- **Response**:
    ```json
    {
        "time_now": "2026-05-03T11:06:24.079Z"
    }
    ```

**Step 2: Get Signing Key**
- **Endpoint**: `POST /ru/api/v1/sign`
- **Host**: `mob.kwikpay.ru`
- **Purpose**: Retrieve a dynamic key used for signing subsequent requests.
- **Request Headers**:
    ```text
    Content-Type: application/json; charset=UTF-8
    X-App-Version: 3.31.0
    X-App-Platform: android
    User-Agent: okhttp/4.12.0
    Host: mob.kwikpay.ru
    ```
- **Request Payload**:
    ```json
    {"platform":"android"}
    ```
- **Response**:
    ```json
    {
        "key": "b2833e0ce5bdf7212db32ffa9128cfaf855fcb01c0c9f"
    }
    ```

**Step 3: Solve Captcha**
- **Service**: Yandex SmartCaptcha
- **Sitekey**: `ysc1_yWzxdchOyjCdAJSUIhxb2ks63oUF1trfIMorSM1ae17ea48a`
- **Purpose**: Obtain `ycaptcha_token` required for phone number submission.
- **Note**: The app opens a webview to `https://mob.kwikpay.ru/captcha.html` to handle the challenge.

**Step 4: Phone Number Submission (Send OTP)**
- **Endpoint**: `POST /ru/api/v4/users`
- **Host**: `mob.kwikpay.ru`
- **Purpose**: Submit phone number and trigger SMS OTP sending.
- **Request Headers**:
    ```text
    X-Signature: 6cda5ce124ddead0f68c8a155fd6cf29ec743fb1e51d84c9dcfadde829f43d6a
    X-Signature-Date: Sun, 03 M05 2026 11:06:24 UTC
    X-App-Version: 3.31.0
    X-App-Platform: android
    Content-Type: application/json; charset=UTF-8
    User-Agent: okhttp/4.12.0
    Host: mob.kwikpay.ru
    ```
- **Request Payload**:
    ```json
    {
        "ad_agreement": true,
        "ycaptcha_token": "dD0xNzc3ODA2Mzg1O2k9MTUyLjU4Ljk3LjEzMTtEPTdEQTM5RTA3NkQ5MjA1NTQ4ODhFMzQ1NzVDNEIyNDc5QTgwNTQxQTc1ODY4NzNBNDkyOTFBM0Q4MTFBQUU5RkJENjVFREVDNzI0NTU3OUI0NEFCRTFGOTAwMzZCOUVGMjI1NTE0QTgyMkY4NjVFNUY5MUQ1MUUyQjY0RjY0QkZBM0Q3OEEyODg2MDNERDgwM0U0NDdDQTkwQjk2MTk3O3U9MTc3NzgwNjM4NTY1NzE1MzY1MTtoPWQ5MTUwMTAwY2M5MDFkNjQ5ZjViYzAxNzFlMTQ4OWI4",
        "phone_country_id": 183,
        "identifier": "dec0abec951ac104",
        "language": "ru",
        "phone": "393513460066",
        "platform": "android",
        "time_zone": "Asia/Kolkata"
    }
    ```
- **Response**:
    ```json
    {
        "auth_type": "sms",
        "repeat_delay": 180
    }
    ```

**Step 5: Verify OTP**
- **Endpoint**: `POST /ru/api/v2/users/confirmation`
- **Host**: `mob.kwikpay.ru`
- **Purpose**: Verify the SMS code received by the user.
- **Request Headers**:
    ```text
    X-App-Version: 3.31.0
    X-App-Platform: android
    Content-Type: application/json; charset=UTF-8
    User-Agent: okhttp/4.12.0
    Host: mob.kwikpay.ru
    ```
- **Request Payload**:
    ```json
    {
        "appmetrica_device_id": "8254840089096201012",
        "fcm_token": "fIjDbGllQPSHhz7WMGDNO5:APA91bGVKjYJy-6EtLWRuXLthLD-wmEBaS85sUxbbapdqsc1Xo6I4e2Ruyhg1_xKwQ5dyvu1-0qAc4s74cNPkQMICs9MoclYY3TeUv3x7Ud2w1MVlHAxkow",
        "identifier": "dec0abec951ac104",
        "idfa": "f51ee336-e489-4882-8c21-95ff06ed4a9a",
        "phone": "393513460066",
        "platform": "android",
        "sms_code": "3333"
    }
    ```
- **Response**:
    ```json
    {
        "error": "invalid_code",
        "message": "Неверный код"
    }
    ```
- **Analysis**: The response indicates a failed verification due to an incorrect code. A successful verification would return session tokens.

## 4. Security & Reversing Notes

### Encryption/Signing Mechanisms

**1. Request Signing (X-Signature)**
- **Header**: `X-Signature`
- **Algorithm**: SHA-256 (64 hex characters)
- **Dependencies**: Uses a dynamic key from `/api/v1/sign` and a specific timestamp format in `X-Signature-Date`.
- **Date Format**: `Day, DD Mmm YYYY HH:MM:SS UTC` (Note: `M05` was observed in the HAR for May).

**2. Bot Protection (Yandex SmartCaptcha)**
- **Provider**: Yandex Cloud
- **Implementation**: The `ycaptcha_token` is required for the registration endpoint. This token is obtained after the user completes the SmartCaptcha challenge in a webview.

**3. Device Fingerprinting**
- The app sends multiple device identifiers:
    - `identifier`: Likely a hardware-bound ID (e.g., Android ID).
    - `appmetrica_device_id`: Analytics-related identifier.
    - `idfa`: Advertising identifier.

### Bot Detection
- KwikPay relies on Yandex SmartCaptcha for behavioral analysis and bot detection. The use of a signing mechanism also prevents simple replay attacks and unauthorized API access from non-app clients.

## 5. Conclusion

### Automation Feasibility: 55% (Medium)

### Critical Blockers:
1. **Yandex SmartCaptcha**: Automated solving of SmartCaptcha requires either advanced OCR/AI or third-party solving services.
2. **Proprietary Signing**: The `X-Signature` logic needs to be fully reverse-engineered to determine the exact payload and key combination used for the HMAC/Hash.
3. **Non-standard Headers**: Handling the unique `X-Signature-Date` format is essential for server-side acceptance.
4. **Device Consistency**: Multiple identifiers must remain consistent to avoid being flagged as suspicious.
