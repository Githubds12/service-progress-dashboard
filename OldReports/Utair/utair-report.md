# Utair Mobile - Research Report

## Metadata
- **Target URL/App**: `ru.utair.android`
- **Researcher**: `Deepanshu Singh`
- **Date**: `07 May, 2026`
- **Status**: `Completed`
- **HAR Files**: `utair.har (34 events)`

## 1. Executive Summary
Utair's mobile application (`ru.utair.android`) uses a multi-stage authentication process involving OAuth token acquisition, device registration, and a stateful login flow. The system primarily utilizes SMS-based verification (identified as `standard` confirmation type) to authenticate users. The backend enforces strict session management via an `attempt_id`, which must be synchronized between the login initiation and confirmation steps. Security measures include the use of `Bearer` tokens for authorization and custom headers for request synchronization. While no traditional captcha was observed, the application relies on device-specific identifiers and time-sensitive tokens to prevent unauthorized access.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for OTP (standard confirmation) |
| **Captcha** | undefined | No captcha was observed in the intercepted flow |
| **Encryption** | Standard HTTPS | Uses Bearer token authorization and custom timestamp headers |
| **Rate Limits** | Unknown | No explicit rate limiting behavior was observed during testing |
| **Endpoints Involved** | 5 | `/oauth/token`, `/api/v1/devices/`, `/api/v1/profile/`, `/api/v1/login/`, `/api/v1/login/confirm/` |
| **Bot Protection** | Internal | Relying on session-bound attempt_ids and device registration |

## 3. Flow Details

### Flow 1: Authentication via SMS OTP

**Step 1: OAuth Handshake**
- **Endpoint**: `POST https://b.utair.ru/oauth/token`
- **Purpose**: Retrieve the initial access token for the session.
- **Request Headers**:
    - `Authorization`: Basic dXRhaXJfYW5kcm9pZDpzZWNyZXQ=
    - `Content-Type`: application/x-www-form-urlencoded
- **Request Payload**:
    ```text
    grant_type=client_credentials
    ```
- **Response Headers**:
    - `Content-Type`: application/json
- **Response Body**:
    ```json
    {
        "access_token": "046d3e7d-f42f-4886-8968-3e445dae65c0",
        "token_type": "bearer",
        "expires_in": 1209599,
        "scope": "read write"
    }
    ```

**Step 2: Device Registration**
- **Endpoint**: `POST https://b.utair.ru/api/v1/devices/`
- **Purpose**: Register the mobile device and associate it with the session.
- **Notable Headers**:
    - `Authorization`: Bearer 046d3e7d-f42f-4886-8968-3e445dae65c0
- **Request Payload**:
    ```json
    {
        "device_id": "c6168e364024f0c4",
        "device_name": "google sdk_gphone64_x86_64",
        "os_type": "android",
        "os_version": "14",
        "app_version": "5.11.0"
    }
    ```
- **Response Body**:
    ```json
    {
        "id": 13914849,
        "device_id": "c6168e364024f0c4",
        "device_name": "google sdk_gphone64_x86_64",
        "os_type": "android",
        "os_version": "14",
        "app_version": "5.11.0",
        "push_token": null
    }
    ```

**Step 3: Profile Initialization**
- **Endpoint**: `POST https://b.utair.ru/api/v1/profile/`
- **Purpose**: Initialize user profile context (GDPR acceptance).
- **Request Payload**:
    ```json
    {
        "gdpr": {
            "accepted": true
        }
    }
    ```
- **Response Body**:
    ```json
    {
        "gdpr": {
            "accepted": true
        }
    }
    ```

**Step 4: SMS OTP Request (Phone Number Submission)**
- **Endpoint**: `POST https://b.utair.ru/api/v1/login/`
- **Purpose**: Submit the phone number to receive an SMS OTP.
- **Request Payload**:
    ```json
    {
        "login_type": "phone",
        "login": "+39 351 739 9395",
        "confirmation_type": "standard"
    }
    ```
<!-- Phone Number: +39 351 739 9395 -->
- **Response Body**:
    ```json
    {
        "attempt_id": "aa4f6163-3a79-487e-95f3-6dafeaa2f185",
        "channel": "phone",
        "confirm_location": "https://b.utair.ru/api/v1/login/confirm/",
        "confirmation_type": "standard"
    }
    ```
- **Analysis**: During initial testing, the first OTP request often fails to deliver a physical SMS. However, after waiting for a 5-minute cooldown period and initiating a second request, a valid SMS OTP is successfully delivered to the device. This behavioral pattern suggests a rate-limiting or anti-spam mechanism that prioritizes delivery on subsequent attempts within the same session context.

**Step 5: OTP Submission**
- **Endpoint**: `POST https://b.utair.ru/api/v1/login/confirm/`
- **Purpose**: Submit the received OTP code for authentication.
- **Request Payload**:
    ```json
    {
        "attempt_id": "aa4f6163-3a79-487e-95f3-6dafeaa2f185",
        "code": "2555"
    }
    ```
<!-- OTP Code: 2555 -->
- **Response Body**:
    ```json
    {
        "code": 40102,
        "message": "Invalid confirm credentials",
        "attempt_id": "aa4f6163-3a79-487e-95f3-6dafeaa2f185"
    }
    ```
- **Analysis**: The 40102 error indicates the server rejected the provided code, likely due to expiration or a mismatch with the `attempt_id`.

## 4. Security & Reversing Notes

### Authentication Mechanism
- **Bearer Token**: Access is controlled via a Bearer token obtained during the initial handshake.
- **Attempt ID**: Each login attempt is tracked using a UUID (`attempt_id`). This ID must be present in the confirmation request to link the code to the specific attempt.
- **Custom Headers**:
    - `timestamph`: A custom header likely used for request integrity or anti-replay.
    - `timestamp`: Standard epoch timestamp.
- **Platform Integrity**: The application identifies itself via `os_type` and `app_version` during device registration.

### Bot Detection & Defense
- **Device Binding**: Registration of `device_id` suggests the server might restrict authentication attempts to registered devices.
- **Session State**: The multi-step flow requires maintaining consistent headers and tokens across all endpoints.

## 5. Conclusion

### Automation Feasibility: 65% (Medium)

### Detailed Conclusion:
The Utair mobile application implements a standard yet structured authentication flow. The use of a stateful `attempt_id` and mandatory device registration adds a layer of complexity for automated interactions, as the sequence of requests must be strictly followed with consistent headers. The primary challenge for automation is the synchronization of the `attempt_id` and the potentially time-sensitive `timestamph` header. 

The observed 40102 error suggests that the server performs rigorous validation on the OTP code and its associated session. To achieve successful automation, one would need to replicate the exact header structure (including the Bearer token) and ensure that the confirmation request is sent within the valid window for the `attempt_id`. Despite these measures, the absence of a visible captcha significantly lowers the barrier for automated SMS requests, provided the session identifiers are correctly managed.
