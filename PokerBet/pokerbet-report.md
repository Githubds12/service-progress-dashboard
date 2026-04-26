# PokerBet - Research Report

## Metadata
- **Target URL/App**: `com.pokerbet.casino`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-26`
- **Status**: `Completed`
- **HAR Files**: `PokerBet.har`

## 1. Executive Summary
PokerBet (tornbee.com) implements a multi-step authentication and registration flow utilizing SMS verification. The platform is heavily protected by **DataDome** and **Cloudflare Turnstile**, which serve as the primary anti-automation barriers. The API communication itself is relatively simple, using plaintext JSON payloads, but it requires careful session management through `_xsrf` tokens provided in response bodies. Automation feasibility is low to medium due to the high-security bot protection layers.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for OTP |
| **Captcha** | Cloudflare Turnstile & DataDome | Both protection layers were observed in the traffic |
| **Encryption** | None | Payloads are transmitted in plaintext JSON |
| **Rate Limits** | Unknown | No rate limiting behavior was explicitly observed during testing |
| **Endpoints Involved** | 2 | `/api/v2/reg_forms/.../set_phone/`, `/api/v2/reg_forms/.../registration/` |
| **Bot Protection** | DataDome & Cloudflare | Advanced bot detection and challenge pages |

## 3. Flow Details

### Flow 1: Registration

**Step 1: Request OTP (Set Phone)**
- **Endpoint**: `POST https://tornbee.com/api/v2/reg_forms/6329ae824a8a282e41d22024/set_phone/`
- **Purpose**: Initialize registration flow and request an SMS OTP
- **Notable Headers**:
    - `User-Agent`: `okhttp/4.11.0`
    - `Content-Type`: `application/json`
- **Request Payload**:
    ```json
    {
      "phone": "+380635550123",
      "promo_code": "",
      "metadata": {
        "page": false,
        "attempt_index": 1
      }
    }
    ```
- **Response**:
    ```json
    {
      "_xsrf": "2|99ea0564|313a21e3111869e9732aabd414665002|1777224597",
      "nick": "user465126021",
      "promo_code": "",
      "phone": "+380635550123",
      "DEBUG": 0
    }
    ```
- **Analysis**: The `_xsrf` token is returned in the response body and must be handled for stateful interactions.

**Step 2: Verify OTP & Register**
- **Endpoint**: `POST https://tornbee.com/api/v2/reg_forms/6329ae824a8a282e41d22024/registration/`
- **Purpose**: Submit the received OTP and complete the registration process
- **Request Payload**:
    ```json
    {
      "phone": "+380635550123",
      "password": "PASSWORD_HERE",
      "promo_code": "",
      "code": "333333",
      "metadata": {
        "page": false,
        "attempt_index": 3
      },
      "welcome_bonus": "68cbfefb20caa93ca8fba298",
      "currency": "USD"
    }
    ```
- **Response (Invalid Code)**:
    ```json
    {
      "DEBUG": 0,
      "_xsrf": "...",
      "error": [
        {
          "interface": "auth_form",
          "message": "authorization_error",
          "code": 10,
          "data": "invalid code"
        }
      ]
    }
    ```
- **Analysis**: The flow combines OTP verification and final registration in a single step.

## 4. Security & Reversing Notes
- **DataDome**: The presence of `api-js.datadome.co` indicates sophisticated bot detection. Automation attempts must mimic a real device environment perfectly to avoid blocking.
- **Cloudflare Turnstile**: Used as a silent or interactive challenge to verify human users.
- **XSRF Protection**: The `_xsrf` token is highly dynamic and tied to the session.

## 5. Conclusion

### Automation Feasibility: 35% (Low-Medium)

### Detailed Conclusion
The PokerBet registration flow is straightforward in terms of API structure, but it is heavily guarded by DataDome and Cloudflare. This makes simple script-based automation extremely difficult without high-quality residential proxies and advanced browser/device mimicking capabilities. The use of the `_xsrf` token in the JSON body is a non-standard but simple state management technique. Feasibility is low unless the bot protection layers are bypassed.
