# JoyBuy - Research Report

## Metadata
- **Target URL/App**: `com.joybuy.jdi`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-03`
- **Status**: `Completed`
- **HAR Files**: `JoyBuy.har`

## 1. Executive Summary
JoyBuy (com.joybuy.jdi) implements a comprehensive security framework for its authentication flows, leveraging JD.com's core security infrastructure. The application utilizes multi-step verification including account existence checks, custom captcha challenges, and OTP-based login/registration. Key security measures include payload encryption for sensitive data (phone numbers), device fingerprinting (jnos-product-code, mtaUuid, x-api-device-token), and request signing (`sign` parameter). Automation feasibility is Medium-Low due to the presence of custom slider captchas and encrypted identifiers that require reversing the encryption logic.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for OTP delivery |
| **Captcha** | Xiaomi CAPTCHA / Slider | Custom slider captcha implemented via `user_account_getCaptchaSessionId` |
| **Encryption** | AES/Custom | Encrypted `identifier` and `mobile` fields; request signing via `sign` parameter |
| **Rate Limits** | Unknown | No explicit rate limiting observed in the single flow captured |
| **Endpoints Involved** | 4 | `verifyAccount`, `getCaptchaSessionId`, `sendVerifyCode`, `loginByVerifyCode` |
| **Bot Protection** | Custom JD Security | Implements proprietary JD.com anti-fraud measures and captcha |

## 3. Flow Details

### Flow 1: Registration / Login by OTP

**Step 1: Verify Account**
- **Endpoint**: `POST https://color-api.joybuy.com/?appid=joybuyAPP&functionId=user_account_verifyAccount`
- **Purpose**: Checks if the account exists and determines the next action (e.g., `mobile_code_register`).
- **Notable Headers**:
    - `X-Referer-Package`: `com.joybuy.jdi`
    - `x-api-device-token`: `926eb180f3b6393f`
- **Request Payload**:
    ```json
    {
        "personalized": true,
        "verticalTag": "cn_ybxt_b2c",
        "businessTag": "cn_ybxt_b2c",
        "pickUpSiteId": "20000068",
        "userActionId": "user_account_verifyAccount"
    }
    ```
- **Response**:
    ```json
    {
        "success": true,
        "result": true,
        "code": "200",
        "data": {
            "exist": false,
            "wl": false,
            "riskType": 2,
            "action": "mobile_code_register",
            "stepCode": "2f77606c83a94452b707929468b73aed"
        }
    }
    ```

**Step 2: Get Captcha Session**
- **Endpoint**: `POST https://color-api.joybuy.com/?appid=joybuyAPP&functionId=user_account_getCaptchaSessionId`
- **Purpose**: Retrieves a session ID for captcha challenge.
- **Request Payload**:
    ```json
    {
        "sessionSource": "reg",
        "riskType": 2,
        "mobile": "dbfRzlGfFW3%2F4wEuAIb7pfKnYH7lBElZZyImnxS2LA6r7ikVM%252BZyVq72208aXVOJkJ6UBQ3ZXFbL4xylRgfa8pibucGbxlYG6xdYxqJsgNI6%252FK%252BpgJ7YoFzR6IqdXIxsSGrcZ74RO3pDLYK6kFJQh%252BbY8gwxfKliNNSZbsMCwEI%253D", <!-- Phone Number (Encrypted) -->
        "mobilePrefix": "+39" <!-- Phone Prefix -->
    }
    ```
- **Response**:
    ```json
    {
        "success": true,
        "result": true,
        "code": "200",
        "data": {
            "sessionId": "RR8kggABAAADMKWdUD4AMM7ap0OlGSDTQcIuS5c7kER5Siy25H-s91cp8kXqnV91Hx4tbUL30CirrMBkpwoGagAA"
        }
    }
    ```

