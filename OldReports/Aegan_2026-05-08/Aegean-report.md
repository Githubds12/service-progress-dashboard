# Aegean Airlines - Research Report

## Metadata
- **Target URL/App**: `com.aegean.airlines.prod`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-08`
- **Status**: `Completed`
- **HAR Files**: `Aegan.har`

## 1. Executive Summary
Aegean Airlines implements a secure authentication flow for its Miles+Bonus members. The process involves a password-based credential check followed by a mandatory Two-Factor Authentication (2FA) via SMS or Email. The system utilizes a robust session-tracking mechanism using `twoFactorToken`, `SessionId`, and `DeviceId`. Notably, the application enforces strict rate limiting on OTP requests, returning HTTP 429 when thresholds are exceeded. Bot protection is enhanced via `hCaptcha` (observed in telemetry/static assets) and specific API key validation. Automation feasibility is assessed as Medium (60%) due to the encrypted nature of the `twoFactorToken` and the presence of rate limiting.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | 2FA via SMS is the primary verification channel |
| **Captcha** | hCaptcha Unknown | hCaptcha artifacts and verification endpoints observed |
| **Encryption** | TLS + Token Encapsulation | Sensitive data is encapsulated within the `twoFactorToken` |
| **Rate Limits** | 429 Too Many Requests | Explicitly observed: "You have exceeded the maximum number of one-time password attempts." |
| **Endpoints Involved** | 3 | `/connect/auth/password`, `/connect/send-otp`, `/connect/v2/validate-otp` |
| **Bot Protection** | Rate Limiting + API Keys | Strict enforcement of OTP request limits and `x-mobapi-key` validation |

## 3. Flow Details

### Flow 1: Authentication (Login)

**Step 1: Password Submission**
- **Endpoint**: `POST https://mobapi.aegeanair.com/connect/auth/password?lang=en&appVersion=102&origin=app`
- **Purpose**: Authenticate user credentials and initiate the 2FA flow.
- **Request Headers**:
    ```text
    x-mobapi-key: cc791b21-d5b0-4b71-b054-a1cd9e98e5ea
    User-Agent: Aegean/1.1.8 (Android:Google Store; OS:15; Device:Google:Pixel-7; Library:okhttp/4.12.0)
    DeviceId: 231cf7e8-b701-3800-83b0-35cb04b1908f
    SessionId: 0114c1f0-c719-437f-a69a-91f83e18baa3
    Content-Type: application/json; charset=UTF-8
    ```
- **Request Payload**:
    ```json
    {
      "password": "Facebook@ds12,",
      "username": "deepanshusinghdigitalheroes@gmail.com"
    }
    ```
- **Response**:
    - **Status**: 200 OK
    - **Body**: Contains the `twoFactorToken` required for subsequent steps.

**Step 2: Send OTP (SMS Request)**
- **Endpoint**: `POST https://mobapi.aegeanair.com/connect/send-otp?lang=en&appVersion=102&origin=app`
- **Purpose**: Trigger the delivery of a 6-digit OTP code to the user's mobile device.
- **Request Headers**:
    ```text
    x-mobapi-key: cc791b21-d5b0-4b71-b054-a1cd9e98e5ea
    User-Agent: Aegean/1.1.8 (Android:Google Store; OS:15; Device:Google:Pixel-7; Library:okhttp/4.12.0)
    DeviceId: 231cf7e8-b701-3800-83b0-35cb04b1908f
    SessionId: 0114c1f0-c719-437f-a69a-91f83e18baa3
    Content-Type: application/json; charset=UTF-8
    ```
- **Request Payload**:
    ```json
    {
      "channel": "sms",
      "language": "en",
      "to": "+39 3515023566",
      "twoFactorToken": "K3vR5kFprYL0+IUuQ9wt1j+eEBG5k+JSNxoBchLx65KlslFRT+JXW5KUQTWHiCfzdeUSTeD86PG4B91c5cTWmVk+gstJXJ1s5uXNWAGtBph86Wa4hWP892UHiPDRac90Ts60cn/gZGUf56wZwZhQ4Yj/opzIXnhzMVm/VzZPH3oZ9mjt8OfjKj+IJEzPgbmDd00Px9fuqLT0vDHw09/ygV7M67Nk30ZvT/I0BhfV1b89HvLhoMcE+Hb1gi+whQ7V"
    }
    ```
