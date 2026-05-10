# PullAndBear - Security Reconnaissance Report

## Metadata
- **Target URL/App**: `pullandbear.com` / `com.inditex.pullandbear`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-10`
- **Status**: `Completed`
- **HAR Files**: `PullAndBear.har`

## 1. Executive Summary
PullAndBear, a global fashion retailer under the Inditex group, utilizes a sophisticated multi-factor authentication flow on its mobile application. The analysis reveals a structured API ecosystem hosted on `www.pullandbear.com/itxrest/2/`. Authentication is performed via short-lived validation codes sent to either email or SMS, followed by a final login request that requires both the received OTP and the user's password. The platform is protected by Akamai Bot Manager, as evidenced by `ak_bmsc` cookies and high-entropy session identifiers (`ITXSESSIONID`, `UAITXID`).

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS/Email | Dual options available via `OTP-SMS` or `OTP-EMAIL` |
| **Captcha** | undefined | No visible captcha triggers found in the standard flow |
| **Encryption** | TLS/Standard | standard JSON payloads over HTTPS |
| **Rate Limits** | Unknown | No explicit rate limit errors (429) captured |
| **Endpoints Involved** | 2 | `account-validation-code` (Send) and `phone-logon` (Submit) |
| **Bot Protection** | High | Akamai Bot Manager integration detected |

## 3. Technical Traces

### 3.1 SMS Request (OTP Send)
The application requests a validation code by specifying the logon identifier and the desired channel.

**Request**:
```http
POST https://www.pullandbear.com/itxrest/2/user/store/28009400/account-validation-code?appId=4&languageId=-1&catalogId=20309455
Content-Type: application/json; charset=UTF-8
User-Agent: PullAndBear_eCom/2604.1.0 (Pixel 7; Android; 15; en-IN; ITXCORE 1)

{
  "logon": "+393720514818",
  "option": "OTP-SMS"
}
```

**Response**:
```json
{
  "email": "***********************roes@gmail.com",
  "rueiData": {
    "StoreLangRUEI": "<!--itxStoreLang='en'-->"
  }
}
```

### 3.2 OTP Submission (Login)
The final authentication step combines the phone details, the received 6-digit code, and the account password.

**Request**:
```http
POST https://www.pullandbear.com/itxrest/2/user/store/28009400/phone-logon?appId=4&languageId=-1&catalogId=20309455
Content-Type: application/json; charset=UTF-8
Cookie: ak_bmsc=...; ITXSESSIONID=...; ITXDEVICEID=...

{
  "phone": {
    "countryCode": "+39",
    "subscriberNumber": "3720514818"
  },
  "code": "252525",
  "password": "REDACTED"
}
```

**Response (Invalid OTP/Password)**:
```json
{
  "description": "_ERR_VALIDATION",
  "action": null,
  "key": "_ERR_VALIDATION",
  "commitMark": true,
  "url": null,
  "causes": [
    {
      "description": "The password or verification code you entered is incorrect. Please try again.",
      "action": null,
      "key": "_ERR_VALIDATION_AUTHENTICATION",
      "commitMark": false,
      "url": null,
      "parameters": []
    }
  ]
}
```

## 4. Automation Feasibility
- **Feasibility**: Medium (65%)
- **Reasoning**: The API uses standard JSON payloads and predictable endpoint structures. However, the presence of Akamai Bot Manager requires proper cookie management and header mirroring (User-Agent, Device ID). The requirement of a password alongside the OTP for `phone-logon` implies that automation is best suited for account login/verification rather than pure registration unless the flow is slightly different for new users.

## 5. Conclusion
PullAndBear implements a secure and user-friendly authentication system. The integration with Inditex's centralized API (`itxrest`) suggests a robust backend architecture. For automation, researchers should focus on maintaining session persistence and handling the Akamai cookies correctly to avoid triggering bot detection during high-frequency requests.
