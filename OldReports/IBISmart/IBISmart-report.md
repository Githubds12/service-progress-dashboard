# IBI SMART - Security Analysis Report

## Metadata
- **Target URL/App**: `ibi.co.il` / `com.ibidev.ibitrade`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-26`
- **Status**: `Completed`
- **HAR Files**: `IBISmart.har`

## 1. Executive Summary
IBI SMART (com.ibidev.ibitrade) implements a straightforward OTP-based onboarding and authentication flow. The application uses a central API host (`smartapi.ibi.co.il`) for handling phone number registration and OTP validation. Security measures include a static `api-key` in the request headers and Cloudflare protection for the API endpoints. No advanced bot protection like specialized captchas or complex request signing was observed during the initial onboarding steps. Automation feasibility is high due to the lack of dynamic challenges, though Cloudflare's presence suggests potential rate limiting or behavioral monitoring.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS / Voice Call | SMS is the primary channel for OTP delivery |
| **Captcha** | undefined | No captcha challenges were observed during testing |
| **Encryption** | None | Data is transmitted in plain JSON format |
| **Rate Limits** | Unknown | No rate limiting behavior (429) was observed during testing |
| **Endpoints Involved** | 2 | `/api/onboarding/otp/start`, `/api/onboarding/otp/validate` |
| **Bot Protection** | Cloudflare | Cloudflare protection implemented on API endpoints |

## 3. Flow Details

### Flow 1: Phone Verification (Onboarding)

**Step 1: Request OTP**
- **Endpoint**: `POST /api/onboarding/otp/start`
- **Purpose**: Initiate OTP sending to the provided phone number.
- **Notable Headers**:
    - `api-key`: `msdjfo@%#T^YrgsrfSFDHnmblpfsjbfsnk;ml358ueoj5%Y#Y%#yhfb#%@#$^T@4nt436hdgjmdhfmg`
    - `User-Agent`: `Android + 3.1.9`
    - `Host`: `smartapi.ibi.co.il`
- **Request Payload**:
    ```json
    {"isVoice":false,"phone":"0541234567"}
    ```
- **Response**:
    ```json
    {"success":true}
    ```
- **Analysis**: The request requires a static API key. The phone number is sent in plain text.

**Step 2: Validate OTP**
- **Endpoint**: `POST /api/onboarding/otp/validate`
- **Purpose**: Submit the received OTP code for verification.
- **Notable Headers**:
    - `api-key`: `msdjfo@%#T^YrgsrfSFDHnmblpfsjbfsnk;ml358ueoj5%Y#Y%#yhfb#%@#$^T@4nt436hdgjmdhfmg`
    - `User-Agent`: `Android + 3.1.9`
- **Request Payload**:
    ```json
    {"code":"323232","phone":"0541234567","utm_source":"app"}
    ```
- **Response**:
    ```json
    {"success":false}
    ```
- **Analysis**: This step validates the 6-digit OTP code against the phone number.

## 4. Security & Reversing Notes

### API Authentication
The application relies on a static `api-key` header for all onboarding requests. This key appears to be hardcoded in the application binary and is consistent across requests.

### Bot Protection (Cloudflare)
The responses include Cloudflare headers (`Server: cloudflare`, `CF-RAY`), indicating that the API is behind Cloudflare's WAF. While no interactive challenges were triggered during testing, Cloudflare may employ passive fingerprinting or rate limiting for automated traffic.

### Data Integrity
The payload structure is simple JSON. No additional request signing (HMAC) or body encryption is used, making it relatively easy to intercept and replay requests.

## 5. Conclusion

### Automation Feasibility: High (> 70%)

### Detailed Conclusion:
The automation feasibility for IBI SMART is high. The core authentication flow consists of two simple API calls with predictable JSON payloads. The primary security mechanism is a static API key, which is easily reproducible. The absence of interactive captchas (like reCAPTCHA or hCaptcha) significantly lowers the barrier for automation. However, developers should be aware of the Cloudflare protection, which might require high-quality proxies or browser-mimicking headers to bypass potential passive detection. Overall, the flow is robust but lacks advanced anti-bot measures.
