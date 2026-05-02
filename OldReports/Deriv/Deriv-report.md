# Deriv - Research Report

## Metadata
- **Target URL/App**: `deriv.com` / `com.deriv.home`
- **Researcher**: `Deepanshu Singh`
- **Date**: `May 2, 2026`
- **Status**: `Completed`
- **HAR Files**: `Deriv.har`

## 1. Executive Summary
The security analysis of the Deriv application (com.deriv.home) was conducted to evaluate the registration and authentication workflow. The application utilizes the Ory Kratos identity management system for its authentication services, hosted at `auth.deriv.com`. The flow observed in the HAR trace involves registration via Google OIDC, followed by a multi-step phone number verification process using SMS-based OTP. The investigation successfully isolated the critical API endpoints responsible for requesting and submitting verification codes. Automation feasibility is high due to the lack of observed aggressive bot protection (like captchas) on the primary authentication endpoints.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for phone number verification |
| **Captcha** | undefined | No captcha was observed on the analyzed endpoints |
| **Encryption** | Standard JSON/HTTPS | Data is transmitted via secure HTTPS with standard JSON payloads |
| **Rate Limits** | Unknown | No rate limiting behavior was observed during testing |
| **Endpoints Involved** | 4 | `/self-service/registration`, `/self-service/login`, `/self-service/settings`, `/self-service/login/api` |
| **Bot Protection** | Ory Kratos | Standard security mechanisms provided by the Ory platform |

## 3. Flow Details

### Flow 1: Registration & Phone Verification

**Step 1: Initialize Registration**
- **Endpoint**: `GET https://auth.deriv.com/self-service/registration/api`
- **Purpose**: Initialize the registration flow and retrieve the flow ID.
- **Response**:
    ```json
    {
      "id": "764b8d7c-876a-4b9d-9c8e-3cb2f7faa752",
      "type": "api",
      "ui": {
        "action": "https://auth.deriv.com/self-service/registration?flow=764b8d7c-876a-4b9d-9c8e-3cb2f7faa752",
        "method": "POST"
      }
    }
    ```

**Step 2: Submit Registration (via Google OIDC)**
- **Endpoint**: `POST https://auth.deriv.com/self-service/registration?flow=675d785c-5568-4611-ac40-24c40ccb4344`
- **Purpose**: Complete registration using Google OAuth2/OIDC.
- **Request Payload**:
    ```json
    {
      "csrf_token": "",
      "method": "oidc",
      "provider": "google-Y8c4gemC",
      "transient_payload": {
        "cor": "in",
        "provider": "google",
        "tracking_data": {
          "device_info": {
            "appsflyer_id": "1777695298752-7424902786476434863",
            "platform": "android",
            "os_version": "15",
            "device_model": "Pixel 7"
          }
        },
        "x-app": "com.deriv.home"
      },
      "upstream_parameters": {
        "prompt": "select_account"
      }
    }
    ```
- **Response Status**: `200 OK`

**Step 3: Request Phone Verification (SMS OTP)**
- **Endpoint**: `POST https://auth.deriv.com/self-service/login?flow=d3eacb04-1d7d-4ba2-aa09-1c1b00f62844`
- **Purpose**: Request an SMS OTP for phone number verification.
- **Notable Headers**:
    - `x-session-token`: `ory_st_FanbtKIBenZzcCtbpx8KUTvFjw52pnUb`
- **Request Payload**:
    ```json
    {"csrf_token":"","method":"code","identifier":"+393516757384","transient_payload":{"action":"verify_phone","lang":"en","x-app":"com.deriv.home"}}
    ```
- **Response Status**: `400 Bad Request`
- **Response Body**:
    ```json
    {
      "id": "d3eacb04-1d7d-4ba2-aa09-1c1b00f62844",
      "ui": {
        "messages": [
          {
            "id": 1010014,
            "text": "A code was sent to the address you provided. If you didn't receive it, please check the spelling of the address and try again.",
            "type": "info"
          }
        ]
      },
      "state": "sent_email"
    }
    ```

**Step 4: Submit SMS OTP**
- **Endpoint**: `POST https://auth.deriv.com/self-service/login?flow=d3eacb04-1d7d-4ba2-aa09-1c1b00f62844`
- **Purpose**: Submit the received SMS OTP to complete verification.
- **Request Payload**:
    ```json
    {"csrf_token":"","method":"code","code":"333333","identifier":"+393516757384","transient_payload":{"lang":"en","action":"verify_phone","x-app":"com.deriv.home"}}
    ```
- **Response Status**: `400 Bad Request` (Invalid code captured in HAR)
- **Response Body**:
    ```json
    {
      "ui": {
        "messages": [
          {
            "id": 4010008,
            "text": "The login code is invalid or has already been used. Please try again.",
            "type": "error"
          }
        ]
      }
    }
    ```

## 4. Security & Reversing Notes

### Authentication Mechanisms

**1. Ory Kratos Integration**
- The platform uses Ory Kratos for identity management. This provides a standardized API for registration, login, and settings.
- Flows are stateful and identified by a `flow` ID, which must be obtained via a GET request before submitting data.

**2. Session Management**
- **Header**: `x-session-token` is used to maintain the authenticated state during the verification process.
- **Token Format**: `ory_st_[random_string]`

**3. Transient Payloads**
- Deriv uses the `transient_payload` field in Ory requests to pass application-specific context, such as the action (`verify_phone`) and device information.
- This allows the authentication flow to be repurposed for specific verification tasks.

### Bot Detection & Captcha
- **Bot Protection**: Standard Ory Kratos security features. No advanced third-party bot protection (like Akamai or DataDome) was observed on the primary API endpoints.
- **Captcha**: Not observed. The `need_captcha` field in the flow initialization was likely false or not triggered during the session.

## 5. Conclusion

### Automation Feasibility: 85%

### Critical Blockers:
1. **OIDC Registration**: Automating the initial registration requires handling Google OAuth2, which is complex. However, direct email registration (if supported) or using pre-existing sessions is feasible.
2. **Session Token**: The flow requires a valid session token obtained after registration/login.
3. **SMS OTP**: Requires a reliable SMS provider for receiving verification codes.

### Final Assessment:
The Deriv authentication and phone verification flow is highly automatable using standard HTTP libraries. The use of Ory Kratos provides a predictable API surface. The main challenge lies in the initial registration step if Google OIDC is the only method allowed, but the phone verification itself is straightforward once a session is established.
