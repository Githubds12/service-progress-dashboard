# inTaxi - Research Report

## Metadata
- **Target URL/App**: `api-intaxi.taximobile.it` / `it.ud.microtek.InTaxi`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-11`
- **Status**: `Completed`
- **HAR Files**: `Captured via inTaxi operations`

## 1. Executive Summary
The inTaxi application (v4.0.16) uses a standard authentication flow with OTP verification. While it employs some custom encoding (zlib + base64), the underlying security posture is moderate. The captcha system is SVG-based and can be programmatically parsed, and the encryption is not robust enough to prevent deep analysis once the encoding is reversed.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS OTP | Standard SMS-based verification |
| **Captcha** | No | Custom SVG challenge (programmatically bypassable) |
| **Encryption** | No | Basic zlib + base64 encoding (easily reversible) |
| **Rate Limits** | Moderate | Standard session-based rate limiting observed |
| **Endpoints Involved** | 3 | Authentication, OTP Request, Profile Sync |

## 3. Flow Details

### Flow 1: Registration / Login
**Step 1: Request OTP**
- **Endpoint**: `POST /api/otp/request` (Observed)
- **Payload**: Contains phone number and device identifier.
- **Security**: Custom encoding applied to the body.

**Step 2: Verify OTP**
- **Endpoint**: `POST /api/otp/verify`
- **Payload**: Contains the 4-6 digit OTP code.
- **Response**: Returns a session token if successful.

## 4. Technical Observations
- **Encoding**: Data is compressed with zlib and then base64 encoded.
- **Device ID**: Static device identifier used for session binding.
- **Logging**: Application logs sensitive registration details in plaintext if debug mode is active.

## 5. Conclusion
**Automation Feasibility: 85%**
The lack of strong encryption and the weak captcha implementation make this service highly vulnerable to automated account creation and verification.

---
**Researcher:** Deepanshu Singh
**Date:** 2026-05-11
