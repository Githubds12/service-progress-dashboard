# Tuda (Taxi Maxim) - Research Report

## Metadata
- **Target URL/App**: `com.tuda.android`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-30 09:50`
- **Status**: `Completed`
- **HAR Files**: `Tuda.har`

## 1. Executive Summary
Tuda (com.tuda.android), part of the Taxi Maxim ride-hailing ecosystem, utilizes a regionalized API structure (e.g., `cabinet-id.taximaxim.com`) for its authentication services. The authentication flow is a standard SMS-based OTP verification. However, the platform implements a significant security hurdle in the form of a mandatory `sig` (signature) parameter for all API requests. This signature appears to be a checksum or HMAC of the request components, preventing simple replay attacks. Automation feasibility is medium, contingent on reverse-engineering the `sig` generation logic within the Android binary.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | 4-digit OTP code sent via SMS |
| **Captcha** | undefined | No visual captcha was triggered during the flow |
| **Encryption** | Request Signing | Dynamic `sig` parameter required in the URL |
| **Rate Limits** | 60s | `NextTryInSeconds` enforces a 1-minute retry interval |
| **Endpoints Involved** | 2 | `/sms/send`, `/Sms/confirm` |
| **Bot Protection** | High | Device-bound `udid` and dynamic request signatures |

## 3. Flow Details

### Flow 1: Registration & SMS Verification

**Step 1: Request SMS OTP**
- **Endpoint**: `POST /Services/Public.svc/api/v2/login/code/sms/send`
- **Purpose**: Initiate SMS delivery to the user's phone number
- **Notable Headers/Params**:
    - `udid`: `685a7cb25495a2e2`
    - `sig`: `11a343c5e63688e30fc7d583d151ffac` (Dynamic)
    - `rt`: `041842.933` (Timestamp-based)
- **Request Payload**:
    <!-- Phone Submission -->
    ```json
    {
      "locale": "en",
      "phone": "393515878949",
      "type": "sms",
      "smstoken": "fZYl4d5RSuH",
      "isDefault": "1"
    }
    ```
- **Response**:
    ```json
    {
      "Type": "sms",
      "AuthKey": "b6ec7805-999e-4bfb-8fce-be28d46cb47d",
      "NextTryInSeconds": 60,
      "Length": 4,
      "Success": true
    }
    ```

**Step 2: Verify OTP**
- **Endpoint**: `POST /Services/Public.svc/api/v2/login/code/Sms/confirm`
- **Purpose**: Validate the SMS code and establish a session
- **Notable Params**:
    - `sig`: `8f4703820e243b32bea62e78ca92a519`
- **Request Payload**:
    <!-- OTP Submission -->
    ```json
    {
      "phone": "393515878949",
      "authKey": "b6ec7805-999e-4bfb-8fce-be28d46cb47d",
      "type": "Sms",
      "code": "3333",
      "udid": "685a7cb25495a2e2"
    }
    ```
- **Response**:
    ```json
    {
      "Success": false,
      "Message": "Invalid phone number or code."
    }
    ```

## 4. Security & Reversing Notes

### Request Signing (The `sig` Hurdle)
The primary security mechanism is the `sig` parameter. Analyzing the HAR traffic reveals that each request has a unique signature. For automation to succeed, the algorithm (likely MD5 or SHA-1 with a secret salt and concatenated request parameters) must be extracted from the native `.so` libraries or the Java classes of the application.

### Device Binding
Requests are heavily tied to the `udid` and `rt` parameters. The server likely tracks the session state using the `AuthKey` returned in the first step, mapping it to the device identifier and phone number.

## 5. Conclusion

### Automation Feasibility: 55% (Medium)

### Detailed Conclusion:
Automating Tuda is possible but requires a non-trivial reverse-engineering effort to replicate the `sig` generation. Without the correct signature, the server returns a `403 Forbidden` error (as seen in the early `Settings` calls in the trace). The clean JSON structure of the payloads otherwise makes the implementation straightforward once the signing hurdle is bypassed. Use of rotating proxies and precise device headers is recommended to avoid IP-based rate limiting.
