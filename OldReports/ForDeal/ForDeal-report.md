# Fordeal - Research Report

## Metadata
- **Target URL/App**: `com.fordeal.android`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-03`
- **Status**: `Completed`
- **HAR Files**: `ForDeal.har`

## 1. Executive Summary
Fordeal implements a sophisticated mobile API architecture with custom request signing and device tracking. The authentication flow primarily relies on SMS-based OTP verification. The application uses a custom gateway (`gw.fordeal.com`) with complex headers including `sign` (request signature) and `f-g` (likely an encrypted device/session payload). Automation feasibility is Medium to Low due to the requirement of correctly generating these signatures and managing session-bound tokens like `gw-token` and `ca-token`.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | primary channel for OTP |
| **Captcha** | undefined | No captcha was observed during the captured flow |
| **Encryption** | Custom Signing & Encrypted Headers | `sign` header for request integrity and `f-g` for device tracking |
| **Rate Limits** | Unknown | No rate limiting behavior was observed during testing |
| **Endpoints Involved** | 2 | `dwp.customerCenter.captchaSend`, `dwp.customerCenter.signIn` |
| **Bot Protection** | Custom | Custom API signatures and device fingerprinting implemented |

## 3. Flow Details

### Flow 1: Phone Number Login / Sign-in

**Step 1: Send OTP (SMS Request)**
- **Endpoint**: `POST https://gw.fordeal.com/gw/dwp.customerCenter.captchaSend/2`
- **Purpose**: Request an OTP code via SMS to the provided phone number.
- **Notable Headers**:
    - `gw-did`: `3c1dee66-0ba2-43f1-88b9-3ac5590fe8a3` (Device ID)
    - `sign`: `721fb1ac27fb30ee7190e1b99c0dc7a5` (Request signature)
    - `f-g`: `SwYWmCKP6RSoR5bKPeFA/yPBtF3t86R1qPg7vzJpb4HGKsuOYNEiXMwPwcaJ1OeTktfoqK3iKByeuEj7sSIihiJfKYGpuZAdUiwRVQJXngUoKl2GXY9O2YtxRg2NjdLsxLX+X4fLgB+GEbkE3JDr9YfBNgA/UZfqJpl1S3/k1Ygkf3b35iKAGoo5ghwrTQ/rfGo3bmn19VXpzvCxXb0Iof+G1UHapGkTeoMsv8daYlqo6julalSQ/Crcb0e/PiCBwgR+NAgFGBDBe3N85N/DpRZ7m733CMXLiJkn1m70PGlioGdDXRsgCKyDRJkGFpcEKdrpMrUd+3EKeXWaPdWpGA==`
- **Request Payload**:
    ```json
    {
      "number": "+393515889024",
      "signFrom": "SIGN_IN"
    }
    ```
- **Response**:
    ```json
    {
      "api": "dwp.customerCenter.captchaSend",
      "code": 1001,
      "data": true,
      "dmsg": "",
      "msg": "",
      "v": "2"
    }
    ```

**Step 2: Verify OTP & Sign-in**
- **Endpoint**: `POST https://gw.fordeal.com/gw/dwp.customerCenter.signIn/1`
- **Purpose**: Verify the received OTP and authenticate the user.
- **Notable Headers**:
    - `gw-did`: `3c1dee66-0ba2-43f1-88b9-3ac5590fe8a3`
    - `sign`: `[Dynamic Signature]`
    - `f-g`: `[Encrypted Payload]`
- **Request Payload**:
    ```json
    {
      "blackBox": "oGPEM1777804915KgJN4quK7k8",
      "loginKey": "+393515889024",
      "quickSignFrom": "SIGN_IN",
      "quickSignTag": false,
      "registerNewAccountTag": false,
      "secret": "3625",
      "type": "PHONE_CAPTCHA"
    }
    ```
- **Response**:
    ```json
    {
      "api": "dwp.customerCenter.signIn",
      "code": 1001,
      "data": {
        "showQuickSignInPopup": false,
        "signErrorCode": 100436020,
        "signSuccess": false,
        "signErrorMsg": "Invalid verification code"
      },
      "dmsg": "",
      "msg": "",
      "v": "1"
    }
    ```
- **Analysis**: The request uses a `blackBox` parameter likely for anti-fraud/device fingerprinting. The OTP submitted in the HAR was `3625`.

## 4. Security & Reversing Notes

### Encryption/Signing Mechanisms

**1. Request Signing (`sign` header)**
- **Purpose**: Ensures request integrity and prevents tampering.
- **Analysis**: The signature is a 32-character hex string (MD5 hash format), likely calculated based on the request parameters, timestamp (`ct`), and a secret key/salt.

**2. Device/Session Tracking (`f-g` header)**
- **Purpose**: Advanced device fingerprinting and session binding.
- **Analysis**: Large base64 encoded blob that likely contains encrypted device information and state.

**3. API Gateway Logic**
- **Endpoint Structure**: All requests go through `https://gw.fordeal.com/gw/[api_name]/[version]`.
- **Data Wrapper**: Request bodies are typically wrapped in a `data=` URL-encoded parameter.

## 5. Conclusion

### Automation Feasibility: 45%

### Detailed Conclusion:
Fordeal's security is moderate. While it lacks heavy captchas in the initial flow, the combination of request signing and encrypted device tracking headers (`f-g`, `blackBox`) makes automation non-trivial. The `sign` header needs to be correctly calculated for every request. If the signing logic can be reversed (likely found in the app's obfuscated code or web view JS), automation is highly feasible. The presence of `blackBox` suggests the use of a third-party or custom anti-fraud SDK.
