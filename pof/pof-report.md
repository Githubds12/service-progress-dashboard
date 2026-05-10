# Plenty Of Fish (POF) - Research Report

## Metadata
- **Target URL/App**: `pof.com` / `com.pof.android`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-10`
- **Status**: `Completed`
- **HAR Files**: `pof.har`

## 1. Executive Summary
Plenty Of Fish (POF), a major dating platform, utilizes a highly obfuscated and binary-heavy communication protocol for its Android application. The analysis of the `pof.har` file revealed that all primary API interactions with `2.api.pof.com` are performed via `POST` requests to a single root endpoint. These requests lack standard human-readable JSON or form-data bodies; instead, they use custom headers like `X-Content-Encoding: gzip` and `x-Accepts: compression` to transmit binary-encoded payloads. The response data is similarly binary and base64-encoded, making traditional traffic analysis and endpoint mapping extremely challenging without reversing the application's underlying protocol implementation.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Observed as the primary verification channel |
| **Captcha** | undefined | No third-party captcha (e.g., Google, hCaptcha) was detected |
| **Encryption** | Binary/Custom | Gzip-compressed binary payloads over HTTP |
| **Rate Limits** | Unknown | No rate limiting behavior (429/403) was captured in the trace |
| **Endpoints Involved** | 1 | Single root endpoint `https://2.api.pof.com/` for all actions |
| **Bot Protection** | High | Heavy use of binary obfuscation and custom session/install IDs |

## 3. Technical Traces

### 3.1 Binary API Communication
All functional requests are routed through a single endpoint with custom headers for compression and session tracking.

**Request**:
```http
POST https://2.api.pof.com/ HTTP/1.1
Host: 2.api.pof.com
User-Agent: Dalvik 5.63.0.1516574; (Linux; U; Android 15; Pixel 7; OFF; en_IN) fb83d770c0ee0fa3; 411x914x2.625
X-Content-Encoding: gzip
x-Accepts: compression
X-POF-App-Session-Id: d65bb132-a9a4-43e8-a95b-18fdad7a44dc
x-pof-install-id: f386575e-4e2d-4313-956e-9845c777819d
Content-Type: text/plain
Content-Length: [Binary Data Length]
```
<!-- Note: The request body is GZIP-compressed binary data, not human-readable. -->

**Response**:
```http
HTTP/1.1 200 OK
Content-Type: text/plain

[Base64 Encoded Binary Data]
```

## 4. Automation Feasibility
- **Feasibility**: Low (< 40%)
- **Reasoning**: The application employs a proprietary binary protocol. Unlike standard REST APIs that use JSON, POF uses GZIP-compressed binary blobs for both requests and responses. Automating the SMS verification flow would require a deep dive into the APK's native or Java code to understand the serialization logic and properly reconstruct the binary payloads. Without this protocol reversal, direct HTTP automation is not currently possible.

## 5. Conclusion
The POF Android application implements robust technical defenses against automated interaction. By consolidating all API actions into a single endpoint and using compressed binary payloads, the platform effectively hides its internal logic and parameter names. While the SMS verification code (198695) was successfully received, the submission of this code happens within the encrypted binary stream. Professional automation would require a full protocol reconstruction based on application reverse engineering.
