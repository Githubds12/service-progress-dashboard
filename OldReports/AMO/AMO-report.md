# AMO - Research Report

## Metadata
- **Target URL/App**: `amo.co` / `com.xiaoyu.amo`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29`
- **Status**: `Completed`
- **HAR Files**: `AMO.har`

## 1. Executive Summary
AMO is a social discovery platform that uses a centralized API hosted at `api.chatie.love`. The registration flow is standard, using SMS verification. The API implements a parameter-based signing mechanism (`sign` parameter) for security, likely to prevent unauthorized request modification. No advanced bot protection like Captcha was observed in the captured flows. Automation feasibility is Moderate, primarily depending on the complexity of the signing algorithm.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | primary channel for OTP |
| **Captcha** | undefined | No captcha challenges observed |
| **Encryption** | None | Data transmitted in plain JSON over HTTPS |
| **Rate Limits** | Unknown | No explicit rate limits encountered during analysis |
| **Endpoints Involved** | 2 | `/api/polaris/login-reg-sms-v2`, `/api/polaris/overseas-cellphone-login` |
| **Bot Protection** | Cloudflare | Infrastructure protection via Cloudflare |

## 3. Flow Details

### Flow 1: Registration / Login

**Step 1: Request SMS Code**
- **Endpoint**: `GET https://api.chatie.love/api/polaris/login-reg-sms-v2`
- **Purpose**: Send OTP to the user's phone
- **Notable Parameters**:
    - `countryCode`: `39` (Italy)
    - `cellphone`: `3517085288`
    - `sign`: `4be7a6bc18d866a986f8e1ceeec68cc4bce6d5e5` (SHA-1 signature)
- **Response**:
    ```json
    {
      "code": "000000",
      "message": "success",
      "data": {
        "resultCode": "000000",
        "message": null
      },
      "serverTime": 1777442979315,
      "traceId": "11a8dd12-221b-424b-a046-d27ec0bd84db"
    }
    ```

**Step 2: Submit OTP**
- **Endpoint**: `POST https://api.chatie.love/api/polaris/overseas-cellphone-login`
- **Purpose**: Verify OTP and authenticate
- **Request Payload**:
    ```json
    {
      "countryCode": "39",
      "cellphone": "3517085288",
      "code": "5555",
      "deviceId": "7418730820363355914",
      "anonymousId": "dbe025202541f5f4",
      "unionUserLogin": false
    }
    ```
- **Query Parameters**:
    - `unionUserLogin`: `false`
    - `anonymousId`: `dbe025202541f5f4`
    - `code`: `5555`
    - `countryCode`: `39`
    - `sign`: `d5a76bac406729323aa8f123a41f5174cb5852f2`
    - `cellphone`: `3517085288`
    - `deviceId`: `7418730820363355914`
- **Response**:
    ```json
    {
      "code": "300002",
      "message": "incorrect verification code",
      "data": null,
      "serverTime": 1777443070298,
      "traceId": "b66838b6-bec2-4fd3-9bed-68654539fd12"
    }
    ```

## 4. Security & Reversing Notes

### Signing Mechanism
Both the SMS request and the login request require a `sign` parameter. This is a 40-character hex string, which strongly suggests a SHA-1 hash. The signature likely includes query parameters, a timestamp, and a static salt/secret embedded in the application.

### Headers
The application sends several custom headers:
- `App-Key`: `111001`
- `Platform`: `android`
- `Version-Name`: `2.30.0`
- `Version-Code`: `2511`
- `Yanhong-Channel`: `polaris`

## 5. Conclusion

### Automation Feasibility: Moderate (60%)

### Detailed Conclusion:
The AMO registration flow is relatively simple but includes a signing requirement for all critical API requests. While no Captcha was present, the `sign` parameter acts as a significant hurdle for automation. Reversing the signing algorithm (identifying the secret and parameter order) is the primary requirement for successful automation. Once the signing logic is replicated, the lack of behavioral challenges makes the platform highly susceptible to automated interactions.
