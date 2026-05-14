
# CubaMessenger - Research Report

## Metadata
- **Target URL/App**: `www.cubamessenger.com` / `com.cubamessenger.cubamessengerapp`
- **Researcher**: `Security Research Team`
- **Date**: `2026-04-26`
- **Status**: `Completed`
- **HAR Files**: `CubaMessenger.har`

## 1. Executive Summary
CubaMessenger (com.cubamessenger.cubamessengerapp) is a messaging and remittance application tailored for the Cuban market. The application utilizes a direct SMS-based authentication flow. Users provide their phone number and country code to receive a 4-digit OTP, which is then submitted to obtain a persistent `auth_token`. Subsequent API calls use this token within multipart/form-data payloads. No advanced bot protection (like Captcha or specialized anti-fraud SDKs) was observed in the captured registration/login traffic.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Direct OTP verification for login/registration |
| **Captcha** | undefined | No captcha observed in the authentication flow |
| **Encryption** | Standard | HTTPS; application-level tokens (`auth_token`) |
| **Rate Limits** | Unknown | No rate limiting behavior observed in HAR |
| **Endpoints Involved** | 2 | `/api/v2/login/send_sms`, `/api/v2/login/get_token` |

## 3. Flow Details

### Flow 1: SMS Authentication

**Step 1: Request SMS OTP**
- **Endpoint**: `POST https://www.cubamessenger.com/api/v2/login/send_sms`
- **Purpose**: Triggers the delivery of a verification code to the user's phone.
- **Notable Headers**:
    - `Content-Type`: `multipart/form-data`
- **Request Payload**:
    ```text
    --boundary
    Content-Disposition: form-data; name="country_code"
    91
    --boundary
    Content-Disposition: form-data; name="phone_number"
    8791267460
    --boundary
    Content-Disposition: form-data; name="device_id"
    d4b61f49a46af465
    ...
    ```
- **Response**:
    ```json
    {"success": true}
    ```

**Step 2: Verify OTP and Obtain Token**
- **Endpoint**: `POST https://www.cubamessenger.com/api/v2/login/get_token`
- **Purpose**: Submits the received SMS code to authenticate the session.
- **Request Payload**:
    ```text
    --boundary
    Content-Disposition: form-data; name="sms_code"
    1885
    --boundary
    Content-Disposition: form-data; name="phone_number"
    8791267460
    ...
    ```
- **Response**:
    ```json
    {
      "success": true,
      "auth_token": "57eea19ac2c0e7dc7780d52303cf4d4d4d988e7cf85ca32fd6139487711f5a33",
      "user": {
        "id": "3110765",
        "phone_number": "8791267460",
        "balance": "1.00",
        ...
      }
    }
    ```

### Flow 2: Authenticated Session Actions

**Step 1: Synchronize Data**
- **Endpoint**: `POST https://www.cubamessenger.com/api/v2/sync/synchronize`
- **Notable Headers**:
    - `Content-Type`: `multipart/form-data`
- **Request Payload**:
    ```text
    --boundary
    Content-Disposition: form-data; name="auth_token"
    57eea19ac2c0e7dc7780d52303cf4d4d4d988e7cf85ca32fd6139487711f5a33
    ...
    ```
- **Response**:
    ```json
    {
      "success": true,
      "user": { ... },
      "date": "2026-04-26 07:01:48",
      ...
    }
    ```

## 4. Security & Reversing Notes

### Protocol Implementation
The application exclusively uses `multipart/form-data` for its API communication, even for simple key-value pairs. This is a common pattern in legacy or cross-platform mobile frameworks.

### Session Management
The `auth_token` returned in the `get_token` response is the primary session identifier. It is passed as a form field in almost every subsequent request. There is no standard `Authorization` header usage observed.

### Device Binding
Requests include `device_id`, `device_model`, and `device_os_version`. While these are submitted, they do not appear to be cryptographically signed or verified against a hardware-backed keystore in the observed traffic.

## 5. Conclusion

### Automation Feasibility: 85%

### Critical Blockers:
1. **SMS OTP**: The only real barrier is the requirement for a valid physical or virtual phone number to receive the code.
2. **Multipart Formatting**: Automation scripts must correctly handle the generation of multipart boundaries and field dispositions.

### Summary:
CubaMessenger implements a straightforward authentication mechanism that is highly amenable to automation once the SMS challenge is bypassed. The lack of secondary bot protection layers (Captchas, WAF challenges) makes it a low-complexity target for security researchers.
