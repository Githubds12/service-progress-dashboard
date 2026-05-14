# WestStein - Research Report

## Metadata
- **Target URL/App**: `com.weststeincard.weststein`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-02`
- **Status**: `Completed`
- **HAR Files**: `WestStein.har`

## 1. Executive Summary
WestStein Card provides a mobile banking experience with a two-step verification process for new registrations. The platform uses a JWT-based authentication system. The registration flow involves an initial email verification followed by a phone number validation step. The initial registration request is protected by Google reCAPTCHA v2, while subsequent verification steps utilize numeric codes.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | Email & SMS | Two-step verification (Email token then Phone OTP) |
| **Captcha** | reCAPTCHA v2 (Google) | Observed in the initial registration/apply step |
| **Encryption** | None | Standard JSON payloads over HTTPS, JWT for session |
| **Rate Limits** | Unknown | No rate limiting behavior was observed during testing |
| **Endpoints Involved** | 4 | `/api/apply/private`, `/api/user/confirm`, `/api/user/phone/validate`, `/api/user/phone/confirm-validation` |
| **Bot Protection** | Google reCAPTCHA | Implemented on the registration endpoint |

## 3. Flow Details

### Flow 1: User Registration & Verification

**Step 1: Initial Application (Registration)**
- **Endpoint**: `POST https://api.weststeincard.com/api/apply/private`
- **Purpose**: Submit user details and trigger email verification.
- **Request Headers**:
    ```text
    Content-Type: application/json
    User-Agent: okhttp/4.11.0
    ```
- **Request Body**:
    ```json
    {
      "address": {"city": "Haap", "country": 72, "line1": "82 abbjjs", "postalCode": "23551"},
      "dateOfBirth": "01-02-1998",
      "email": "deepanshusingh@example.com",
      "firstName": "Deepanshu",
      "lastName": "Singh",
      "password": "[PASSWORD]",
      "phone": "3519884403",
      "phoneCountry": 72,
      "g-recaptcha-response": "[RECAPTCHA_TOKEN]"
    }
    ```
- **Response Body**:
    ```json
    {
      "messages": [],
      "errors": null,
      "response": {"id": 711742736, "firstName": "DEEPANSHU", "lastName": "SINGH", "verified": false, "phoneVerified": false}
    }
    ```

**Step 2: Confirm Email / Initial Token**
- **Endpoint**: `POST https://api.weststeincard.com/api/user/confirm/721150`
- **Purpose**: Verify the initial token sent to the user's email.
- **Request Headers**:
    ```text
    X-Android-Package: com.weststeincard.weststein
    authorization: Bearer eyJhbGciOiJIUzUxMiJ9...
    ```
- **Response Body**:
    ```json
    {
        "messages": [],
        "errors": null,
        "response": null
    }
    ```

**Step 3: Request Phone Validation (OTP)**
- **Endpoint**: `GET https://api.weststeincard.com/api/user/phone/validate`
- **Purpose**: Trigger the SMS OTP delivery.
- **Response Body**:
    ```json
    {
        "messages": [],
        "errors": null,
        "response": null
    }
    ```

**Step 4: Confirm Phone Validation**
- **Endpoint**: `POST https://api.weststeincard.com/api/user/phone/confirm-validation?code=333333&language=EN`
- **Purpose**: Verify the 6-digit SMS OTP.
- **Response Body**:
    ```json
    {
      "messages": [],
      "errors": [
        {
          "field": "code",
          "id": "schemas.invalid",
          "defaultMessage": "Invalid verification code",
          "variables": null
        }
      ],
      "response": null
    }
    ```

## 4. Security & Reversing Notes

### Authentication
WestStein uses Bearer JWT tokens for session management. The token contains the user's email and session UUID.

### Bot Protection
The initial `/api/apply/private` request requires a `g-recaptcha-response` token. This indicates that WestStein has implemented Google reCAPTCHA to prevent automated account creation. However, the subsequent email and phone verification steps do not appear to have additional CAPTCHA gates.

### Tracking
The app heavily uses Google Tag Manager (`gtag-event`) to track every step of the registration flow, including `mob_registration_successful` and `mob_email_verification_completed`.

## 5. Conclusion

### Automation Feasibility: 85%

### Detailed Conclusion:
The WestStein registration flow is well-structured and follows predictable REST patterns. While the initial registration is protected by reCAPTCHA, the verification lifecycle (Email & SMS) is straightforward once a session is established. Automation is feasible but requires handling the initial CAPTCHA challenge.

### Strengths:
- Simple RESTful API.
- Clear two-step verification flow.

### Weaknesses:
- Google reCAPTCHA protection on registration.
- Two-step verification (Email + SMS).
