
# Shopee.ph - Research Report

## Metadata
- **Target URL/App**: `shopee.ph`
- **Researcher**: `Security Research Team`
- **Date**: `2025-12-25`
- **Status**: `Completed`
- **HAR Files**: `1.har - 7.har (3 flows: Signup, Forgot Password, Login)`

## 1. Executive Summary
Shopee.ph implements a robust multi-layered security system with advanced anti-automation measures. The platform uses sophisticated device fingerprinting (Shumei/数美), custom header signing (x-sap-sec), encrypted payloads, and slider captcha verification. All three flows (signup, forgot password, login) follow similar OTP-based verification patterns with SMS as the primary channel. Automation feasibility is low due to complex cryptographic challenges and real-time device fingerprinting requirements.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS / WhatsApp / Call | SMS primary (channel 1), WhatsApp (channel 6), Voice call (channel 2) |
| **Captcha** | Yes | Slider captcha with encrypted security_data payload |
| **Encryption** | Yes | Multiple layers: x-sap-sec header signing, device fingerprinting (shopee_webUnique_ccd), encrypted captcha responses |
| **Rate Limits** | High | 60s cooldown between OTP requests, session-based tracking |
| **Endpoints Involved** | 7 | get_settings_v2, captcha/verify_v2, send_vcode, verify_vcode, register, login_by_password |

## 3. Flow Details

### Flow 1: Signup (Registration)

**Step 1: Get OTP Settings**
- **Endpoint**: `POST /api/v4/otp/get_settings_v2`
- **Purpose**: Initialize OTP session and retrieve available verification channels
- **Notable Headers**:
    - `x-csrftoken`: CSRF protection token
    - `af-ac-enc-sz-token`: Device fingerprint token (Shumei SDK)
    - `x-sap-ri`: Request identifier for anti-fraud
    - `x-sap-sec`: Signed request header (large encrypted payload ~6KB)
    - `x-sz-sdk-version`: 1.12.26-5 (Shumei SDK version)
- **Request Payload**:
    ```json
    {
        "operation": 8,
        "encrypted_phone": "",
        "phone": "639311834075",
        "supported_channels": [1, 2, 3, 6, 0, 5],
        "support_session": true,
        "client_identifier": {
            "security_device_fingerprint": "Ec+OSVXflJNC/zAIZRPbUA==|qQhaWUWqd6h8VJqo9RwPlbMOUUM/GlLatiERQ9pgTRfEpSvdRSEUoyYDLcKs1FAoi8iypkG17TQB4w==|8jcAYcgfpqQzJngT|08|3"
        }
    }
    ```
- **Response**:
    ```json
    {
        "error": 0,
        "data": {
            "need_login": false,
            "need_captcha": true,
            "captcha_scene": "signup",
            "preferred_channel": 6,
            "available_channels": [6, 2, 1],
            "session_info": {
                "seed": "2fd1ab6f-4938-468a-a88e-4cf7ab1f4f96",
                "remaining_resend_cooldown_sec": 0
            },
            "captcha_app_key": "User.PC"
        }
    }
    ```

**Step 2: Verify Captcha**
- **Endpoint**: `POST /api/v4/anti_fraud/captcha/verify_v2`
- **Purpose**: Solve slider captcha and get verification token
- **Request Payload**:
    ```json
    {
        "security_data": "ByQBAAAAAQAAAIAAAAmUgqoIbQAAKK0KAAAAlQAAAAAAAAkAVTJGc2RHVmtYMS9n... [6KB encrypted blob]"
    }
    ```
- **Response**:
    ```json
    {
        "security_data": "U2FsdGVkX19uK+rVt5WS67CtnTm7W1OmN1iLzn1x4WEAMn05hzOhssnm... [encrypted response]"
    }
    ```
- **Analysis**: Captcha uses encrypted challenge-response with AES encryption (SaltedX prefix indicates OpenSSL format)

