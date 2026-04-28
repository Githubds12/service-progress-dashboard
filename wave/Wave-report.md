# Wave - Research Report

## Metadata
- **Target URL/App**: `com.wave.personal` (Wave Mobile Money)
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29`
- **Status**: `Completed`
- **HAR Files**: `Wave.har`

## 1. Executive Summary
Wave Mobile Money uses a GraphQL-based backend (`ml.mmapp.wave.com/graphql`). The registration and authentication flows are protected by **Google reCAPTCHA Enterprise** (`www.recaptcha.net/recaptcha/api3/mri`), which is triggered before the `SignupMutation`. The app also collects detailed device fingerprinting (`deviceId`, `deviceModel`). Automation feasibility is low due to the integrated reCAPTCHA protection and GraphQL structure.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | OTP sent after reCAPTCHA verification |
| **Captcha** | Yes | Google reCAPTCHA Enterprise (`6Lc69y8r...`) |
| **Encryption** | Partial | HTTPS with GraphQL payloads |
| **Rate Limits** | Unknown | Enforced via reCAPTCHA and backend |
| **Endpoints Involved** | 2 | `recaptcha/api3/mri`, `/graphql` (SignupMutation) |
| **Bot Protection** | High | Google reCAPTCHA Enterprise |

## 3. Flow Details

### Flow 1: Signup / Registration

**Step 1: reCAPTCHA Verification**
- **Endpoint**: `POST https://www.recaptcha.net/recaptcha/api3/mri`
- **Purpose**: Obtain a reCAPTCHA token for the signup request.
- **Payload**: Contains package name `com.wave.personal` and site key `6Lc69y8rAAAAAL4h1ONHifmEB0I8wskZdp52j0qE`.

**Step 2: Signup Mutation (Trigger SMS)**
- **Endpoint**: `POST https://ml.mmapp.wave.com/graphql`
- **Purpose**: Initialize the signup process and trigger the SMS.
- **Request Payload**:
    ```json
    {
      "operationName": "SignupMutation",
      "variables": {
        "mobile": "+22379225144",
        "device": {
          "deviceId": "461b1cafb880b09e",
          "deviceName": "Pixel 7",
          "deviceModel": "Google Pixel 7"
        },
        "ui": "SMARTPHONE_APP"
      },
      "query": "mutation SignupMutation($mobile: String!, $device: DeviceInput!) { signup(mobile: $mobile, device: $device) { tokenId } }"
    }
    ```
- **Response Payload**:
    ```json
    {
      "data": {
        "signup": {
          "tokenId": "ST_ml_2d571IEXlQhp",
          "__typename": "SignupResponse"
        }
      }
    }
    ```

**Step 3: Verify OTP (Submit Code)**
- **Endpoint**: `POST https://ml.mmapp.wave.com/graphql`
- **Purpose**: Submit the OTP code received via SMS.
- **Request Payload**:
    ```json
    {
      "operationName": "CustomerVerifyAuthCode",
      "variables": {
        "tokenId": "ST_ml_2d571IEXlQhp",
        "code": "3333",
        "autofilled": false,
        "insecureCurrentlyLoggedInUserSessionIds": [],
        "insecureCurrentlyLoggedInUserMobiles": []
      },
      "query": "mutation CustomerVerifyAuthCode($tokenId: String!, $code: String!) { verifyAuthCode(tokenId: $tokenId, code: $code) { success } }"
    }
    ```
- **Response Payload (Error Case)**:
    ```json
    {
      "errors": [
        {
          "message": "Le code de validation était incorrect ou a expiré.",
          "code": "bad-sms-code"
        }
      ],
      "data": {
        "verifyAuthCode": null
      }
    }
    ```

## 4. Security & Reversing Notes

### Bot Protection (reCAPTCHA)
- The application uses `com.google.android.gms.recaptcha.Recaptcha` client.
- The `SignupMutation` likely expects a reCAPTCHA token in the headers or variables (not fully visible in the truncated body but typical for this setup).

### GraphQL Backend
- Uses Apollo Kotlin/Android client.
- Operation names are descriptive (`SignupMutation`, `RefreshAppRemoteConfigQuery`).

## 5. Conclusion

### Automation Feasibility: 20%

### Critical Blockers:
1. **reCAPTCHA Enterprise**: Bypassing reCAPTCHA programmatically requires a captcha solving service or browser-based automation.
2. **Device Fingerprinting**: Backend validates `deviceId` and other hardware metadata.
