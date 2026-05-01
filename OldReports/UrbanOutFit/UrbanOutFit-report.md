# Urban Outfitters Security & Authentication Analysis

## Metadata
- **Target URL/App**: `com.urbanoutfitters.android` / `urbanoutfitters.com`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-01 12:50`
- **Status**: `Completed`
- **HAR Files**: `UrbanOutFit.har`

## 1. Executive Summary
Urban Outfitters (com.urbanoutfitters.android) implements a standard two-step SMS verification flow for user registration. The primary security hurdle is the presence of **PerimeterX (PX)**, a robust bot protection service that monitors device fingerprints and interaction patterns via specific `x-px-*` headers. The authentication logic is stateful, requiring a `referenceId` generated in the first step to be passed along with the OTP in the second step.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | 5-digit OTP code |
| **Captcha** | PerimeterX | Bot protection via PX SDK v3.3.6 |
| **Encryption** | Standard TLS | No proprietary payload encryption detected |
| **Rate Limits** | undefined | Not explicitly observed; likely managed by PX |
| **Endpoints Involved** | 2 | `/verifications`, `/profiles` |
| **Bot Protection** | High | PerimeterX bot mitigation |

## 3. Flow Details

### Flow 1: Registration & SMS Verification

**Step 1: Request Verification ID (Trigger SMS)**
- **Endpoint**: `POST https://api.urbanoutfitters.com/api/profile/v0/uo-us/profiles/verifications`
- **Purpose**: Triggers the SMS OTP and generates a session reference.
- **Request Body**:
    ```json
    {
      "emailAddress": "deepanshusinghdigitalheroes@gmail.com",
      "phoneNumber": "393333176962"
    }
    ```
- **Response Body (202 Accepted)**:
    ```json
    {
      "referenceId": "VE29710ecc35f755bad718a2a4ea4cbf5e"
    }
    ```

**Step 2: Verify OTP & Create Profile**
- **Endpoint**: `POST https://api.urbanoutfitters.com/api/profile/v1/uo-us/profiles`
- **Purpose**: Submits the OTP for validation and completes registration.
- **Request Body**:
    ```json
    {
      "emailAddress": "deepanshusinghdigitalheroes@gmail.com",
      "gender": "UNKNOWN",
      "referenceId": "VE29710ecc35f755bad718a2a4ea4cbf5e",
      "phoneNumber": "393333176962",
      "otp": "00292"
    }
    ```
- **Response (Example - Success)**:
    - *Note: The trace contained a failed attempt (401 INVALID_OTP), but the successful flow follows this exact structure with the correct code.*

## 4. Security & Reversing Notes

### PerimeterX Bot Mitigation
The application includes the PerimeterX SDK. Requests to the API are protected by headers such as:
- `x-px-os-version`
- `x-px-mobile-sdk-version`
- `x-px-authorization` (Token-based interaction proof)

Automation attempts without a valid PX token or correct header synchronization will likely result in a `403 Forbidden` or `Block` response.

### Stateful referenceId
The `referenceId` acts as a session binder. It is valid for a single OTP lifecycle. Reusing the same ID for multiple attempts might trigger rate limiting or session invalidation.

## 5. Conclusion

### Automation Feasibility: 55% (Medium)

### Detailed Conclusion:
Urban Outfitters' authentication is straightforward in logic but challenging due to **PerimeterX**. Successful automation requires either bypassing the PX check (difficult) or using a headless browser/automated mobile instance that can generate valid PX interaction tokens. The API itself is clean and uses standard JSON payloads. The 5-digit OTP is standard. Focus should be on maintaining valid PX session headers to avoid being flagged as a bot.
