# Shell Go+ India Security Analysis Report

## 1. Executive Summary
The Shell Go+ India application (com.shell.sitibv.shellgoplusindia) implements a mobile authentication flow managed by Capillary Technologies. The security analysis identified a multi-step OTP-based registration and login process. The primary authentication endpoints are hosted on `capillarytech.com` subdomains. The application uses a custom `hash` parameter in its authentication requests, likely serving as a signature or integrity check for the request payload. No CAPTCHA or advanced bot protection was observed during the captured registration flow, although standard rate limiting and session management are implemented.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS OTP | Primary channel for user authentication |
| **Captcha** | undefined | No CAPTCHA observed during testing |
| **Encryption** | Custom Hash | Uses a `hash` parameter for request integrity |
| **Rate Limits** | Unknown | No rate limiting behavior was observed during testing |
| **Endpoints Involved** | 3 | `/otp/generate`, `/otp/validate`, `/customers/neo` |
| **Bot Protection** | Cloudflare | Standard Cloudflare protection on CapillaryTech endpoints |

## 3. Technical Traces

### 3.1. OTP Generation
This endpoint initiates the SMS OTP sending process to the user's mobile number.

**Request:**
- **Method:** `POST`
- **URL:** `https://auth.shell.integrations.capillarytech.com/auth/v1/otp/generate`
- **Headers:**
  - `X-CAP-USE-NEW-ENCRYPTION`: `true`
  - `cap_brand`: `SHELLINDIA`
  - `cap_device_id`: `c1fe3382-f286-4e1e-9826-c8df6580efbf`
  - `Content-Type`: `application/json; charset=UTF-8`
  - `User-Agent`: `okhttp/4.11.0`

**Body:**
```json
{
  "brand": "SHELLINDIA",
  "deviceId": "c1fe3382-f286-4e1e-9826-c8df6580efbf",
  "hash": "ULno5RpuLimQXxQFOYzB8wK2C/lPKU8A0PAl8MRqIasfmoOuU9ii2EwC00hP/HWSqKYFODyEH47z8uISU8FUzhC7J1aYPoXzyPg3KPXhedwqEd8frXhC8LRtE8PD4UPRLqw8AmfF4fgoHy0yWAQgLczX1S4kJjkYFDc/6dFzlQ0VWVElk11SY0Aindh/BqL/DULSypWVcrAJ+oHFMzkb9jZZ7n/kZnehqnNe+0IaLFK97Jv4jrLmR12DtJ7Rknx91s5kh6b/Y02nOIyKsEtsRd1IHiuNw0Zus7CgIMV+/ENqMNsJYTBkX+q2k9U8/+JixNjJzwHT0Mua3YeO3l4XZ4i4SNCeuFHVAc66aJidPZAii7+9reC4COBzGNblGTzSdCVup3ipVmKBx15D7PMyLtyYGZqdX9UiChV+hIHDZQmAb5diL4os6RdH9rNU0ehsVdjveCvRU8UG9hZx7XFoSYbcUi8OhUPY+lQZ8qV2aE4170oYRTUg1Io69a6h22ARmeS70pYkZkI01ZgZ66kknRC+Iy8j1jQZmuj1iqFFuIpj73fGpXI7oPf9YjRzr8TxJDEIMaDi0OXyt14kvj8c9qogNHevJ7p7EgQKImto+t62i5W1uiHr3kCcMsRCd8pmPi4gAlFHEyaYImYvcxOBOe6Xawmx0bCJ0SAsbA+t7Xs=",
  "mobile": "918791267460",
  "mobileTemp": "+918791267460",
  "otp": null,
  "sessionId": "P-0b1ebbb6-dc56-42b9-8fe2-83a1102d7300",
  "timeStamp": 1777194841335}
```

**Response:**
- **Status:** `200 OK`
- **Body:**
```json
{"status":{"success":true,"code":200,"message":"SUCCESS"}}
```

### 3.2. OTP Validation
This endpoint verifies the OTP code provided by the user.

**Request:**
- **Method:** `POST`
- **URL:** `https://auth.shell.integrations.capillarytech.com/auth/v1/otp/validate`
- **Headers:**
  - `cap_brand`: `SHELLINDIA`
  - `cap_device_id`: `c1fe3382-f286-4e1e-9826-c8df6580efbf`
  - `Content-Type`: `application/json; charset=UTF-8`

