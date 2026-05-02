# XTB - Research Report

## Metadata
- **Target URL/App**: `com.xtb.xmobile2`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-02`
- **Status**: `Completed`
- **HAR Files**: `XTB.har`

## 1. Executive Summary
XTB (xStation Mobile) uses a modern gRPC-based architecture for its mobile application. The registration and phone verification flow involves multiple gRPC calls to `ipax.xtb.com`. The payloads are encoded in Protobuf, requiring specific message structures for automation. The flow includes submitting a phone number, configuring verification, and finally confirming the 6-digit SMS OTP. No CAPTCHA or advanced bot protection was observed in the captured verification flow.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS (gRPC) | 6-digit numeric OTP |
| **Captcha** | None | No captcha challenges observed in the flow |
| **Encryption** | Protobuf | Binary serialization used for all gRPC requests |
| **Rate Limits** | Unknown | Not tested during capture |
| **Endpoints Involved** | 3 | `SendPhoneNumber`, `PostPhoneVerificationConfiguration`, `SendPhoneVerificationConfirmation` |
| **Bot Protection** | None | No visible bot protection mechanisms |

## 3. Flow Details

### Flow 1: Phone Verification (gRPC)

**Step 1: Send Phone Number**
- **Endpoint**: `POST https://ipax.xtb.com/pl.xtb.ipax.pub.grpc.onboarding.activation.v3.CustomerDataService/SendPhoneNumber`
- **Purpose**: Submit the user's phone number to trigger OTP.
- **Request Headers**:
    ```text
    Content-Type: application/grpc
    authorization: Bearer eyJhbGciOiJSUzI1NiIs...
    User-Agent: xStation Mobile Android/2.167.0 15 grpc-java-okhttp/1.77.0
    app-version: 2.167.0
    os-type: Android
    ```
- **Request Body (Binary/Protobuf)**:
    `\x00\x00\x00\x00\x1a\n\x1869f5990380c6477a46e49034 +393522050181  IT`
- **Response Body**:
    `\x00\x00\x00\x00\x15\b\x06\x10<\x1a\r+393522050181(\x00`

**Step 2: Configuration Verification**
- **Endpoint**: `POST https://ipax.xtb.com/pl.xtb.ipax.pub.grpc.onboarding.activation.v3.CustomerDataService/PostPhoneVerificationConfiguration`
- **Purpose**: Prepare the session for OTP confirmation.
- **Request Body (Binary/Protobuf)**:
    `\x00\x00\x00\x00\x1a\n\x1869f5990380c6477a46e49034`
- **Response Body**:
    `\x00\x00\x00\x00\x15\b\x06\x10<\x1a\r+393522050181(\x00`

**Step 3: Confirm Phone Verification**
- **Endpoint**: `POST https://ipax.xtb.com/pl.xtb.ipax.pub.grpc.onboarding.activation.v3.CustomerDataService/SendPhoneVerificationConfirmation`
- **Purpose**: Submit the 6-digit SMS OTP for verification.
- **Request Body (Protobuf Mapped)**:
    ```json
    {
      "1": "69f5990380c6477a46e49034", // Session/Customer ID
      "2": "121212",                   // SMS OTP
      "3": "+393522050181"             // Phone Number
    }
    ```
- **Raw Request Body (Binary)**:
    `\x00\x00\x00\x001\n\x1869f5990380c6477a46e49034\x12\x06121212\x1a\r+393522050181`
- **Response Body (Failure Example)**:
    `\x00\x00\x00\x00&\x12$\b\t\x12 Verification code does not match`

## 4. Security & Reversing Notes

### gRPC Implementation
The app uses `grpc-java-okhttp`. Automation requires a gRPC-compatible client and the corresponding `.proto` definitions or manual construction of the Protobuf payloads.

### Authentication
The session appears to be tied to a UUID/Hash (e.g., `69f5990380c6477a46e49034`) observed in the request bodies.

## 5. Conclusion

### Automation Feasibility: 70%

### Detailed Conclusion:
XTB's use of gRPC makes it slightly more complex to automate than standard REST APIs, but the flow itself is straightforward without CAPTCHA. The main challenge is correctly encoding/decoding the Protobuf messages. Once the message structure is mapped, automation is highly reliable.

### Strengths:
- Clean gRPC architecture.
- No CAPTCHA observed.

### Weaknesses:
- Protobuf serialization adds an entry barrier for simple scripts.
