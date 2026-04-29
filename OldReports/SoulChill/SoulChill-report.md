# SoulChill - Research Report

## Metadata
- **Target URL/App**: `com.live.soulchill` (SoulChill)
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29`
- **Status**: `Completed`
- **HAR Files**: `SoulChill.har`

## 1. Executive Summary
SoulChill (part of the Momo/Immomo Group) employs an extremely high level of security to protect its authentication services. All critical API communication under the `api-base.soulchill.live` domain is encrypted using a proprietary mechanism (`isEncryption: true`) and compressed via GZIP. The payloads and responses are transmitted as Base64-encoded encrypted blobs (`mzip`), effectively masking all sensitive data including phone numbers and OTP codes. Additionally, the platform integrates **CheckTrustworthiness** and **Forter** for device integrity and behavioral analysis. Automation is categorized as low feasibility due to the requirement for deep reverse engineering of the native encryption libraries.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | 6-digit OTP code delivered via encrypted channels |
| **Captcha** | Geetest v4 / reCAPTCHA | Integrated as behavioral challenges during registration |
| **Encryption** | Advanced | Proprietary Momo Group encryption (`mzip`) with request signing |
| **Rate Limits** | Strict | Managed via CheckTrustworthiness and device fingerprinting |
| **Endpoints Involved** | 2 | `sendVerifyCode`, `loginPhone` |

## 3. Flow Details

### Flow 1: Mobile Authentication

**Step 1: Phone Number Submitting Endpoint (SMS Trigger)**
- **Endpoint**: `POST https://api-base.soulchill.live/api/session/sendVerifyCode`
- **Purpose**: Initiate the authentication session and trigger the SMS OTP delivery.
- **Notable Headers**:
    - `isEncryption`: true (Indicates encrypted payload)
    - `fr`: ba9aeb5b148803764a3da68cad2f7e062e622b35 (Dynamic session/fraud identifier)
    - `x-req-compress`: gzip
- **Request Payload**:
    ```text
    mzip=IpnQAJ6i9BpfuhzDeKv87Isfxu+zrfOolPafyI1qBvEVczCXzVmkiy2yU4i9utQ0MJ9EZhdazEdRShUfrOxR/1D1HlGPPxQDuIpDpSErNZi0ItxplhKsFISvBuNZw7yMz+Pwnb88Nt/bkmRgCVfxpfaYpKNyOEYaropCX3ZIEE0a/o4OMawndnVtxw2HRq0iqiH023g56jceryVV6Pk3pqW3+Qx0f5UTEblYEMAXr/Y=
    ```
- **Response Headers**:
    ```text
    Server: openresty
    Content-Encoding: gzip
    ```
- **Response Body**:
    ```text
    kcZJOEG8OD09R1LJtN/WFo8PwutNAhWWZPCsYpCEGdBPW2tlxEN+lKJMPpVs4inWlIE9NV5DutK50f1badbzP3SjJad6n80VkNYYYuvaASnPdc/c2fa8n4trbk0EQ8ypMSQf0lug5n4nKzIHocvMgQ==
    ```

**Step 2: Submit SMS OTP (Login)**
- **Endpoint**: `POST https://api-base.soulchill.live/api/session/loginPhone`
- **Purpose**: Verify the OTP and authenticate the user session.
- **Notable Headers**:
    - `User-Agent`: SoulChill/4.24_b2604233 Android/4252
    - `isEncryption`: true
- **Request Payload**:
    ```text
    mzip=QlFBdDZFdDMwTVVocmlELy9wSDBRb0JNdzg5TE5QRmMrSzIvWGYrTUY4QTNlZTgzR0JyL2xCOXh4d3Jwa01Vb1dzSjdtVFBHZ0Rrdk5VZHYxcnliTGt2d1ViZVltVzdRdUVPUGNnaXZVNkxTQmlmN0J6SWdPME5Fa1ZNZjdjZGtXMUlZK2oxMUk4WWNLeE41ck5IcFpmU0Jva3BWSEI1SXgvNXI3M0FmbGtHby9UNTRSK205UFF3M...
    ```
- **Response Body**:
    ```text
    kcZJOEG8OD09R1LJtN/WFo8PwutNAhWWZPCsYpCEGdBPW2tlxEN+lKJMPpVs4inWlIE9NV5DutK50f1badbzP3SjJad6n80VkNYYYuvaASnPdc/c2fa8n4trbk0EQ8ypMSQf0lug5n4nKzIHocvMgQ==
    ```

## 4. Security & Reversing Notes

### Proprietary Momo Encryption
- SoulChill uses the **Momo Group "mzip" encryption** protocol. This protocol encrypts the entire key-value structure of the request body before Base64 encoding.
- Decryption requires reversing the `libmomo.so` (or similar) native library, which handles AES-CBC/RSA and GZIP compression logic.

### Device Integrity (CheckTrustworthiness)
- The app integrates the **CheckTrustworthiness** SDK (`checktrustworthiness.com`), which performs extensive environmental checks (root detection, emulator checks, proxy detection) before allowing critical API calls.

### Behavioral Analysis (Forter)
- **Forter** is used to monitor user behavior and device consistency. Requests without valid Forter tokens (`lvBk7kGkmkNP...`) are likely flagged as high-risk or blocked.

## 5. Conclusion

### Automation Feasibility: 5%

### Critical Blockers:
1. **End-to-End Encryption**: The `mzip` protocol ensures that no data is visible in transit, requiring native library hook or reverse engineering.
2. **Device Trust Score**: CheckTrustworthiness ensures that only legitimate physical devices can successfully interact with the backend.
3. **Advanced Bot Protection**: The combination of Forter and Geetest v4 makes standard browser-based automation impossible.
4. **Momo Ecosystem**: As part of the Momo group, SoulChill shares a highly mature security infrastructure designed to combat high-volume automated attacks.
