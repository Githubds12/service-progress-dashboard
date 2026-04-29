# Luno - Research Report

## Metadata
- **Target URL/App**: `co.bitx.android.wallet`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29 22:53`
- **Status**: `Completed`
- **HAR Files**: `Luno.har`

## 1. Executive Summary
Luno (co.bitx.android.wallet) implements a secure mobile-first API using Google Protobuf for binary serialization and a custom request signing mechanism (`LunoSigV2`). The authentication flow transitions from a standard JSON-based registration to a binary-serialized onboarding state machine. The platform uses Cloudflare for perimeter security and Google reCAPTCHA for bot protection during the initial signup phase. Automation is feasible but requires a correct implementation of the `LunoSigV2` HMAC-SHA256 signature and Protobuf field mapping.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for identity verification |
| **Captcha** | reCAPTCHA v2 Checkbox (Google) | Triggered during `/api/m1/signup` |
| **Encryption** | Protobuf (Binary) | `application/octet-stream` payloads with custom signing |
| **Rate Limits** | 60s Cooldown | Explicitly observed as `ErrOTPMinInterval` |
| **Endpoints Involved** | 5 | `/signup`, `/authorize`, `/onboarding/individual/flow` |
| **Bot Protection** | LunoSigV2 + Cloudflare | Request signing tied to `hmac_secret` and device tokens |

## 3. Flow Details

### Flow 1: Registration & Device Authorization

**Step 1: User Signup**
- **Endpoint**: `POST /api/m1/signup`
- **Purpose**: Initial account creation
- **Request Payload**:
    ```json
    {
        "email": "deepanshusinghdigitalheroes@gmail.com",
        "password": "[REDACTED]",
        "location": "IN",
        "captcha_response": "03AFcWeA7..."
    }
    ```
- **Response**:
    ```json
    {
        "success": true
    }
    ```

**Step 2: Device Authorization**
- **Endpoint**: `POST /api/m1/authorize`
- **Purpose**: Exchange credentials for session keys and HMAC secrets
- **Request Payload**:
    ```json
    {
        "email": "deepanshusinghdigitalheroes@gmail.com",
        "password": "[REDACTED]",
        "android_device_id": "76ad6ad62418e8bc",
        "make": "Google",
        "model": "Pixel 7",
        "os_version": "15"
    }
    ```
- **Response**:
    ```json
    {
        "api_key_id": "jwjghbpbjq35g",
        "api_key_secret": "imWhGf5YM5yysM-URbVFGEKzS072n5YE35PUxwwRDWc",
        "hmac_secret": "1421b7e48e97849c512a41c442d357a7cec9cb4eef285d7b8dde0c815a148e70",
        "new_user": false
    }
    ```

### Flow 2: Onboarding & Phone Verification

**Step 1: Submit Phone Number**
- **Endpoint**: `POST /api/onboarding/individual/flow`
- **Purpose**: Request SMS OTP for a specific mobile number
- **Notable Headers**:
    - `Authorization`: `Basic andqZ2hicGJqcTM1ZzppbVdoR2Y1WU01eXlzTS1VUmJWRkdFS3pTMDcybjVZRTM1UFV4d3dSRFdj`
    - `X-Luno-Signature`: `LunoSigV2 giJ43FAAvFyPXhGwdz+OSfNd+lbdIxYVhC0Zjogosvo=`
    - `X-Luno-Device-Id-Token`: `ZHQxebT1y4z/tJml4bTiL4zEJA==:EfulTxaqBcSnvIXUuEQuEBQ/pkM=`
- **Request Payload (Decoded Protobuf)**:
    <!-- Phone Submission -->
    ```protobuf
    2: 187
    3: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    4 {
      1: "dialling_code"
      2: "+39"
    }
    4 {
      1: "phone_number"
      2: "3517602732"
    }
    ```
- **Response Payload (Decoded Protobuf)**:
    ```protobuf
    # Contains UI instructions for OTP entry
    Onboard: Check SMS
    Enter the 6-digit code we sent to +393517602732
    ```

**Step 2: Verify OTP**
- **Endpoint**: `POST /api/onboarding/individual/flow`
- **Purpose**: Submit the 6-digit verification code
- **Request Payload (Decoded Protobuf)**:
    <!-- OTP Submission -->
    ```protobuf
    2: 188
    3: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    4 {
      1: "pin"
      2: "999999"
    }
    ```
- **Response Payload (Decoded Protobuf)**:
    ```protobuf
    # Error response for invalid code
    ErrPhoneCodeInvalid: Invalid verification code
    pin: You added an incorrect code
    ```

## 4. Security & Reversing Notes

### Binary Protocol (Protobuf)
Luno utilizes Google Protobuf for all state-changing onboarding requests. The payloads are serialized into `application/octet-stream`. Reversing revealed a consistent message structure:
- **Field 2**: Request sequence identifier.
- **Field 3**: JWT state token containing session metadata and the current flow step.
- **Field 4**: Key-value pairs for user input (e.g., `phone_number`, `pin`).

### Request Signing (LunoSigV2)
The `X-Luno-Signature` is an HMAC-SHA256 hash likely calculated over the request path, timestamp, and body using the `hmac_secret` provided during the `/authorize` step. This prevents request tampering and replay attacks.

### Bot Detection & Rate Limiting
- **Cloudflare**: Protects the API endpoints from volumetric attacks.
- **Cooldown**: A 60-second cooldown is enforced between OTP resend requests, returning an `ErrOTPMinInterval` error if violated.
- **Device Fingerprinting**: The `X-Luno-Device-Id-Token` binds the session to a specific hardware identifier.

## 5. Conclusion

### Automation Feasibility: 60% (Medium)

### Detailed Conclusion:
The Luno authentication flow is well-structured and uses modern security practices. The primary hurdle for automation is the **LunoSigV2** signature generation, which requires the `hmac_secret` obtained via a legitimate login session. Once the signature and Protobuf serialization are handled, the flow is highly predictable. The reliance on standard reCAPTCHA for signup means that bypass tools can be integrated. Recommendations for automation include implementing a full Protobuf message builder and accurately mirroring the device fingerprinting headers.
