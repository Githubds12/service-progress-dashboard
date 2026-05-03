# Flowwow - Research Report

## Metadata
- **Target URL/App**: `com.flowwow`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-02`
- **Status**: `Completed`
- **HAR Files**: `Flowwow.har`

## 1. Executive Summary
Flowwow is a marketplace for flowers and gifts. The Android application implements an OTP-based authentication system using SMS as the primary channel. The API requests are secured using a custom MD5-based `hash` parameter in the query string, which likely signs the request parameters. No advanced bot protection like reCAPTCHA or Cloudflare was observed during the captured registration flow. Automation feasibility is assessed as High (>70%) if the hashing logic can be replicated.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | primary channel for OTP |
| **Captcha** | undefined | No captcha was observed during the auth flow |
| **Encryption** | Custom Hash | MD5-based `hash` parameter in query strings |
| **Rate Limits** | Unknown | No rate limiting behavior was observed during testing |
| **Endpoints Involved** | 2 | `/clientapp/client/smsCode`, `/api2/client/login` |
| **Bot Protection** | Custom Hash | API-level security using request signing |

## 3. Flow Details

### Flow 1: SMS Registration / Login

**Step 1: Send SMS OTP**
- **Endpoint**: `GET https://apis.flowwow.com/clientapp/client/smsCode`
- **Purpose**: Request an SMS OTP for the provided phone number.
- **Request**:
    - **Method**: `GET`
    - **Headers**:
        ```http
        User-Agent: FW App android/5.3.2-PROD (com.flowwow; android:15; model:Pixel 7)
        FW-FB-TOKEN: 23024911
        Device-Unique-ID: 4a56fb123539e585
        adjust-device-id: 4f73900ad62db1507dd9b326054dfbe9
        ```
    - **Query Parameters**:
        - `app_version`: `5.3.2`
        - `lang`: `en`
        - `partner_id`: `1005`
        - `phone`: `393513820450` <!-- Phone number used in test -->
        - `hash`: `28ab3c35e80c478a1956b8027b65ce3c`
- **Response**:
    - **Status**: `200 OK`
    - **Body**:
        ```json
        {"result":[],"status":1}
        ```

**Step 2: Verify OTP and Login**
- **Endpoint**: `POST https://api2.flowwow.com/api2/client/login`
- **Purpose**: Submit the received OTP code to authenticate the user.
- **Request**:
    - **Method**: `POST`
    - **Headers**:
        ```http
        Content-Type: application/x-www-form-urlencoded
        User-Agent: FW App android/5.3.2-PROD (com.flowwow; android:15; model:Pixel 7)
        FW-FB-TOKEN: 23024911
        Device-Unique-ID: 4a56fb123539e585
        ```
    - **Query Parameters**:
        - `app_version`: `5.3.2`
        - `lang`: `en`
        - `partner_id`: `1005`
        - `hash`: `5a311b79f48b1ea13fa05456c3c51262`
    - **Body**:
        ```form-data
        phone=393513820450&code=333333&currency=USD&main_docs_agreed=1&advertising_agreed=1
        ```
        <!-- OTP Code 333333 was a test attempt -->
- **Response**:
    - **Status**: `200 OK`
    - **Body**:
        ```json
        {"status":0,"errors":[{"code":3,"msg":"Incorrect code.\nTry entering the code again","hideError":true}]}
        ```

## 4. Security & Reversing Notes

### Custom Hashing Mechanism
The application includes a `hash` parameter in almost every API request. This 32-character hex string is likely an MD5 hash of the request parameters combined with a static salt or device-specific token. Reversing the hashing logic is required for full automation.

### Device Identifiers
The requests use several device-specific headers and parameters:
- `Device-Unique-ID`: Android device identifier.
- `adjust-device-id`: Adjust SDK identifier.
- `FW-FB-TOKEN`: A token obtained during the app initialization phase (`addToken` endpoint).

## 5. Conclusion
Flowwow's authentication flow is straightforward but protected by a request signing mechanism (`hash`). No third-party bot protection services are implemented on the observed endpoints.

### Automation Feasibility: High (75%)
The flow is simple (2 steps), and the main challenge is replicating the `hash` calculation. Once the hashing logic is extracted from the APK, the service can be easily automated.

### Recommendations:
- Reverse engineer the APK to identify the `hash` generation logic.
- Implement the hashing in the automation script to allow dynamic parameter changes (e.g., different phone numbers).
