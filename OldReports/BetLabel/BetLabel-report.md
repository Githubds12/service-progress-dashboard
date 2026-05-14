# BetLabel - Research Report

## Metadata
- **Target App**: `BetLabel (org.betlabel.client)`
- **Version**: `253.0.3`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-26`
- **Host**: `andind2022.com`

## 1. Executive Summary
BetLabel is a sports betting application. The registration and authentication flow involve a multi-step process: initial registration with captcha solving, followed by SMS-based OTP delivery and verification. The application uses a custom session management system where a `Guid` and `Token` are exchanged after each successful step to maintain state.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for phone verification |
| **Captcha** | Image Captcha | Required during the registration phase |
| **Encryption** | None | Data is sent in standard JSON format over TLS |
| **Rate Limits** | 300s | 300-second (5-minute) retry timeout for OTP resend |
| **Endpoints Involved** | 3 | `/Registration`, `/SendCode`, `/CheckCode` |
| **Bot Protection** | Image Captcha | Custom captcha implementation on registration |

## 3. Flow Details

### Step 1: Registration (Trigger OTP)
- **Endpoint**: `POST https://andind2022.com/Account/v1.1/Mb/Register/Registration`
- **Purpose**: Submit user details and captcha to initialize registration.
- **Notable Headers**:
    - `Content-Type`: `application/json`
- **Request Payload**:
    ```json
    {
      "CaptchaId": "d0821b02-60dc-4555-8279-20e3c1c77edd",
      "ImageText": "...",
      "Data": {
        "RegType": 2,
        "Phone": "<!-- Phone Number Highlight --> <mark>8791267460</mark>",
        ...
      }
    }
    ```
- **Response Payload**: Returns an `Auth` object with a `Guid` and `Token`.

### Step 2: Send OTP
- **Endpoint**: `POST https://andind2022.com/Account/v1/SendCode`
- **Purpose**: Request the SMS code.
- **Request Payload**:
    ```json
    {
      "Auth": {
        "Guid": "752c5099-3f38-42ae-a409-24280f0125a1",
        "Token": "E49DBA053FDD465C8510AC25D425EE0E"
      }
    }
    ```

### Step 3: Verify OTP
- **Endpoint**: `POST https://andind2022.com/Account/v1/CheckCode`
- **Purpose**: Submit the verification code.
- **Request Payload**:
    ```json
    {
      "Data": {
        "Code": "<!-- OTP Highlight --> <mark>92617</mark>"
      },
      "Auth": {
        "Guid": "752c5099-3f38-42ae-a409-24280f0125a1",
        "Token": "771C57FBCE624BE2A9B89283AC2DEA60"
      }
    }
    ```

## 4. Conclusion

### Automation Feasibility: Medium (50%)

### Detailed Conclusion:
BetLabel's flow is standard for betting applications. The primary challenge for automation is the image captcha required during registration. Once the captcha is solved (either via OCR or manual input), the subsequent steps for sending and checking the OTP are straightforward JSON requests. The 300-second rate limit on OTP resends is quite strict, necessitating a reliable first-time delivery.

**Strengths**:
- Clear RESTful API.
- Predictable session management (`Guid`/`Token`).

**Weaknesses**:
- Mandatory image captcha.
- Strict 5-minute cooldown for OTP resends.

**Recommendations**:
Automation should include an OCR module for the image captcha. The `Token` is dynamic and must be updated from the response of each preceding request.
