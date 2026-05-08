# Fairpari - Research Report

## Metadata
- **Target URL/App**: `fairpari.com` / `org.fairpari.client`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-08`
- **Status**: `Completed`
- **HAR Files**: `fairpari.har`

## 1. Executive Summary
Fairpari (org.fairpari.client) implements a multi-step registration flow on the `andind2022.com` backend. The system utilizes custom image-based captcha verification and request signing (`X-Sign` header) to prevent automated registrations. The flow consists of initial data submission (phone number, currency, etc.), captcha solving, OTP delivery via SMS, and final verification. Automation feasibility is medium, requiring captcha bypass and reverse engineering of the request signing algorithm.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for OTP delivery |
| **Captcha** | Custom Image Captcha | Requires solving an image challenge, integrated with `CaptchaId` and `ImageText` |
| **Encryption** | X-Sign Header Signing | Requests are signed with a custom cryptographic hash/signature |
| **Rate Limits** | Unknown | No explicit 429 errors observed, but likely session-limited |
| **Endpoints Involved** | 4 | `/Register/Registration`, `/SendCode`, `/CheckCode`, `/hd-api/verify` |
| **Bot Protection** | Custom | Includes request signing and behavioral telemetry (`/Fatman/` events) |

## 3. Flow Details

### Flow 1: Registration (Signup)

**Step 1: Submit Registration Data & Captcha**
- **Endpoint**: `POST https://andind2022.com/Account/v1.1/Mb/Register/Registration`
- **Purpose**: Initial registration submission with phone number and solved captcha.
- **Notable Headers**:
    - `X-Sign`: Custom request signature (N7lEADA0FFP5L1M1WAgFbEt8d3f6D9o5/...)
    - `X-BundleId`: `org.fairpari.client`
    - `AppGuid`: `aa96c36dff5e61fd_2`
    - `X-Request-Guid`: `339_aa96c36dff5e61fd_2_1778254839539_51_1455992946`
- **Request Payload**:
    ```json
    {
      "CaptchaId": "60b9e81b-b4b3-4879-b9dd-35cf31c2608c",
      "ImageText": "Hg9M1VXO5tCf9pViUbvXcKrQc0EZO4Kn4XBdteaS342V--JUOKSkSh8RzfOTXC2lcYZ8fn3fv9cY1PDvrLnWbNJJ25V5aBHNKjNLxMHUWIVMuJfr02FQFjJXtIionW8opTjuOGgsdVUWndgSALG8bckJTkk0iP4cfH5J-w8v6X0nTKPeUEWtynm7tBOLI1Q83GqLYan33IjPIlIiD1oVxS2enpn7pZwmzzKIQmZY0_GYEQnWZPNULZu5YA4XamXbd5Szbd7bRGK0s_WtlzNiAFOscq2zRd4DAJRyudS-tokTj9Q-1qzedMkq5zV0g_HUUKO_MDbbt060zfrT5v0Eqe8-IZGxAScqGokeoCN6V5p0u5vP_ilglmldqguzco2xkq8f6T1berwbxanmo2i8pqb6-66gtt6cy_jd9wxx_fqn6qfchflLdeQ7GJDPZZO8bVFGHHYd-jCCR2pBrs_7jDHwKfrAYOuMUsWtW13jBzjX955JmnFQiy2LQvKlPAXVc6AmDGdG5l8IfmUJ3NRr3lbu7c4FI-vPUuHdZYGsz197g9XlBvnRoHbAFE7XugU_1tTQQk3Zu_naCp7_Qy53vsUq77jJ-9QbQzmVd1yWR7EBHM2hCXva1MHD-8UemBYXH",
      "Data": {
        "RegType": 2,
        "CountryId": 79,
        "CurrencyId": 12,
        "Phone": "3720514700",
        "RulesConfirmation": 1,
        "SharePersonalDataConfirmation": 1,
        "TimeZone": "5.3"
      }
    }
    ```
- **Response**:
    ```json
    {
      "Success": true,
      "Value": {
        "Auth": {
          "CodeType": "Sms",
          "Guid": "6ff93f2f-4072-4ae7-98d5-291e685faf65",
          "Token": "E01FCC8C82A24AA28C094AD6EE51EB6D",
          "Hash": "6ff93f2f-4072-4ae7-98d5-291e685faf65|E01FCC8C82A24AA28C094AD6EE51EB6D"
        },
        "CodeTypes": [
          "Sms",
          "Telegram"
        ]
      }
    }
    ```
- **Analysis**: This endpoint is the **Phone Number Submitting Endpoint**. It requires a solved captcha (`ImageText`) and a valid `X-Sign` header.

**Step 2: Request OTP Code**
- **Endpoint**: `POST https://andind2022.com/Account/v1/SendCode`
- **Purpose**: Trigger SMS OTP delivery to the provided phone number.
- **Request Payload**:
    ```json
    {
      "Data": {},
      "Auth": {
        "Guid": "6ff93f2f-4072-4ae7-98d5-291e685faf65",
        "Token": "E01FCC8C82A24AA28C094AD6EE51EB6D"
      }
    }
    ```
- **Response**:
    ```json
    {
      "Success": true,
      "Value": {
        "RAS": 300,
        "Auth": {
          "Guid": "6ff93f2f-4072-4ae7-98d5-291e685faf65",
          "Token": "9E686A879AAC424E9FF69D326B8A2A46",
          "Hash": "6ff93f2f-4072-4ae7-98d5-291e685faf65|9E686A879AAC424E9FF69D326B8A2A46"
        }
      }
    }
    ```
- **Analysis**: Uses the `Guid` and `Token` from the registration response. Returns a new `Token` for the next step.

**Step 3: Verify OTP Code**
- **Endpoint**: `POST https://andind2022.com/Account/v1/CheckCode`
- **Purpose**: Verify the OTP received via SMS.
- **Request Payload**:
    ```json
    {
      "Data": {
        "Code": "252525"
      },
      "Auth": {
        "Guid": "6ff93f2f-4072-4ae7-98d5-291e685faf65",
        "Token": "FEED87A7ADCA477F912A62E561BB88E1"
      }
    }
    ```
- **Response**:
    ```json
    {
      "Success": false,
      "Error": "Verification code is incorrect.",
      "ErrorCode": 100371
    }
    ```
- **Analysis**: Final step in the OTP verification flow.

## 4. Security & Reversing Notes

### Encryption/Signing Mechanisms
- **Request Signing (X-Sign)**: All critical requests carry an `X-Sign` header. This signature likely hashes the request body, headers, and a timestamp using a client-side secret.
- **Custom Captcha**: The captcha system is custom-built. It returns a `CaptchaId` and requires the solved text to be sent as `ImageText`.
- **Behavioral Telemetry**: The app sends events to `/Fatman/event.json`, tracking user interactions (e.g., `registration_by_phone`, `sms`).

## 5. Conclusion
### Automation Feasibility: 50%
Automation is feasible but requires solving the custom image captcha and accurately reproducing the `X-Sign` header signature logic. The multi-step token exchange (`Guid`/`Token`) is straightforward once the initial signing and captcha are bypassed.