**Step 3: Send OTP**
- **Endpoint**: `POST /api/v4/otp/send_vcode`
- **Request Payload**:
    ```json
    {
        "phone": "639311834075",
        "force_channel": true,
        "m_token": "",
        "captcha_signature": "f8e633bc61d97e5b982ac0c9df2a684e1fcaf62f... [512 bytes hex signature]",
        "operation": 8,
        "channel": 1,
        "supported_channels": [1, 2, 3, 6, 0, 5],
        "support_session": true,
        "client_identifier": {
            "security_device_fingerprint": "Ec+OSVXflJNC/zAIZRPbUA==|..."
        }
    }
    ```
- **Response**:
    ```json
    {
        "error": 0,
        "data": {
            "delivery_channel": 1,
            "session_info": {
                "seed": "2fd1ab6f-4938-468a-a88e-4cf7ab1f4f96",
                "remaining_resend_cooldown_sec": 60,
                "remaining_switch_cooldown_sec": 60
            }
        }
    }
    ```

**Step 4: Verify OTP**
- **Endpoint**: `POST /api/v4/otp/verify_vcode`
- **Request Payload**:
    ```json
    {
        "vcode": "381859",
        "support_session": true,
        "operation": 8,
        "phone": "639311834075",
        "client_identifier": {
            "security_device_fingerprint": "Ec+OSVXflJNC/zAIZRPbUA==|..."
        }
    }
    ```
- **Response**:
    ```json
    {
        "error": 0,
        "data": {
            "vcode_token": "EBjCqxvxd+ugtzqDWPhpDk5OmLo6c3V75J4LTZO4B/4v3b2ClY/W7IO9eBb9HrVw..."
        }
    }
    ```
- **Analysis**: Returns vcode_token used for final registration, sets SPC_P_V cookie

**Step 5: Complete Registration**
- **Endpoint**: `POST /api/v4/account/register`
- **Request Payload**:
    ```json
    {
        "phone": "639311834075",
        "password": "9c4229cd7ed05ae115d7fd75bd0a8ff347fa81017998e08dad2cbb46f6f02ef2",
        "vcode_token": "EBjCqxvxd+ugtzqDWPhpDk5OmLo6c3V75J4LTZO4B/4v...",
        "client_identifier": {
            "security_device_fingerprint": "Ec+OSVXflJNC/zAIZRPbUA==|..."
        }
    }
    ```
- **Response**:
    ```json
    {
        "error": 0,
        "data": {
            "nonce": "EOyP1K4P_To9fBc8BJ94c8Q4gbcL1A5iX1MRedkxJzjyL0stW1lK8mFZDT3L3vjK...",
            "userid": 7946462471
        }
    }
    ```
- **Analysis**: Password is SHA256 hashed, sets authentication cookies (SPC_EC, SPC_ST)

### Flow 2: Forgot Password (Password Reset)

**Step 1-4: Same as Signup**
- Uses `operation: 14` instead of `operation: 8`
- Same endpoints: get_settings_v2 → captcha/verify_v2 → send_vcode → verify_vcode
- Returns vcode_token for password reset authorization

**Step 5: Reset Password**
- **Endpoint**: `POST /api/v4/account/reset_password` (inferred)
- **Analysis**: Uses vcode_token from Step 4 to authorize password change

### Flow 3: Login

**Step 1: Login by Password**
- **Endpoint**: `POST /api/v4/account/login_by_password`
- **Purpose**: Direct login with phone and password
- **Request Payload**:
    ```json
    {
        "phone": "639311834075",
        "password": "9c4229cd7ed05ae115d7fd75bd0a8ff347fa81017998e08dad2cbb46f6f02ef2",
        "support_ivs": true,
        "client_identifier": {
            "security_device_fingerprint": "y3pUjD+hvBNehxGiARyCng==|..."
        }
    }
    ```
- **Response**:
    ```json
    {
        "error": 0,
        "data": {
            "userid": 7946462471,
            "ivs_flow_no": null,
            "ivs_token": null
        }
    }
    ```
- **Analysis**: Sets session cookies (SPC_EC, SPC_ST, SPC_SI), no OTP required for normal login

## 4. Security & Reversing Notes

### Encryption/Signing Mechanisms

