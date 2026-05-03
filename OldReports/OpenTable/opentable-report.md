# OpenTable - Research Report

## Metadata
- **Target URL/App**: `OpenTable`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-03`
- **Status**: `Completed`
- **HAR Files**: `OpenTable.har (1 flow: SMS Verification)`

## 1. Executive Summary
OpenTable's Android application (version 26.13.2) implements a Two-Factor Authentication (2FA) flow for account verification and security. The flow is managed via a dedicated mobile API (`mobile-api.opentable.com`) and involves a two-step process: initiating the SMS request and confirming the received code. While the captured HAR showed a 404 error during the confirmation step, the request structure remains consistent with standard RESTful patterns. The platform utilizes Akamai Bot Manager (`ak_bmsc` cookies) for anti-automation protection.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for 2FA |
| **Captcha** | Undefined | No visible captcha in the captured 2FA flow |
| **Encryption** | Standard | HTTPS with OAuth2 Bearer tokens |
| **Rate Limits** | Unknown | Not explicitly captured in the trace |
| **Endpoints Involved** | 2 | `/api/v1/2fa/start`, `/api/v1/2fa/confirm` |

## 3. Flow Details

### Flow 1: SMS Verification

**Step 1: Start 2FA (Send OTP)**
- **Endpoint**: `POST https://mobile-api.opentable.com/api/v1/2fa/start`
- **Purpose**: Initiate the SMS OTP delivery to the specified phone number.
- **Notable Headers**:
    - `Authorization`: Bearer `96ce9a64-6265-4748-8208-4ea77ef18afa`
    - `User-Agent`: `com.opentable/26.13.2; android; android/15; 2.6/2400x1080; 39f68efd-b805-48e9-bd6b-231dc4f8f916/Anonymous`
    - `X-OT-SessionId`: `fa749163-8503-4d09-aef4-9754cf6d27b8`
- **Request Payload**:
    ```json
    {
      "phone": {
        "countryCode": "39",
        "countryId": "IT",
        "number": "3516308644"
      },
      "target": "SMS"
    }
    ```
- **Response**:
    ```json
    {
      "correlationId": "a74eb528-a07b-4a35-b9c5-6e6bda5ba211"
    }
    ```
- **Analysis**: The endpoint returns a `correlationId` which must be passed in the subsequent confirmation request to link the OTP to the session.

**Step 2: Confirm 2FA (Verify OTP)**
- **Endpoint**: `POST https://mobile-api.opentable.com/api/v1/2fa/confirm`
- **Purpose**: Submit the OTP code received via SMS for verification.
- **Request Payload**:
    ```json
    {
      "allowPhoneRecycling": true,
      "code": "369258",
      "correlationId": "a74eb528-a07b-4a35-b9c5-6e6bda5ba211",
      "phone": {
        "countryCode": "39",
        "countryId": "IT",
        "number": "3516308644"
      }
    }
    ```
- **Response**:
    - **Status**: `404 Not Found`
- **Analysis**: The captured flow shows a 404 response for the confirmation attempt. This could indicate an expired session, incorrect `correlationId`, or an issue with the specific test account/phone number used during capture.

## 4. Security & Reversing Notes

### Encryption/Signing Mechanisms

**1. OAuth2 Authentication**
- **Mechanism**: The app uses a Bearer token for authorized requests.
- **Token Generation**: An anonymous token is retrieved from `https://mobile-api.opentable.com/oauth/consumer/token` using client credentials (`client_id=ot-anonymous-apps`, `client_secret=0pentab1e`).

**2. Bot Detection (Akamai)**
- **Cookies**: `ak_bmsc`
- **Analysis**: OpenTable uses Akamai Bot Manager to detect and block automated traffic. Successful automation would likely require handling Akamai's challenge-response mechanisms or using high-quality proxies and browser-mimicking headers.

## 5. Conclusion

### Automation Feasibility: 40%

### Critical Blockers:
1. **Akamai Bot Manager**: The presence of `ak_bmsc` cookies indicates robust anti-bot protection that may block simple scripted requests.
2. **404 Response**: The failure of the confirmation endpoint in the trace suggests potential strict session or environment validation that was not fully met during the HAR capture.
3. **Session Consistency**: The `correlationId` and `X-OT-SessionId` must be correctly synchronized across the flow.
