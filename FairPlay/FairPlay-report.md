# FairPlay (poker21.fairplaycard.royalclub) Security Reconnaissance Report

## 1. Executive Summary
The **FairPlay** application (`poker21.fairplaycard.royalclub`) is a mobile gaming platform that utilizes a centralized API for user authentication and session management. The application's security architecture relies heavily on a custom encryption and signing mechanism for all API requests and responses. All sensitive communications, including phone number submission and registration, are transmitted as hex-encoded encrypted payloads over HTTPS. While the application implements a `sign` field to ensure data integrity, the absence of standard third-party bot protection (like reCAPTCHA or Cloudflare Turnstile) suggests a reliance on proprietary obfuscation.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | OTP-based verification for account registration. |
| **Captcha** | undefined | No third-party captcha challenges were observed in the traffic. |
| **Encryption** | Custom Hex-Encoded Binary | Payloads are transmitted as encrypted hex strings with an MD5-style signature. |
| **Rate Limits** | Unknown | No explicit rate-limiting errors (HTTP 429) were captured. |
| **Endpoints Involved** | 2 | `/app/sendPhoneMsg`, `/auth/playerRegister` |
| **Bot Protection** | Custom Encryption/Signing | Proprietary signing and encryption mechanism on the `api.bnxdw4a.com` host. |

## 3. Technical Findings
### 3.1 Authentication Flow
The authentication process follows a standard two-step SMS verification flow:
1.  **SmsRequest**: The client sends an encrypted payload to the `/app/sendPhoneMsg` endpoint containing the user's mobile number.
2.  **VerifyOtp**: After receiving the SMS, the client submits the OTP and registration details to `/auth/playerRegister`.

### 3.2 Encryption & Integrity
Each request contains three primary fields:
-   `data`: An encrypted hex string containing the actual request parameters (phone, OTP, device info).
-   `sign`: A cryptographic signature (likely MD5) used to verify that the payload has not been tampered with.
-   `dateTime`: A Unix timestamp (milliseconds) used for request freshness.

## 4. API Traces

### Step 1: Request SMS Verification
-   **Endpoint**: `POST https://api.bnxdw4a.com/app/sendPhoneMsg`
-   **Method**: `POST`
-   **Purpose**: Trigger the delivery of an OTP to the user's mobile device.

**Request Traces**:
```json
{
  "url": "https://api.bnxdw4a.com/app/sendPhoneMsg",
  "method": "POST",
  "headers": {
    "Host": "api.bnxdw4a.com",
    "Content-type": "application/json",
    "User-Agent": "Mozilla/5.0 (Linux; Android 15; Pixel 7 Build/AP4A.250205.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/147.0.7727.138 Mobile Safari/537.36",
    "X-Requested-With": "poker21.fairplaycard.royalclub"
  },
  "body": {
    "data": "FD5ACE5FBAAEFF8E1A44EA30CE48D80760F76D42C8221730DCCB33944DE9E157DA5A01DE01B55F41EA10DD9CBE4B031C",
    "sign": "4d961c5ad3b0239e534f86215a39d14c",
    "dateTime": "1778829941565"
  }
}
```

**Response Traces**:
```json
{
  "code": 200,
  "msg": "",
  "data": "5E7C42717DCA08F97126E227FFF1A40315E6EC19AF6731D82FEAF76816A27776AC00D9671B765617F62A723FB8E03B0E05C6A9CA9664A5C0221C0F87B36D9C5F1C1DB87B647D008B14F225FF6D735256A57C148BDAD3D31675B777289524AC7A",
  "dateTime": 1778829942132
}
```

### Step 2: Register/Verify OTP
-   **Endpoint**: `POST https://api.bnxdw4a.com/auth/playerRegister`
-   **Method**: `POST`
-   **Purpose**: Finalize registration by submitting the received OTP and setting a password.

