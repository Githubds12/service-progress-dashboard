
# Kimi (com.moonshot.kimichat) - Research Report

## Metadata
- **Target URL/App**: `com.moonshot.kimichat`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-12`
- **Status**: `Completed`
- **HAR Files**: `Kimi.har`

## 1. Executive Summary
Kimi (com.moonshot.kimichat) implements a robust security architecture for its Android application, utilizing a gateway service for configuration and a dedicated API for user authentication. The platform enforces anti-automation measures primarily through a mandatory captcha challenge required for SMS OTP delivery. All authentication requests are tied to unique device and session identifiers (`x-msh-device-id`, `x-msh-session-id`). Automation feasibility is low due to the complexity of the captcha output generation.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for account registration/login |
| **Captcha** | Custom Captcha (Moonshot) | Requires `captcha_output` in the verify-code request |
| **Encryption** | Standard HTTPS / JWT | Uses Bearer tokens and custom session headers |
| **Rate Limits** | Unknown | No explicit rate limiting observed in the capture |
| **Endpoints Involved** | 4 | register, verify-code, register/trial, disabled-country-code |

## 3. Flow Details

### Flow: Account Registration / Login

**Step 1: Get Blocked Countries**
- **Endpoint**: `GET https://www.kimi.com/api/user/sms/disabled-country-code`
- **Purpose**: Retrieve the list of country codes where SMS services are unavailable for compliance.
- **Request**:
    - **Headers**:
        ```http
        Host: www.kimi.com
        x-msh-device-id: 7640628574839392513
        x-msh-session-id: 1731746206925922117
        User-Agent: Kimi/2.7.0 (Android 13; Scale/3.0)
        ```
- **Response**:
    ```json
    [
        {"country_name":"俄罗斯","country_code":"+7"},
        {"country_name":"伊朗","country_code":"+98"},
        {"country_name":"叙利亚","country_code":"+963"},
        {"country_name":"朝鲜","country_code":"+850"},
        {"country_name":"古巴","country_code":"+53"},
        {"country_name":"乌克兰","country_code":"+380"}
    ]
    ```

**Step 2: Request SMS OTP (Send Code)**
- **Endpoint**: `POST https://www.kimi.com/api/user/sms/verify-code`
- **Purpose**: Initiate OTP delivery to the user's phone number.
- **Notable Headers**:
    - `Content-Type`: application/json
    - `x-msh-device-id`: 7640628574839392513
- **Request Payload**:
    ```json
    {
        "phone": "3720515808", <!-- Phone Number -->
        "country_code": "+39",
        "action": "register",
        "captcha_id": "9afd0ff784ef4682a875c5aac7c099cf",
        "lot_number": "",
        "pass_token": "",
        "gen_time": "",
        "captcha_output": "QjGAuvoHrcpuxlbw7cp4WnIbbjzG4rtSlpc7EDovNHQS._ujzPZpeCInSxIT4WunuDDh8dRZYF2GbBGWyHlC6q5uEi9x-TXT9j7J705vSsBXyTar7aqFYyUltKYJ7f4Y2TXm_1Mn6HFkb4M7URQ_rWtpxQ5D6hCgNJYC0HpRE7.2sttqYKLoi7yP1KHzK-PptdHHkVwb77cwS2EJW7Mj_PsOtnPBubTmTZLpnRECJR99dWTVC11xYG0sx8dJNLUxUFxEyzTfX4nSmQz_T5sXATRKHtVAz7nmV0De5unmflfAlUwMGKlCT1khBtewlgN5nHvyxeD8Z1_fPVzi9oznl-sbegj6lKfCWezmLcwft8.4yaVh6SlzXJq-FnSK.euq9OBd5jYc82ge2_hEca1fGU--SkPRzgwkzew4O4qjdS2utdPwFONnhKAIMJRPUmCV4lPHG1OeRDvyNV8sCnuFMw7leasxIhPoycl4pm5bNy70Z1laozEGJgItVNr3"
    }
    ```
- **Response**:
    - **Status**: 200 OK
    - **Body**: `null`

**Step 3: Verify OTP (Registration Submission)**
- **Endpoint**: `POST https://www.kimi.com/api/user/register/trial`
- **Purpose**: Submit the verification code to complete the registration process.
- **Request Payload**:
    ```json
    {
        "phone": "3720515808", <!-- Phone Number -->
        "verify_code": "111111", <!-- OTP Code Sample 1 -->
        "country_code": "+39",
        "wx_user_id": ""
    }
    ```
- **Response (Invalid Code)**:
    - **Status**: 400 Bad Request
    - **Body**:
        ```json
        {
            "error_type": "user.verify_code.invalid",
            "message": "Incorrect verification code",
            "detail": "Incorrect verification code"
        }
        ```

**Step 4: Device Registration**
- **Endpoint**: `POST https://www.kimi.com/api/device/register`
- **Purpose**: Finalize device registration and obtain authentication tokens.
- **Request Payload**:
    ```json
    {
        "push_device_id": "",
        "push_provider": "jpush"
    }
    ```
- **Response**:
    - **Status**: 200 OK
    - **Body**:
        ```json
        {
            "access_token": "eyJhbGciOiJIUzUxMi...", <!-- JWT Access Token -->
            "refresh_token": "eyJhbGciOiJIUzUxMi..." <!-- JWT Refresh Token -->
        }
        ```

## 4. Security & Reversing Notes

### Authentication Mechanisms
The application uses a hybrid authentication model:
1. **Device Binding**: All requests are required to include `x-msh-device-id` and `x-msh-session-id`.
2. **JWT Tokens**: After successful registration/login, the server issues a standard JWT Bearer token used for authorization in subsequent API calls to `kimi.gateway`.

### Bot Detection & Captcha
- **Custom Captcha**: The `sms/verify-code` endpoint is protected by a mandatory `captcha_output`. This field appears to be a large encoded blob (~1KB) that validates client-side integrity and user interaction.
- **Device Fingerprinting**: The `device_id` is generated and registered during the first launch, creating a unique link between the app instance and the server.

### Gateway Architecture
The app communicates with `apiv2/kimi.gateway` for most high-level services (chat, config, membership). These endpoints strictly enforce authentication, returning `401 Unauthorized` with `REASON_INVALID_AUTH_TOKEN` if headers are missing or expired.

## 5. Conclusion

### Automation Feasibility: Low (30%)

### Detailed Conclusion
The Kimi authentication flow is well-protected against simple automation. The primary challenge is the requirement for a valid `captcha_output` in the SMS request. This token is likely generated by a proprietary challenge-response mechanism within the Moonshot SDK. 

To automate this service, one would need to:
1. Reverse-engineer the `captcha_output` generation logic.
2. Maintain valid `device_id` and `session_id` state.
3. Handle the gateway configuration requirements.

The reliance on unique hardware/session identifiers and custom bot protection makes Kimi a low-feasibility target for high-speed automated registration without significant effort in solving the captcha layer.
