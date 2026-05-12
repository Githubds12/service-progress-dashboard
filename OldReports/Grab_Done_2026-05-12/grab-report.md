# Grab - Research Report

## Metadata
- **Target URL/App**: `com.grabtaxi.passenger`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-12`
- **Status**: `Completed (High Difficulty)`
- **HAR Files**: `Grab.har`

## 1. Executive Summary
Grab (com.grabtaxi.passenger) implements a high-security authentication flow that heavily relies on **Arkose Labs (FunCaptcha)** for bot protection. The login flow involves initiating a challenge session, solving a puzzle (Arkose), and then requesting an SMS OTP. The inclusion of Arkose Labs makes automated interaction extremely difficult without sophisticated captcha-solving services or browser-based automation. The API endpoints are well-structured but require valid session tokens and consistent device fingerprints.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS + Arkose Captcha | SMS OTP is preceded by an Arkose Labs challenge |
| **Captcha** | Arkose Labs | Slider/Puzzle captcha required for OTP request |
| **Encryption** | Standard TLS | Payloads are JSON, but session tokens are JWT-based |
| **Rate Limits** | Moderate | Enforced via Arkose Labs and server-side tracking |
| **Endpoints Involved** | 4 | `/grabid/v1/phone/otp`, `/grabid/v1/phone/token`, `/v1/challengesession/challengeSession`, `/v1/challengesession/challengeSession/verifyChallenge` |
| **Bot Protection** | Arkose Labs | Uses Arkose Labs FunCaptcha for all sensitive actions |

## 3. Flow Details

### Flow 1: Sign-in / Signup via Phone

**Step 1: Initialize Challenge Session**
- **Endpoint**: `GET https://api.grab.com/grabid/v1/challengesession/challengeSession`
- **Purpose**: Get a challenge session ID for Arkose Labs.

**Step 2: Solve Arkose Challenge**
- **Endpoint**: `POST https://api.grab.com/grabid/v1/challengesession/challengeSession/verifyChallenge`
- **Purpose**: Submit the solved captcha token.

**Step 3: Request OTP (Send SMS)**
- **Endpoint**: `POST https://api.grab.com/grabid/v1/phone/otp`
- **Full Request Headers**:
    ```text
    X-Grab-Device-ID: 3346dff226996b4a
    X-Ray: eyJhIjoiVDBcL2U3...
    Authorization: grabsecure 57e8887a910ca1d095d76a39edba12c4516690ebfc742eaa21d84d778e1d6f0d
    X-GRAB-CHALLENGE-ID: 261bf861-dba1-42ad-9cfb-869adf49a2c0
    Content-Type: application/json; charset=UTF-8
    ```
- **Full Request Body**:
    ```json
    {
      "method": "SMS",
      "countryCode": "IT",
      "phoneNumber": "393720513142",
      "templateID": "pax_android_production",
      "numDigits": 6,
      "deviceID": "3346dff226996b4a",
      "deviceManufacturer": "Google",
      "deviceModel": "Pixel 7",
      "locale": "en_IN",
      "scenario": "signup"
    }
    ```
- **Full Response Body**:
    ```json
    {
      "challengeID": "700a4967-985e-48d3-a82a-739563b154a7",
      "evURL": "",
      "vendor": ""
    }
    ```