**Request Traces**:
```json
{
  "url": "https://api.bnxdw4a.com/auth/playerRegister",
  "method": "POST",
  "headers": {
    "Host": "api.bnxdw4a.com",
    "Content-type": "application/json",
    "X-Requested-With": "poker21.fairplaycard.royalclub"
  },
  "body": {
    "data": "0C1768830C101729FDB304D2FD02883D63E4D330D81DD743B76ECDE689368C17A08CB60EB91913C5BD2DBF0C006977CBB6A36B71B32FFEFEEBA540A79A13B570C4690104CE8E7D70DC1D1A3D98D89DFF9320645F3531F67BC9D5D7B7B771B7CCC97E232C887D3401E38A307368659B587101FFCE1983966E623CBE7414C06FD8292AAE1F5AC3E924E70107A1551C2255CD7815CB181CE285FDE69A23E6424B1D7B0F33AC1314CA62FAE1D67DA2836A74C13E5B25604F458D7AD4D4078EB1AD537047F2E1C955DA626D18E63B188035FF936BC8C8B55BBAF5C71117790413B7AA539AE8EBD849E187E98E0DAB5D5B4B6C138FC781CEC877D5C2F1008FF012D71480C2EB4645F53FD00CE7F2325AD586D6BB457018F5F47C96B22E1AEF6E37B05EF4430C1DF861BB803DC9C7DC23DDABE65B20C927FB22C0BF07B469E18C92D1031D8C7E46E1A09B16A86908A4E30623B30B339DB7BDE325C5BB242D60201094FA0EAF56E8C06B79FC4FEC7BFD7BEEC1794890C1F6E3C416661D3B0B24F3318E417A1047CABF9B19B4457951D7353916DB04642CE8C8CC352FBD9E6FBBE18B5B65FC4D1EE4E93B4154B6397C1BA8A3D38A8886AF9DC48E8F3A54EE4E7A602794F27607255A1DB9521D2B41B05A4DB08D632CCC0132467D2CA3678DB13AAA9BDA5D666ACBC213326E21B0AA4537BE0A3B965EDEEF1AEC9F35A8CF0651A7EBCCE0403CCA88563D5E00C70E103C34370DA1CDE22BC2FB7DBEE0FC8CC6CDD2E51D6F05C866757CF67FA65F2C5092851B8E644A36AE6268AC18A83EAC83BADC0284B38066899E39DA8462DF1A88B6F67B66AFA569E223BC4BDEC65972326991B39BDFF5549D4BE76017462BAFB49B025439F69079580D9C41718E1A1942BCD5DA139C650824CD243A24446AF3D33927F5B741699BC83214AC07A73DD08D1CB44537DA05",
    "sign": "b24ecba7102f8ac34cfac1417fa66a26",
    "dateTime": "1778830025707"
  }
}
```

**Response Traces**:
```json
{
  "msg": "",
  "code": 500,
  "data": "5E7C42717DCA08F97126E227FFF1A403C80D545C833B273255852AA2CC1A5ED839CCC44DD7BE732AFF22A8A4C05207B0B7F5D58F8B66B143AFFCF087018173F21E65452EC141A3126345435D1350628BA2236FB78047E505B3BE81F3B795DD09"
}
```

## 5. Conclusion
The **FairPlay** application implements a robust, albeit custom, security model using encrypted payloads and cryptographic signing. The primary challenge for automation lies in reversing the hex-encoded encryption layer used on the `api.bnxdw4a.com` endpoints. While the application lacks standard bot protection mechanisms like reCAPTCHA, the custom signing process acts as a significant barrier. 

**Automation Feasibility: Medium (50%)**
Full automation is possible if the client-side encryption logic (found in the application's JavaScript assets) can be successfully reversed. The predictable nature of the two-step OTP flow simplifies the logical implementation once the payload structure is deciphered.

**Recommendations**:
-   Decompile the APK to identify the specific encryption algorithm (likely AES or a custom XOR cipher).
-   Analyze the JavaScript bundle at `https://www.bg678s.com/static/js/index.js` for signing logic.
-   Implement a proxy to handle the real-time signing of requests if the algorithm uses rotating keys.
