# inTaxi - Research Report

## Metadata
- **Target App**: `inTaxi`
- **Package Name**: `it.ud.microtek.InTaxi`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-11`
- **Status**: `Completed`
- **HAR Files**: `inTaxi.har`

## 1. Executive Summary
The **inTaxi** Android application implements a structured multi-step registration and authentication process. The security model relies on TLS for transport layer security and a secondary layer of data obfuscation using **zlib compression** followed by **base64 encoding** for all API request and response bodies. The application utilizes a custom SVG-based captcha challenge during the SMS generation phase to prevent automated bot interactions. While the encryption layer is standard and easily reversed, the captcha provides a moderate hurdle for automation. Automation feasibility is rated as high due to the predictable API structure and simple encoding scheme.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for OTP-based registration |
| **Captcha** | Text CAPTCHA | Custom SVG-based challenge |
| **Encryption** | Zlib + Base64 | Custom data obfuscation layer |
| **Rate Limits** | Unknown | No rate limiting behavior observed in testing |
| **Endpoints Involved** | 3 | getSubscriptionConfiguration, generaCodice, completaRegistrazione |

## 3. Flow Details

### Flow 1: User Registration / Authentication

**Step 1: Get Subscription Configuration & Captcha**
- **Endpoint**: `POST /appmobile/getSubscriptionConfiguration`
- **Purpose**: Retrieve system parameters and the initial captcha challenge.
- **Notable Headers**:
    - `User-Agent`: `Dart/3.6 (dart:io)`
    - `Content-Type`: `application/x-www-form-urlencoded`
- **Request Payload (Decoded)**:
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
- **Response (Decoded)**:
    ```json
    {
      "esito": true,
      "errore": false,
      "tipo": "getSubscriptionConfiguration",
      "parametri": {
        "magic": "1c8c88995b2f6fbaab17a28ee5e22cae3b1805fe",
        "image": "<svg xmlns=\"http://www.w3.org/2000/svg\" ...>...</svg>",
        "usePhoneController": true
      }
    }
    ```
- **Analysis**: Returns a `magic` token required for the next step and an SVG image containing the text captcha.

**Step 2: Request SMS OTP**
- **Endpoint**: `POST /appmobile/generaCodice`
- **Purpose**: Submit phone number and solved captcha to trigger SMS dispatch.
<!-- Phone Number: 00393720518803 -->
- **Request Payload (Decoded)**:
    ```json
    {
      "tipo": "generaCodice",
      "oauth": "bc4ae3d0-ca17-11e3-9c1a-0800200c9a66",
      "deviceUUID": "4ec58b222c30aecd",
      "ver": "4.0.16",
      "mittente": "00393720518803",
      "magic": "1c8c88995b2f6fbaab17a28ee5e22cae3b1805fe",
      "captcha": "5957"
    }
    ```
- **Response (Decoded)**:
    ```json
    {
      "esito": true,
      "errore": false,
      "tipo": "generaCodice",
      "id": 66875566
    }
    ```

**Step 3: Verify SMS OTP & Complete Registration**
- **Endpoint**: `POST /appmobile/completaRegistrazione`
- **Purpose**: Verify the 5-digit code and submit user profile details.
<!-- OTP Code: 25888 -->
- **Request Payload (Decoded)**:
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
      "vatNumber": "63728281",
      "yearOfBirth": "1999",
      "city": "Hapur",
      "gender": "Maschio",
      "tacViewed": 1
    }
    ```
- **Response (Decoded)**:
    ```json
    {
      "esito": false,
      "errore": "Invalid registration code. Please note that each code received via SMS is valid for a maximum of 60 minutes and can only be used once.",
      "tipo": "completaRegistrazione"
    }
    ```

## 4. Security & Reversing Notes

### Encryption & Data Protection
The application uses a custom data protection layer for all API communications:
1.  **Serialization**: Data is formatted as a JSON object.
2.  **Compression**: The JSON string is compressed using the **zlib** algorithm.
3.  **Encoding**: The compressed binary data is encoded into **Base64**.
4.  **Transport**: The Base64 string is sent as the value of the `data` parameter in a standard `application/x-www-form-urlencoded` POST request.

### Captcha Implementation
The captcha is delivered as an SVG image within the `getSubscriptionConfiguration` response. This is a non-standard approach where the server sends the actual vector paths for the captcha characters. While this prevents simple image-based bot detection, the structured nature of SVG paths might actually make it easier for automated scripts to extract character features without rendering.

## 5. Conclusion

### Automation Feasibility: 85%

### Strengths:
1.  **Custom Data Encoding**: The zlib + base64 combination provides a basic layer of obfuscation that hides the payload from simple network sniffers.
2.  **SVG Captcha**: The use of SVG for captcha challenges is a clever way to avoid delivering bitmap images, making it harder for standard OCR but potentially easier for path-based analysis.

### Weaknesses:
1.  **Predictable IDs**: The `id` field in requests appears to be a simple incrementing counter or timestamp-based value.
2.  **Static OAuth Key**: The `oauth` field in the request bodies remains static across multiple requests.
3.  **No Advanced Bot Protection**: Beyond the captcha, no advanced measures like device fingerprinting (Shumei, Akamai) or request signing were observed.

**Researcher:** Deepanshu Singh
**Date:** 2026-05-11
