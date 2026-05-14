# Lyft - Research Report

## Metadata
- **Target URL/App**: `me.lyft.android`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-07`
- **Status**: `Completed`
- **HAR Files**: `lyft.har`

## 1. Executive Summary
Lyft's Android application implements a standard OAuth2-based authentication flow for phone number verification. The process involves obtaining a client access token using basic authentication, followed by an OTP request to the `/v1/phoneauth` endpoint. The final verification is performed via the `/oauth2/access_token` endpoint using a custom grant type `urn:lyft:oauth2:grant_type:phone`. While the flow is straightforward, it is protected by various headers including `x-session`, `x-client-session-id`, and specialized `Authorization` tokens. Automation feasibility is rated as Medium due to the requirement of maintaining valid session identifiers and handling potential rate limits or bot protection measures not fully captured in the initial trace.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for OTP delivery |
| **Captcha** | undefined | No captcha challenges were observed in the captured flow |
| **Encryption** | Standard HTTPS/TLS | All communication is conducted over encrypted TLS channels |
| **Rate Limits** | Partial | Rate limits (429) observed on telemetry endpoints (Sentry); Unknown for main API |
| **Endpoints Involved** | 3 | `/oauth2/access_token`, `/v1/phoneauth` |
| **Bot Protection** | Internal Session Tracking | Uses `x-session` and `x-client-session-id` for tracking |

## 3. Flow Details

### Flow 1: Phone Number Authentication

**Step 1: Get Client Access Token**
- **Endpoint**: `POST https://api.lyft.com/oauth2/access_token`
- **Purpose**: Obtain an initial Bearer token for subsequent API calls.
- **Notable Headers**:
    - `Authorization`: Basic `ZVNhdDctaXU5ZG9NOlp0dkxEejBuMS1rSlZ3a0l2eEM0aVNKMHlNdkp5ZFBx`
    - `x-session`: `eyJhIjoiMTQ2OGYwYmY1ZGIxOGI3YyIsImgiOnRydWUsImsiOiI1YTdjZWM4OC01YTBhLTQ2ZmItYWI4My04ZmU0NDM3Y2ZkNDgifQ==`
    - `user-agent`: `lyft:android:15:2026.16.3.1777447561`
- **Request Payload**:
    ```text
    grant_type=client_credentials
    ```
- **Response**:
    ```json
    {
      "token_type": "Bearer",
      "access_token": "WiACBvVK7R/M7VNHKPqqDl96zc4+2aRmechXbcrOMruESCbgaSrJME3miUavg1pdBANBM6xeCPMdizbgtDeA8EjNTePJ6iBQ2S/V2+xBMUmcoxJYp/JGHbw=",
      "expires_in": 86400,
      "scope": "privileged.price.upfront public users.create"
    }
    ```

**Step 2: Request Phone Auth (SMS Request)**
- **Endpoint**: `POST https://api.lyft.com/v1/phoneauth`
- **Purpose**: Initiate SMS OTP delivery to the user's phone number.
- **Notable Headers**:
    - `Authorization`: Bearer `QxIjxs7v4E0RZUCgtdRQj4sGB+scPoY6dkdJ+4e6gbmuZWU1To5wNRjB9WZm6pYOuO0kiPHIkhBIlan5KBYn2O71EvXwyUaYH0cjDJhIoFp60FPi71fhx+Q=`
    - `x-session`: `eyJhIjoiMTQ2OGYwYmY1ZGIxOGI3YyIsImYiOiJmNTFlZTMzNi1lNDg5LTQ4ODItOGMyMS05NWZmMDZlZDRhOWEiLCJoIjp0cnVlLCJrIjoiNWE3Y2VjODgtNWEwYS00NmZiLWFiODMtOGZlNDQzN2NmZDQ4In0=`
- **Request Payload**:
    ```json
    {
      "phone_number": "+393518831002", <!-- phone_number: +393518831002 -->
      "voice_verification": false,
      "message_format": "sms_android_retriever",
      "client_configuration": "release"
    }
    ```
- **Response**:
    ```json
    {
      "message_format_accepted": true,
      "verification_code_length": 6
    }
    ```

**Step 3: Verify OTP (OTP Submit)**
- **Endpoint**: `POST https://api.lyft.com/oauth2/access_token`
- **Purpose**: Submit the received OTP code to obtain a final authentication token.
- **Notable Headers**:
    - `Authorization`: Basic `ZVNhdDctaXU5ZG9NOlp0dkxEejBuMS1rSlZ3a0l2eEM0aVNKMHlNdkp5ZFBx`
- **Request Payload**:
    ```text
    grant_type=urn%3Alyft%3Aoauth2%3Agrant_type%3Aphone&phone_number=%2B393518831002&phone_code=258899&identifiers=W3sidHlwZSI6ImFuZHJvaWRfYmFja3VwX3Rva2VuIiwic291cmNlIjoibHlmdF9hbmRyb2lkX2FwcCIsIm5hbWUiOiI1YTdjZWM4OC01YTBhLTQ2ZmItYWI4My04ZmU0NDM3Y2ZkNDgifV0%3D
    ```
    <!-- phone_number: +393518831002 -->
    <!-- phone_code: 258899 -->
- **Response**:
    ```json
    {
      "error": "invalid_grant",
      "error_description": "No matching phone number and phone code found."
    }
    ```
- **Analysis**: The endpoint returns an `invalid_grant` error if the OTP is incorrect, which confirms this is the correct verification endpoint.

## 4. Security & Reversing Notes

### Authentication Mechanisms

**1. Client Credentials**
- Initial access is gated by a `Basic` auth token hardcoded or pre-shared in the app.
- This token is used to get a temporary `Bearer` token.

**2. Session Tracking**
- `x-session` and `x-client-session-id` are used across all requests to maintain state.
- `x-session` appears to be a base64 encoded JSON object containing installation and device identifiers.

**3. Phone Auth Grant Type**
- Lyft uses a custom OAuth2 grant type `urn:lyft:oauth2:grant_type:phone` specifically for phone-based logins.

**4. Rate Limiting (Telemetry)**
- High frequency `429 Too Many Requests` status codes were observed on Sentry telemetry endpoints (`o4507234886615040.ingest.us.sentry.io`).
- This suggests strict rate limiting on error reporting and analytics, although no rate limiting was explicitly triggered on the core authentication endpoints during the captured flow.

## 5. Conclusion

### Automation Feasibility: 60%

### Detailed Conclusion:
The Lyft authentication flow is relatively standard but requires careful handling of session headers and OAuth2 grant types. The use of multiple tokens (Basic and Bearer) and encoded session data adds a layer of complexity for automation. However, since no CAPTCHA was observed in the initial flow, automation is feasible if the session generation logic can be replicated or captured reliably.

Recommendations:
- Monitor for the appearance of CAPTCHA challenges during high-frequency requests.
- Ensure all `x-session` and `x-client-session-id` headers are correctly mirrored from the app's behavior.
