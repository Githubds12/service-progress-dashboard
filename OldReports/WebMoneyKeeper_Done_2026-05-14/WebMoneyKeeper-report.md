# WebMoney Keeper (com.webmoney.my) - Research Report

## Metadata
- **Target URL/App**: `com.webmoney.my`
- **Researcher**: `Security Research Team`
- **Date**: `2026-05-14`
- **Status**: `Completed`
- **HAR Files**: `WebMoneyKeeper.har`
- **OTP Code**: `0815` (Note: `25252` also observed in capture)

## 1. Executive Summary
WebMoney Keeper (Android) utilizes a SOAP-based XML protocol over HTTPS for its primary authentication and account management flows. The application communicates with multiple subdomains under `web.money` (e.g., `api4mini.web.money`, `events-api.web.money`). The authentication flow involves initializing a session, performing an authenticated login with an `authHash`, and conducting phone verification through a multi-step SOAP process. Security measures include session-bound requests, proprietary auth hashing, and polling-based SMS status verification.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Polling-based verification with GetSmsStatus |
| **Captcha** | undefined | No captcha challenge was triggered during the flow |
| **Encryption** | SOAP XML | Payloads use XML structure with session-bound authHash |
| **Rate Limits** | Unknown | No rate limiting behavior (429/Cooldown) was observed |
| **Endpoints Involved** | 4 | NewSession, AuthenticateWithOptions, SetMobilePhoneNumberBeginEx, SetMobilePhoneNumberEndWithConfirmation |

## 3. Flow Details

### Flow 1: Authentication & Session Initialization

**Step 1: Initialize Session**
- **Endpoint**: `POST https://api4mini.web.money/SimpleAuthApi.asmx`
- **SOAP Action**: `http://mini.webmoney.ru/api/NewSession`
- **Purpose**: Retrieve a unique `sessionId` for the current device/app instance.
- **Request Body**:
    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <NewSession xmlns="http://mini.webmoney.ru/api">
          <appId>c73fa9c3-77f1-456e-8568-e61a16b4d1f7</appId>
        </NewSession>
      </soap:Body>
    </soap:Envelope>
    ```
- **Response**:
    ```xml
    <NewSessionResponse xmlns="http://mini.webmoney.ru/api">
      <NewSessionResult>0</NewSessionResult>
      <sessionId>8ca092af-98a3-4aca-b0f1-5f8d154bbe17</sessionId>
    </NewSessionResponse>
    ```

**Step 2: Authenticate with Options**
- **Endpoint**: `POST https://api4mini.web.money/SimpleAuthApi.asmx`
- **SOAP Action**: `http://mini.webmoney.ru/api/AuthenticateWithOptions`
- **Purpose**: Authenticate the user session using WMID/Phone and a calculated `authHash`.
- **Request Body (Truncated)**:
    ```xml
    <AuthenticateWithOptions xmlns="http://mini.webmoney.ru/api">
      <sessionId>8ca092af-98a3-4aca-b0f1-5f8d154bbe17</sessionId>
      <login>368803903456</login>
      <authHash>ac8d80ddf315aaaf8816fda746f36e46</authHash>
      <options>
        <Reason>SignIn</Reason>
        <DeviceId>c0723dce1f9f3080b85e6629d777d3b7</DeviceId>
        <Meta>
          <NameAndValue><Name>vendor</Name><Value>Google</Value></NameAndValue>
          <NameAndValue><Name>model</Name><Value>Pixel 7</Value></NameAndValue>
          <NameAndValue><Name>app-ver</Name><Value>5.4.72</Value></NameAndValue>
        </Meta>
      </options>
    </AuthenticateWithOptions>
    ```
- **Response**:
    ```xml
    <AuthenticateWithOptionsResponse xmlns="http://mini.webmoney.ru/api">
      <AuthenticateWithOptionsResult>0</AuthenticateWithOptionsResult>
    </AuthenticateWithOptionsResponse>
    ```

### Flow 2: Mobile Number Verification (SMS)

