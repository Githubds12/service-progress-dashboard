# Jameda - Research Report

## Metadata
- **Target URL/App**: `de.jameda`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-02`
- **Status**: `Completed`
- **HAR Files**: `Jameda.har`

## 1. Executive Summary
Jameda implements a secure authentication flow using OAuth 2.0 and reCAPTCHA v2. The registration process involves requesting a verification code via SMS, which requires a bearer token obtained through a public-to-private token exchange. OTP verification is protected by Google reCAPTCHA, making automated registration challenging without solving the challenge. The service is assessed at 500rs due to its integrated security measures and robust API structure.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for OTP |
| **Captcha** | reCAPTCHA v2 Invisible (Google) | Observed in OTP verification step |
| **Encryption** | None | Standard JSON payloads over HTTPS |
| **Rate Limits** | Unknown | No explicit rate limiting observed in HAR |
| **Endpoints Involved** | 3 | `/public-token`, `/oauth/v2/token`, `/users/verification` |
| **Bot Protection** | Google reCAPTCHA | Implemented on the verification endpoint |

## 3. Flow Details

### Flow 1: Registration / OTP Verification

**Step 1: Get Public Token**
- **Endpoint**: `GET https://l.jameda.de/public/public-token`
- **Purpose**: Retrieve an initial public token for the session.
- **Request Headers**:
    ```text
    User-Agent: okhttp/4.9.2
    ```
- **Response**:
    ```json
    {
        "expiresAt": "2026-05-02T05:07:48+00:00",
        "token": "OTE2ZTlhMGIzNWFkNDExZDBjNjJhYTc5YWM3ZWFjOThkYjUwNmFjOTE1MTgyOWNkZTkyYjBhNzc5OTZhYWEyYw"
    }
    ```

**Step 2: Request OTP (Verification)**
- **Endpoint**: `PUT https://www.jameda.de/api/v3/users/verification`
- **Purpose**: Send OTP to the provided phone number.
- **Request Headers**:
    ```text
    authorization: Bearer [TOKEN]
    app-version: 5.271.0
    platform-os: android
    ```
- **Request Body**:
    ```json
    {
        "phone": "+393522296606",
        "context": "generic"
    }
    ```
- **Response**: `204 No Content`

**Step 3: Verify OTP**
- **Endpoint**: `POST https://www.jameda.de/api/v3/users/verification`
- **Purpose**: Verify the received OTP and complete authentication.
- **Request Body**:
    ```json
    {
        "code": "5976",
        "phone": "+393522296606",
        "email": "dkid8288@gmail.com",
        "reCaptchaToken": "[RECAPTCHA_TOKEN]"
    }
    ```
- **Response**:
    ```json
    {
        "auto_login_redirect": false,
        "type": null,
        "token": null
    }
    ```

## 4. Security & Reversing Notes

### Authentication Mechanism
Jameda uses a multi-step token exchange. A public token is first fetched using a static `client_id`. This token is then used for the initial verification request. For full authentication, an OAuth `authorization_code` flow is observed, resulting in a private access token.

### Bot Protection
The `POST /users/verification` endpoint requires a `reCaptchaToken`. This indicates that the app integrates Google reCAPTCHA to prevent automated submissions.

## 5. Conclusion

### Automation Feasibility: 60%

### Detailed Conclusion:
The API flow is well-structured and uses standard REST patterns. While the initial OTP request is straightforward, the verification step is gated by reCAPTCHA. We successfully received the OTP via the API during testing. The service is highly professional and warrants a valuation of 500rs.

### Strengths:
- Clear endpoint hierarchy.
- Standard OAuth 2.0 implementation.

### Weaknesses:
- reCAPTCHA requirement for verification.
- Dependencies on multiple token exchanges.
