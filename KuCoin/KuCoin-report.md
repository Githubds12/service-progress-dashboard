# KuCoin (com.kubi.kucoin) - Research Report

## Metadata
- **Target URL/App**: `com.kubi.kucoin`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-27`
- **Status**: `Completed`
- **HAR Files**: `KuCoin.har (Flow: Account Check -> Captcha -> OTP Send -> OTP Verify -> Register)`

## 1. Executive Summary
KuCoin implements a sophisticated, multi-layered security architecture for user onboarding. The process is gated by **GeeTest v4** bot protection, which is triggered upon the initial OTP request attempt. Behind the scenes, KuCoin leverages **Forter** for behavioral fraud analysis and employs strict device fingerprinting via custom headers (`X-DEVICE-NO`, `token_sm`). The registration flow is highly structured, requiring sequential validation of the account state, bot verification, and SMS OTP confirmation before final account creation.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS OTP | 6-digit numeric code sent via SMS |
| **Captcha** | GeeTest v4 Slide | GeeTest v4 (triggered on second validation-code request) |
| **Encryption** | SSL/TLS | Standard HTTPS with Forter-backed risk assessment |
| **Rate Limits** | Medium | Limit of 20 OTP requests per session/number observed |
| **Endpoints Involved** | 6 | check-user-account, captcha-validation, validation-code, verify-validation-code, sign-up |
| **Bot Protection** | GeeTest v4, Forter | Integrated bot and fraud prevention stack |

## 3. Flow Details

### Flow 1: New User Registration
The primary flow involves identity verification and account setup.

**Step 1: Check Account Status**
- **Endpoint**: `POST https://appapi-v2.xcoinsystem.com/app/v1/auth/check-user-account`
- **Description**: Verifies if the phone number is already in use.
- **Request**:
```text
Headers: {
  "X-APP-VERSION": "4.24.0",
  "X-APP_ID": "com.kubi.kucoin",
  "token_sm": "BtibO20dIgoWjn3eP0NJZu980PIFmr6TVnEFZdIgIlq3w+B+Jdy+kutOGCN/lRjK..."
}
Body: account=91-8791267460
```
- **Response**:
```json
{
  "success": true,
  "code": "200",
  "msg": "success",
  "retry": false,
  "data": false
}
```

**Step 2: Trigger Captcha**
- **Endpoint**: `POST https://appapi-v2.xcoinsystem.com/app/v1/auth/validation-code`
- **Description**: Initial request to send OTP. Returns a 40011 error indicating that a Captcha is required.
- **Request**:
```json
{
  "channel": "SMS",
  "loginToken": "",
  "receiver": "+91-8791267460",
  "validationBiz": "REGISTER"
}
```
- **Response**:
```json
{
  "success": false,
  "code": "40011",
  "msg": "reCAPTCHA or GeeTest required.",
  "retry": false,
  "data": null
}
```

**Step 3: Solve Captcha**
- **Endpoint**: `POST https://appapi-v2.xcoinsystem.com/app/v1/auth/captcha-validation`
- **Description**: Submits the GeeTest v4 response token.
- **Request**:
```text
Body: bizType=PHONE_REGISTER&captchaType=GEETEST&response=%7B%22captcha_id%22%3A%22d8a78f9ef7db4fcf864cfd257a728e39%22%2C%22lot_number%22%3A%22c3efb8648d8148a1bc9bb0c41f37b109%22%2C%22pass_token%22%3A%22ee005690c9c85d1afd7d2efc81a2654e5e7daf1442723cc1f2011928685d8660%22%2C%22gen_time%22%3A%221777288711%22%2C%22captcha_output%22%3A%228JNNelbm2j8YqQkdSJB_rFDNDPmdJqBc5AERug4...%22%7D&secret=d8a78f9ef7db4fcf864cfd257a728e39
```
- **Response**:
```json
{
  "success": true,
  "code": "200",
  "msg": "success",
  "retry": false,
  "data": null
}
```

**Step 4: Request SMS OTP**
- **Endpoint**: `POST https://appapi-v2.xcoinsystem.com/app/v1/auth/validation-code`
- **Description**: Re-submits the OTP request after successful Captcha validation.
- **Request**:
```json
{
  "channel": "SMS",
  "loginToken": "",
  "receiver": "+91-8791267460",
  "validationBiz": "REGISTER"
}
```
- **Response**:
```json
{
  "success": true,
  "code": "200",
  "msg": "success",
  "data": {
    "retryAfterSeconds": 59,
    "retryTimes": 3
  }
}
```

**Step 5: Verify OTP**
- **Endpoint**: `POST https://appapi-v2.xcoinsystem.com/app/v1/auth/verify-validation-code`
- **Description**: Validates the 6-digit SMS code.
- **Request**:
```json
{
  "bizType": "REGISTER",
  "receiver": "+91-8791267460",
  "seq": 1,
  "validations": {
    "SMS": "449935"
  }
}
```
- **Response**:
```json
{
  "success": true,
  "code": "200",
  "msg": "success",
  "retry": false,
  "data": null
}
```

**Step 6: Account Sign-Up**
- **Endpoint**: `POST https://appapi-v2.xcoinsystem.com/app/v1/auth/sign-up`
- **Description**: Final step to create the account with password and metadata.
- **Request**:
```text
Body: password=910c7b07a7e92470fa5cd730cc21da62&userName=%2B91-8791267460&userAccountType=PHONE&utm_source=GOOGLE&anonymousId=410e33d01629a331&...
```
- **Response**:
```json
{
  "success": true,
  "code": "200",
  "msg": "success",
  "data": {
    "id": "69ef462616150500016afeb6",
    "uid": 255882134,
    "phone": "8791267460"
  }
}
```

## 4. Security & Reversing Notes
- **GeeTest v4**: The implementation requires a valid `lot_number` and `pass_token` from the GeeTest server. This effectively blocks simple headless automation.
- **Forter Behavioral Analysis**: KuCoin monitors user interactions via `m.api.forter.com`. Automated scripts must mimic human-like timing and header consistency to avoid being flagged.
- **Device Fingerprinting**: The `X-DEVICE-NO` and `token_sm` headers are used to bind the session to a specific device instance.
- **API Domain**: KuCoin uses a dedicated API gateway (`appapi-v2.xcoinsystem.com`) which differs from the main web domain.

## 5. Conclusion

### Automation Feasibility: 35%

### Critical Blockers:
1. **GeeTest v4 Bot Protection**: Mandatory for the OTP request. Requires a complex token generation process.
2. **Device Signature (`token_sm`)**: Requires reversing of the device profile generation logic.
3. **Behavioral Tracking**: Forter integration increases the risk of account flagging during automated signup attempts.

### Recommendations:
Automation efforts should focus on using high-quality proxies and mobile-integrated automation frameworks (e.g., Appium) that can interact with the GeeTest challenge in a real-device environment.
