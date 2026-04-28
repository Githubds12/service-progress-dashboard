# Poppo Live - Research Report

## Metadata
- **Target URL/App**: `com.baitu.qingshu` (Poppo Live)
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29`
- **Status**: `Completed`
- **HAR Files**: `Poppo.har`

## 1. Executive Summary
Poppo Live implements a multi-layered security stack to prevent automated registration and abuse. The system integrates **Alibaba (Aliyun) Captcha** for interaction verification and **Fengkong Cloud (ShuMei)** for advanced device fingerprinting and risk assessment. The registration flow requires a successful Aliyun captcha verification (`SceneId: 8gwq6bozc`) to obtain a `captchaVerifyParam`, which is then passed to the SMS trigger endpoint (`/public/phone-code`). Automation is highly complex due to the encrypted Aliyun telemetry and device fingerprinting requirements.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | OTP code received via Aliyun-secured trigger |
| **Captcha** | Aliyun Captcha | Mandatory interactive challenge |
| **Encryption** | Advanced | Encrypted device profiles via ShuMei SDK |
| **Rate Limits** | Strict | Managed via Aliyun CloudAuth |
| **Endpoints Involved** | 3 | `/public/captcha-check`, `/public/phone-code`, `/user/login` |
| **Bot Protection** | High | Aliyun + ShuMei (Fengkong Cloud) |

## 3. Flow Details

### Flow 1: Registration / Login

**Step 1: Captcha Verification**
- **Endpoint**: `GET https://api.vshowapi.com/public/captcha-check`
- **Purpose**: Verify user interaction and obtain a verification token.
- **Request Parameters (Legitimate)**:
    ```text
    uuid: 217daab874cc196f
    captchaVerifyParam: {"sceneId":"8gwq6bozc","certifyId":"TpqLup02FX","deviceToken":"U0dfV0VCIzM3OTVkMjgyNDJhMTE2MTliYzI1Zjc4NmY4NGU1M2Q0...","data":"JRMnTw8IDQE3LA4LVVdNMHn1ZVtBfTEwbzkCNFWrIAEoWkObAKcYHBVXMZJxNQ0Rw750cm1HJxi7jNwFiPUSBZRG7x0AUE1pNUofXS9RSKY1ej0OKC9ab9BZYH0PYiI8fRxfMdxeBP5PYX0Pe5xF2h6JZGYYwdwJIUK1BXk5h6BwZwIPBzZQYk1kf2pwRVc%2F1lEgHwxsHz8xNwRLCT97C3B4l%2BVUkTkW1o0aBR4TLcBkl3lMdMK2JhpzugIibbYEOhYcGmR2JFB2QzcNO2Z6ImIUIMFrdX42USVLYBkcUhpaW2ZgsNQhkHJxyAR8Y1CeLA1pZWIXG2goGC5uPmxhXjQdKnRRbRkqbX1NbWEjEkQNRXRfRb8YXwthNgJPPhMAGp464FgbUQX69ir14OolRD%2Fo8971LoXX8GEz4b2GaXZrLnn2LiORaHpnW08VLl8LK3FLNPopeOh7Z3ZoK%2B9KdbZUWRJnDhEsPPRKSSwgXrYOTClmLfIBJDfotd6iJYaBBHglG81qegMJFzEGZjUpIXQ%2FN0NdYSgSCO4oQWodQ7FKcCXHWEcBtuc9dWrdfQsegJE9Rohb%2FiJFN4%2BFWrR30Xpyc0UtlTEDAzonE7xaaTF4GGNkaZ8QKislPnYwKHRJc2IpDSBKfkxBebFzHkgOXlcjK68wVjgMe5L6VClnRtxZZSwHEJ1%2FahcCWJodXBzraD4hGUs%2FGgskLlJLcDw0Rw82yiYuRg83F38FcEZF9vzkbEHwVjFeWfn77byzJuvVIlgybCc7VE5cWGogFkFmpz54Jx0RYQDyMSBhIyYop%2BzyQgCqJU5PPQMMW2gVVUIvFXeSQUInfVmNh0mkBJ8E1SqYny0Hd2RvHChwfxVuFhV%2BeExzIV8eV2wuAHucTMNNKRvpBqJroFgXTCIB%2BUJiSysy3A8tNx%2BeLUsQHII29VANMdNBHSR0gHkWaDt4DGA1ejUCUXgvdHIGLq0veCMaTHFpCDhPoA9IOU4hN3tqr5p%2FcWLOGmaRc09w2lw6IUSUUkRFZzAsOiU8bUjrcQ0HIsFpduJtZKBvoiozXS2LIUgRMXIzFQRSzUZvgSSniqghMop7MjcU1QSsfx0uEwsUJxZQaVpEXRx8r2WpklcE0HYXG002Mkp4EEkVd3l2ASBaeRV9d6hh9BRiW7htTm1L0kdLcCLhOkslK1RYT2%2Fosn5UAXVWDzo%2FMBkARV4oAjZARmRAJicXKjhLUxbhGndsexNfqzcOTyI3hz9JTSwfgY9IhVCCBJPe4Vp0TB9kE%2FA4UX5WDAl%2BEUsaQDZeZGkSHy%2F3KnRRQDtqGxsyRmAoYnF2Vm2bYj575UY1xF09bgNK%2FefJwS7imHY1jAUIcZBWu2WpuimSEEZkPjM3YAwOeDQ%2BdR4Zfb8d0wReRxlZr3cNAE4VGmkZRGsierIL6WkEZyO5CjT4dkcaqbNhe4OjKHYrIykMWi8R1wkoJcGcSihuRxEqEwEldWgVHGMPBk0mbVAXc0otaaMXFRsOXXpeFXZnRG6qI28aUVgXdaFw2uAeLLJtWkRCatpiDBEfSQs4c0N5IpU3D"}
    ```
