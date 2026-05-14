# Daraz - Research Report

## Metadata
- **Target URL/App**: `com.daraz.android` (Daraz Bangladesh / Lazada framework)
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-28`
- **Status**: `Completed`
- **HAR Files**: `Daraz.har`

## 1. Executive Summary
Daraz heavily utilizes the Alibaba/Lazada `mtop` (Mobile Taobao Open Platform) framework. The authentication mechanism is protected by sophisticated Alibaba anti-bot technologies, requiring custom signed headers (`x-sign`, `x-sgext`, `x-mini-wua`) and an encrypted Web User Agent (`wua`) token inside the request body. Both the SMS OTP request and verification endpoints enforce these checks, preventing straightforward API automation without reverse engineering the Alibaba security SDK.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | OTP sent via SMS (`deliveryType="sms"`) |
| **Captcha** | Invisible | `wua` and `x-mini-wua` act as invisible device behavior tracking |
| **Encryption** | Yes | `x-sign` for request integrity; `epss` and `wua` are encrypted payloads |
| **Rate Limits** | Unknown | Enforced at the `mtop` gateway layer |
| **Endpoints Involved** | 2 | `sendverificationsms`, `loginbyotp` |
| **Bot Protection** | High | Alibaba/mtop SDK Device Fingerprinting & Request Signing |

## 3. Flow Details

### Flow 1: Signup / Login (OTP)

**Step 1: Send Verification SMS**
- **Endpoint**: `POST https://acs-m.daraz.com.bd/gw/mtop.lazada.member.user.biz.sendverificationsms/1.0/`
- **Purpose**: Initialize session and send the OTP to the user's phone.
- **Notable Headers**:
    - `x-sign`: Cryptographic signature of the request payload and headers.
    - `x-mini-wua`: Web User Agent environment payload.
    - `x-sgext`: Extension data for security.
    - `epss`: Encrypted payload specific to anti-bot checks.
    - `x-umt`, `x-utdid`, `x-apdid-token`: Alibaba device tracking identifiers.
- **Request Payload**:
    ```text
    wua=wMQW_UPYTcaJ5ab4Zw...&data={"bizScene":"MyAccountTab","checkRisk":"true","deliveryType":"sms","enablePhoneRegisterConvertLogin":"false","lzdAppVersion":"1.6","pageSource":"welcome_page","phone":"1331745359","phonePrefixCode":"880","platform":"android","resend":"false","sendCodeTemplate":"default","type":"OTP_LOGIN"}
    ```
- **Response**:
    ```json
    {
        "api": "mtop.lazada.member.user.biz.sendverificationsms",
        "data": {
            "codeLength": "6",
            "deliveryType": "SMS",
            "messageId": "*******359|1777399474128"
        },
        "ret": ["SUCCESS::调用成功"],
        "v": "1.0"
    }
    ```

**Step 2: Verify OTP**
- **Endpoint**: `POST https://acs-m.daraz.com.bd/gw/mtop.lazada.member.user.loginbyotp/1.0/`
- **Purpose**: Submit the OTP to complete login/registration.
- **Request Payload**:
    ```text
    wua=wMQW_TxfOVTNxhkB...&data={"autoFillSuccess":false,"bizScene":"MyAccountTab","code":"111111","deliveryType":"sms","lzdAppVersion":"1.6","pageSource":"welcome_page","phone":"1331745359","phonePrefixCode":"880","platform":"android","supportAutoFill":true,"type":"OTP_LOGIN"}
    ```
- **Response**:
    ```json
    {
        "api": "mtop.lazada.member.user.loginbyotp",
        "data": {},
        "ret": ["LZD_MEMBER_USER_1019::Invalid verification code."],
        "v": "1.0"
    }
    ```

## 4. Security & Reversing Notes

### Encryption/Signing Mechanisms

**1. Request Signing (`x-sign`)**
- **Algorithm**: Standard Alibaba `mtop` signing (often HMAC-SHA256 based on app key, timestamp, and payload).
- **Analysis**: If `x-sign` is mismatched, the gateway immediately drops the request. The signing secret is typically hidden inside the Alibaba security library (`libsgmain.so`).

**2. Device Fingerprinting (`wua` / `x-mini-wua`)**
- **Format**: Large URL-encoded Base64 string.
- **Analysis**: These tokens capture environmental parameters, device ID, emulator artifacts, and sensor data. The token rotates or expires, making replay attacks unfeasible.

**3. Session & Device Tracking**
- **Headers**: `x-utdid` (Universal Token Device ID), `x-apdid-token`, `x-umidtoken`. These persist across sessions to build a trust profile of the device.

## 5. Conclusion

### Automation Feasibility: 10%

### Critical Blockers:
1. **Alibaba mtop Framework**: Reversing the `x-sign` and `wua` generation requires deep hooking into `libsgmain.so` (unidbg or Frida). 
2. **Strict Gateway**: Without the proper headers, requests do not even reach the business logic layer. Simple Python API scripts are completely blocked.
