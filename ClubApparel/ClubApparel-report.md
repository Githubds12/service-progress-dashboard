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
- **Request Payload**:
    ```json
    {
      "body": {
        "grant_type": "password",
        "password": "...",
        "response_type": "token",
        "username": "CAAPP_USER"
      },
      "endpoint": "/api/v1/authorization/tokens",
      "method": "post",
      "oauth": "Basic V0VCQVBJX0tFWTpUX19aRTI3aXBj"
    }
    ```
- **Response**: Returns an `AccessToken` (e.g., `30205962-16e3-4870-a92e-3b98933911c9`).

**Step 2: Request SMS OTP**
- **Endpoint**: (Same AWS Proxy URL)
- **Purpose**: Triggers the enrollment OTP to the user's phone.
- **Request Payload**:
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
      "oauth": "OAuth {AccessToken}"
    }
    ```
- **Response**: Returns a `verify_id` (e.g., `wXunnmXm`).

**Step 3: Verify OTP**
- **Endpoint**: `POST https://p1appg-pcapi.loyalty.peoplecloud.epsilon.com/api/v1/authorization/profiles/tokens`
- **Purpose**: Validates the OTP and establishes the user session.
- **Custom Header**: `source-application: APP-Android|{verify_id}|{random_val}|{random_val}`
- **Request Payload**:
    <!-- Form-URL-Encoded -->
    ```
    grant_type=SSO&response_type=token&SocialToken={OTP}&SocialTokenSecret={PHONE}&isSetPassword=false&username=
    ```

## 4. Security & Reversing Notes

### Custom Headers
The `source-application` header is critical. It must contain the `verify_id` received in Step 2. Failure to include this or using an expired ID results in a `400 Bad Request` or `GrantTypeInvalid` error.

### Proxy Architecture
All core loyalty actions are abstracted through the `3jhe81bobb` AWS Lambda proxy. This ensures that the client secret and internal Epsilon endpoint structure are not exposed directly, although the proxy payload itself reveals the underlying API structure.

## 5. Conclusion

### Automation Feasibility: 65% (Medium)

### Detailed Conclusion:
ClubApparel's integration with PeopleCloud Epsilon is well-structured but can be automated with a script that handles the three-step flow. The primary challenge is maintaining the session state (AccessToken and verify_id) across different domains. Use of a session-aware HTTP client (like Python `requests.Session`) and proper header synchronization is essential. No complex captchas or fingerprinting were detected, making this a stable target for automation once the flow is implemented.
