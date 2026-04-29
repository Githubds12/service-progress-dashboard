# PaySend - Research Report

## Metadata
- **Target URL/App**: `paysend.com` / `com.paysend.app`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-29`
- **Status**: `Completed`
- **HAR Files**: `PaySend.har`

## 1. Executive Summary
PaySend implements a hybrid API architecture using both JSON and XML over HTTPS. The registration process involves initializing a session with a phone number and email via a JSON endpoint, followed by OTP verification via an XML-based endpoint. The system uses session identifiers (`balId`) and authentication keys (`authKey`) for state management. Cloudflare is implemented for infrastructure protection, but no active Captcha challenges or custom payload encryption were observed in the registration flow. Automation feasibility is assessed as High.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | primary channel for OTP |
| **Captcha** | undefined | No captcha challenges observed during testing |
| **Encryption** | None | Plain JSON/XML payloads over HTTPS |
| **Rate Limits** | Unknown | No rate limiting behavior was observed during testing |
| **Endpoints Involved** | 2 | `/api/json/registration`, `/api/xml.jsp` |
| **Bot Protection** | Cloudflare | Cloudflare protection implemented on the API infrastructure |

## 3. Flow Details

### Flow 1: Registration (Signup)

**Step 1: Phone Number Submission**
- **Endpoint**: `POST https://api.paysend.com/api/json/registration`
- **Purpose**: Initialize registration and request OTP
- **Request**:
    ```json
    {
      "client_id": "PAYSEND_MOBILE_APP",
      "secret": "12345678",
      "phone": "393519566477",
      "email": "deepanshusinghdigitalheroes@gmail.com",
      "marketing_opt_in": "0"
    }
    ```
- **Response**:
    ```json
    {
      "balId": "84-254275832719555",
      "authKey": "5856dae3bc4b20ce2de68ed809cad65166d6030b27cf035d74dd041509a4a9b7da14649766966d230e33086315ba4f54c33988de6b5e6ba0a9a4902d95482fdf",
      "authType": "REGTOKEN",
      "alreadyRegistered": false,
      "countryId": "380",
      "code": 0,
      "sms_confirm": {
        "created": "2026-04-29T05:11:48.60Z",
        "expired": "2026-04-29T05:21:48.60Z",
        "confirm_type": "REGISTER_WALLET",
        "object_id": "84-254275832719555",
        "lifetime": 10,
        "resend_time": 45,
        "new_smscode_enabled": true,
        "flashcall": false,
        "delivery_channel": "SMS"
      }
    }
    ```

**Step 2: OTP Submission**
- **Endpoint**: `POST https://api.paysend.com/api/xml.jsp`
- **Purpose**: Verify the SMS code
- **Request**:
    ```xml
    <request>
       <auth>
          <client_software>Android v4.9.10</client_software>
          <id>84-254275832719555</id>
          <key>5856dae3bc4b20ce2de68ed809cad65166d6030b27cf035d74dd041509a4a9b7da14649766966d230e33086315ba4f54c33988de6b5e6ba0a9a4902d95482fdf</key>
          <lang>en</lang>
          <store>google</store>
          <auth_type>REGTOKEN</auth_type>
          <sec_uuid>a6e33d486bfb5b2e</sec_uuid>
       </auth>
       <extra name="confirm_type">REGISTER_WALLET</extra>
       <extra name="object_id">84-254275832719555</extra>
       <extra name="code">111122</extra>
       <extra name="appsflyer_id">1777439440919-5500968674385231351</extra>
       <extra name="ga_instance_id">b1ffcc5445f6dcecebf211e6685da26b</extra>
       <request_type>submit_smsconfirm_code</request_type>
    </request>
    ```
- **Response**:
    ```xml
    <response>
    	<result code="43" message="Incorrect code" />
    </response>
    ```

## 4. Security & Reversing Notes

### API Architecture
PaySend uses a dual-protocol API:
1. **JSON API**: Used for initial registration steps and specific wallet operations.
2. **XML API**: A legacy-style SOAP-like API used for auth verification, resending codes, and profile management.

### Session Management
The platform relies on two main tokens returned after phone submission:
- `balId`: Acts as a session or user identifier (e.g., `84-254275832719555`).
- `authKey`: A 128-character hex string used for signing subsequent XML requests.

### Bot Detection
- **Cloudflare**: Detectable via `cf-ray` and `cf-cache-status` headers.
- **Fingerprinting**: The app sends `sec_uuid` (likely a device UUID) and integration IDs like `appsflyer_id` and `ga_instance_id` to track the source of the registration.

## 5. Conclusion

### Automation Feasibility: High (> 70%)

### Detailed Conclusion:
The automation feasibility for PaySend is high due to the lack of complex bot protection mechanisms like Captcha or payload encryption. The API follows a predictable flow, transitioning from JSON to XML. While the `authKey` is required for OTP submission, it is provided directly by the server in the first step. The presence of Cloudflare suggests that IP-based rate limiting or WAF rules might be active, but no behavioral blockers were identified during the analysis. The integration of device identifiers (`sec_uuid`) indicates that maintaining consistent device state is necessary for successful automation.
