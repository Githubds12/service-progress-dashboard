# 1xCasino - Research Report

## Metadata
- **Target URL/App**: `org.xbet.casino`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29`
- **Status**: `Completed`
- **HAR Files**: `1xCasino.har`

## 1. Executive Summary
1xCasino (org.xbet.casino) utilizes a sophisticated multi-step registration flow integrated with the 1xBet security ecosystem. The platform employs high-level anti-automation measures, including **HD-API** (Huawei/Honor Bot Protection) and a dynamic **X-Sign** request signature header. The registration process requires solving a custom slider-based captcha before an OTP can be requested via SMS. All API communications are secured via custom headers and telemetry payloads, making standalone automation highly challenging.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | 5-digit OTP code sent via SMS |
| **Captcha** | Slider CAPTCHA | Custom "hand" puzzle slider captcha |
| **Encryption** | Custom Signing | `X-Sign` header required for registration and captcha steps |
| **Rate Limits** | Unknown | No explicit rate limiting observed in the trace |
| **Endpoints Involved** | 4 | `/GetCaptcha`, `/Registration`, `/SendCode`, `/CheckCode` |
| **Bot Protection** | HD-API |Huawei/Honor Bot Protection (hdf.js) collected via `/hd-api/m/verify` |

## 3. Flow Details

### Flow 1: Registration & SMS Verification

**Step 1: Get Captcha Challenge**
- **Endpoint**: `POST /captcha/v1/GetCaptcha`
- **Purpose**: Initialize captcha session
- **Notable Headers**:
    - `X-Sign`: `86306FfAc2Y9VE49MA2890UAP6IC90SBOrNkLF9IdEzqFn7D...` (Large dynamic signature)
    - `AppGuid`: `19127443fe88a20f_2`
- **Request Payload**:
    ```json
    {"AppGuid":"19127443fe88a20f_2","Language":"en_IN","Method":"Registration","VersionGen":3,"Login":""}
    ```
- **Response**:
    ```json
    {"id":"e2d38f1b-24c0-4c33-baa3-559db38ec2e9","tasks":[{"image":"OpenFrame","count":0,"letCount":0,"type":4}]}
    ```

**Step 2: Submit Registration & Solved Captcha**
- **Endpoint**: `POST /Account/v2/Casino/Register/Registration`
- **Purpose**: Create account and verify captcha
- **Request Payload**:
    <!-- Registration and Captcha Submission -->
    ```json
    {
      "CaptchaId": "e2d38f1b-24c0-4c33-baa3-559db38ec2e9",
      "ImageText": "VUgxsCk5Q08HaPrt5_n4TEvBfe6xpLMM1CD60htS3uOI_KDPNHg...", 
      "Data": {
        "Phone": "9600032078",
        "RegType": 2,
        "CountryId": 71,
        "CurrencyId": 99,
        "RulesConfirmationAll": 1
      }
    }
    ```
- **Response**:
    ```json
    {
      "Success": true,
      "Value": {
        "Auth": {
          "Guid": "dd5f359a-85bb-4d6d-847d-bc0be37f9f76",
          "Token": "171A63C7678743E88E1E99FC5436ECF0"
        },
        "CodeTypes": ["Sms"]
      }
    }
    ```

**Step 3: Request SMS OTP**
- **Endpoint**: `POST /Account/v1/SendCode`
- **Purpose**: Trigger SMS delivery to the registered number
- **Request Payload**:
    <!-- SMS Request -->
    ```json
    {
      "Data": {},
      "Auth": {
        "Guid": "dd5f359a-85bb-4d6d-847d-bc0be37f9f76",
        "Token": "171A63C7678743E88E1E99FC5436ECF0"
      }
    }
    ```
- **Response**:
    ```json
    {
      "Success": true,
      "Value": {
        "RAS": 300,
        "Auth": {
          "Guid": "dd5f359a-85bb-4d6d-847d-bc0be37f9f76",
          "Token": "CECBEC9AE7D14DD2AC14D3571CDB1D5D"
        }
      }
    }
    ```

**Step 4: Verify OTP**
- **Endpoint**: `POST /Account/v1/CheckCode`
- **Purpose**: Submit the 5-digit code for account activation
- **Request Payload**:
    <!-- OTP Submission -->
    ```json
    {
      "Data": {
        "Code": "44444"
      },
      "Auth": {
        "Guid": "dd5f359a-85bb-4d6d-847d-bc0be37f9f76",
        "Token": "CECBEC9AE7D14DD2AC14D3571CDB1D5D"
      }
    }
    ```
- **Response**:
    ```json
    {
      "Success": false,
      "Error": "Verification code is incorrect.",
      "ErrorCode": 100371
    }
    ```

## 4. Security & Reversing Notes

### HD-API (Bot Protection)
The application integrates the **HD-API** (detected via `hdf.js` and `/hd-api/m/verify`). This service collects extensive environmental data from the device to generate a trust score. The payload sent to the verify endpoint is significantly large (~22KB), containing encrypted hardware and software identifiers.

### X-Sign Header Signing
Most critical endpoints require an `X-Sign` header. This is a dynamic signature generated on the client-side, likely signing the request parameters and a timestamp. Without replicating this signing logic, automated requests will be rejected by the server.

### Custom Slider Captcha
The captcha system (`/captcha/v1/GetCaptcha`) provides a "hand" or "puzzle" challenge. The solution is submitted as an encrypted string (`ImageText`) in the registration request. This requires visual puzzle solving and behavioral simulation (simulated drag events).

## 5. Conclusion

### Automation Feasibility: 35% (Low)

### Detailed Conclusion:
Automating the 1xCasino registration flow presents extreme technical challenges. The combination of **HD-API** telemetry and the **X-Sign** header signing creates a multi-layered barrier that requires deep reverse engineering of the application's native libraries or obfuscated logic. Additionally, the custom slider captcha adds a layer of visual challenge that cannot be bypassed via simple request replay. A successful automation strategy would likely involve a hybrid approach using a headless browser or a specialized native bridge to generate valid signatures and solve the captcha.
