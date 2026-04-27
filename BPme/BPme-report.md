# BPme (Poland) - Research Report

## Metadata
- **Target URL/App**: `com.bp.app.bpme.global.pl`
- **Researcher**: `Antigravity`
- **Date**: `2026-04-27`
- **Status**: `Completed`
- **HAR Files**: `BPme.har (Account Settings & Identity Flow)`

## 1. Executive Summary
BPme (Poland) implements a dual-layer security architecture for identity and profile management. Core authentication and sensitive attribute verification (like phone numbers) are managed through **ForgeRock (energyid.bp.com)** using a multi-step callback system (`IDToken` inputs). Backend synchronization and post-login profile updates are handled via **gRPC over HTTP/2 (app.bpglobal.com)**. The platform is protected by **AWS WAF**, which triggers visual/slider captchas during sensitive operations. Automation feasibility is low to medium due to the requirement of handling AWS WAF tokens and complex gRPC message structures.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS OTP | Verified via ForgeRock `IDToken` callbacks |
| **Captcha** | Yes | AWS WAF (Human Verification) with `challenge.js` and `captcha.js` |
| **Encryption** | Yes | TLS 1.3, JWT-based `authId` session tokens, and binary gRPC encoding |
| **Rate Limits** | Medium | 30s cooldown enforced via `expiryDurationInSec` in verification responses |
| **Endpoints Involved** | 5 | `/authenticate`, `/access_token`, `/userinfo`, `/BPme/Service` (gRPC), `/BPme/Page` (gRPC) |

## 3. Flow Details

### Flow: Phone Verification (Account Settings / Personal Information)

**Step 1: Initialize Verification Session**
- **Endpoint**: `POST https://energyid.bp.com/am/json/realms/root/realms/bravo/authenticate`
- **Purpose**: Initialize the authentication session and trigger AWS WAF challenge if necessary.
- **Notable Headers**:
    - `X-Requested-With`: `com.bp.app.bpme.global.pl`
    - `Content-Type`: `application/json`
- **Response**: Returns a HTML challenge page (AWS WAF) or a set of callbacks for user input.

**Step 2: Solve AWS WAF Captcha**
- **Endpoint**: `POST https://6ae9290696ae.a93af50d.ap-south-1.captcha.awswaf.com/6ae9290696ae/verify`
- **Purpose**: Validate the captcha solution and obtain a `voucher` to continue the ForgeRock flow.

**Step 3: Submit Phone Number**
- **Endpoint**: `POST https://energyid.bp.com/am/json/realms/root/realms/bravo/authenticate`
- **Purpose**: Submit the telephone number to the identity provider.
- **Request Payload**:
    ```json
    {
      "authId": "eyJ0eXAiOiJKV1QiLCJraWQiOiJJb1Z4V3NLT2J6ZDB2TTFhNVBIVHNYZ2J2Zlk9I...",
      "callbacks": [
        {
          "type": "StringAttributeInputCallback",
          "input": [
            {
              "name": "IDToken3",
              "value": "+918791267460"
            }
          ]
        }
      ]
    }
    ```
- **Response**:
    ```json
    {
      "authId": "...",
      "callbacks": [
        {
          "type": "MetadataCallback",
          "output": [
            {
              "name": "data",
              "value": {
                "output": {
                  "type": "data",
                  "messageTextKey": "web.registration.otp-verification.otp-code-input.placeholder"
                }
              }
            }
          ]
        }
      ]
    }
    ```

**Step 4: Submit OTP Code**
- **Endpoint**: `POST https://energyid.bp.com/am/json/realms/root/realms/bravo/authenticate`
- **Purpose**: Verify the SMS code received by the user.
- **Request Payload**:
    ```json
    {
      "authId": "...",
      "callbacks": [
        {
          "type": "StringAttributeInputCallback",
          "input": [
            {
              "name": "IDToken4",
              "value": "548761"
            }
          ]
        }
      ]
    }
    ```
- **Response**:
    ```json
    {
      "tokenId": "pEr2aYE4v6vWjbh9lGrAkGFq03c.*AAJTSQACMDIAAlNLABxIaDhFR2xoQi8xRFdyTmdlVGNBRm5Eall2Wk09...",
      "successUrl": "https://energyid.bp.com/am/oauth2/authorize?..."
    }
    ```

**Step 5: Synchronize Profile (Backend Update)**
- **Endpoint**: `POST https://app.bpglobal.com/BPme/Service` (gRPC)
- **Purpose**: Update the service backend with the verified phone number and profile status.
- **Request Payload (Decoded gRPC)**:
    ```
    ...
    VALIDATE_CIP_OTP_NUMBER
    +918791267460
    Asia/Kolkata
    screen_name
    button_name: verify
    button_click
    isFirstVisitAfterLogin: true
    ...
    ```

## 4. Security & Reversing Notes

### Encryption/Signing Mechanisms
- **JWT (authId)**: ForgeRock uses a large JWT-like string (`authId`) to maintain state across multiple POST requests. This token includes `iat`, `exp`, and encrypted session data.
- **gRPC Encoding**: Backend communication uses gRPC with `gzip` compression. Messages are binary-encoded and require specific `.proto` definitions for full reconstruction.
- **AWS WAF Tokens**: Requests to `energyid.bp.com` are protected by AWS WAF cookies (`aws-waf-token`), which are generated after solving the captcha challenge.

### Bot Detection
- **AWS WAF**: Monitors request patterns and triggers captchas for high-risk IPs or frequent attempts.
- **Identity Session Binding**: ForgeRock binds the verification flow to the `tokenId` and `authId`, preventing cross-session replay.

## 5. Conclusion

### Automation Feasibility: 35%

### Critical Blockers:
1. **AWS WAF Integration**: Automated solving of the slider/visual captcha requires advanced computer vision or headless browser interaction.
2. **gRPC Complexity**: The service backend expects binary-encoded gRPC messages. Any automation must correctly implement the protobuf schema and handle `gzip` compression.
3. **ForgeRock State Management**: The verification journey is stateful; if a step fails or the `authId` expires, the entire flow must be restarted from the beginning.