- **Response (Rate Limited)**:
    - **Status**: 429 Too Many Requests
    - **Body**:
    ```json
    {
      "data": {
        "errorCode": "600",
        "errorMessage": "You have exceeded the maximum number of one-time password attempts. Please try again later."
      },
      "success": false
    }
    ```

**Step 3: OTP Verification**
- **Endpoint**: `POST https://mobapi.aegeanair.com/connect/v2/validate-otp?lang=en&appVersion=102&origin=app`
- **Purpose**: Verify the 6-digit OTP code to finalize the login.
- **Request Headers**:
    ```text
    x-mobapi-key: cc791b21-d5b0-4b71-b054-a1cd9e98e5ea
    User-Agent: Aegean/1.1.8 (Android:Google Store; OS:15; Device:Google:Pixel-7; Library:okhttp/4.12.0)
    DeviceId: 231cf7e8-b701-3800-83b0-35cb04b1908f
    SessionId: 0114c1f0-c719-437f-a69a-91f83e18baa3
    Content-Type: application/json; charset=UTF-8
    ```
- **Request Payload**:
    ```json
    {
      "channel": "sms",
      "longTermToken": true,
      "oneTimePassword": "362514",
      "twoFactorToken": "K3vR5kFprYL0+IUuQ9wt1j+eEBG5k+JSNxoBchLx65KlslFRT+JXW5KUQTWHiCfzdeUSTeD86PG4B91c5cTWmVk+gstJXJ1s5uXNWAGtBph86Wa4hWP892UHiPDRac90Ts60cn/gZGUf56wZwZhQ4Yj/opzIXnhzMVm/VzZPH3oZ9mjt8OfjKj+IJEzPgbmDd00Px9fuqLT0vDHw09/ygV7M67Nk30ZvT/I0BhfV1b89HvLhoMcE+Hb1gi+whQ7V"
    }
    ```
- **Response (Invalid OTP)**:
    - **Status**: 401 Unauthorized
    - **Body**:
    ```json
    {
      "data": {
        "errorCode": "605",
        "errorMessage": "The one-time password that you entered is invalid. Please try again."
      },
      "success": false
    }
    ```

## 4. Security & Reversing Notes

### Authentication Mechanisms
1. **Token Encapsulation**: The `twoFactorToken` appears to be an encrypted or signed blob containing the session state. It is returned after the password check and must be passed to all subsequent OTP endpoints.
2. **Static API Keys**: The `x-mobapi-key` is constant for the application version and serves as a primary access credential for the mobile API.
3. **Session Binding**: Requests are strictly bound to `DeviceId` and `SessionId`, preventing cross-device session replay without modifying these identifiers.

### Bot Detection
- **Rate Limiting**: Aegean enforces a strict cooldown period for OTP requests. Exceeding approximately 3-5 requests triggers an HTTP 429 response.
- **WAF/Captcha**: The presence of `_sec/cp_challenge/verify` and `hcaptcha` endpoints in the background traffic suggests that Aegean can trigger interactive challenges if suspicious behavior is detected.

## 5. Conclusion

### Automation Feasibility: Medium (60%)

### Detailed Conclusion:
Aegean Airlines' authentication API is well-designed with standard mobile security patterns. The reliance on a single `twoFactorToken` to bridge the gap between credential verification and OTP submission simplifies the flow logic but requires careful state management. The primary obstacles to full automation are the strict rate limiting (429) and the potential for hCaptcha challenges. Automation is feasible by mimicking the mobile app's headers (`x-mobapi-key`, `DeviceId`, `SessionId`) and ensuring a sufficient delay between requests to avoid triggering the rate limiter. Security researchers should focus on the entropy of the `twoFactorToken` and whether the `DeviceId` can be easily spoofed to bypass local rate limits.

## 6. Conclusion
The security reconnaissance of Aegean Airlines (Miles+Bonus) reveals a mature 2FA implementation. By separating credential checks from OTP validation through an encrypted session token, the platform maintains a high level of security against unauthorized access. While bot protection mechanisms like rate limiting are in place, the consistent use of JSON payloads and clear error reporting provides a viable path for technical integration and automated security assessments. researchers should remain aware of the background telemetry that monitors device integrity throughout the session lifecycle.
