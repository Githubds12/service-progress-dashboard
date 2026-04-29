# BPme (Poland) - Security Research Report

## Metadata
- **Researcher**: Deepanshu Singh
- **Date**: 2026-04-27
- **Target App**: `com.bp.app.bpme.global.pl` (v2.4.3)
- **Status**: Completed Analysis

## 1. Executive Summary
BPme (Poland) utilizes a sophisticated identity management framework based on **ForgeRock Access Management**. Sensitive user operations, specifically phone number verification within the account settings, are governed by a stateful multi-step authentication journey. This journey involves sequential `IDToken` callbacks for submitting identifying data and verifying One-Time Passwords (OTP). The infrastructure is further hardened by **AWS WAF (Web Application Firewall)**, which transparently injects bot-detection challenges (Slider/Visual Captcha) to mitigate automated abuse. While the identity layer is REST-based, the backend synchronization for profile updates leverages **gRPC over HTTP/2**, adding a significant layer of complexity to the reversing and automation process.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS OTP | Managed via ForgeRock sequential callbacks |
| **Captcha** | AWS WAF CAPTCHA | Slider/Visual challenges triggered on sensitive POSTs |
| **Encryption** | TLS 1.3 / JWT | Session state maintained via encrypted `authId` JWTs |
| **Rate Limits** | Unknown | No explicit 429 errors observed in the trace |
| **Endpoints Involved** | 4 | ForgeRock Auth, gRPC Service, AWS WAF Verify |
| **Bot Protection** | AWS WAF | Advanced behavioral and challenge-based protection |

## 3. Flow Details

### Flow: Personal Information Phone Verification

**Step 1: Initiate Identity Journey**
- **Endpoint**: `POST https://energyid.bp.com/am/json/realms/root/realms/bravo/authenticate`
- **Request**:
    ```json
    {
      "authId": "initial_session_id"
    }
    ```
- **Response**:
    ```json
    {
      "authId": "eyJ0eXAiOiJKV1QiLCJraWQi...",
      "callbacks": [
        {
          "type": "StringAttributeInputCallback",
          "input": [ { "name": "IDToken3", "value": "" } ]
        }
      ]
    }
    ```

**Step 2: Submit Phone Number**
- **Endpoint**: `POST https://energyid.bp.com/am/json/realms/root/realms/bravo/authenticate`
- **Request**:
    <!-- Phone Number Submission -->
    ```json
    {
      "authId": "...",
      "callbacks": [
        {
          "type": "StringAttributeInputCallback",
          "input": [ { "name": "IDToken3", "value": "+918791267460" } ]
        }
      ]
    }
    ```
- **Response**: Returns the next callback set for OTP input.

**Step 3: Submit OTP Verification**
- **Endpoint**: `POST https://energyid.bp.com/am/json/realms/root/realms/bravo/authenticate`
- **Request**:
    <!-- OTP Submission -->
    ```json
    {
      "authId": "...",
      "callbacks": [
        {
          "type": "StringAttributeInputCallback",
          "input": [ { "name": "IDToken4", "value": "548761" } ]
        }
      ]
    }
    ```
- **Response**:
    ```json
    {
      "tokenId": "pEr2aYE4v6vWjbh9lGrAkGFq03c...",
      "successUrl": "/am/oauth2/authorize?..."
    }
    ```

## 4. Security & Reversing Notes
- **State Management**: The `authId` token is a critical state-carrying JWT. If the sequence is broken or the token expires, the entire verification journey resets.
- **gRPC Synchronization**: Post-verification, the app triggers a `VALIDATE_CIP_OTP_NUMBER` event via gRPC to `app.bpglobal.com/BPme/Service`. This is a binary-encoded message containing the validated phone number and platform metadata.
- **Captcha Implementation**: AWS WAF challenges are injected dynamically. Automation must handle the `aws-waf-token` and solve the resulting visual challenge.

## 5. Conclusion

### Automation Feasibility: Low (30%)

### Detailed Conclusion
The BPme (Poland) security posture is robust, primarily due to the layered defense provided by ForgeRock and AWS WAF. The identity flow is highly stateful, making session-based automation difficult without a full browser context. Furthermore, the reliance on binary gRPC for backend synchronization requires custom protobuf implementations for any reliable scraping or automated interaction. While the core OTP flow is identifiable, the combined hurdles of AWS WAF captchas and gRPC message structures make large-scale automation unfeasible without significant engineering effort.
