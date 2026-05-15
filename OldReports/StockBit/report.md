# Reconnaissance Report - StockBit

## Service Information
- **Service Name:** StockBit
- **Package Name:** `com.stockbit.android`
- **Version:** `3.21.2`
- **Endpoint:** `https://exodus.stockbit.com`

## Technical Analysis

### Authentication Flow
The application uses a multi-step registration/login process involving email verification followed by phone number verification.

#### 1. Email Verification Trigger
- **URL:** `https://exodus.stockbit.com/registration/v3/check/email`
- **Method:** `POST`
- **Request Body:**
```json
{
  "email": "deepanshusinghdigitalheroes@gmail.com",
  "key": "",
  "type": 1
}
```
- **Response Body:**
```json
{
  "message": "Otp email verification successfully sent ",
  "data": {
    "send_email": false,
    "status": "not_verified",
    "key": "Y2So4DXRkIur6a2z",
    "valid": false
  }
}
```

#### 2. Email OTP Verification
- **URL:** `https://exodus.stockbit.com/registration/v3/otp/email`
- **Method:** `POST`
- **Request Body:**
```json
{
  "key": "Y2So4DXRkIur6a2z",
  "otp": "9260"
}
```
- **Response Body:**
```json
{
  "message": "Verify otp code successful",
  "data": {
    "send_email": false,
    "status": "valid",
    "key": "Y2So4DXRkIur6a2z",
    "valid": true,
    "state": "STATE_CHECK_EMAIL_REGISTER"
  }
}
```

#### 3. SMS Verification Trigger
- **URL:** `https://exodus.stockbit.com/registration/v3/check/phone`
- **Method:** `POST`
- **Request Body:**
```json
{
  "channel": "CHANNEL_SMS",
  "code": "39",
  "key": "Y2So4DXRkIur6a2z",
  "phone": "3720514424"
}
```
- **Response Body:**
```json
{
  "message": "A verification code has been sent to your number ",
  "data": {
    "send_phone": true,
    "status": "not_verified",
    "key": "Y2So4DXRkIur6a2z",
    "valid": true
  }
}
```

#### 4. SMS OTP Verification
- **URL:** `https://exodus.stockbit.com/registration/v3/otp/phone`
- **Method:** `POST`
- **Request Body:**
```json
{
  "key": "Y2So4DXRkIur6a2z",
  "otp": "3636",
  "player_id": "80468e4b037310fb64516bb894a5be9ffb59940dad3cd8f2ce7a1be1297ceacf",
  "pushnotif_id": "80468e4b037310fb64516bb894a5be9ffb59940dad3cd8f2ce7a1be1297ceacf"
}
```
- **Response Body (Invalid Example):**
```json
{
  "message": "The code you entered is invalid",
  "error_type": "INVALID_PARAMETER"
}
```

## Key Findings
- The service uses the **Exodus** backend for registration.
- SMS requests are routed through `registration/v3/check/phone`.
- The `key` parameter is mandatory and tracks the session state across email and phone verification steps.

## Status
- **OTP Delivery:** Functional
- **API Security:** TLS 1.3, standard header authentication.
- **Bot Detection:** Sentry and Flipt integration for feature flagging and crash reporting.
