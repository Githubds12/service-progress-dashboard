# Galarm Reconnaissance Report

## 1. Executive Summary
Reconnaissance on the Galarm Android application (`com.galarmapp`) has identified a Firebase-driven authentication architecture. The app uses several cloud-based services for its core functionality, with a heavy emphasis on security through encryption and bot protection.

## 2. Infrastructure Details
- **Backend Infrastructure**: Google Cloud Functions (Firebase).
- **Domain**: `us-central1-migrateto3.cloudfunctions.net`.
- **SMS Provider**: `checkmobi`.
- **Bot Protection**: Google reCAPTCHA v2.
- **App Platform**: Android (com.galarmapp).

## 3. Critical Endpoints
| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/getCountriesCodesForWhatsAppVerificationHttps` | POST | Retrieves country-specific verification configuration. |
| `/sendVerificationCodeHttps` | POST | Triggers SMS OTP delivery (requires reCAPTCHA token). |
| `/verifyCodeHttps` | POST | Verifies the OTP code and completes the login/registration. |

## 4. Observed Payloads
### OTP Request Payload
```json
{
  "data": {
    "cipher": "U2FsdGVkX1...",
    "token": "0cAFcWeA5...",
    "mobileNumber": "3720511560",
    "countryCode": "39"
  }
}
```
The `cipher` field is a base64-encoded encrypted string (Salted__). The `token` is a reCAPTCHA v2 token.

## 5. Security Posture
- **Request Signing/Encryption**: All sensitive requests use a `cipher` field, indicating the data is encrypted on the client side.
- **Challenge-Response**: Integration of reCAPTCHA at the network level prevents simple automated code bombing.
- **Provider Redundancy**: The app queries for country-specific WhatsApp/SMS codes, suggesting a flexible verification logic.

## 6. Conclusion
Galarm's authentication flow is well-protected against basic automation attempts. The combination of Google's bot protection and client-side encryption provides a robust defense for the registration process.