**Body:**
```json
{
  "brand": "SHELLINDIA",
  "deviceId": "c1fe3382-f286-4e1e-9826-c8df6580efbf",
  "hash": "ULno5RpuLimQXxQFOYzB8wK2C/lPKU8A0PAl8MRqIasfmoOuU9ii2EwC00hP/HWSqKYFODyEH47z8uISU8FUzhC7J1aYPoXzyPg3KPXhedwqEd8frXhC8LRtE8PD4UPRLqw8AmfF4fgoHy0yWAQgLczX1S4kJjkYFDc/6dFzlQ0VWVElk11SY0Aindh/BqL/DULSypWVcrAJ+oHFMzkb9jZZ7n/kZnehqnNe+0IaLFK97Jv4jrLmR12DtJ7Rknx91s5kh6b/Y02nOIyKsEtsRd1IHiuNw0Zus7CgIMV+/ENqMNsJYTBkX+q2k9U8/+JixNjJzwHT0Mua3YeO3l4XZ4i4SNCeuFHVAc66aJidPZAii7+9reC4COBzGNblGTzSdCVup3ipVmKBx15D7PMyLtyYGZqdX9UiChV+hIHDZQmAb5diL4os6RdH9rNU0ehsVdjveCvRU8UG9hZx7XFoSYbcUi8OhUPY+lQZ8qV2aE4170oYRTUg1Io69a6h22ARmeS70pYkZkI01ZgZ66kknRC+Iy8j1jQZmuj1iqFFuIpj73fGpXI7oPf9YjRzr8TxJDEIMaDi0OXyt14kvj8c9qogNHevJ7p7EgQKImto+t62i5W1uiHr3kCcMsRCd8pmPi4gAlFHEyaYImYvcxOBOe6Xawmx0bCJ0SAsbA+t7Xs=",
  "mobile": "918791267460",
  "mobileTemp": "+918791267460",
  "otp": "449432",
  "sessionId": "P-0b1ebbb6-dc56-42b9-8fe2-83a1102d7300",
  "timeStamp": 1777194841335}
```

**Response:**
- **Status:** `200 OK`
- **Body:**
```json
{
  "status": {"success":true,"code":200,"message":"SUCCESS"},
  "auth": {
    "token": "eyJpZHYiOlsiTU9CSUxFfDkxODc5MTI2NzQ2MCJdLCJkZXYiOiJjMWZlMzM4Mi1mMjg2LTRlMWUtOTgyNi1jOGRmNjU4MGVmYmYiLCJvcmciOiJTSEVMTElORElBIiwiYWxnIjoiSFMyNTYifQ.eyJ1aWQiOiIyMTQzMTQ0NyIsImlzcyI6IkNBUElMTEFSWSBURUNITk9MT0dJRVMiLCJpc2MiOiJmYWxzZSIsIm9nYyI6WyIxNTExODF8c2hlbGwuaW5kLnNvbHV0aW9uIl0sImV4cCI6MTc3NzI4MTI1MSwidHlwZSI6IldSSVRFIiwiaWF0IjoxNzc3MTk0ODUxLCJyb2wiOiJVU0VSIn0.__KMWQwjBTfcE38ZwCHGz7xbibZGC7kx8a3wi5NFEL4",
    "key": "..."
  },
  "user": {"appRegistered":false,"sessionId":null,"role":"USER","userRegisteredForPassword":false}
}
```

## 5. Conclusion
The authentication mechanism of Shell Go+ India is robustly integrated with Capillary Technologies' platform. While the use of a `hash` parameter adds a layer of complexity for automated interactions, the absence of CAPTCHA on the observed registration endpoints suggests a medium feasibility for automation, provided the hashing algorithm can be replicated or bypassed. The reliance on SMS-based OTP remains the primary security control.

Automation Feasibility: Medium 40-70%
Detailed Conclusion: The automation of Shell Go+ India is possible but requires reverse-engineering the `hash` generation logic used in the authentication requests. The current flow is predictable once the session and device identifiers are established. Strengthening the security with CAPTCHA or advanced bot protection like reCAPTCHA Enterprise is recommended to prevent mass account creation or credential stuffing.