**1. Device Fingerprinting (Shumei/数美 SDK)**
- **Header**: `af-ac-enc-sz-token` and `shopee_webUnique_ccd` cookie
- **Format**: `base64_part1==|base64_part2==|base64_part3|digits|digit`
- **Example**: `Ec+OSVXflJNC/zAIZRPbUA==|qQhaWUWqd6h8VJqo9RwPlbMOUUM/GlLatiERQ9pgTRfEpSvdRSEUoyYDLcKs1FAoi8iypkG17TQB4w==|8jcAYcgfpqQzJngT|08|3`
- **Analysis**: Generated by Shumei anti-fraud SDK (x-sz-sdk-version: 1.12.26-5), collects browser fingerprint, canvas, WebGL, audio context, fonts, plugins, timezone, screen resolution, etc.

**2. Request Signing (x-sap-sec)**
- **Size**: ~6-8KB base64 encoded signature
- **Purpose**: Signs entire request (headers + body + timestamp)
- **Algorithm**: Likely HMAC-SHA256 or RSA signature with server-provided keys
- **Rotation**: Changes per request, tied to session and device fingerprint
- **Reversing Difficulty**: Very high - requires extracting signing logic from obfuscated JavaScript

**3. Captcha Encryption**
- **Request**: `security_data` field contains encrypted slider captcha solution
- **Response**: Encrypted `security_data` with validation result
- **Format**: AES-256-CBC with "Salted__" prefix (OpenSSL EVP_BytesToKey format)
- **Analysis**: Slider position, timing data, mouse trajectory encrypted before submission

**4. Password Hashing**
- **Algorithm**: SHA-256
- **Format**: Lowercase hex string (64 characters)
- **Example**: `9c4229cd7ed05ae115d7fd75bd0a8ff347fa81017998e08dad2cbb46f6f02ef2`

**5. Session Management**
- **Cookies**: 
  - `SPC_EC`: Encrypted credentials (HttpOnly, Secure)
  - `SPC_ST`: Session token (HttpOnly, Secure)
  - `SPC_SI`: Session ID
  - `SPC_T_ID` / `SPC_T_IV`: Tracking ID with IV for encryption
  - `SPC_CLIENTID`: Client identifier
  - `csrftoken`: CSRF protection

### Captcha Integration
- **Type**: Slider captcha (drag to complete puzzle)
- **Provider**: Custom implementation with Shumei integration
- **Token Flow**: captcha_signature (512 bytes hex) required for send_vcode
- **Validation**: Server-side validation of slider position, timing, and mouse behavior
- **Bypass Difficulty**: Very high - requires solving visual puzzle + mimicking human behavior

### Bot Detection
- **SDK**: Shumei (数美科技) anti-fraud SDK v1.12.26-5
- **Headers Monitored**:
  - `af-ac-enc-dat`: Encrypted action data
  - `x-sap-ri`: Request identifier
  - `x-sap-sec`: Request signature
- **Behavioral Analysis**: Mouse movements, timing patterns, keyboard events
- **Device Consistency**: Fingerprint must remain consistent across requests
- **TLS Fingerprinting**: Likely monitors TLS/SSL handshake patterns

### Key Security Features
1. **Multi-layer encryption**: Device fingerprint + request signing + captcha encryption
2. **Session binding**: All requests tied to session seed and device fingerprint
3. **Rate limiting**: 60s cooldown enforced server-side with session tracking
4. **CSRF protection**: Token validation on all state-changing requests
5. **Replay protection**: Signatures include timestamp, single-use tokens
6. **Channel verification**: Multiple OTP delivery methods with fallback

## 5. Conclusion

### Automation Feasibility: 15%

### Critical Blockers:
1. **Shumei SDK Integration**: Device fingerprinting requires executing proprietary JavaScript SDK that performs extensive browser environment checks
2. **x-sap-sec Signature**: Request signing algorithm not publicly documented, requires reverse engineering obfuscated code
3. **Slider Captcha**: Visual puzzle solving with behavioral analysis (timing, trajectory)
4. **Session Consistency**: All security tokens must remain consistent across multi-step flow
5. **TLS Fingerprinting**: Server likely validates client TLS fingerprint matches expected browser

Zoomed item to 125 per cent.