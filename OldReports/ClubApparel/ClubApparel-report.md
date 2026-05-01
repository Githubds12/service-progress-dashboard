# ClubApparel Security & Authentication Analysis

## Metadata
- **Target URL/App**: `com.appemirates.clubapparel` / `clubapparel.com`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-30 11:10`
- **Status**: `Completed`
- **HAR Files**: `ClubApparel.har`

## 1. Executive Summary
ClubApparel (com.appemirates.clubapparel) utilizes the **PeopleCloud Epsilon** loyalty and CRM platform for its mobile authentication. The architecture involves a secure AWS Lambda proxy (`3jhe81bobb.execute-api.ap-southeast-1.amazonaws.com`) that handles internal loyalty scripts. The authentication flow is multi-stage, requiring a client-level AccessToken before triggering the SMS. A session-specific `verify_id` is then used in a custom header during the final OTP validation step. Automation is feasible but requires precise handling of the proxied request structure and headers.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | 4-digit OTP code |
| **Captcha** | undefined | No captcha was observed during the enrollment flow |
| **Encryption** | Standard TLS | No proprietary payload encryption; uses standard JSON |
| **Rate Limits** | undefined | Not explicitly observed in the trace |
| **Endpoints Involved** | 3 | `/tokens`, `/MobileEnrollOTP/invoke`, `/profiles/tokens` |
| **Bot Protection** | Medium | AWS API Gateway + Custom Headers (`source-application`) |

## 3. Flow Details

### Flow 1: Registration & SMS Verification

**Step 1: Obtain Client Access Token**
- **Endpoint**: `POST https://3jhe81bobb.execute-api.ap-southeast-1.amazonaws.com/prod/club-apparel/epsilon/internal`
- **Purpose**: Authenticates the mobile app client to the Epsilon backend.
- **Actual Request Body**:
    ```json
    {
      "body": {
        "grant_type": "password",
        "password": "v@nW2JX845=c",
        "response_type": "token",
        "username": "CAAPP_USER"
      },
      "endpoint": "/api/v1/authorization/tokens",
      "method": "post",
      "oauth": "Basic V0VCQVBJX0tFWTpUX19aRTI3aXBj"
    }
    ```
- **Actual Response Body (201 Created)**:
    ```json
    {
      "Username": "CAAPP_USER",
      "AccessToken": "30205962-16e3-4870-a92e-3b98933911c9",
      "access_token": "30205962-16e3-4870-a92e-3b98933911c9",
      "token_type": "OAuth",
      "RefreshToken": "d9d65d0f-9d43-424c-9503-5463cf8f3116",
      "refresh_token": "d9d65d0f-9d43-424c-9503-5463cf8f3116",
      "AccessTokenExpiration": "2026-05-03T16:47:54.9553972Z",
      "expires_in": 300000,
      "RefreshTokenExpiration": "2026-05-03T23:27:54.9553972Z",
      "Success": true,
      "RequireSsl": true,
      "IsPasswordExpired": false,
      "TenantId": "3e0da31e-4947-7616-e053-5ba8e70a2457",
      "TenantName": "FUSION TENANT",
      "description": "API Response!",
      "code": 0
    }
    ```

**Step 2: Request SMS OTP**
- **Endpoint**: (Same AWS Proxy URL)
- **Purpose**: Triggers the enrollment OTP to the user's phone.
- **Actual Request Body**:
    ```json
    {
      "body": {
        "IsForgotPassword": false,
        "PhoneNumber": "393720511791"
      },
      "endpoint": "/api/v1/infrastructure/scripts/MobileEnrollOTP/invoke",
      "headers": {
        "Accept-Language": "en-US",
        "Program-Code": "CAAPP",
        "content-type": "application/json"
      },
      "method": "post",
      "oauth": "OAuth 30205962-16e3-4870-a92e-3b98933911c9"
    }
    ```
- **Actual Response Body (201 Created)**:
    ```json
    {
      "data": {
        "verify_id": "wXunnmXm",
        "to": {
          "mobile": "393720511791"
        },
        "flow_id": ""
      },
      "IsOtpVerified": false,
      "IsPasswordSetUpDone": false,
      "description": "API Response!",
      "code": 0
    }
    ```

**Step 3: Verify OTP**
- **Endpoint**: `POST https://p1appg-pcapi.loyalty.peoplecloud.epsilon.com/api/v1/authorization/profiles/tokens`
- **Purpose**: Validates the OTP and establishes the user session.
- **Actual Request Headers (CRITICAL)**:
    - **Source-Application**: `APP-Android|wXunnmXm|2222|8791`
    - *(Note: The OTP is passed directly in this header. Format: `APP-Android|{verify_id}|{OTP}|{random_val}`. In this case, **2222** is the OTP.)*
    - **Authorization**: `Basic TU9CSUxFX0tFWTpTM2N1cmUuMTIz`
- **Actual Request Body (Form-URL-Encoded)**:
    ```
    grant_type=SSO&response_type=token&SocialToken=IT&SocialTokenSecret=393720511791&isSetPassword=false&username=
    ```
    *(Note: `SocialToken=IT` appears to be a country/locale identifier or placeholder when the OTP is supplied via the custom header.)*
- **Actual Response Body (400 Bad Request)**:
    ```json
    {
      "ErrorCode": "GrantTypeInvalid",
      "Message": "Grant Type is invalid."
    }
    ```
    *Note: The SocialToken "IT" in the trace likely indicates a country code selection or a partial user interaction during the HAR capture.*

## 4. Security & Reversing Notes

### Custom Headers
The `Source-Application` header is critical. It must contain the `verify_id` received in Step 2. Failure to include this or using an expired ID results in a `400 Bad Request` or `GrantTypeInvalid` error.

### Proxy Architecture
All core loyalty actions are abstracted through the `3jhe81bobb` AWS Lambda proxy. This ensures that the client secret and internal Epsilon endpoint structure are not exposed directly, although the proxy payload itself reveals the underlying API structure.

## 5. Conclusion

### Automation Feasibility: 65% (Medium)

### Detailed Conclusion:
ClubApparel's integration with PeopleCloud Epsilon is well-structured but can be automated with a script that handles the three-step flow. The primary discovery is that the **OTP is passed within the `Source-Application` header** rather than the standard request body. The format `APP-Android|{verify_id}|{OTP}|{random_val}` must be followed exactly. The primary challenge is maintaining the session state (AccessToken and verify_id) and correctly constructing this composite header. Use of a session-aware HTTP client (like Python `requests.Session`) and proper header synchronization is essential. No complex captchas or fingerprinting were detected, making this a stable target for automation once the flow is implemented.
