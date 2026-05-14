# Galarm - Research Report

## Metadata
- **Target URL/App**: `galarmapp.com` / `com.galarmapp`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-08`
- **Status**: `Completed`
- **HAR Files**: `galarm.har`

## 1. Executive Summary
Galarm (com.galarmapp) implements a secure authentication flow using Firebase Cloud Functions (migrateto3) and Google reCAPTCHA v2. The application utilizes a multi-step verification process involving reCAPTCHA solving, encrypted payload submission, and OTP delivery via the Checkmobi provider. Automation feasibility is low due to the combination of reCAPTCHA v2 and AES-encrypted payloads (`cipher` field).

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Verified via Checkmobi provider |
| **Captcha** | reCAPTCHA v2 Checkbox (Google) | Mandatory for triggering OTP delivery |
| **Encryption** | AES-256-CBC (Salted__) | Sensitive request data is encrypted in the `cipher` field |
| **Rate Limits** | Unknown | No rate limiting observed in the single flow capture |
| **Endpoints Involved** | 3 | `/getCountriesCodesForWhatsAppVerificationHttps`, `/sendVerificationCodeHttps`, `/verifyCodeHttps` |
| **Bot Protection** | Google reCAPTCHA v2 | Implemented on the `/sendVerificationCodeHttps` endpoint |

## 3. Flow Details

### Flow 1: Registration / Login

**Step 1: Solve reCAPTCHA**
- **Endpoint**: `POST https://www.google.com/recaptcha/api2/userverify`
- **Purpose**: Solve a reCAPTCHA v2 challenge to obtain a verification token.
- **Analysis**: The resulting token is required for the subsequent OTP request.

**Step 2: Request OTP Code**
- **Endpoint**: `POST https://us-central1-migrateto3.cloudfunctions.net/sendVerificationCodeHttps`
- **Purpose**: Trigger SMS OTP delivery to the provided phone number.
- **Notable Headers**:
    - `Firebase-Instance-ID-Token`: `fstBkQB2TGCtBwr5ZtU5Wk:APA91bEVfW3E8q_1arEiC3RxUFK9YtDa42BKI03xNiq...`
    - `X-Firebase-AppCheck`: `eyJlcnJvciI6IlVOS05PV05fRVJST1IifQ==`
- **Request Payload**:
    ```json
    {
      "data": {
        "cipher": "U2FsdGVkX19U72Zk01JcEWYqI/I4QiUfvxe1yWPoRGaOEDgDhzlzvmujKfhGBfvrd6UJvM6OLVyc4GAtWsDpsquRTN+//O2/pwgCUGS/4y5gSrNgZ5Da6ZlEa9EWNuR46t94U2Jxfx7U+qk3oqbWD/OBoSOwEjWFJTnHVnbkXwFI=",
        "apiVersion": "v2",
        "os": "android",
        "fromUid": null,
        "mobileNumber": "3720511560",
        "countryCode": "39",
        "ip": "49.43.161.81",
        "token": "0cAFcWeA5hmPl0JBtrk7beJ0APgamGldryfIqehWzMLN7XfkA2x_Uwjgjo3S3Ef8a6rX5FEsICGWZT6NNocLrpprR0td6Hx_3bdhjaL18LLwto2iHo9Ro1qZQHKrzoH1enPqizceL2HFLbTp2vGpCxRCzHWhbIZ54EYNwlrD5-NtAcs6WVjRPVGSQi-HGBo-qXluKsAfnBFKAaP5afv_C6hmWhoWyRq6v3h8jgHUkLvvvhI6un4q2RuxSduGpNlZgt0nYk--wz5SW1jtVCNzcKkGmGm4Tl8zMhUF_4ArxFK96NuSdZAn_BOyY8HXarRicXTjgTKDfxlr-CqZXNH937m1BqvsGwNwjPmrd4M8aHRWg-_zl_k8wadfMciz1xLdPoHNd_TiKkgG3JViO6a6Xa_zl2fj6ub43FV1asNHQIcTPCS-e5HVCVPC1IlMZ5mZeKtleZ389IegH1LvoyuTLcetKdUbHsOXU1jV..."
      },
      "cca2": "IT"
    }
    ```
- **Response**:
    ```json
    {
      "result": {
        "status": "success",
        "result": {
          "requestId": "SMS-A1BB3D81-8686-7A2F-9722-3A4D8D657B7F",
          "source": "checkmobi"
        }
      }
    }
    ```
- **Analysis**: This endpoint is the **Phone Number Submitting Endpoint**. It requires the reCAPTCHA token and an encrypted `cipher` blob.

**Step 3: Verify OTP Code**
- **Endpoint**: `POST https://us-central1-migrateto3.cloudfunctions.net/verifyCodeHttps`
- **Purpose**: Verify the OTP code received via SMS.
- **Request Payload**:
    ```json
    {
      "data": {
        "cipher": "U2FsdGVkX18fDHn6zaBEcWR+l3iWcV6wbs/KG2W5VkikyohPRR0wR/HIiJ+jMQIfppmNTSJWOA26rVRyTSd5wysA1aAtT0Vu2iR6NDiTU/UFeXv7g/FPAfBnb0wbR0Abelqhb6r0WgoRYisnWUurZa/yGSHqefOHe7dZkNJQVgU=",
        "code": "2514",
        "os": "android",
        "mobileNumber": "3720511560",
        "ip": "49.43.161.81",
        "phoneId": "819dbd62-4722-4863-b0ca-a0e0dbe445e2",
        "source": "checkmobi",
        "apiVersion": "v2",
        "requestId": "SMS-A1BB3D81-8686-7A2F-9722-3A4D8D657B7F",
        "countryCode": "39",
        "cca2": "IT"
      }
    }
    ```
- **Response**:
    ```json
    {
      "result": {
        "status": "failure",
        "error": "Please check the code and try again."
      }
    }
    ```
- **Analysis**: Final verification step. Returns a status message indicating success or failure.

## 4. Security & Reversing Notes

### Encryption/Signing Mechanisms
- **AES Encryption (Salted__)**: The `cipher` field in request payloads contains data encrypted using AES. The "Salted__" prefix suggests the use of OpenSSL's standard key derivation (EVP_BytesToKey). Reversing this would require identifying the secret key and IV within the Android APK (likely obfuscated).
- **reCAPTCHA v2**: The code delivery endpoint is guarded by a mandatory reCAPTCHA v2 token, making headless automation difficult.

## 5. Conclusion
### Automation Feasibility: 15%
Automation is highly difficult due to the mandatory reCAPTCHA v2 challenge and the use of encrypted payloads for all critical verification steps. Bypassing these measures would require significant reverse engineering of the encryption logic and integration with a captcha-solving service.
