# maxim - Research Report

## Metadata
- **Target URL/App**: `com.taxsee.taxsee` (Maxim — order taxi, food)
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29`
- **Status**: `Completed`
- **HAR Files**: `Maxim.har`

## 1. Executive Summary
Maxim (Taxsee) uses a city-specific subdomain architecture (e.g., `abakan.taximaxim.ru`) for its taxi and delivery services. The authentication flow is secured by a mandatory signature parameter (`sig`) on all API requests, which likely signs the query parameters (including `rt` timestamp and `udid`) against a client secret. Verification is performed via a 4-digit SMS OTP. Automation feasibility is limited by the request signing mechanism and device-specific telemetry.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | 4-digit OTP code |
| **Captcha** | None | Not observed in the registration flow |
| **Encryption** | Standard | HTTPS with JSON payloads |
| **Rate Limits** | Moderate | Enforced via signature and backend |
| **Endpoints Involved** | 2 | `/login/code/sms/send`, `/login/code/Sms/confirm` |
| **Bot Protection** | Moderate | Request signing (`sig`) and device fingerprinting |

## 3. Flow Details

### Flow 1: Login / Registration

**Step 1: Request SMS OTP**
- **Endpoint**: `POST https://abakan.taximaxim.ru/0000/Services/Public.svc/api/v2/login/code/sms/send?city=18&platform=CLAPP_ANDROID&source=playmarket&udid=3974a226932ff5cf&device=Google%2FPixel+7%2F15&version=3.17.2&locale=en&density=xxhdpi&rt=204015.438&sig=a4d97a93d3144822a8cd980d4792a26b`
- **Request Headers**:
    ```text
    User-Agent: Dalvik/2.1.0 (Linux; U; Android 15; Pixel 7 Build/AP4A.250205.002)
    Content-Type: application/json; charset=utf-8
    ```
- **Request Body**:
    ```json
    {
      "locale": "en",
      "phone": "393519061133",
      "type": "sms",
      "smstoken": "vEMdSjfFO6R"
    }
    ```
- **Response Body**:
    ```json
    {
      "Type": "sms",
      "AuthKey": "7d4b2b83-1679-44ea-8113-6a9c66ef2002",
      "AuthReqId": null,
      "SuggestToCallForOrdering": false,
      "ResultCode": 0,
      "NextTryInSeconds": 60,
      "Length": 4,
      "Success": true,
      "Message": "We sent a message with a code to <b>+39 351 906 1133.</b>",
      "UniversalDialog": null
    }
    ```

**Step 2: Verify SMS OTP**
- **Endpoint**: `POST https://abakan.taximaxim.ru/0000/Services/Public.svc/api/v2/login/code/Sms/confirm?city=18&platform=CLAPP_ANDROID&source=playmarket&udid=3974a226932ff5cf&device=Google%2FPixel+7%2F15&version=3.17.2&locale=en&density=xxhdpi&rt=204158.197&sig=77036c9a14207a3aaf45d985be45f0b8`
- **Request Headers**:
    ```text
    Content-Type: application/json; charset=utf-8
    ```
- **Request Body**:
    ```json
    {
      "phone": "393519061133",
      "type": "sms",
      "authKey": "7d4b2b83-1679-44ea-8113-6a9c66ef2002",
      "code": "3333",
      "udid": "3974a226932ff5cf"
    }
    ```
- **Response Body (Error Case)**:
    ```json
    {
      "Success": false,
      "Message": "Invalid phone number or code.",
      "resetTimer": false
    }
    ```

## 4. Security & Reversing Notes

### Request Signing (`sig`)
- All requests to `Public.svc` include a `sig` parameter in the URL.
- This signature is generated based on the URL parameters, including `rt` (uptime in milliseconds) and `udid` (device identifier).
- Reverse engineering the `sig` generation logic (likely in native library or obfuscated Java) is required for automation.

### Telemetry & Fingerprinting
- The app uses AppsFlyer (`appsflyersdk.com`) for install tracking and attribution.
- Detailed device metadata (BSSID, SIM status, SSID) is sent during the initial `/login` call.

## 5. Conclusion

### Automation Feasibility: 40%

### Critical Blockers:
1. **Request Signature (`sig`)**: Mandatory for all API calls.
2. **City-based Routing**: Requires identifying the correct subdomain for the target phone number's region.
