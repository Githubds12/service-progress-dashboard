# buz - Research Report

## Metadata
- **Target URL/App**: `com.interfun.buz` (Buz: Instant Messenger)
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29`
- **Status**: `Completed`
- **HAR Files**: `buz.har`

## 1. Executive Summary
Buz (Interfun) uses a gRPC-style JSON proxy architecture (`httpproxy.buz-app.com`) for its core services. The authentication flow involves a standard SMS OTP trigger (`sendSmsCode`) followed by a phone login (`phoneLogin`). The application integrates several telemetry and risk assessment services, including **TiyaLive** (CloudConf) and **VocalBeats**. The API payloads are plain JSON, but require a unique `traceId` and `deviceId` (imDeviceParams) for successful authentication.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | 6-digit OTP code |
| **Captcha** | None | No interactive captcha observed during registration |
| **Encryption** | Standard | HTTPS with JSON payloads |
| **Rate Limits** | Moderate | Enforced via `traceId` and device identification |
| **Endpoints Involved** | 2 | `sendSmsCode`, `phoneLogin` |
| **Bot Protection** | Moderate | ShuMei (TiyaLive) integration for risk profiling |

## 3. Flow Details

### Flow 1: Registration / Login

**Step 1: Request SMS Code**
- **Endpoint**: `POST https://httpproxy102.buz-app.com/com.buz.idl.login.service.BuzNetLoginService/sendSmsCode`
- **Request Headers**:
    ```text
    User-Agent: Buz/1.98.0 (Android; 15; Google Pixel 7)
    Content-Type: application/json; charset=utf-8
    ```
- **Request Body**:
    ```json
    {
      "request": {
        "installedApp": [1],
        "phone": "39-3513534110",
        "phoneInputType": 5,
        "resend": false,
        "riskParams": {
          "mediaChannel": "Organic",
          "storeChannel": "google"
        },
        "traceId": "90ca23dd3ecf842374e654941dd47829",
        "type": 3
      }
    }
    ```
- **Response Body**:
    ```json
    {
      "code": 0,
      "message": "success",
      "response": {
        "ttl": 60
      }
    }
    ```

**Step 2: Submit SMS OTP (Login)**
- **Endpoint**: `POST https://httpproxy102.buz-app.com/com.buz.idl.login.service.BuzNetLoginService/phoneLogin`
- **Request Headers**:
    ```text
    Content-Type: application/json; charset=utf-8
    ```
- **Request Body**:
    ```json
    {
      "request": {
        "imDeviceParams": {
          "clientVersion": 10020100,
          "deviceId": "Ac1ba13a19428ebafe2543ac70266759c",
          "deviceType": "android-35"
        },
        "phone": "39-3513534110",
        "riskParams": {
          "mediaChannel": "Organic",
          "storeChannel": "google"
        },
        "smsCode": "855885",
        "traceId": "96677abe4dac6fb49d1b349c3d202813"
      }
    }
    ```
- **Response Body**:
    ```json
    {
      "code": 1,
      "msg": "17b0a4c3d6564081843d1de2d1fc593b"
    }
    ```

## 4. Security & Reversing Notes

### Trace ID & Device Identification
- The `traceId` is a 32-character hex string generated locally.
- `imDeviceParams` contains a persistent `deviceId` which is likely tied to the hardware or install instance.

### Risk Management (TiyaLive)
- The app communicates with `tycollectproxy.tiyalive.com` to fetch cloud configurations and report profile metadata. This is part of the ShuMei risk management suite used by Interfun.

## 5. Conclusion

### Automation Feasibility: 70%

### Critical Blockers:
1. **Device Fingerprinting**: Requires consistent `deviceId` and `traceId` generation.
2. **Risk Assessment**: High-frequency attempts may be flagged by the TiyaLive/ShuMei integration.
