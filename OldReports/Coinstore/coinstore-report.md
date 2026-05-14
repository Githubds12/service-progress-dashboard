# Coinstore - Research Report

## Metadata
- **Target URL/App**: `coinstore.com` / `com.io.coinstore`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-08`
- **Status**: `Completed`
- **HAR Files**: `Coinstore.har`

## 1. Executive Summary
Coinstore (com.io.coinstore) utilizes a sophisticated authentication and security architecture. The identified flow focus on binding a mobile phone number to an existing email-registered account. This process is multi-layered, requiring email verification followed by SMS verification. The system implements GeeTest captcha for bot protection and uses specialized "gateways" for code delivery. Automation is feasible but requires handling GeeTest challenges and multi-step session states.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS + Email | Dual verification required for binding |
| **Captcha** | GeeTest | Observed on code delivery endpoints |
| **Encryption** | Standard HTTPS | No observed custom encryption on main payloads |
| **Rate Limits** | Unknown | Not tested during capture |
| **Endpoints Involved** | 4 | `/gateway/send/email`, `/strategy/validCode`, `/gateway/send/sms`, `/mobile/binding/save` |
| **Bot Protection** | GeeTest Captcha | Guards the SMS delivery gateway |

## 3. Flow Details

### Flow 1: Phone Binding (Post-Registration)

**Step 1: Request Email Verification Code**
- **Endpoint**: `POST https://api.coinstore.com/v2/user/common/gateway/send/email`
- **Purpose**: Verify the account owner via email before allowing phone binding.
- **Request Payload**:
    ```json
    {
      "email": "de****@gmail.com",
      "scene": "6",
      "token": "c08e711b5e965290fa16b7b2fd710462dd8393197b66b3b14186682d9aa56f94"
    }
    ```
- **Response**:
    ```json
    {
      "code": "0",
      "message": "Succeed",
      "data": {}
    }
    ```

**Step 2: Submit Email Code**
- **Endpoint**: `POST https://api.coinstore.com/v2/user/strategy/validCode`
- **Purpose**: Validate the email code to unlock the phone binding step.
- **Request Payload**:
    ```json
    {
      "smsCode": "",
      "googleCode": "",
      "scene": "6",
      "emailCode": "566804"
    }
    ```
- **Response**:
    ```json
    {
      "code": "0",
      "message": "Succeed",
      "data": {}
    }
    ```

**Step 3: Request SMS Code to New Phone**
- **Endpoint**: `POST https://api.coinstore.com/v2/user/common/gateway/send/sms`
- **Purpose**: Trigger OTP delivery to the new phone number (`+82` in this capture).
- **Request Payload**:
    ```json
    {
      "countryCode": "+82",
      "mobile": "1012345678",
      "scene": "6",
      "token": ""
    }
    ```
- **Response**:
    ```json
    {
      "code": "0",
      "message": "Succeed",
      "data": {}
    }
    ```
- **Analysis**: This endpoint is protected by **GeeTest**. The `token` field may correspond to a captcha validation token.

**Step 4: Finalize Phone Binding**
- **Endpoint**: `POST https://api.coinstore.com/v2/user/mobile/binding/save`
- **Purpose**: Link the phone number to the account using the received SMS code.
- **Request Payload**:
    ```json
    {
      "countryCode": "+82",
      "mobile": "1012345678",
      "googleValidCode": "",
      "scene": "6",
      "mobileValidCode": "25889"
    }
    ```
- **Response**:
    ```json
    {
      "code": "10075",
      "message": "Incorrect SMS code",
      "data": {}
    }
    ```
- **Analysis**: If successful, the phone number is permanently associated with the user profile.

## 4. Security & Reversing Notes

### Captcha Implementation
- **GeeTest**: The presence of `static.geetest.com` and `api.geevisit.com` indicates that Coinstore uses GeeTest's behavioral captcha. This is a significant hurdle for purely headless automation.

### Scene Constants
- **Scene "6"**: Identified as the constant for `Phone Binding` operations across multiple endpoints.
- **Scene "2"**: Used during initial email registration.

## 5. Conclusion
### Automation Feasibility: 40%
The flow is logically structured and uses standard JSON payloads. However, the requirement for active session cookies, dual-factor verification (Email -> SMS), and GeeTest captcha protection lowers the feasibility for simple automation scripts. Integration with a captcha-solving service and a browser-based automation tool (like Selenium or Puppeteer) would be required for a successful implementation.
