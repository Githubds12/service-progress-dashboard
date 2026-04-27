# Sage - Research Report

## Metadata
- **Target URL/App**: `com.sage.accounting`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-27`
- **Status**: `Completed`
- **HAR Files**: `Sage.har`

## 1. Executive Summary
Sage (com.sage.accounting) implements a secure authentication and enrollment flow using Sage ID (powered by Auth0). The process involves selecting a multi-factor authentication (MFA) method, submitting a phone number for SMS enrollment, and verifying the received OTP. The flow is managed through a series of redirects and POST requests to the `id.sage.com` domain, utilizing a `state` parameter to maintain session integrity. No captcha or complex bot protection was observed during the documented flow.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | primary channel for OTP |
| **Captcha** | undefined | No captcha was observed during the testing |
| **Encryption** | None | Standard HTTPS with session-based `state` tracking |
| **Rate Limits** | Unknown | No rate limiting behavior was observed during testing |
| **Endpoints Involved** | 3 | `/u/mfa-enroll-options`, `/u/mfa-phone-enrollment`, `/u/mfa-sms-enrollment-verify` |
| **Bot Protection** | Auth0 | Managed MFA flow via Auth0 |

## 3. Flow Details

### Flow 1: MFA Enrollment (SMS)

**Step 1: Choose MFA Option**
- **Endpoint**: `POST https://id.sage.com/u/mfa-enroll-options`
- **Purpose**: Select "phone" as the MFA enrollment method.
- **Request Headers**:
    - `Content-Type`: `application/x-www-form-urlencoded`
    - `Host`: `id.sage.com`
- **Request Payload**:
    ```text
    state=hKFo2SBSRFdzUUNGYlg4c3pEY1JEdjUwbldaZUdMTk9hdVlBX6Fuqm1mYS1lbnJvbGyjdGlk2SB0QTFfUzdscXptRzR3V3hrZkxNOHpwNlZ5NVNXRWMyM6NjaWTZIEsxODVlVE9aTlliemFsazZIQTFVa2N2dFV0NTVETWpi&action=phone
    ```
- **Response**:
    - **Status**: `302 Found`
    - **Location**: `/u/mfa-phone-enrollment?state=...`

**Step 2: Submit Phone Number (SMS Request)**
- **Endpoint**: `POST https://id.sage.com/u/mfa-phone-enrollment`
- **Purpose**: Submit the user's phone number to receive an OTP via SMS. <!-- Phone Number Submitting Endpoint -->
- **Request Headers**:
    - `Content-Type`: `application/x-www-form-urlencoded`
    - `Host`: `id.sage.com`
- **Request Payload**:
    ```text
    state=hKFo2SBSRFdzUUNGYlg4c3pEY1JEdjUwbldaZUdMTk9hdVlBX6Fuqm1mYS1lbnJvbGyjdGlk2SB0QTFfUzdscXptRzR3V3hrZkxNOHpwNlZ5NVNXRWMyM6NjaWTZIEsxODVlVE9aTlliemFsazZIQTFVa2N2dFV0NTVETWpi&phone=8791267460&type=sms
    ```
- **Response**:
    - **Status**: `302 Found`
    - **Location**: `/u/mfa-sms-enrollment-verify?state=...`

**Step 3: Verify OTP**
- **Endpoint**: `POST https://id.sage.com/u/mfa-sms-enrollment-verify`
- **Purpose**: Verify the OTP received via SMS.
- **Request Headers**:
    - `Content-Type`: `application/x-www-form-urlencoded`
    - `Host`: `id.sage.com`
- **Request Payload**:
    ```text
    state=hKFo2SBSRFdzUUNGYlg4c3pEY1JEdjUwbldaZUdMTk9hdVlBX6Fuqm1mYS1lbnJvbGyjdGlk2SB0QTFfUzdscXptRzR3V3hrZkxNOHpwNlZ5NVNXRWMyM6NjaWTZIEsxODVlVE9aTlliemFsazZIQTFVa2N2dFV0NTVETWpi&code=867009
    ```
- **Response**:
    - **Status**: `302 Found`
    - **Location**: `/u/mfa-recovery-code-enrollment?state=...`
- **Analysis**: Upon successful verification, the user is redirected to the recovery code enrollment step.

## 4. Conclusion

### Automation Feasibility: High > 70%
The authentication flow for Sage is straightforward as it relies on standard Auth0 MFA patterns. The `state` parameter is the only dynamic token that needs to be tracked across redirects. No advanced bot protection, captchas, or custom header signing were observed, making this flow highly feasible for automation.

### Detailed Conclusion
The Sage (com.sage.accounting) MFA enrollment flow is implemented via Auth0 on the `id.sage.com` domain. The process is robust yet lacks aggressive anti-automation measures such as image challenges or behavioral analysis. Security is primarily handled through session-bound state tokens. Automation is achievable by correctly handling the sequences of redirects and maintaining the state parameter throughout the flow. It is recommended to monitor for any future implementation of Cloudflare Turnstile or reCAPTCHA Enterprise which Auth0 can easily integrate.
