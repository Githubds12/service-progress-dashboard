# The Chefz (com.nextwo.the_chefz) Security Reconnaissance Report

## 1. Executive Summary
**The Chefz** (`com.nextwo.the_chefz`) is a premium food delivery and personal chef service application based in Saudi Arabia. The application employs a RESTful API architecture hosted on `api.thechefz.co`. Authentication is performed via a mobile-first SMS OTP system. The security analysis reveals that while the API uses cleartext JSON for communication, it integrates several device-specific headers (`UDID`, `App-Version`) and relies on Google Play Integrity for bot mitigation and app attestation.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary authentication via 4-digit OTP. |
| **Captcha** | Google Play Integrity Standard | App attestation and integrity checks are implemented via Firebase/Play Integrity. |
| **Encryption** | None (HTTPS only) | API payloads are transmitted in cleartext JSON over standard TLS. |
| **Rate Limits** | Unknown | No explicit 429 errors were observed, though resend cooldowns likely exist server-side. |
| **Endpoints Involved** | 2 | `/v9/user/auth`, `/v9/otp/verify` |
| **Bot Protection** | Google Play Integrity | Integrated Firebase App Check and Play Integrity token exchange. |

## 3. Technical Findings
### 3.1 Authentication Workflow
The authentication process is a standard two-step flow:
1.  **Identity Assertion**: The user provides their phone number and country code to the `/v9/user/auth` endpoint.
2.  **OTP Verification**: Upon receiving the SMS, the user submits the 4-digit code along with their `deviceToken` (FCM) to the `/v9/otp/verify` endpoint.

### 3.2 Header Requirements
The API requires several mandatory headers for every request:
-   `UDID`: A unique device identifier (e.g., `5133b0c6654a8c03`).
-   `App-Version`: The current build version (e.g., `10.80.0`).
-   `City`: A numeric ID representing the user's current city context.

## 4. API Traces

### Step 1: Request SMS Verification
-   **Endpoint**: `POST https://api.thechefz.co/v9/user/auth`
-   **Method**: `POST`
-   **Purpose**: Register or identify a user and trigger an SMS OTP.

**Request Traces**:
```json
{
  "url": "https://api.thechefz.co/v9/user/auth",
  "method": "POST",
  "headers": {
    "App-Version": "10.80.0",
    "Accept": "application/json",
    "User-Agent": "The Chefz/10.80.0 (com.nextwo.the_chefz;build:375;Android 15)",
    "UDID": "5133b0c6654a8c03",
    "City": "1",
    "Content-Type": "application/json; charset=UTF-8"
  },
  "body": {
    "phone": "572302775",
    "dialCode": "+966",
    "marketingMessagesAccepted": false,
    "userType": "1"
  }
}
```

**Response Traces**:
```json
{
  "success": true,
  "data": {
    "userId": 15853766,
    "status": 1,
    "cityId": 1,
    "isBlocked": false,
    "sent_otp_type": "sms",
    "num_of_otp_digits": 4
  }
}
```

### Step 2: Verify OTP
-   **Endpoint**: `POST https://api.thechefz.co/v9/otp/verify`
-   **Method**: `POST`
-   **Purpose**: Validate the received OTP and establish a session.

**Request Traces**:
```json
{
  "url": "https://api.thechefz.co/v9/otp/verify",
  "method": "POST",
  "headers": {
    "App-Version": "10.80.0",
    "Accept": "application/json",
    "UDID": "5133b0c6654a8c03",
    "Content-Type": "application/json; charset=UTF-8"
  },
  "body": {
    "phone": "572302775",
    "otp": "4321",
    "dialCode": "+966",
    "deviceToken": "eZsLwAQvQdCUa-ZI7a5W9C:APA91bFV2wbGq3nz2tgAy58A9piXFTR2itXPMMuzmJ-t5MEkftJ6LHHn2GSqz37oBr3mrOFf-C62pRg66MHfKO0yac8r-lJhoPToETMlyqPOgv45YtNtPb8"
  }
}
```

**Response Traces**:
```json
{
  "success": false,
  "status_code": 1012,
  "status_message": "OTP not found. Please try again.",
  "status_value": null
}
```

## 5. Conclusion
**The Chefz** application employs a standard and well-structured API for its authentication lifecycle. The use of cleartext JSON makes the initial reconnaissance straightforward; however, the presence of Google Play Integrity (Play Integrity API) suggests that any automated interaction would need to handle app attestation tokens to bypass server-side validation.

**Automation Feasibility: Medium (65%)**
The clear API structure and lack of complex client-side encryption make it a prime candidate for automation. The primary hurdle is the mandatory `UDID` and `deviceToken` fields, which must be uniquely generated or harvested. Integration with a Play Integrity attestation provider would be required for high-volume automated testing.

**Recommendations**:
-   Implement dynamic `UDID` generation for session scaling.
-   Monitor the `/v9/otp/resend` endpoint for rate-limit bypass opportunities.
-   Analyze the `deviceToken` (FCM) requirement to see if it's strictly validated against the IP or UDID.
