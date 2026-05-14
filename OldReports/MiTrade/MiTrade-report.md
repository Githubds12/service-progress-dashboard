# MiTrade - Security Analysis Report

## Metadata
- **Target URL/App**: `https://www.mitrade.com` / `com.mitrade.mobile`
- **Researcher**: `Deepanshu Singh`
- **Date**: `25-04-2026`
- **Status**: `Completed`
- **HAR Files**: `MiTrade.har`

## 1. Executive Summary
MiTrade is a multi-asset trading platform that employs significant security measures for its mobile application. The authentication flow is primarily OTP-based (SMS) but is heavily guarded by two different captcha systems: **Google reCAPTCHA** and **hCaptcha**. The app communicates with a secondary API domain (`app.mokmoki.com`) to manage authentication and user profiles. Automation is technically feasible but requires the integration of advanced captcha-solving services and strict adherence to a ticket-based session flow.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS OTP | Mobile number verification required for registration |
| **Captcha** | Google reCAPTCHA / hCaptcha | Dual integration; tokens required for OTP and signup |
| **Security Stack** | reCAPTCHA, hCaptcha, Adjust | Uses multiple external security and tracking providers |
| **Rate Limits** | High | Enforced via captcha validation and ticket expiration |
| **Endpoints Involved** | 3 | verification-codes, verification/submit, signup |

## 3. Flow Details

### Registration Flow

**Step 1: Request OTP**
- **Endpoint**: `POST https://app.mokmoki.com/api/v1/misc/verification-codes`
- **Purpose**: Trigger SMS OTP delivery.
- **Request Payload**:
    ```text
    phoneNumber=8791267460&method=SMS&countryCallingCode=91&purpose=REGISTER&reCAPTCHAToken=[TOKEN]&reCAPTCHAPlatform=google
    ```
- **Response**: 
    ```json
    {
      "success": true
    }
    ```
- **Analysis**: The `reCAPTCHAToken` is validated server-side. The app may switch to `reCAPTCHAPlatform=hcaptcha` if challenged.

**Step 2: Submit Verification Code**
- **Endpoint**: `POST https://app.mokmoki.com/api/v1/customers/verification/submit`
- **Purpose**: Validate the SMS code and obtain a session ticket.
- **Request Payload**:
    ```text
    code=449720&countryCallingCode=91&mobileNumber=8791267460&type=REGISTER
    ```
- **Response**:
    ```json
    {
      "success": true,
      "value": {
        "ticket": "530DF250AC4B4F9AB789918BB6CE5837"
      }
    }
    ```
- **Analysis**: The `ticket` is a single-use token valid for the next signup step.

**Step 3: Complete Signup**
- **Endpoint**: `POST https://app.mokmoki.com/api/v1/customers/signup`
- **Purpose**: Finalize account creation with a password and session ticket.
- **Request Payload**:
    ```text
    password=[PASSWORD]&baseCurrencyCode=USD&ticket=530DF250AC4B4F9AB789918BB6CE5837&countryCallingCode=91&mobileNumber=8791267460&registerCountryCode=IN&rememberMe=true&source=app_android
    ```
- **Response**:
    ```json
    {
      "success": true,
      "value": {
        "mode": "DEMO",
        "userToken": "CF5513D78CAC1270BBA8522FF404B283"
      }
    }
    ```
- **Analysis**: Returns the `userToken` (Bearer-like token) for authorized API calls.

## 4. Security & Reversing Notes

### 1. Dual Captcha Protection
- MiTrade integrates both Google reCAPTCHA v2/v3 and hCaptcha. This redundancy allows the server to pivot challenges if one provider is bypassed or fails to verify the user.
- Automation scripts must implement handlers for both providers and include the correct `reCAPTCHAPlatform` parameter.

### 2. Ticket-Based Flow
- The use of a `ticket` in Step 2 creates a stateful verification flow. This prevents attackers from skipping the OTP verification step and proceeding directly to registration.

### 3. API Obfuscation
- Using `app.mokmoki.com` instead of a direct `mitrade.com` subdomain is a common tactic to obscure API infrastructure and potentially use specialized proxy/WAF protections.

## 5. Conclusion
MiTrade's security is robust due to its heavy reliance on two distinct captcha providers. The API design is clean but strictly stateful. Automated interaction requires a high-quality captcha solver and precise session management.

**Automation Feasibility: 35%** (High effort due to dual-captcha logic).
