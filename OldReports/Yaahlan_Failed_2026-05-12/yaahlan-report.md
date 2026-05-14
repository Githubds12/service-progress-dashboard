# Yaahlan - Research Report

## Metadata
- **Target URL/App**: `com.immomo.biz.yaahlan`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-12`
- **Status**: `Unsuccessful (Encrypted Payload)`
- **HAR Files**: `yaahlan.har`

## 1. Executive Summary
Yaahlan (com.immomo.biz.yaahlan) implements a highly secure authentication flow with encrypted payloads and multi-step verification. Research indicates that the application uses an encrypted `mdata` parameter for login, likely managed by the Immomo security framework. Due to the complexity of this encryption and the lack of a decryption mechanism, automated API extraction and interaction are currently not feasible. The service is marked as unsuccessful for the current automation sprint.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS / UpVerify | Supports standard SMS OTP and UpVerify (sending SMS to a number) |
| **Captcha** | undefined | No captcha was observed in the captured flow |
| **Encryption** | Encrypted Payload | `mdata` field in the login request is encrypted |
| **Rate Limits** | Unknown | No rate limiting behavior (HTTP 429) was observed |
| **Endpoints Involved** | 2 | `/mdp-user/login/sendVerifyCode`, `/web/user/login/loginWeb` |
| **Bot Protection** | Internal Risk Management | Uses `mmuid`, `deviceId`, and `riskType` for security |

## 3. Flow Details

### Flow 1: Login via SMS OTP / UpVerify

**Step 1: Send Verify Code**
- **Endpoint**: `POST https://gw-api.yaahlan.fun/yaahlan/mdp-user/login/sendVerifyCode`
- **Purpose**: Initiate OTP verification or UpVerify flow.
- **Request Headers**:
    - `Host`: `gw-api.yaahlan.fun`
    - `Content-Type`: `application/x-www-form-urlencoded`
    - `User-Agent`: `Mozilla/5.0 (Linux; Android 15; Pixel 7 Build/AP3A.240617.008; wv) ...`
- **Request Body**:
    ```text
    areaCode=39&mmuid=fcd1feb4e5fbe62d3ded48eb1e8b136c8698e054&mmuidv3=55d64301426dec7e419b365364873f1661383ca15fcc20c282260df10193f0006f&riskType=0&mobile=3720517038&countryAreaCode=IT&scene=login
    ```
- **Response**:
    ```json
    {
      "ec": 200,
      "em": "success",
      "data": {
        "needUpVerify": 1,
        "upVerifyUrl": "https://www.yaahlan.fun/fep/momo/yaahlan-fe/account-security/sendSMSToVerify.html?_ui=256&_bid=1005534&receiver=+16265873464&content=YH3476&from=login&upVerifyToken=1be6505495264f359113fb651b86f111"
      },
      "timestamp": 1778565050
    }
    ```
- **Analysis**: The server responds with `needUpVerify: 1`, indicating that the user must send an SMS to `+16265873464` with content `YH3476` to verify their identity.

**Step 2: Login Submission**
- **Endpoint**: `POST https://gw-api.yaahlan.fun/yaahlan/web/user/login/loginWeb`
- **Purpose**: Finalize login after verification.
- **Request Body**:
    ```text
    mdata=P%2FVvAkoQoU5jPwYBopSnB1klaHsreFh9XBQsPb0eW4PzpGgK2JFZmfLEHRG71r637aQmBx5FR8pmct%2BV... [Encrypted Blob]
    ```
- **Response**:
    ```text
    k+S6cXiRmGW2gm3xOR1MFDpvtj2LDa+0o4VS/VgBpjfflsjT3Se9VMX+Qx2i2Vk2LMuRLO0vklHDZUSAOIIldsdxhkMhVj6f+TusnlGn8jYpUysRF98Sdht82IdI3ZNrJkFL7Kt6684nU1NHzi0qeXuKay2k9CneGPimk... [Encrypted Response]
    ```
- **Analysis**: Both request and response payloads are encrypted, requiring decryption of the `mdata` parameter to proceed with automation.

## 4. Security & Reversing Notes

### Encryption/Signing Mechanisms
1. **Payload Encryption (mdata)**: The main login request uses a field named `mdata` which contains a large encrypted string. This is common in apps using Momo/Immomo security frameworks.
2. **Device Fingerprinting (mmuid)**: The app sends `mmuid` and `mmuidv3` in every request, which are unique device identifiers used for bot detection and risk management.
3. **UpVerify Flow**: The use of UpVerify (sending SMS instead of receiving) is a strong anti-spam measure as it requires a real SIM card capable of sending messages.

## 5. Conclusion

### Automation Feasibility: Low (35%)

### Critical Blockers:
1. **Encrypted Payloads**: The `mdata` parameter is encrypted and its generation logic is likely inside obfuscated native libraries (e.g., `libmmsecurity.so`).
2. **UpVerify Requirements**: Automated testing is difficult as it requires the ability to send specific SMS messages from the registered phone number.
3. **Device Fingerprinting**: High dependency on consistent `mmuid` and `deviceId` values.

### Detailed Conclusion:
Yaahlan implements a sophisticated security model that combines device-bound identifiers with encrypted communication. The "UpVerify" mechanism significantly raises the bar for automated account creation and mass-login attempts. While the basic API flow is straightforward (request → verify → login), the cryptographic challenges and the need for outgoing SMS verification make it a highly secure target. Automation is currently only feasible if the encryption keys and signing logic are extracted from the application's binary.