- **Response**:
    ```json
    {
      "code": 200,
      "message": "success",
      "data": {
        "status": 1,
        "backend_token": "TpqLup02FX_8gwq6bozc_..."
      }
    }
    ```

**Step 2: Request SMS Code**
- **Endpoint**: `GET https://api.vshowapi.com/public/phone-code?type=register&phone=393518579897&use=sms&email=&has_whatsapp=0&captcha=&c_key=&p=android&smei_id=Bg%2FvQ%2B1gGBXo4nNymLDKhQ0gG1tkUOUSHxy8ZBnO0GeXTX5PQBIH1VCYrNqTU6LvaMOqbRoGoysxLE36gp3yxjQ%3D%3D&device_name=google%20Pixel%207&c=poppo&v=534&sl=en&l=en&mcc=0&vs=5.4.534.0424&uuid=217daab874cc196f`
- **Response Body**:
    ```json
    {
      "code": 200,
      "message": "success",
      "data": []
    }
    ```

**Step 3: Submit SMS OTP (Login/Register)**
- **Endpoint**: `POST https://api.vshowapi.com/user/login?type=phone&userid=0&login_type=&phone=%2B39%20351%20857%209897&ext_token=333333&password=Facebook%40ds12%2C&inland=0&p=android&smei_id=Bg%2FvQ%2B1gGBXo4nNymLDKhQ0gG1tkUOUSHxy8ZBnO0GeXTX5PQBIH1VCYrNqTU6LvaMOqbRoGoysxLE36gp3yxjQ%3D%3D&device_name=google%20Pixel%207&c=poppo&v=534&sl=en&l=en&mcc=0&vs=5.4.534.0424&uuid=217daab874cc196f`
- **Request Body**:
    ```text
    type=phone&userid=0&login_type=&phone=%2B39%20351%20857%209897&ext_token=333333&password=Facebook%40ds12%2C&inland=0&install_data=%7B%22af_status%22%3A%22Organic%22%2C%22af_message%22%3A%22organic%20install%22%2C%22is_first_launch%22%3Atrue%7D&p=android&smei_id=Bg%2FvQ%2B1gGBXo4nNymLDKhQ0gG1tkUOUSHxy8ZBnO0GeXTX5PQBIH1VCYrNqTU6LvaMOqbRoGoysxLE36gp3yxjQ%3D%3D&device_name=google%20Pixel%207&c=poppo&v=534&sl=en&l=en&mcc=0&vs=5.4.534.0424&uuid=217daab874cc196f
    ```
- **Response Body (Error Case)**:
    ```json
    {
      "code": 401,
      "message": "Verification code error",
      "data": []
    }
    ```

## 4. Security & Reversing Notes

### Device Fingerprinting (ShuMei)
- The app uses ShuMei (Fengkong Cloud) SDK to collect deep device telemetry.
- Encrypted profiles are sent to `fp-sa-it-acc.fengkongcloud.com`.
- Failure to provide valid ShuMei tokens may result in captcha loops or silent blocking.

### Aliyun CloudAuth
- The Aliyun SDK handles the captcha and CloudAuth flow.
- Requests to `aliyuncs.com` include HMAC-SHA1 signatures and encrypted payloads.

## 5. Conclusion

### Automation Feasibility: 5%

### Critical Blockers:
1. **Aliyun Captcha**: Requires a valid `deviceToken` and encrypted interaction data.
2. **ShuMei Fingerprinting**: Extremely robust device identity tracking.
3. **Encrypted Parameters**: Multiple parameters are encrypted or signed via native SDKs.
