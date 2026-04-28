# eneba - Research Report

## Metadata
- **Target URL/App**: `com.eneba.app` (Eneba: Buy Games & Gift Cards)
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29`
- **Status**: `Completed`
- **HAR Files**: `eneba.har`

## 1. Executive Summary
Eneba implements a sophisticated security architecture for account verification and transaction security. The system utilizes **Cloudflare Managed Challenges (Turnstile)** to secure its OAuth 2.0 authentication and a GraphQL-based API for multi-step verification (Email & Phone). The flow requires solving a Cloudflare challenge to obtain a token, followed by an OAuth password grant, and finally, separate GraphQL mutations for email and phone verification. Automation is categorized as high difficulty due to Cloudflare's mandatory clearance and the multi-factor verification requirements.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | Email & SMS | Dual-factor verification required for account activation |
| **Captcha** | Cloudflare Challenge | Mandatory Turnstile clearance for authentication |
| **Encryption** | Standard | HTTPS with OAuth and GraphQL payloads |
| **Rate Limits** | Strict | Managed by Cloudflare WAF |
| **Endpoints Involved** | 4 | `/oauth/token`, `/graphql/`, `cloudflare/challenge`, `mercure` |
| **Bot Protection** | High | Cloudflare Bot Management |

## 3. Flow Details

### Flow 1: Authentication & Email Verification

**Step 1: Obtain OAuth Token**
- **Endpoint**: `POST https://my.eneba.com/oauth/token`
- **Request Headers**:
    ```text
    User-Agent: EnebaApp v1.9.34 (1226); Android (15); Pixel 7
    Content-Type: multipart/form-data; boundary=f1a29fd1-a149-43a6-bc77-e8f7eac2d3fb
    ```
- **Request Body**:
    ```text
    --f1a29fd1-a149-43a6-bc77-e8f7eac2d3fb
    content-disposition: form-data; name="grant_type"
    password
    --f1a29fd1-a149-43a6-bc77-e8f7eac2d3fb
    content-disposition: form-data; name="client_id"
    875b7ca2-6022-11e8-afac-0242ac15000a
    --f1a29fd1-a149-43a6-bc77-e8f7eac2d3fb
    content-disposition: form-data; name="username"
    deepanshusinghdigitalheroes@gmail.com
    --f1a29fd1-a149-43a6-bc77-e8f7eac2d3fb
    content-disposition: form-data; name="password"
    Facebook@ds12,
    --f1a29fd1-a149-43a6-bc77-e8f7eac2d3fb
    content-disposition: form-data; name="captcha"
    1.68qS0Jqjt288... (Turnstile Token)
    --f1a29fd1-a149-43a6-bc77-e8f7eac2d3fb
    content-disposition: form-data; name="captchaProvider"
    TURNSTILE
    --f1a29fd1-a149-43a6-bc77-e8f7eac2d3fb--
    ```
- **Response Body**:
    ```json
    {
      "token_type": "Bearer",
      "expires_in": 2592000,
      "access_token": "eyJ0eXAiOiJKV1Q...",
      "refresh_token": "def502000f..."
    }
    ```

**Step 2: Confirm Email**
- **Endpoint**: `POST https://graphql.eneba.com/graphql/`
- **Request Body**:
    ```json
    {
      "operationName": "User_splashConfirmEmailUsingCode",
      "variables": {
        "input": {
          "code": "606556",
          "email": "deepanshusinghdigitalheroes@gmail.com",
          "nsid": "36200ac9-8148-4f50-9d52-06fbac92edae"
        }
      },
      "query": "mutation User_splashConfirmEmailUsingCode($input: User_ConfirmEmailUsingCodeInput!) { User_confirmEmailUsingCode(input: $input) { id success } }"
    }
    ```
- **Response Body**:
    ```json
    {
      "data": {
        "User_confirmEmailUsingCode": {
          "id": "2d9ade62-433e-11f1-a467-669941668f9a",
          "success": true,
          "__typename": "User_ConfirmEmailUsingCodeResponse"
        }
      }
    }
    ```

### Flow 2: Phone Verification (Trigger & Submit)

**Step 1: Request Phone Confirmation (SMS Trigger)**
- **Endpoint**: `POST https://graphql.eneba.com/graphql/`
- **Request Body**:
    ```json
    {
      "operationName": "UserPhoneConfirmRequest",
      "variables": {
        "context": {
          "country": "IN",
          "region": "india",
          "language": "en"
        }
      },
      "query": "mutation UserPhoneConfirmRequest($context: ContextInput!) { User_phoneConfirmRequest(context: $context) { success eventNotificationTopic } }"
    }
    ```
- **Response Body**:
    ```json
    {
      "data": {
        "User_phoneConfirmRequest": {
          "success": true,
          "eventNotificationTopic": "PhoneConfirmRequestCommand/9642bbd8-433e-11f1-8902-72dd9c31aadc"
        }
      }
    }
    ```

**Step 2: Submit Phone Confirmation Code (OTP)**
- **Endpoint**: `POST https://graphql.eneba.com/graphql/`
- **Request Body (Legitimate)**:
    ```json
    {
      "operationName": "UserPhoneConfirm",
      "variables": {
        "context": {
          "country": "IN",
          "region": "india",
          "language": "en"
        },
        "input": {
          "code": "99999",
          "nsid": "36200ac9-8148-4f50-9d52-06fbac92edae"
        }
      },
      "query": "mutation UserPhoneConfirm($context: ContextInput!, $input: User_PhoneConfirmInput!) { User_phoneConfirm(context: $context, input: $input) { id success } }"
    }
    ```
- **Response Body (Error Case)**:
    ```json
    {
      "errors": [
        {
          "message": "Phone confirmation token invalid",
          "code": "USER_ERROR"
        }
      ],
      "data": {
        "User_phoneConfirm": null
      }
    }
    ```

## 4. Security & Reversing Notes

### Cloudflare & Bot Protection
- Mandatory Turnstile verification is required for the `/oauth/token` endpoint. 
- NSure SDK is used for additional device fingerprinting during registration/login.

### Real-time Notifications (Mercure)
- The app subscribes to `events.eneba.com/events-hub` via the Mercure protocol to receive real-time updates on confirmation commands.

## 5. Conclusion

### Automation Feasibility: 10%

### Critical Blockers:
1. **Cloudflare WAF**: Solving the Turnstile challenge programmatically.
2. **Multi-Factor Flow**: Separate codes for email and phone.
3. **Fingerprinting**: Integration of NSure and Mixpanel for identity tracking.
