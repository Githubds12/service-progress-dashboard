# YandexEats - Research Report

## Metadata
- **Target App**: `YandexEats (ru.foodfox.client)`
- **Version**: `26.15.0`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-26`
- **Host**: `passport.yandex.ru`

## 1. Executive Summary
YandexEats is a food delivery service by Yandex. The application uses the centralized Yandex Passport authentication gateway for user login and registration. The flow involves a multi-step verification process, primarily using SMS-based OTP. Bot protection is implemented via Yandex SmartCaptcha and device-level integrity checks. Automation requires handling the Yandex Passport track session and potentially solving visual or invisible captchas.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for OTP verification |
| **Captcha** | Yandex SmartCaptcha | Triggered during the authentication/registration flow |
| **Encryption** | None | Data is sent in standard JSON/Form-encoded format over TLS |
| **Rate Limits** | High | Standard Yandex Passport rate limiting (3-5 attempts per window) |
| **Endpoints Involved** | 3+ | `/bundle/auth/password/submit/`, `/bundle/auth/code/submit/`, `/bundle/track/check-phone-confirmation` |
| **Bot Protection** | Yandex SmartCaptcha | Integrated into the Passport auth flow |

## 3. Flow Details

### Step 1: Authentication Initialization
- **Endpoint**: `POST https://mobileproxy.passport.yandex.net/1/bundle/auth/password/submit/`
- **Purpose**: Initialize the authentication track and submit the initial identifier (phone/email).
- **Notable Headers**:
    - `X-Yandex-AM-App-ID`: `ru.foodfox.client`
    - `User-Agent**: `android (26.15.0)`
- **Request Payload**:
    ```json
    {
      "login": "<!-- Phone Number Highlight --> <mark>+79991234567</mark>",
      "client_id": "c0ebe342af7d48fbbbfcf2d2eedb8f9e",
      "track_id": "9de95e64e378e4adacb4229a162d1d0bb4"
    }
    ```
- **Response**: Returns a `track_id` and the next required step (e.g., `code`).

### Step 2: Verify OTP
- **Endpoint**: `POST https://passport.yandex.ru/pwl-yandex/api/passport/track/check-phone-confirmation`
- **Purpose**: Submit the verification code received via SMS.
- **Request Payload**:
    ```json
    {
      "track_id": "9de95e64e378e4adacb4229a162d1d0bb4",
      "code": "<!-- OTP Highlight --> <mark>356532</mark>"
    }
    ```
- **Response Payload**:
    ```json
    {
      "status": "ok",
      "is_complete": true
    }
    ```

## 4. Conclusion

### Automation Feasibility: Medium (45%)

### Detailed Conclusion:
YandexEats leverages the robust Yandex Passport infrastructure, making automation moderately difficult due to SmartCaptcha and track-based session management. While the endpoints are well-defined, the server-side logic for triggering captchas is based on behavioral analysis and IP reputation. Successful automation requires a high-quality proxy network and a dedicated SmartCaptcha solver.

**Strengths**:
- Unified authentication flow across Yandex services.
- Sophisticated bot protection (SmartCaptcha).

**Weaknesses**:
- Predictable multi-step flow (Init -> Submit -> Verify).
- Lack of additional application-level signing beyond Passport's default security.

**Recommendations**:
To automate YandexEats, focus on integrating a Yandex SmartCaptcha solver. Ensure that the `track_id` is maintained consistently throughout the session. The use of a standard Android WebView for the Passport flow means that session cookies and device IDs are critical for avoiding blocks.
