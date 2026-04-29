# Yamaha Motor ID - Security Analysis Report

## Metadata
- **Target URL/App**: `https://www.yamaha-motor.co.jp` / `jp.co.yamahamotor.yamahamotorcycleconnect.sccu`
- **Researcher**: `Deepanshu Singh`
- **Date**: `25-04-2026`
- **Status**: `Completed`
- **HAR Files**: `Yamaha.har`

## 1. Executive Summary
Yamaha Motor ID uses a specialized authentication infrastructure hosted on a dedicated domain (`c377768625-eu.com`). The registration process is a 3-step OTP-based flow secured by **Google reCAPTCHA Enterprise**. The system utilizes a stateful `token` that must be passed between steps (`sendotp` -> `authotp` -> `register`). Automation is feasible but requires handling reCAPTCHA Enterprise challenges and maintaining the integrity of the session token throughout the flow.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS OTP | Mobile number verification required for registration |
| **Captcha** | Google reCAPTCHA Enterprise | Required for the initial OTP request step |
| **Security Stack** | reCAPTCHA, API Key | Token-based session management with static API keys |
| **Rate Limits** | Moderate | Enforced via captcha and session token validity |
| **Endpoints Involved** | 3 | sendotp, authotp, register |

## 3. Flow Details

### Registration Flow

**Step 1: Request OTP**
- **Endpoint**: `POST https://www.c377768625-eu.com/sendotp`
- **Purpose**: Trigger SMS OTP delivery and initialize session.
- **Request Payload**:
    ```json
    {
      "phoneNumber": "+918791267460",
      "locale": "en",
      "g-recaptcha-response": "[RECAPTCHA_TOKEN]",
      "apiKey": "3_ebNf1cv6h3vwvGujn8ipy0Vwl4i0lW12fCe6WCdT39aZOr2Ab5wnpNLikFUPcjqf"
    }
    ```
- **Response**: 
    ```json
    {
      "result": 0,
      "errordetail": "000",
      "token": "pJLOZVTOnVlhGTVDXySsxUAYJSxycMXa"
    }
    ```
- **Analysis**: The `token` returned here is mandatory for the next step.

**Step 2: Verify OTP**
- **Endpoint**: `POST https://www.c377768625-eu.com/authotp`
- **Purpose**: Validate the SMS code.
- **Request Payload**:
    ```json
    {
      "phoneNumber": "+918791267460",
      "otp": "610193",
      "token": "pJLOZVTOnVlhGTVDXySsxUAYJSxycMXa",
      "apiKey": "3_ebNf1cv6h3vwvGujn8ipy0Vwl4i0lW12fCe6WCdT39aZOr2Ab5wnpNLikFUPcjqf"
    }
    ```
- **Response**:
    ```json
    {
      "result": 0,
      "errordetail": "000",
      "token": "oiIeqHagSBvdnvYiBWQvtMbpCoFKTkrJ"
    }
    ```
- **Analysis**: Upon success, a *new* `token` is returned for the final registration step.

**Step 3: Register Account**
- **Endpoint**: `POST https://www.c377768625-eu.com/register`
- **Purpose**: Finalize registration with user details.
- **Request Payload**:
    ```json
    {
      "phoneNumber": "+918791267460",
      "password": "[PASSWORD]",
      "birthYear": "1981",
      "birthMonth": "10",
      "birthDay": "8",
      "token": "oiIeqHagSBvdnvYiBWQvtMbpCoFKTkrJ",
      "apiKey": "3_ebNf1cv6h3vwvGujn8ipy0Vwl4i0lW12fCe6WCdT39aZOr2Ab5wnpNLikFUPcjqf"
    }
    ```
- **Response**:
    ```json
    {
      "result": 0,
      "errordetail": "000"
    }
    ```

## 4. Security & Reversing Notes

### 1. ReCAPTCHA Enterprise
- The app uses Google reCAPTCHA Enterprise on the `/sendotp` endpoint. This is a higher tier of protection than standard reCAPTCHA and may involve behavioral analysis.

### 2. Dedicated Domain
- Yamaha uses `c377768625-eu.com` for its identity services. This is a common pattern for "Gigya" (now SAP Customer Data Cloud) or similar CIAM providers, but here it appears to be a custom implementation for Yamaha's global ID system.

### 3. Static API Key
- The `apiKey` (`3_ebNf...`) appears to be static for the application.

## 5. Conclusion
Yamaha's authentication flow is well-structured and stateful. The use of cascading tokens ensures that each step is verified before the next can proceed. Automation requires a reliable reCAPTCHA Enterprise solver.

**Automation Feasibility: 45%** (Standard flow, but requires enterprise captcha solving).