**Step 1: Initiate Phone Binding/Verification**
- **Endpoint**: `POST https://api4mini.web.money/AccountApi.asmx`
- **SOAP Action**: `http://mini.webmoney.ru/api/SetMobilePhoneNumberBeginEx`
- **Purpose**: Send a verification code to the target phone number.
- **Request Body**:
    ```xml
    <SetMobilePhoneNumberBeginEx xmlns="http://mini.webmoney.ru/api">
      <sessionId>8ca092af-98a3-4aca-b0f1-5f8d154bbe17</sessionId>
      <countryCode>39</countryCode>
      <mobilePhone>3720519093</mobilePhone>
    </SetMobilePhoneNumberBeginEx>
    ```
- **Response**:
    ```xml
    <SetMobilePhoneNumberBeginExResponse xmlns="http://mini.webmoney.ru/api">
      <SetMobilePhoneNumberBeginExResult>0</SetMobilePhoneNumberBeginExResult>
    </SetMobilePhoneNumberBeginExResponse>
    ```

**Step 2: Poll SMS Status**
- **Endpoint**: `POST https://api4mini.web.money/SmsApi.asmx`
- **SOAP Action**: `http://mini.webmoney.ru/api/GetSmsStatus`
- **Purpose**: Monitor the delivery status of the SMS.
- **Response**:
    ```xml
    <GetSmsStatusResponse xmlns="http://mini.webmoney.ru/api">
      <GetSmsStatusResult>0</GetSmsStatusResult>
    </GetSmsStatusResponse>
    ```

**Step 3: Confirm Phone Number (Submit OTP)**
- **Endpoint**: `POST https://api4mini.web.money/AccountApi.asmx`
- **SOAP Action**: `http://mini.webmoney.ru/api/SetMobilePhoneNumberEndWithConfirmation`
- **Purpose**: Finalize verification by submitting the received OTP code.
- **Request Body**:
    ```xml
    <SetMobilePhoneNumberEndWithConfirmation xmlns="http://mini.webmoney.ru/api">
      <sessionId>8ca092af-98a3-4aca-b0f1-5f8d154bbe17</sessionId>
      <requestId>1423037</requestId>
      <code>25252</code>
    </SetMobilePhoneNumberEndWithConfirmation>
    ```
- **Response Body**:
    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <soap:Body>
        <SetMobilePhoneNumberEndWithConfirmationResponse xmlns="http://mini.webmoney.ru/api">
          <SetMobilePhoneNumberEndWithConfirmationResult>189</SetMobilePhoneNumberEndWithConfirmationResult>
          <confirmation>
            <Id>0</Id><Tag /><IconUrl /><Methods /><Properties /><Meta />
          </confirmation>
        </SetMobilePhoneNumberEndWithConfirmationResponse>
      </soap:Body>
    </soap:Envelope>
    ```
- **Analysis**: The response code `189` corresponds to an "Incorrect Value" error as per the `ErrorsApi.asmx` lookup.

## 4. Security & Reversing Notes

### Protocol Overview
- **SOAP/XML**: The application uses a standard SOAP 1.1/1.2 envelope.
- **Namespace**: All core logic resides in `http://mini.webmoney.ru/api`.
- **Session Management**: A UUID `sessionId` is required for almost all requests after initialization.

### Authentication (authHash)
- The `authHash` appears to be a 32-character hex string (likely MD5 or a truncated SHA).
- It is likely calculated using the user's password/secret and the `sessionId`.

### Device Metadata
- The `AuthenticateWithOptions` call sends detailed device metadata (model, vendor, OS version, app build).
- `DeviceId` (c0723dce1f9f3080b85e6629d777d3b7) is used for hardware binding.

## 5. Conclusion
### Automation Feasibility: 70%
The SOAP-based protocol is structured and relatively easy to replicate. The primary challenge for automation is the generation of the `authHash` and the consistent management of the `sessionId`. Since the payloads are cleartext XML (not encrypted at the application layer beyond TLS), standard automation tools can interact with these endpoints effectively.

### Key Blockers:
1. **authHash Logic**: Requires reverse engineering the Android APK to understand how the hash is derived from the user credentials and session ID.
2. **Device Fingerprinting**: Consistency in `DeviceId` and `Meta` information may be monitored server-side to prevent account takeover.
