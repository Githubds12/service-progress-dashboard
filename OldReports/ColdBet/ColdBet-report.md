# ColdBet - Research Report

## Metadata
- **Target URL/App**: `org.coldbet.client` (ColdBet)
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29`
- **Status**: `Completed`
- **HAR Files**: `ColdBet.har`

## 1. Executive Summary
ColdBet implements a multi-stage registration and authentication flow secured by a proprietary image-based captcha system and SMS verification. The application communicates with the backend via the `andind2022.com` domain using JSON-based REST APIs. The registration process begins with solving an image captcha to obtain a `CaptchaId`, followed by submitting user details (including the phone number) to the `Registration` endpoint. This step generates an authentication token (`Guid`/`Token`) required for the subsequent SMS trigger (`SendCode`) and verification (`CheckCode`) steps. Automation is moderately difficult due to the custom image captcha and mandatory session-based tokens.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | 5-digit OTP code |
| **Captcha** | Custom Image | Required during initial registration phase |
| **Encryption** | Standard | HTTPS with JSON payloads |
| **Rate Limits** | Moderate | Enforced via `AppGuid` and session tokens |
| **Endpoints Involved** | 4 | `Registration`, `SendCode`, `CheckCode`, `GetCaptcha` |
| **Bot Protection** | Moderate | Custom Captcha + Session Tracking |

## 3. Flow Details

### Flow 1: Registration & SMS Verification

**Step 1: Phone Number Submitting Endpoint (Registration)**
- **Endpoint**: `POST https://andind2022.com/Account/v1.1/Mb/Register/Registration`
- **Request Headers**:
    ```text
    User-Agent: org.coldbet.client-user-agent/coldbet-v253.0.2
    Content-Type: application/json; charset=UTF-8
    AppGuid: 737844568a148476_2
    Host: andind2022.com
    ```
- **Request Body**:
    ```json
    {
      "CaptchaId": "7cac7628-2ee5-4c72-8801-373ac2061412",
      "ImageText": "tVZUh89VZOTq0KZKlOqr4fBYLjeeK...",
      "Data": {
        "RegType": 2,
        "CountryId": 79,
        "Phone": "<!-- 3513422210 -->",
        "RulesConfirmationAll": 1,
        "TimeZone": "5.3"
      }
    }
    ```
- **Response Headers**:
    ```text
    Server: Angie
    Content-Type: application/json; charset=utf-8
    api-supported-versions: 1.0, 1.1, 1.2, 2.0
    ```
- **Response Body**:
    ```json
    {
      "Success": true,
      "Value": {
        "Auth": {
          "CodeType": "Sms",
          "Guid": "a110b6eb-ac3e-4802-986b-f7305337fff8",
          "Token": "251F1C17F6424133B65A9239D97A652B",
          "Hash": "a110b6eb-ac3e-4802-986b-f7305337fff8|251F1C17F6424133B65A9239D97A652B"
        },
        "CodeTypes": ["Sms"]
      }
    }
    ```

**Step 2: Trigger SMS Code**
- **Endpoint**: `POST https://andind2022.com/Account/v1/SendCode`
- **Request Headers**:
    ```text
    X-Message-Id: kwlgDGPE33C
    AppGuid: 737844568a148476_2
    Content-Type: application/json; charset=UTF-8
    ```
- **Request Body**:
    ```json
    {
      "Data": {},
      "Auth": {
        "Guid": "a110b6eb-ac3e-4802-986b-f7305337fff8",
        "Token": "251F1C17F6424133B65A9239D97A652B"
      }
    }
    ```
- **Response Headers**:
    ```text
    api-supported-versions: 1.0, 1.1, 1.2, 2.0, 3.0
    ```
- **Response Body**:
    ```json
    {
      "Success": true,
      "Value": {
        "RAS": 300,
        "Auth": {
          "Guid": "a110b6eb-ac3e-4802-986b-f7305337fff8",
          "Token": "96EF162AC5DE4E6CA14D9221F7F38959",
          "Hash": "a110b6eb-ac3e-4802-986b-f7305337fff8|96EF162AC5DE4E6CA14D9221F7F38959"
        }
      }
    }
    ```

**Step 3: Submit SMS OTP (Verification)**
- **Endpoint**: `POST https://andind2022.com/Account/v1/CheckCode`
- **Request Headers**:
    ```text
    X-BundleId: org.coldbet.client
    AppGuid: 737844568a148476_2
    Content-Type: application/json; charset=UTF-8
    ```
- **Request Body**:
    ```json
    {
      "Data": {
        "Code": "<!-- 2222 -->"
      },
      "Auth": {
        "Guid": "a110b6eb-ac3e-4802-986b-f7305337fff8",
        "Token": "96EF162AC5DE4E6CA14D9221F7F38959"
      }
    }
    ```
- **Response Body (Example)**:
    ```json
    {
      "Success": false,
      "Error": "Verification code is incorrect.",
      "ErrorCode": 100371
    }
    ```

## 4. Security & Reversing Notes

### Custom Captcha System
- The app fetches an image captcha from `/captcha/v1/GetCaptcha`.
- The solved text must be sent to `Registration` to proceed. This effectively blocks mass automated registration attempts without OCR or manual solving.

### Session & Token Lifecycle
- The `Guid` and `Token` pairs are dynamic and refreshed after each successful step (e.g., after `SendCode`, a new `Token` is issued for `CheckCode`).
- Requests are validated against the `AppGuid` (Device ID) and several custom headers (`X-Message-Id`, `X-Request-Guid`).

## 5. Conclusion
ColdBet provides a solid defensive layer by combining a traditional image captcha with a strictly stateful API flow. The requirement for a valid `CaptchaId` to initiate the registration sequence prevents low-effort botting. Furthermore, the granular token rotation (Auth Guid/Token) between the SMS trigger and verification steps ensures that each session is tightly controlled. While the API payloads are transparent JSON, the orchestration required to maintain valid sessions and solve the interactive captcha makes automated abuse significantly more resource-intensive.
