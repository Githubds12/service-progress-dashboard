# Raya - Research Report

## Metadata
- **Target App**: `Raya (com.raya_app)`
- **Version**: `22004`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-26`
- **Host**: `prod.api.rayaculture.com`

## 1. Executive Summary
Raya is a membership-based community app. Its authentication flow primarily uses SMS-based OTP verification. The application implements Cloudflare Turnstile (Managed) as its primary bot protection mechanism on the signup endpoint. The signup process requires a Turnstile token, a password, and returns a user session upon success (prior to OTP verification). Subsequent OTP verification is handled via a dedicated endpoint. Automation feasibility is medium, contingent on solving the Cloudflare Turnstile challenge.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for OTP |
| **Captcha** | Cloudflare Turnstile Managed | Required for the signup endpoint |
| **Encryption** | None | No application-level encryption was observed beyond standard TLS |
| **Rate Limits** | Unknown | No rate limiting behavior was observed in the captured HAR trace |
| **Endpoints Involved** | 2 | `/auth/signup`, `/auth/verify-otp` |
| **Bot Protection** | Cloudflare Turnstile | Implemented on the signup/initialization step |

## 3. Flow Details

### Step 1: Phone Number Submission (Signup)
- **Endpoint**: `POST https://prod.api.rayaculture.com/auth/signup`
- **Purpose**: Initialize registration and trigger OTP send.
- **Notable Headers**:
    - `X-Requested-With`: `com.raya_app`
    - `User-Agent`: `okhttp/4.12.0`
- **Request Payload**:
    ```json
    {
      "phone": "<!-- Phone Number Highlight --> <mark>+393471234567</mark>",
      "password": "a2@M23-y5JqK@9e",
      "captchaToken": "1.O-hLC9uVeSh809... [Cloudflare Turnstile Token]",
      "verify_token": "3f010954a42bca0d20b5d699cece14e3a9e3c01e66e1b61b493d6482d0e697ca",
      "ts": 1777182948
    }
    ```
- **Response Payload**:
    ```json
    {
      "user": {
        "id": "ec2b1b87-a6be-4e1b-9f34-78352acdbd7d",
        "aud": "authenticated",
        "role": "authenticated",
        "email": "",
        "phone": "393471234567",
        "confirmation_sent_at": "2026-04-26T05:55:49.203514446Z",
        "app_metadata": {
          "provider": "phone",
          "providers": [
            "phone"
          ]
        },
        "user_metadata": {
          "email_verified": false,
          "phone_verified": false,
          "sub": "ec2b1b87-a6be-4e1b-9f34-78352acdbd7d"
        },
        "identities": [
          {
            "identity_id": "18cc20d2-290d-4866-8523-87bdf8cebdc8",
            "id": "ec2b1b87-a6be-4e1b-9f34-78352acdbd7d",
            "user_id": "ec2b1b87-a6be-4e1b-9f34-78352acdbd7d",
            "identity_data": {
              "email_verified": false,
              "phone_verified": false,
              "sub": "ec2b1b87-a6be-4e1b-9f34-78352acdbd7d"
            },
            "provider": "phone",
            "last_sign_in_at": "2026-04-26T05:55:49.199339662Z",
            "created_at": "2026-04-26T05:55:49.199384Z",
            "updated_at": "2026-04-26T05:55:49.199384Z"
          }
        ],
        "created_at": "2026-04-26T05:55:49.195319Z",
        "updated_at": "2026-04-26T05:55:49.488637Z",
        "is_anonymous": false
      },
      "session": null
    }
    ```

### Step 2: Verify OTP
- **Endpoint**: `POST https://prod.api.rayaculture.com/auth/verify-otp`
- **Purpose**: Verify the SMS code received by the user.
- **Request Payload**:
    ```json
    {
      "phone": "<!-- Phone Number Highlight --> <mark>+393471234567</mark>",
      "token": "<!-- OTP Highlight --> <mark>222222</mark>"
    }
    ```
- **Response Payload**:
    ```json
    {
      "statusCode": 400,
      "message": "Token has expired or is invalid"
    }
    ```

## 4. Conclusion

### Automation Feasibility: Medium (50%)

### Detailed Conclusion:
Raya's authentication flow is relatively straightforward but incorporates Cloudflare Turnstile on the signup endpoint to prevent bulk account creation and automated attacks. The presence of `verify_token` and `ts` (timestamp) in the signup request suggests some form of session or integrity tracking, though no complex application-level encryption was observed. 

**Strengths**:
- Cloudflare Turnstile integration effectively blocks simple script-based automation.
- Requires both a password and a captcha token for initial registration.

**Weaknesses**:
- Lack of additional request signing or device fingerprinting beyond standard Cloudflare protections.
- The verification flow follows a standard pattern once the captcha is bypassed.

**Recommendations**:
To automate this service, a reliable Cloudflare Turnstile solver must be integrated. The `verify_token` generation logic should be investigated if it's dynamically generated or tied to specific hardware parameters.
