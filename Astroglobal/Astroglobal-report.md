# AstroGlobal - Research Report

## Metadata
- **Target URL/App**: `astroglobal.com` / `com.astroglobal.app`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-10`
- **Status**: `Completed`
- **HAR Files**: `Astroglobal.har`

## 1. Executive Summary
AstroGlobal is an astrology and consultation platform. The Android application implements a standard OTP-based authentication flow. The process involves two primary steps: checking user registration (which triggers the SMS OTP) and verifying the received OTP. The security implementation is straightforward with no advanced bot protection (like Captcha or complex encryption) observed in the captured traffic. Automation feasibility is high.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | primary channel for OTP |
| **Captcha** | undefined | No captcha challenge was observed during testing |
| **Encryption** | None | Standard JSON payloads over HTTPS |
| **Rate Limits** | Unknown | No rate limiting behavior was explicitly observed during testing |
| **Endpoints Involved** | 2 | `/account/check-user/`, `/account/verify-otp/` |
| **Bot Protection** | None | No active bot protection detected on the API endpoints |

## 3. Flow Details

### Flow 1: Authentication (Login/Signup)

**Step 1: Check User / Request OTP**
- **Endpoint**: `POST https://api.astroglobal.com/account/check-user/`
- **Purpose**: Verify if the user is registered and trigger the SMS OTP delivery.
- **Notable Headers**:
    - `Content-Type`: `application/json`
    - `User-Agent`: `okhttp/4.9.2`
- **Request Payload**:
    ```json
    {
        "phone": "7456821389", <!-- Phone Number -->
        "sign_up_method": "STANDARD"
    }
    ```
- **Response**:
    ```json
    {
        "user_registered": false
    }
    ```

**Step 2: Verify OTP**
- **Endpoint**: `POST https://api.astroglobal.com/account/verify-otp/`
- **Purpose**: Submit the received OTP code for verification.
- **Request Payload**:
    ```json
    {
        "otp": "3625", <!-- OTP Code -->
        "phone": "7456821389" <!-- Phone Number -->
    }
    ```
- **Response**:
    ```json
    {
        "success": true,
        "detail": "Invalid OTP or Expired OTP!"
    }
    ```
- **Analysis**: Interestingly, the server returns `success: true` even when the detail message indicates an invalid OTP. This might be a quirk of the API's response structure or state handling.

## 4. Security & Reversing Notes

### Encryption/Signing Mechanisms
The application uses standard JSON payloads over HTTPS. No custom signing headers or body encryption were found in the API communication.

### Captcha Integration
No Captcha implementation (like Google reCAPTCHA or GeeTest) was observed in the authentication flow.

### Bot Detection
There were no visible bot detection mechanisms or device fingerprinting SDKs (like Shumei or DataDome) active during the authentication requests.

## 5. Conclusion

### Automation Feasibility: High (> 90%)

### Detailed Conclusion:
The AstroGlobal authentication flow is highly susceptible to automation. The endpoints are clean, use standard JSON, and lack any significant anti-bot measures such as Captcha, request signing, or device fingerprinting. The two-step process (check-user followed by verify-otp) is easily reproducible in any standard HTTP client or scripting language.
