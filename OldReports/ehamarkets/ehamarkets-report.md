# ehamarkets - Research Report

## Metadata
- **Target URL/App**: `com.trade.trade211` (EHA Markets)
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29`
- **Status**: `Completed`
- **HAR Files**: `ehamarkets.har`

## 1. Executive Summary
EHA Markets implements a standard OTP-based registration flow. The application uses a custom API signature (`auth` parameter) to secure its requests. The flow involves sending a registration SMS, checking the SMS code, and then completing the registration with a password and device telemetry. Automation is feasible if the `auth` signature generation logic is reverse-engineered.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | OTP sent via SMS |
| **Captcha** | No | No CAPTCHA observed in the HAR flow |
| **Encryption** | Partial | `auth` signature used for request integrity |
| **Rate Limits** | Unknown | Standard server-side limits likely apply |
| **Endpoints Involved** | 3 | `send/regist/sms`, `check/regist/sms`, `register/v2` |
| **Bot Protection** | Low/Medium | Signature-based protection (`auth` parameter) |

## 3. Flow Details

### Flow 1: Registration (Signup)

**Step 1: Send Registration SMS**
- **Endpoint**: `POST https://m.eapeakwealth.com/user/info/send/regist/sms`
- **Purpose**: Trigger SMS OTP for the given phone number.
- **Request Payload**:
    ```text
    t=1777401451630&deviceId=...&v=1.3.7.53&telCode=39&username=3513093982&auth=af92cc915d6e95951db569be74d8d30b
    ```
- **Response**:
    ```json
    {"code": 200, "message": "success"}
    ```

**Step 2: Check Registration SMS**
- **Endpoint**: `POST https://m.eapeakwealth.com/user/info/check/regist/sms`
- **Purpose**: Verify the OTP code received by the user.
- **Request Payload**:
    ```text
    t=1777401471384&code=3905&telCode=39&username=3513093982&auth=ffdffd0dffef38befb59df2062915be8
    ```
- **Response**:
    ```json
    {"code": 200, "message": "success"}
    ```

**Step 3: Complete Registration**
- **Endpoint**: `POST https://m.eapeakwealth.com/user/info/register/v2`
- **Purpose**: Finalize registration with password and device details.
- **Request Payload**:
    ```text
    code=3905&password=...&diviceSsaid=...&appsflyerId=...&auth=b77ef068a871ec7d35ade4d83a302700
    ```

## 4. Security & Reversing Notes

### Encryption/Signing Mechanisms

**1. Request Signature (`auth`)**
- **Algorithm**: Likely a salted MD5 or HMAC-SHA signature of the request parameters and a secret key.
- **Reversing**: The signing logic resides in the native library or obfuscated Java code.

**2. Device Tracking**
- **Parameters**: `deviceId`, `diviceSsaid`, `appsflyerId`, `diviceAppSetId` are collected to track the registration source.

## 5. Conclusion

### Automation Feasibility: 70%

### Critical Blockers:
1. **Auth Signature**: Requires reverse engineering the `auth` parameter generation to automate API calls.
2. **Device Fingerprinting**: Standard trackers (AppsFlyer) are present.
