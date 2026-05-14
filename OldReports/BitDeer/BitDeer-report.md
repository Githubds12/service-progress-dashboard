## 1. Executive Summary
The security analysis of Bitdeer (com.bitdeer.cloud.android) focused on the authentication and registration flow. The application utilizes a phone-based OTP system reinforced with GeeTest v4 bot protection. While the initial OTP request is gated by a captcha challenge, the subsequent verification and registration steps rely on standard OTP validation. The API traffic is transmitted over HTTPS, with common fields such as `nonce`, `timestamp`, and `token` used for request tracking and integrity.

## 2. Application Information
- **App Name**: Bitdeer
- **Package Name**: **`com.bitdeer.cloud.android`**
- **Version**: **`3.10.0`**
- **Main Host**: **`galaxy.bitdeer.tech`** / **`galaxy.bitdeer.com`**

## 3. Authentication Flow Analysis
The authentication process consists of three primary stages: captcha verification, OTP delivery, and account creation/login.

### 3.1 Captcha Challenge
Before an OTP can be requested, the client must solve a **GeeTest v4** challenge.
- **Endpoint**: **`https://galaxy.bitdeer.tech/api/uc/geetest/form`**
- **Purpose**: Retrieves the captcha configuration and **`lot_number`**.

### 3.2 Requesting SMS OTP
Once the captcha is solved, the client sends the verification data to the server.
- **Endpoint**: **`https://galaxy.bitdeer.tech/api/user/passport/captcha`**
- **Method**: **`POST`**
- **Payload Structure**:
```json
{
  "identifier": "**91-8791267460**",
  "license": "1409609154",
  "type": 1,
  "verify_data": {
    "captcha_id": "adf6f520763439fd58ff8ba763e448be",
    "captcha_output": "...",
    "gen_time": "1777179604",
    "lot_number": "...",
    "pass_token": "..."
  },
  "common": { ... }
}
```

### 3.3 OTP Verification & Registration
The application verifies the code and proceeds to register the user.

#### A. OTP Verification (Check)
- **Endpoint**: **`https://galaxy.bitdeer.tech/api/user/passport/registerCheck`**
- **Method**: **`POST`**
- **Request Trace**:
```json
{
  "captcha": "**806809**",
  "identifier": "**91-8791267460**",
  "type": 1,
  "common": {
    "channel": "2",
    "device": "google_Pixel 7",
    "deviceip": "10.72.156.144",
    "language": "en_US",
    "nonce": "epjmAT1QN8egsII8",
    "platform": "android",
    "sdk": "15",
    "timestamp": "1777179637865",
    "timezone": "GMT+05:30",
    "timezone_id": "Asia/Kolkata",
    "token": "bf8ac7b5-ffb8-4671-a206-9810ca2d4025",
    "version": "3.10.0"
  }
}
```
- **Response Trace**:
```json
{
  "code": 0,
  "data": {},
  "msg": "success",
  "timestamp": 1777179638,
  "trace_id": "7bcc91287ec0d9dc5cf8139db17f789a",
  "url": ""
}
```

#### B. Registration Submission
- **Endpoint**: **`https://galaxy.bitdeer.tech/api/user/passport/register`**
- **Method**: **`POST`**
- **Request Trace**:
```json
{
  "captcha": "**806809**",
  "identifier": "**91-8791267460**",
  "password": "wE7_axv2$bXme-a",
  "type": 1,
  "common": {
    "channel": "2",
    "device": "google_Pixel 7",
    "deviceip": "10.72.156.144",
    "language": "en_US",
    "nonce": "IB0I4IOt5B3MCo8d",
    "platform": "android",
    "sdk": "15",
    "timestamp": "1777179653539",
    "timezone": "GMT+05:30",
    "timezone_id": "Asia/Kolkata",
    "token": "bf8ac7b5-ffb8-4671-a206-9810ca2d4025",
    "version": "3.10.0"
  }
}
```
- **Response Trace**:
```json
{
  "code": 0,
  "data": {
    "illegalNick": 0,
    "last_login_time": 0,
    "refresh_token": "59f4d28212073244b1d5dae9de02a9c7",
    "session": "jFG03krkylaA1w7H5llOd2IYgnO3k9sirW1BfQDw264nRKVElJpe10NBmpmW1CKI6FKQJBX2YRaNxi4nzhfMLkwPiTP9mB4Yrxz/jsJULvSZvxuEU3DjZonc8efrdqGqc4DBDQtkw2rR2pzYGPahQWkHOobv+K3svIep39/KCndMQLJKv4WVhbwyIJqw3iAmQPVfDXspYXc7EbSJAOh0eQ+enqB00Wj8W7aiCGS0tMgscUhHQhS4uIk4Xf+4Pjj59VkosMZbCOejgTufk1PrPRW5cokp/0vKtoec/c298EzEUxH608ny1YFoWBKmYYixbrRzTnbkIgUSyMqILHSOqghluMYJkDct1IrG80FHd8aSc0eN3NE5uLbFQZXUPhyUDN10gGLW6V1a9GhNWz6YMYuWlJ5UDLbZfeNEGED8eJmPy2It1RxYldr37Z5jrt+JcUbtLTvfxf6LPW+CChZDDSeq6pEhMUxGZg4ne6a+DQV0dlhTjB9leyORAHYWjF/ETksgxK6QRolOJYTDSM551uryMr5khnNO6aNZZ51VxCOySJ0vCEmRSQrzU2PobH9VA3FYBxen4ouo4Z1jVZ1D4ggdvOnsjM4LQMDq7sBbL9DqzPsN3a1eZh1NoZcvlatItObmhZ3a9yVvQrKqMP0lPRHgMUi3Z85dbIbNIhzl6Gf1v3YivmKLFHEH0Cq/JlYdJtxtq3uAOzr3ryGnyhsOddAWvdJH0IpIeSrRNa5vPpuovnfAhZV0y+m5R9LxqzbBc0HR5ZEW3wCWYq9D+RjXHeoP5cHdJP4P/HYobau5i14dCMN0kxCWNuPDjYwrYwmKKN5+4uaHg8t2MKARiELF1UvJwm4TC75Nt1L9v1ZquVoXtNWfRxQDMHzHVr8N8jip",
    "session_expire": 1777611653
  },
  "msg": "success",
  "timestamp": 1777179653,
  "trace_id": "377d8119a516f4027f7639471a1eb672",
  "url": ""
}
```

## 4. Security Mechanisms
- **Bot Protection**: GeeTest v4 is implemented on the OTP request endpoint to prevent automated SMS bombing.
- **Request Integrity**: Every request includes a `common` block with a `nonce`, `timestamp`, and `token`. These are likely used for backend validation and replay protection.
- **TLS/SSL**: All communication is performed over encrypted channels (HTTPS).

## 5. Vulnerability Assessment
- **Rate Limiting**: While GeeTest prevents high-frequency automated requests, there were no obvious backend rate limits observed beyond the captcha requirement.
- **Session Management**: The `session` token returned upon successful registration is long-lived and includes multiple encrypted/encoded segments.

## 6. Conclusion
Bitdeer demonstrates a robust authentication architecture by integrating third-party bot protection (GeeTest) into its critical SMS delivery flow. The implementation of request metadata (nonces and timestamps) further enhances the security posture against simple replay attacks.
