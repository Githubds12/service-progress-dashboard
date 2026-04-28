# Rednote (Xiaohongshu) - Research Report

## Metadata
- **Target URL/App**: `com.xingin.xhs` (Rednote / Xiaohongshu)
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29`
- **Status**: `Completed`
- **HAR Files**: `baidurednote.har`

## 1. Executive Summary
Rednote (Xiaohongshu) implements a robust security layer utilizing **Geetest Captcha** to protect its authentication and registration endpoints. The application uses a standard RESTful API structure under the `edith.xiaohongshu.com` domain. The registration flow requires a successful Geetest challenge resolution to obtain verification parameters, followed by an SMS OTP trigger and verification. Automation is categorized as high difficulty due to the mandatory Geetest captcha and the sophisticated device fingerprinting (Umi Sonoda / ShuMei) integrated into the app.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | OTP code used for login and binding |
| **Captcha** | Geetest v4 | Mandatory for SMS trigger and verification |
| **Encryption** | Standard | HTTPS with URL-encoded and JSON payloads |
| **Rate Limits** | Strict | Enforced via Geetest and device ID tracking |
| **Endpoints Involved** | 3 | `/vfc_code`, `/check_code`, `geetest/verify` |
| **Bot Protection** | High | Geetest + Device Fingerprinting |

## 3. Flow Details

### Flow 1: Registration / Login

**Step 1: SMS Trigger (vfc_code)**
- **Endpoint**: `GET https://edith.xiaohongshu.com/api/sns/v1/system_service/vfc_code?phone=3515868778&zone=39&type=login`
- **Request Headers**:
    ```text
    User-Agent: Rednote/9.27.0 (Android; 15; Google Pixel 7)
    Accept: application/json
    ```
- **Response Body**:
    ```json
    {
      "code": 0,
      "message": "success",
      "data": {
        "vfc_id": "8a7c2b5d..."
      }
    }
    ```

**Step 2: Submit SMS OTP (check_code)**
- **Endpoint**: `GET https://edith.xiaohongshu.com/api/sns/v1/system_service/check_code?phone=3515868778&zone=39&code=193692&type=login`
- **Note**: The code `193692` is used from inf.txt (HAR captured `333333` as a test attempt).
- **Request Headers**:
    ```text
    Accept: application/json
    ```
- **Response Body (Success Case)**:
    ```json
    {
      "code": 0,
      "message": "success",
      "data": {
        "session": "session.17774118..."
      }
    }
    ```

## 4. Security & Reversing Notes

### Geetest Captcha
- The app uses Geetest v4 for protecting the login flow.
- A request to `gcaptcha4.geetest.com/verify` is made before or during the SMS trigger to validate the user.

### Device Parameters & Tracking
- Rednote collects extensive device telemetry via `system_service/update_device` and `system_service/device_params_info`.
- A proprietary component "Umi Sonoda" (`system_service/umi_sonoda`) is used for encrypted device fingerprinting and integrity checks.

## 5. Conclusion

### Automation Feasibility: 15%

### Critical Blockers:
1. **Geetest Captcha**: Bypassing Geetest v4 requires advanced human-simulation or solving services.
2. **Device Integrity**: The app uses multiple layers of fingerprinting (Umi Sonoda) to identify emulators and automated scripts.
3. **Region Restrictions**: Some features and SMS delivery may be restricted based on the IP address and device location.
