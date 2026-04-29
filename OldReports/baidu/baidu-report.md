# Rednote (Xiaohongshu) - Research Report

## Metadata
- **Target URL/App**: `com.xingin.xhs` (Rednote / Xiaohongshu)
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29`
- **Status**: `Completed`
- **HAR Files**: `baidurednote.har`

## 1. Executive Summary
Rednote (Xiaohongshu) implements a sophisticated security architecture designed to mitigate automated attacks and unauthorized API access. The system utilizes **Geetest v4** as a mandatory interaction challenge before triggering SMS OTPs. Authentication is performed via a REST API under the `edith.xiaohongshu.com` domain, which requires extensive custom headers (`shield`, `x-mini-sig`, `xy-common-params`) for request validation. These headers are generated using a proprietary device integrity component known as **"Umi Sonoda"**. Automation is categorized as high difficulty due to the mandatory captcha and the complex request signing mechanism.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | OTP code required for login and phone binding |
| **Captcha** | Geetest v4 | Mandatory for SMS trigger and verification steps |
| **Encryption** | Standard | HTTPS with JSON and URL-encoded payloads |
| **Rate Limits** | Strict | Enforced via Geetest and device ID tracking |
| **Endpoints Involved** | 3 | `/vfc_code`, `/check_code`, `geetest/verify` |
| **Bot Protection** | High | Geetest + Umi Sonoda Device Fingerprinting |

## 3. Flow Details

### Flow 1: Registration / Login Flow

**Step 1: Phone Number Submitting Endpoint (SMS Trigger)**
- **Endpoint**: `GET https://edith.xiaohongshu.com/api/sns/v1/system_service/vfc_code?phone=<!-- 3515868778 -->&zone=39&type=login`
- **Request Headers**:
    ```text
    X-B3-TraceId: bcbc1e746b1f0a0f
    shield: XYAAQABAAAAAEAAABTAAAAUzUWEe0xG1IbD9/c+qCLOlKGmTtFa+lG438Me+FeRK9Cxo24nOdmRZ38q+Rbz8Mp38h+g/A1EwwaFWGLYrP2jio10OEecc250QFjxB/0TOxSt5po
    xy-common-params: fid=&gid=7cb2bf3dfdef5487fb71fdf6d1c122dae7b06d094735913977b4900c&device_model=phone&tz=Asia%2FKolkata&channel=GooglePlay&versionName=9.27.0&deviceId=03982a19-4d44-3335-bb73-d443682b1ef5&platform=android&sid=session.1777411805675623801624&identifier_flag=4...
    User-Agent: Dalvik/2.1.0 (Linux; U; Android 15; Pixel 7 Build/AP4A.250205.002) Resolution/1080*2400 Version/9.27.0 Build/9270802 Device/(Google;Pixel 7) discover/9.27.0 NetType/WiFi
    Host: edith.xiaohongshu.com
    ```
- **Response Headers**:
    ```text
    Server: Tengine
    Content-Type: application/json; charset=utf-8
    Request-Id: bcbc1e746b1f0a0f
    XHS-REQUEST-TIME: 0.153
    EagleId: a3b5529c17774119120904603e
    ```
- **Response Body**:
    ```json
    {"code":0,"success":true,"msg":"","data":{"success":true,"code":0,"message":""}}
    ```

**Step 2: Submit SMS OTP (Verification)**
- **Endpoint**: `GET https://edith.xiaohongshu.com/api/sns/v1/system_service/check_code?phone=<!-- 3515868778 -->&zone=39&code=<!-- 333333 -->&type=login`
- **Request Headers**:
    ```text
    X-B3-TraceId: a7a7bd8367180d0f
    x-mini-sig: 25eb656f4f2f9c5e1e90bdfa55160d0a00e44de6d8536e58d1cc6cd9dc4ebf39
    shield: XYAAQABAAAAAEAAABTAAAAUzUWEe0xG1IbD9/c+qCLOlKGmTtFa+lG438Me+FeRK9Cxo24nOdmRZ38q+Rbz8Mp38h+g/A1EwwaFWGLYrP2jio10OEu8xy38MjyAUzFRMC9R77g
    User-Agent: Dalvik/2.1.0 (Linux; U; Android 15; Pixel 7 Build/AP4A.250205.002) Resolution/1080*2400 Version/9.27.0 Build/9270802 Device/(Google;Pixel 7) discover/9.27.0 NetType/WiFi
    Host: edith.xiaohongshu.com
    ```
- **Response Headers**:
    ```text
    Server: Tengine
    Content-Type: application/json; charset=utf-8
    Request-Id: a7a7bd8367180d0f
    EagleId: a3b5529c17774119182447070e
    ```
- **Response Body (Invalid Case)**:
    ```json
    {"code":-14005,"success":false,"msg":"Incorrect SMS verification code.","data":{}}
    ```

## 4. Security & Reversing Notes

### Geetest Integration
- Rednote utilizes Geetest v4 for behavioral verification. The SMS trigger is blocked until a valid `lot_number` and `payload` from Geetest are provided.

### Request Signing & "Shield"
- The `shield` and `x-mini-sig` headers are critical for API authorization.
- These tokens are generated based on the request URL and body, likely using a native library (`libshield.so`) that incorporates device-specific data and timestamps.

### Device Fingerprinting (Umi Sonoda)
- The application reports extensive device telemetry to `/api/sns/v1/system_service/umi_sonoda` and `/api/sns/v1/system_service/device_params_info`.
- This data is used to build a unique hardware profile, making emulator detection highly effective.

## 5. Conclusion
Rednote (Xiaohongshu) presents a formidable challenge for automation due to its multi-layered defense-in-depth strategy. The mandatory Geetest v4 captcha effectively prevents simple scripted SMS triggers. Furthermore, the reliance on complex, proprietary request signing (Shield/Mini-Sig) and deep hardware-level fingerprinting (Umi Sonoda) ensures that only legitimate, verified mobile devices can interact with the authentication API. Automated verification is only possible with a full browser orchestration layer or specialized reverse engineering of the native signing libraries.
