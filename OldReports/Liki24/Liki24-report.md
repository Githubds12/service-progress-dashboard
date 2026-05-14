## 1. Executive Summary
The security analysis of Liki24 (**`com.liki24.customerapp`**) focuses on the registration and phone verification workflow. The application employs a two-step authentication process: user registration followed by SMS OTP verification. While the app integrates **Firebase App Check** and **Google Play Integrity** for bot protection, the core registration and verification endpoints are accessible via a PHP-based API. The analysis revealed that a **`customerId`** is assigned immediately upon registration, even before the OTP is verified.

## 2. Application Information
- **App Name**: Liki24
- **Package Name**: **`com.liki24.customerapp`**
- **Version**: **`2.2.13`**
- **Main Host**: **`api.liki24.it`**

## 3. Authentication Flow Analysis
The authentication process consists of an initial registration request that triggers an SMS, followed by a code submission.

### 3.1 OTP Request (Registration)
- **Endpoint**: **`https://api.liki24.it/index.php?route=api/customer/registration/`**
- **Method**: **`POST`**
- **Query Parameter**: **`smsHashCode`** (used for automatic SMS reading on Android).
- **Request Trace**:
```json
{
  "telephone": "**393471234567**",
  "firstname": "Deepanshu ",
  "lastname": "Singh",
  "password": "..."
}
```
- **Response Trace**:
```json
{
  "customerId": 103402
}
```

### 3.2 OTP Verification
- **Endpoint**: **`https://api.liki24.it/index.php?route=api/customer/verify/`**
- **Method**: **`POST`**
- **Request Trace**:
```json
{
  "code": "**106145**",
  "telephone": "**393471234567**",
  "firebaseToken": ""
}
```
- **Response Trace (Incorrect Code)**:
```text
"Wrong code 106145"
```

## 4. Security Mechanisms
- **Bot Protection**: The application includes **Firebase App Check** and **Play Integrity** triggers (`generatePlayIntegrityChallenge`), although the primary registration endpoints do not strictly enforce these tokens for basic functionality.
- **SMS Hash Code**: The `smsHashCode` parameter is used to facilitate the **SMS Retriever API** on Android, allowing the app to automatically read the incoming verification code.

## 5. Vulnerability Assessment
- **Early ID Assignment**: The server returns a `customerId` before the phone number is verified. This could potentially be abused to enumerate user accounts or create unverified profiles.
- **Rate Limiting**: No explicit rate limits were observed on the `registration` endpoint during the traffic capture, which may lead to SMS flooding if not managed on the backend.

## 6. Conclusion
Liki24 implements a standard registration-first OTP flow. While the inclusion of modern bot protection frameworks (Firebase/Google) shows a proactive security stance, the reliance on a legacy-style PHP API route for critical authentication steps suggests areas for further hardening, particularly in enforcing verification before resource allocation.
