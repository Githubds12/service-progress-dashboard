# Nestle Waters - Security Analysis Report

## Metadata
- **Target URL/App**: `https://www.buyonline.nestlewaters.ae` / `com.nestle.multibrandwaters.purelife`
- **Researcher**: `Deepanshu Singh`
- **Date**: `25-04-2026`
- **Status**: `Completed`
- **HAR Files**: `NestleWater.har`

## 1. Executive Summary
Nestle Waters (Pure Life) mobile application implements a standard Magento-based (Adobe Commerce) backend with additional security layers including Akamai Bot Manager and Google reCAPTCHA. The authentication flow is centered around mobile number verification via OTP. While the primary business logic is standard, the integration of Akamai on the Egypt-specific endpoints (`nestlewatersegypt.com`) and reCAPTCHA on both UAE and Egypt endpoints provides significant protection against automated attacks. Automation is feasible but requires handling reCAPTCHA tokens and potentially bypassing Akamai's browser-environment checks.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS OTP | Mobile number based verification |
| **Captcha** | Google reCAPTCHA | Integrated into auth endpoints (sendotp, registration) |
| **Security Stack** | Akamai, Firebase | Akamai Bot Manager detected; Firebase for installations and logging |
| **Rate Limits** | Moderate | Handled via session and captcha requirements |
| **Endpoints Involved** | 4 | mobileinit, sendotp, verifyotp, customerregistration |

## 3. Flow Details

### Authentication Flow (Egypt/UAE)

**Step 1: Mobile Initialization**
- **Endpoint**: `POST /rest/en/V1/mobileinit`
- **Purpose**: Retrieve app configuration, country codes, and security flags (e.g., `is_recaptcha_enable`).
- **Request Payload**:
    ```json
    {
      "customerlanguage": "en",
      "device_token": "",
      "device_type": "android",
      "lat": 0.0,
      "long": 0.0,
      "version": "2.0.69"
    }
    ```
- **Response**: 
    ```json
    {
      "code": 200,
      "status": true,
      "message": "Data fetched successfully",
      "data": [
        {
          "cart_item_count": 0,
          "current_language": "ar_SA",
          "currency": "AED",
          "is_recaptcha_enable": true,
          "payment_currency": "AED",
          "categories": [...],
          "countries": [...],
          "mobile_country_code": [{"key": 971, "value": "+971"}, ...]
        }
      ]
    }
    ```

**Step 2: Request OTP**
- **Endpoint**: `POST /rest/en/V1/mobile/sendotp`
- **Purpose**: Send a verification code to the user's mobile number.
- **Request Payload**:
    ```json
    {
      "customer_mobile": "+918791267460",
      "customer_mobile_code": "+91",
      "device_type": "android",
      "lat": 0.0,
      "long": 0.0,
      "recaptchaToken": "0cAFcWeA..." 
    }
    ```
- **Response**:
    ```json
    {
      "code": 200,
      "status": true,
      "message": "OTP sent to your mobile number.",
      "data": [
        {
          "customer_mobile": "+918791267460"
        }
      ]
    }
    ```

**Step 3: Verify OTP**
- **Endpoint**: `POST /rest/en/V1/mobile/verifyotp`
- **Purpose**: Validate the 6-digit code received via SMS.
- **Request Payload**:
    ```json
    {
      "customer_mobile": "+918791267460",
      "email": " ",
      "lat": 0.0,
      "long": 0.0,
      "password": " ",
      "validation_code": "188379"
    }
    ```
- **Response**: 
    ```json
    {
      "code": 200,
      "status": true,
      "message": "OTP verified.",
      "data": [
        {
          "customer_mobile": "+918791267460",
          "redirect": "customerregistration"
        }
      ]
    }
    ```

**Step 4: Customer Registration**
- **Endpoint**: `POST /rest/en/V1/customer/customerregistration`
- **Purpose**: Finalize user profile and obtain session tokens.
- **Request Payload**:
    ```json
    {
      "consent": 1,
      "customer_mobile": "+918791267460",
      "customerToken": "zuE9d4QxItiRNEgKSTMTt2stWE3ycxNw",
      "device_type": "android",
      "dob": "",
      "email": "deepanshusinghdigitalheroes@gmail.com",
      "firstname": "Deepanshu ",
      "gender": 1,
      "lastname": "Singh",
      "lat": 0.0,
      "long": 0.0,
      "optin": 0,
      "password": "1VGtf5JJiNHAnO3bH79FKQ==",
      "recaptchaToken": "0cAFcWeA..."
    }
    ```
- **Response**: 
    ```json
    {
      "code": 200,
      "status": true,
      "message": "User logged in successfully",
      "data": [
        {
          "user_id": 124322,
          "email": "deepanshusinghdigitalheroes@gmail.com",
          "firstname": "Deepanshu ",
          "lastname": "Singh",
          "mobile_no": "+918791267460",
          "customer_token": "eyJraWQiOiIxIiw...",
          "quote_id": 2020711,
          "redirect": "customerlogin"
        }
      ]
    }
    ```

## 4. Security & Reversing Notes

### 1. Akamai Bot Manager
- **Detection**: The presence of `_abck` and `ak_bmsc` cookies, along with calls to `/_bm/get_params`, confirms Akamai Bot Manager.
- **Impact**: Akamai monitors TLS fingerprints and browser behavior. Automated scripts must handle cookie rotation and sensor data submission if challenged.

### 2. Google reCAPTCHA
- **Implementation**: The app uses reCAPTCHA tokens in `sendotp` and `customerregistration`.
- **Bypass Difficulty**: High. Requires a captcha solving service or manual intervention. The backend validates the token server-side.

### 3. Firebase & Pushwoosh
- **Firebase**: Used for installation tracking (`firebaseinstallations.googleapis.com`) and analytics.
- **Pushwoosh**: Used for event tracking and screen opening logs (`PW_ScreenOpen`).

### 4. Encryption
- **Passwords**: Passwords in the registration payload appear to be processed (e.g., `1VGtf5JJiNHAnO3bH79FKQ==`). Further reversing of the Android binary would be required to determine the exact encryption/hashing algorithm used before submission.

## 5. Conclusion
The Nestle Waters app is well-protected against basic automation due to reCAPTCHA and Akamai. However, the API structure is clear and follows standard Magento REST patterns. Successful automation would require a sophisticated environment that can solve/provide reCAPTCHA tokens and maintain Akamai-compliant session states.

**Automation Feasibility: 40%** (Mainly limited by reCAPTCHA and potential Akamai challenges).
