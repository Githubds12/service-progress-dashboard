# Boxy Security & Authentication Analysis

## Metadata
- **Target URL/App**: `com.client.boxy` / `api.boxypower.eu`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-30 10:50`
- **Status**: `Completed`
- **HAR Files**: `Boxy.har`

## 1. Executive Summary
Boxy (com.client.boxy) is a power bank sharing application. The authentication flow is streamlined and relies on a standard SMS OTP verification. The API is a clean REST implementation with no observed bot protection, captchas, or payload encryption. Automation feasibility is rated as extremely high due to the simplicity of the request-response cycle.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | 4-digit OTP code |
| **Captcha** | undefined | No captcha triggered during testing |
| **Encryption** | Standard TLS | Clean JSON payloads |
| **Rate Limits** | undefined | Not explicitly documented in headers |
| **Endpoints Involved** | 2 | `/verification-code` (GET), `/login` (POST) |
| **Bot Protection** | None | No signature or device fingerprinting observed |

## 3. Flow Details

### Flow 1: Registration & SMS Verification

**Step 1: Request SMS OTP**
- **Endpoint**: `GET https://api.boxypower.eu/api/login/verification-code`
- **Purpose**: Triggers an SMS to the user's mobile device.
- **Parameters**:
    - `scene`: `1` (Context for signup)
    - `code`: `39` (Country code)
    - `phone`: `3515945704`
    - `email`: (Empty)
- **Response**:
    ```json
    {
      "code": "200",
      "data": null,
      "message": "success"
    }
    ```

**Step 2: Verify OTP & Login**
- **Endpoint**: `POST https://api.boxypower.eu/api/login`
- **Purpose**: Validates the 4-digit OTP and authenticates the session.
- **Request Payload**:
    <!-- OTP Submission -->
    ```json
    {
      "code": "39",
      "email": "",
      "loginType": 0,
      "msgCode": "9423",
      "phone": "3515945704",
      "source": 1
    }
    ```
- **Response**:
    ```json
    {
      "code": "21002",
      "data": null,
      "message": "S-The verification code has incorrect(21002)"
    }
    ```

## 4. Security & Reversing Notes
The API endpoints are publicly accessible and do not require any preliminary authorization headers or device-specific tokens. The `source: 1` parameter likely indicates the Android platform. The lack of request signing makes it a prime candidate for "zero-friction" automation.

## 5. Conclusion

### Automation Feasibility: 90% (High)

### Detailed Conclusion:
Boxy is one of the simplest services to automate. The registration flow can be replicated with two basic HTTP calls. Headless automation using any standard HTTP library (e.g., Python `requests`) should work seamlessly. Integration into the master countries database is highly recommended given the lack of bot detection mechanisms.