**Step 4: Verify OTP (Exchange for Token)**
- **Endpoint**: `POST https://api.grab.com/grabid/v1/phone/token`
- **Full Request Body**:
    ```json
    {
      "adrID": "3346dff226996b4a",
      "adrIMEI": "3346dff226996b4a",
      "adrIMSI": "",
      "adrMEID": "",
      "adrSERIAL": "unknown",
      "adrUDID": "18a64fb3-79ce-441b-8c1f-680134e7b745",
      "advertisingID": "f51ee336-e489-4882-8c21-95ff06ed4a9a",
      "applicationVersion": "5.408.0(54080000) Build ; Build 151667694",
      "cellularOperator": "",
      "challengeID": "700a4967-985e-48d3-a82a-739563b154a7",
      "cli": "",
      "countryCode": "IT",
      "deviceManufacturer": "Google",
      "deviceModel": "Pixel 7",
      "hints": "newAccount",
      "iosUDID": "",
      "latitude": 1.361216711,
      "longitude": 103.989443071381,
      "otp": "333333",
      "otpAutoFilled": false,
      "phoneNumber": "393720513142",
      "scenario": "signup",
      "snaCarrier": null,
      "snaChallengeID": null,
      "snaErrorDescription": null,
      "snaExecutionCode": null,
      "snaToken": null,
      "source": "android2",
      "sourceID": "",
      "tmSessionID": "",
      "tpToken": {
        "type": "Google",
        "value": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjgwNzZkZGJhYjQxNTU1NmUxNjkxNTRjNmE0YTBiZGJkNDQ2OWI3OWMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIxNDEyNTUxMTM5NzMtMWNybHBucDFkZnJhbmluaGpmNmJ1bDljNDhnbDZzYTYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiIxNDEyNTUxMTM5NzMtazNzY2l1Nzl0NWM1MXJuajloZmp0MmhhcHMwNDM2Z2ouYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTY1OTc2MTM3Njk0MDIxMzIwMzIiLCJlbWFpbCI6ImRlZXBhbnNodXNpbmdoZGlnaXRhbGhlcm9lc0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkRlZXBhbnNodSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NKdS1rWmRfX3g1aDBnZWk2NGVDYUczaEpYdUs5U3pnSi1DWFk2VmhFTktfdkQzaUE9czk2LWMiLCJnaXZlbl9uYW1lIjoiRGVlcGFuc2h1IiwiaWF0IjoxNzc4NTY2MzkwLCJleHAiOjE3Nzg1Njk5OTB9.t6QJv59TnTSmYX0INXJ4n4JZlrfwo8jVQ6uUmlMMzR8E7RWMNW18SctjDiaMjl4r-ZLzugE2p8_crSamCIxS9ew53r6A7qM9S3S2bwncRa_yZhG7fSYtcxznC1muZS6eqe2e9_f8ApIt8FOk2aanwHzWmkbQBAvuqhx6qf7gu_wnlZ_yJUR1I4xonfUZaVeezNcCTUkvcqLt_Jwz0zaD8xj0qSLaO0kc6wlgJPImdx_Uu2mMrpd2uhlyCz7Q8z7wkT-zCf4Ft1uShsqkQpipMBcnj38WyQrC4EDNvXduSoBKfueLBZGIOgEaN48D6SQMtNfE_ac23-C79JgcgNqdqg"
      }
    }
    ```
- **Full Response Body**:
    ```json
    {
      "errors": [
        {
          "code": 16000,
          "message": "Something went wrong and we can't verify the code. Try again later.",
          "details": {
            "numAttemptsLeft": 2
          }
        }
      ]
    }
    ```

## 4. Security & Reversing Notes

### Encryption/Signing Mechanisms
1. **JWT Tokens**: Grab uses JSON Web Tokens (JWT) for session management, providing claims like `aud`, `did` (Device ID), and `group`.
2. **Arkose Labs Integration**: The integration with `grab-api.arkoselabs.com` provides a robust defense against automated OTP requests.
3. **AppsFlyer/Scribe SDKs**: Extensive tracking and fingerprinting are used to monitor user behavior and detect anomalies.

## 5. Conclusion

### Automation Feasibility: 20%

### Critical Blockers:
1. **Arkose Labs Captcha**: Solving the FunCaptcha puzzle is the primary hurdle for any automated script.
2. **Device Fingerprinting**: Grab correlates `deviceID`, `andrID`, and `devUDID` across multiple requests.
3. **Session Binding**: OTP requests are tied to a specific `challengeSessionID`.

### Detailed Conclusion:
Grab's security architecture is top-tier for consumer applications. The combination of mandatory behavioral captchas (Arkose) and strict device fingerprinting makes it highly resistant to basic botting. Automation is only possible using headless browsers with human-like interaction or by integrating paid Arkose solving services, both of which increase the cost and complexity significantly.
