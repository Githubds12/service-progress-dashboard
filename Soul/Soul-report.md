# Soul - Research Report

## Metadata
- **Target URL/App**: `com.soul.android.international`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-08`
- **Status**: `Completed`
- **HAR Files**: `Soul.har`

## 1. Executive Summary
Soul (com.soul.android.international) is a social networking platform that implements standard security measures for its authentication flow. The application utilizes a custom request signing mechanism (`api-sign` version `v7`), request nonces, and device fingerprinting (`device-id`, `sdi`) to secure its API communications. The registration flow primarily relies on SMS-based OTP verification. During testing, the platform returned messages suggesting a preference for email-based registration in certain regions or under specific conditions. No advanced bot protection like Captcha was observed in the captured traffic, though the robust signing and device tracking provide a layer of anti-automation.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for account registration |
| **Captcha** | undefined | No captcha challenges were observed in the captured flow |
| **Encryption** | Custom Signing | Requests are secured with `api-sign` (v7), `cs` checksum, and nonces |
| **Rate Limits** | Unknown | No explicit rate limiting (HTTP 429) was observed in the traces |
| **Endpoints Involved** | 3 | `/account/validate/register`, `/account/smsCode/deliver`, `/account/smsCode/validate` |
| **Bot Protection** | Request Signing | Anti-tampering and device binding via headers |

## 3. Flow Details

### Flow 1: Registration / Login

**Step 1: Validate Registration**
- **Endpoint**: `POST https://api-global.soulapp.me/account/validate/register`
- **Purpose**: Initial check for registration feasibility.
- **Request Headers**:
    ```json
    {
      "api-sign": "CBC460B97B885B28EA4275121245D20C1C82463C",
      "os": "android",
      "api-sign-version": "v7",
      "device-id": "UGl4ZWwgNzdEW3WeeVn2BQ__a4997475a26662c643ac76acd3544177",
      "request-nonce": "7cf8b5fff34e4a39913c6663e40e0baa",
      "app-id": "20000010",
      "app-version": "2.73.1",
      "Content-Type": "application/x-www-form-urlencoded"
    }
    ```
- **Request Body**:
    ```
    <!-- Phone: 3720517396 -->
    (Binary or URL encoded parameters)
    ```
- **Response**:
    ```json
    {
      "code": 10005,
      "message": "Please use email or other methods to sign up.",
      "data": null
    }
    ```

**Step 2: Request SMS OTP**
- **Endpoint**: `POST https://api-global.soulapp.me/account/smsCode/deliver`
- **Purpose**: Trigger SMS delivery to the user's mobile number.
- **Request Headers**:
    ```json
    {
      "api-sign": "54DD6C74D5CF5520EF07126A417A4113CD9BC673",
      "os": "android",
      "api-sign-version": "v7",
      "device-id": "UGl4ZWwgNzdEW3WeeVn2BQ__a4997475a26662c643ac76acd3544177",
      "request-nonce": "0a4bb194ceb34fdfb37f61f963a6a335",
      "app-id": "20000010",
      "app-version": "2.73.1",
      "app-time": "1778212134046",
      "cs": "028fc0d9792de056006f00579414175300ac"
    }
    ```
- **Request Body**:
    ```
    area=39&phone=3720517396&type=REGISTER
    <!-- Phone: 3720517396 -->
    ```
- **Response**:
    ```json
    {
      "code": 10001,
      "message": "success",
      "data": null
    }
    ```

**Step 3: Validate SMS OTP**
- **Endpoint**: `POST https://api-global.soulapp.me/account/smsCode/validate`
- **Purpose**: Verify the OTP received by the user.
- **Request Headers**:
    ```json
    {
      "api-sign": "C10ED7A685E3E0F3DF7917CB62349A3E440B5DF3",
      "os": "android",
      "api-sign-version": "v7",
      "device-id": "UGl4ZWwgNzdEW3WeeVn2BQ__a4997475a26662c643ac76acd3544177",
      "request-nonce": "8d336bfb9d7d404198432d9c85fe6af3",
      "app-id": "20000010"
    }
    ```
- **Request Body (from URL query string)**:
    ```
    area=39&bi=[...]&bik=32755&code=2555&phone=3720517396&type=REGISTER
    <!-- Phone: 3720517396, OTP: 2555 -->
    ```
- **Response**:
    ```json
    {
      "code": 10002,
      "message": "Invalid code. Please try again.",
      "data": null
    }
    ```

## 4. Security & Reversing Notes

### Encryption/Signing Mechanisms

**1. API Signature (api-sign)**
- The application uses a complex signing algorithm (`v7`) that likely incorporates request parameters, timestamp (`app-time`), and a secret key to prevent request tampering.

**2. Device Tracking**
- `device-id` and `sdi` headers are used to bind requests to a specific hardware instance, making it difficult to rotate devices during automated attacks.

**3. Request Integrity**
- `request-nonce` ensures that every request is unique and prevents replay attacks.
- `cs` header likely serves as an additional checksum for data integrity.

### Bot Detection
- Soul implements server-side logic to redirect registration attempts towards email verification (`code 10005`), which might be triggered by suspicious IPs or certain regional constraints.

## 5. Conclusion

### Automation Feasibility: Low < 40%

### Detailed Conclusion:
The automation feasibility for Soul is rated as Low. While no traditional CAPTCHA was encountered, the proprietary `api-sign` (v7) mechanism presents a significant hurdle. Reversing this algorithm would require deep binary analysis of the Android application to understand how signatures are calculated from the request headers and bodies. Furthermore, the platform's proactive redirection to email-based registration indicates a server-side trust scoring system that effectively mitigates simple SMS automation attempts. Recommendations include a deeper dive into the signature generation logic if large-scale automation is required, although current measures provide a strong defense against basic scripting.