**Step 3: Send OTP**
- **Endpoint**: `POST https://color-api.joybuy.com/?appid=joybuyAPP&functionId=user_account_sendVerifyCode`
- **Purpose**: Triggers the SMS OTP sending process after captcha verification.
- **Request Payload**:
    ```json
    {
        "appId": "80001",
        "riskType": 2,
        "idPrefix": "+39", <!-- Phone Prefix -->
        "identifier": "cZSuctPX0ZIp%2BLQvIBG3NQp%2BjVV4PiUf38jBpoMFiPK6wQkXsTZSeGhOvWqKAAh4rQb1lpGbSkxK4DVs9CN9hC7ZBCZL9j41llJodoTno3ptMAqljJWWlCzPRV1rjxTMt9DFVPBluRnyGHu2Qs8Qrtn0vtmyzsVg16m9bv3Mtws%253D", <!-- Phone Number (Encrypted) -->
        "otpType": "2",
        "scene": "2",
        "sessionId": "RR8kggABAAADMKWdUD4AMM7ap0OlGSDTQcIuS5c7kER5Siy25H-s91cp8kXqnV91Hx4tbUL30CirrMBkpwoGagAA",
        "captchaAction": "signup",
        "captchaCode": "SGA9GwABAAABne1WM_4AgPgwuPhz7N08BPlffBv48LO7K-McoRfAHNAH4pJeFVyghZCRmzuv5HiFBzxu6l7fD4KhNE8D9MLd-k0iTHus8mHXw6g37q4CSIDOtXWu-Z5Elz8ZLAwbus4hGK5Bl7boqEWNy5q1D6hRdqybdmUgy0irYCoFQx6_RAM_ZunQBfgJ",
        "countryCode": "GB",
        "siteCode": "UK-Site"
    }
    ```
- **Response**:
    ```json
    {
        "success": true,
        "result": true,
        "code": "200",
        "data": "8ae89d0a0fb84ee587f2095f8209c24c"
    }
    ```
- **Analysis**: The `data` field in the response contains a `stepCode` (or similar token) required for the verification step.

**Step 4: Verify OTP**
- **Endpoint**: `POST https://color-api.joybuy.com/?appid=joybuyAPP&functionId=user_account_loginByVerifyCode`
- **Purpose**: Submits the OTP code received via SMS to complete login/registration.
- **Request Payload**:
    ```json
    {
        "idPrefix": "+39", <!-- Phone Prefix -->
        "identifier": "D15OC18cPN%2FQr04WVzviRNsM%2FZ3LMLMY0vXk991Xc9ToTXFL9zS42Ll7qRsxyhfvY%2F87jfyB012gF5Z5fkeiYXp5kBRyxnxf5kJ2M81FWqfOgAR3UoCuVOFLNroPqZT%2FUHY%2FMHpwowFl%2FV2QBavl%2FXwWyA6VayACDICw39gftXg%3D", <!-- Phone Number (Encrypted) -->
        "otpType": "2",
        "scene": "2",
        "verifyCode": "142536", <!-- OTP Code -->
        "stepCode": "8ae89d0a0fb84ee587f2095f8209c24c"
    }
    ```
- **Response**:
    ```json
    {
        "success": false,
        "result": false,
        "code": "10773",
        "msg": "The verification code you entered is incorrect. Please try again."
    }
    ```
- **Analysis**: The `verifyCode` is the 6-digit OTP. The `stepCode` links this request to the previous SMS request.

## 4. Security & Reversing Notes

### Encryption & Signing
1. **Identifier Encryption**: The `identifier` and `mobile` fields are encrypted before being sent. This likely uses a symmetric encryption algorithm (like AES) with a key derived from the device fingerprint or hardcoded in the app.
2. **Request Signing**: Most requests include a `sign` parameter in the query string. This is a cryptographic hash of the request parameters and body, ensuring data integrity and preventing tampering.
3. **Device Tokens**: Headers like `x-api-device-token` and `uuid` are used to bind the session to a specific device.

### Captcha Integration
The flow includes a `user_account_getCaptchaSessionId` call followed by providing a `captchaCode` in the `sendVerifyCode` request. This indicates a slider or challenge-based captcha that must be solved to obtain the `captchaCode`.

## 5. Conclusion

### Automation Feasibility: 35%

### Detailed Conclusion:
Automation of the JoyBuy authentication flow is moderately difficult. The primary hurdles are:
1. **Payload Encryption**: The phone number (`identifier`) is encrypted, requiring the reverse engineering of the encryption logic from the Android APK.
2. **Captcha Challenge**: The requirement for a `captchaCode` in the SMS request means a slider captcha must be solved or bypassed.
3. **Request Signing**: The `sign` parameter must be correctly calculated for each request, which involves understanding the signing algorithm and secret keys used by the JD.com infrastructure.
4. **Device Fingerprinting**: The server validates various device-related headers and tokens, making it necessary to mimic a legitimate device environment.

However, the API structure is relatively standard for the JD.com ecosystem, and once the encryption/signing logic is cracked, automation becomes more feasible.
