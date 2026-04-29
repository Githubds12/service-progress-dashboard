# LC Waikiki - Research Report

## Metadata
- **Target URL/App**: `com.lcwaikiki.android`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29 23:33`
- **Status**: `Completed`
- **HAR Files**: `LCW.har`

## 1. Executive Summary
LC Waikiki (com.lcwaikiki.android) implements a straightforward REST-based authentication flow over HTTPS. The registration process involves an availability check, a pre-registration step that triggers the SMS OTP, and a final registration step where the user submits the activation code. No advanced bot protection or captcha challenges were observed during the captured flow. Automation feasibility is high due to the predictable JSON-based API structure and lack of complex cryptographic signing.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | 5-digit OTP code sent via SMS |
| **Captcha** | undefined | No captcha observed in the registration flow |
| **Encryption** | Standard HTTPS | Payloads sent in plaintext JSON over SSL |
| **Rate Limits** | Unknown | No rate limiting behavior was observed during testing |
| **Endpoints Involved** | 3 | `checkAlreadyRegisteredCustomer`, `preregister`, `register` |
| **Bot Protection** | undefined | Standard mobile application headers used |

## 3. Flow Details

### Flow 1: Registration & SMS Verification

**Step 1: Check Customer Availability**
- **Endpoint**: `POST /mobile/checkout/api/v1/checkAlreadyRegisteredCustomer`
- **Purpose**: Verify if the email or phone number is already registered
- **Request Payload**:
    ```json
    {
      "email": "deepanshusinghdigitalheroes@gmail.com"
    }
    ```
- **Response**:
    ```json
    {
      "customerValidationResult": {
        "validationCustomerInfo": []
      },
      "status": {
        "code": 200,
        "message": "response.status.success.msg"
      }
    }
    ```

**Step 2: Request SMS OTP (Preregister)**
- **Endpoint**: `POST /mobile/checkout/api/v5/preregister`
- **Purpose**: Submit user details and trigger SMS OTP delivery
- **Notable Headers**:
    - `ApplicationId`: `com.lcwaikiki.android`
    - `VersionCode`: `4.0.41`
    - `Accept-Language`: `tr-TR`
- **Request Payload**:
    <!-- Phone Submission -->
    ```json
    {
      "email": "deepanshusinghdigitalheroes@gmail.com",
      "languageId": 1,
      "phoneAreaCode": "0090",
      "phoneNumber": "5676464646",
      "password": "[REDACTED]",
      "contract": true,
      "privacyPolicy": true,
      "isCheckContractAndPrivacy": true
    }
    ```
- **Response**:
    ```json
    {
      "result": {
        "isConfirmed": true,
        "message": "",
        "validationType": "NoValidationType"
      },
      "status": {
        "code": 200,
        "message": "response.status.success.msg"
      }
    }
    ```

**Step 3: Verify OTP (Final Registration)**
- **Endpoint**: `POST /mobile/checkout/api/v4/register`
- **Purpose**: Submit the activation code to complete account creation
- **Request Payload**:
    <!-- OTP Submission -->
    ```json
    {
      "email": "deepanshusinghdigitalheroes@gmail.com",
      "password": "[REDACTED]",
      "phoneAreaCode": "0090",
      "phoneNumber": "5676464646",
      "activationCode": "22222",
      "isConfirmEmailAndSms": true
    }
    ```
- **Response**:
    ```json
    {
      "status": {
        "code": 2006,
        "message": "Kod hatalı görünüyor."
      }
    }
    ```

## 4. Security & Reversing Notes

### API Structure
The API follows a standard RESTful pattern with descriptive endpoint names. All data is transmitted as JSON objects. The application relies on Turkish as the primary language for error messages (`message: "Kod hatalı görünüyor"`).

### Session Tracking
State is likely managed via cookies or standard HTTP headers, although the registration flow appears to be stateless until the final step, as all user details are re-transmitted in the `/register` request.

## 5. Conclusion

### Automation Feasibility: 85% (High)

### Detailed Conclusion:
The LC Waikiki registration flow is highly amenable to automation. The lack of captcha, obfuscation, or proprietary signing mechanisms makes it a "low-friction" service. The main requirements for successful automation are maintaining the correct `ApplicationId` and `VersionCode` headers and handling the multi-step JSON sequence. The high feasibility score reflects the predictability of the response formats and the standard nature of the OTP delivery trigger.
