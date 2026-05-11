# Reconnaissance Report - inTaxi (it.ud.microtek.InTaxi)

## 1. Executive Summary
The **inTaxi** Android application was analyzed to document its authentication and registration workflow. The application uses a multi-step registration process involving an initial configuration request that provides a custom SVG-based captcha, followed by an SMS OTP request and verification. The network traffic is secured using TLS, and the payload data is further protected by **zlib compression** and **base64 encoding**. The overall security implementation is standard for the industry, though the custom captcha implementation may be susceptible to automated solving via OCR.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for user authentication and registration |
| **Captcha** | Text CAPTCHA (Distorted Characters) | Custom SVG-based captcha returned in the initial config request |
| **Encryption** | Zlib compressed + Base64 encoded JSON | All POST payloads and responses are compressed and encoded |
| **Rate Limits** | Unknown | No explicit rate limiting behavior observed in the captured traces |
| **Endpoints Involved** | 3 | `/appmobile/getSubscriptionConfiguration`, `/appmobile/generaCodice`, `/appmobile/completaRegistrazione` |
| **Bot Protection** | Custom SVG Captcha | Implemented during the SMS request phase |

## 3. Authentication Flow
The authentication flow consists of three primary steps: initialization with captcha retrieval, SMS code generation, and registration completion.

### Step 1: Initial Configuration and Captcha Retrieval
The application first calls the `getSubscriptionConfiguration` endpoint to retrieve operational parameters, including a `magic` token and an SVG image for the captcha challenge.

**Endpoint:** `https://api-intaxi.taximobile.it/appmobile/getSubscriptionConfiguration`
**Method:** `POST`

**Request Headers:**
```http
user-agent: Dart/3.6 (dart:io)
content-type: application/x-www-form-urlencoded; charset=utf-8
host: api-intaxi.taximobile.it
```

**Request Body (Decoded):**
```json
{
  "tipo": "getSubscriptionConfiguration",
  "oauth": "bc4ae3d0-ca17-11e3-9c1a-0800200c9a66",
  "deviceUUID": "4ec58b222c30aecd",
  "device_info": {
    "isVirtual": true,
    "manufacturer": "Google",
    "model": "Pixel 7",
    "platform": "Android",
    "uuid": "4ec58b222c30aecd",
    "version": "15"
  },
  "ver": "4.0.16",
  "lang": "en",
  "tipoApp": "INTAXI"
}
```

**Response Body (Decoded):**
```json
{
  "esito": true,
  "errore": false,
  "tipo": "getSubscriptionConfiguration",
  "parametri": {
    "magic": "1c8c88995b2f6fbaab17a28ee5e22cae3b1805fe",
    "image": "<svg ...>...</svg>",
    "usePhoneController": true
  }
}
```

### Step 2: SMS OTP Request (Phone Number Submission)
The user enters their phone number and solves the captcha. This data is sent back to the server to trigger the SMS dispatch.
<!-- Phone Number: 00393720518803 -->

**Endpoint:** `https://api-intaxi.taximobile.it/appmobile/generaCodice`
**Method:** `POST`

**Request Body (Decoded):**
```json
{
  "tipo": "generaCodice",
  "oauth": "bc4ae3d0-ca17-11e3-9c1a-0800200c9a66",
  "deviceUUID": "4ec58b222c30aecd",
  "ver": "4.0.16",
  "lang": "en",
  "tipoApp": "INTAXI",
  "mittente": "00393720518803",
  "magic": "1c8c88995b2f6fbaab17a28ee5e22cae3b1805fe",
  "captcha": "5957"
}
```

**Response Body (Decoded):**
```json
{
  "esito": true,
  "errore": false,
  "tipo": "generaCodice",
  "id": 66875566
}
```

### Step 3: Registration Completion (OTP Verification)
Finally, the user submits the 5-digit OTP code received via SMS along with their personal details to complete the registration.
<!-- OTP Code: 25888 -->

**Endpoint:** `https://api-intaxi.taximobile.it/appmobile/completaRegistrazione`
**Method:** `POST`

**Request Body (Decoded):**
```json
{
  "tipo": "completaRegistrazione",
  "oauth": "bc4ae3d0-ca17-11e3-9c1a-0800200c9a66",
  "deviceUUID": "4ec58b222c30aecd",
  "ver": "4.0.16",
  "mittente": "00393720518803",
  "codice": "25888",
  "nomeCompleto": "Deepanshu Singh",
  "email": "deepanshusinghdigitalheroes@gmail.com",
  "gender": "Maschio",
  "tacViewed": 1
}
```

**Response Body (Decoded):**
```json
{
  "esito": false,
  "errore": "Invalid registration code. Please note that each code received via SMS is valid for a maximum of 60 minutes and can only be used once.",
  "tipo": "completaRegistrazione"
}
```

## 4. Conclusion
The **inTaxi** application implements a robust but automatable authentication flow. The use of zlib compression for payloads adds a minor layer of complexity for analysis but is easily handled by standard libraries. The custom SVG captcha is the primary bot protection mechanism; however, because it is delivered as structured SVG paths, it could potentially be solved using geometric analysis or rendered and passed to an OCR engine. The application correctly validates registration codes and handles errors gracefully. Overall, the automation feasibility is rated as **High (> 70%)** due to the predictable nature of the API endpoints and the simplicity of the encoding scheme.

**Researcher:** Deepanshu Singh
**Date:** 2026-05-11
