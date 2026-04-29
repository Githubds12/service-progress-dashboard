# Tongcheng (同程旅行) - Research Report

## Metadata
- **Target URL/App**: `ly.com` / `com.tongcheng.android`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29`
- **Status**: `Completed (Reconnaissance Phase)`
- **HAR Files**: `Tongcheng.har`

## 1. Executive Summary
Tongcheng Travel implements a sophisticated security stack centered around **FengKongCloud (Shuidi)** risk management. The application uses encrypted communication for performance monitoring (APM) and user behavior tracking (Trajectory), making traditional traffic analysis challenging. Registration and sensitive flows are protected by selection-based captchas and risk assessment APIs. Automation feasibility is Low to Moderate, requiring bypass of third-party risk control providers.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Standard for Chinese travel apps |
| **Captcha** | selection-set | Powered by FengKongCloud |
| **Encryption** | Strong | Encrypted payloads in `17usoft.com` endpoints |
| **Rate Limits** | Unknown | Managed by Shuidi Risk Control |
| **Endpoints Involved** | 5+ | `fengkongcloud.cn`, `tc.com`, `17u.cn`, `ly.com` |
| **Bot Protection** | Shuidi | Integrated risk management system |

## 3. Flow Details

### Flow 1: SMS Verification Code Request
- **Endpoint**: `POST https://tcmobileapi.17usoft.com/member/MemberHandler.ashx`
- **Purpose**: Trigger OTP sending to the mobile number.
- **Notable Headers**:
    - `secsign`: `dac3426bcacef02a5f58f9e4b4895e4be37b3ae7ef3a8d11c742134927b015f5`
    - `user-dun`: Encrypted device telemetry.
- **Request Body**:
    ```json
    {
      "request": {
        "header": {
          "reqType": "1",
          "reqTime": "1777443916962",
          "traceId": "69c9b19e-1196-419b-a01c-6d1f0ea1548e"
        },
        "body": {
          "mobile": "18651817454",
          "type": "1",
          "vcode": "",
          "loginType": "1",
          "deviceInfo": "bc1a37548b21569d"
        }
      }
    }
    ```
- **Response**:
    ```json
    {
      "response": {
        "header": {
          "rspType": "0",
          "rspCode": "0000",
          "rspDesc": "获取成功",
          "rspTime": "1777443917645"
        }
      }
    }
    ```

### Flow 2: OTP Authentication (Login) Request
- **Endpoint**: `POST https://tcmobileapi.17usoft.com/member/MemberHandler.ashx`
- **Purpose**: Verify the SMS code and authenticate the session.
- **Request Body**:
    ```json
    {
      "request": {
        "header": {
          "reqType": "1",
          "reqTime": "1777443963406",
          "traceId": "0192e21e-1196-419b-a01c-6d1f0ea1548e"
        },
        "body": {
          "mobile": "18651817454",
          "vcode": "1111",
          "loginType": "1",
          "deviceInfo": "bc1a37548b21569d"
        }
      }
    }
    ```
- **Response (Invalid Code)**:
    ```json
    {
      "response": {
        "header": {
          "rspType": "1",
          "rspCode": "3001",
          "rspDesc": "您输入的验证码有误，请重新输入",
          "rspTime": "1777443963584"
        }
      }
    }
    ```

### Flow 3: Risk & Captcha Verification
- **Endpoint**: `https://captcha1.fengkongcloud.cn/ca/v1/log`
- **Organization ID**: `xQsKB7v2qSFLFxnvmjdO`
- **Observation**: Captcha solving returns a `requestId` which is verified by the Shuidi backend.


## 4. Security & Reversing Notes

### Shuidi Integration
Tongcheng relies heavily on `shuidi.tc.com` for risk scoring. Any automated attempt must mimic device fingerprints and solve the icon-selection captcha provided by FengKongCloud.

### Encrypted Communication
Endpoints like `dune.17usoft.com` and `vstlog.17usoft.com` use binary or highly obscured Base64 payloads, likely containing device telemetry used for bot detection.

## 5. Conclusion

### Automation Feasibility: Low (30%)

### Detailed Conclusion:
Tongcheng Travel presents a high barrier to entry for automation due to its reliance on professional-grade risk management services (FengKongCloud). The integration of behavior tracking and selection captchas ensures that simple script-based interactions are easily flagged as suspicious. Future automation efforts would require a full device-emulation approach and an integrated captcha-solving service capable of handling the selection-set challenges.
