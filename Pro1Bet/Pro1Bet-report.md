# Pro1Bet - Research Report

## Metadata
- **Target URL/App**: `org.pro1bet.client`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-02`
- **Status**: `Completed`
- **HAR Files**: `Pro1Bet.har`

## 1. Executive Summary
Pro1Bet is a betting application that utilizes a multi-step registration process involving an initial image captcha challenge followed by SMS OTP verification. The API communicates with `andind2022.com`. The authentication flow is session-based, using a combination of `Guid` and `Token` for state management. While the registration process is gated by a captcha, the subsequent OTP steps are straightforward JSON requests.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | 6-digit numeric OTP |
| **Captcha** | Image Captcha | Required for the initial registration step |
| **Encryption** | None | Standard JSON payloads over HTTPS |
| **Rate Limits** | Unknown | No explicit rate limiting observed in the trace |
| **Endpoints Involved** | 4 | `/GetRegCaptcha`, `/Registration`, `/SendCode`, `/CheckCode` |
| **Bot Protection** | Image Captcha | Implemented on the registration endpoint |

## 3. Flow Details

### Flow 1: User Registration & OTP Verification

**Step 1: Get Captcha**
- **Endpoint**: `GET https://andind2022.com/Account/v1/Mb/Register/GetRegCaptcha?partner=315`
- **Purpose**: Retrieve the captcha challenge for registration.
- **Response**:
    ```json
    {
        "token": "[CAPTCHA_IMAGE_TEXT_OR_DATA]",
        "extra_ctoken": ""
    }
    ```

**Step 2: Submit Registration**
- **Endpoint**: `POST https://andind2022.com/Account/v1.1/Mb/Register/Registration`
- **Purpose**: Register user details and initiate SMS verification.
- **Request Body**:
    ```json
    {
        "CaptchaId": "f5d40a34-19d2-4b1a-bd6e-efc21a7eacbf",
        "ImageText": "[CAPTCHA_TEXT]",
        "Data": {
            "RegType": 2,
            "CountryId": 71,
            "CurrencyId": 99,
            "Phone": "6232975566",
            "RulesConfirmation": 1,
            "SharePersonalDataConfirmation": 1,
            "TimeZone": "5.3"
        }
    }
    ```
- **Response Body**:
    ```json
    {
        "Success": true,
        "Value": {
            "Auth": {
                "CodeType": "Sms",
                "Guid": "3a7eaa05-6bb2-4ad3-a91e-d827c3574b00",
                "Token": "5862CE7A8A564A6D91179648795940D3"
            }
        }
    }
    ```

**Step 3: Send OTP**
- **Endpoint**: `POST https://andind2022.com/Account/v1/SendCode`
- **Purpose**: Trigger the SMS OTP delivery.
- **Request Body**:
    ```json
    {
        "Data": {},
        "Auth": {
            "Guid": "3a7eaa05-6bb2-4ad3-a91e-d827c3574b00",
            "Token": "5862CE7A8A564A6D91179648795940D3"
        }
    }
    ```
- **Response Body**:
    ```json
    {
        "Success": true,
        "Value": {
            "RAS": 300,
            "Auth": {
                "Guid": "3a7eaa05-6bb2-4ad3-a91e-d827c3574b00",
                "Token": "C0C5C23580834312ACDCE098CBD56B44"
            }
        }
    }
    ```

**Step 4: Check OTP Code**
- **Endpoint**: `POST https://andind2022.com/Account/v1/CheckCode`
- **Purpose**: Verify the received 6-digit SMS OTP.
- **Request Body**:
    ```json
    {
        "Data": {
            "Code": "258369"
        },
        "Auth": {
            "Guid": "3a7eaa05-6bb2-4ad3-a91e-d827c3574b00",
            "Token": "C0C5C23580834312ACDCE098CBD56B44"
        }
    }
    ```
- **Response (Failure Example)**:
    ```json
    {
        "Success": false,
        "Error": "Verification code is incorrect.",
        "ErrorCode": 100371
    }
    ```

## 4. Security & Reversing Notes

### Bot Protection
The registration endpoint is protected by an image captcha. Automated scripts would need to integrate a captcha solving service to proceed with registration.

### State Management
The system uses a `Guid` and a rotating `Token` in the `Auth` object for all subsequent requests after registration. This ensures that the flow must be followed sequentially.

## 5. Conclusion

### Automation Feasibility: 75%

### Detailed Conclusion:
Pro1Bet's registration flow is standard for betting applications. The use of image captcha provides a basic level of bot protection. Once the captcha is solved, the SMS verification process is straightforward. The API is robust and clearly documented in the captured traffic.

### Strengths:
- Clear endpoint separation.
- Rotating tokens for session security.

### Weaknesses:
- Image captcha is the only major barrier to automation.
