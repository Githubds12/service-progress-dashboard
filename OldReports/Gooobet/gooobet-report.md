# Gooobet Security Analysis Report

## 1. Executive Summary
The security analysis of the Gooobet Android application (org.gooobet.client, version gooobet-v253.0.1) reveals a sophisticated registration and authentication flow integrated with a custom bot protection mechanism (HD-API). The application utilizes a multi-step process for account creation, involving a captcha acquisition step followed by a complex "hd-api/verify" challenge that generates a security token. This token is mandatory for the registration request. Subsequent to registration, a two-factor authentication (2FA) process via SMS is triggered. While the API structure is clear, the presence of the HD-API sensor data collection in the verification step significantly complicates automation feasibility.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for OTP verification |
| **Captcha** | Custom | HD-API Bot Protection with "OpenFrame" challenge |
| **Encryption** | None | Standard JSON payloads (except encrypted HD-API body) |
| **Rate Limits** | Unknown | No rate limiting behavior was observed during testing |
| **Endpoints Involved** | 5 | `/Account/v1.1/Mb/Register/Registration`, `/captcha/v1/GetCaptcha`, `/hd-api/verify`, `/Account/v1/SendCode`, `/Account/v1/CheckCode` |
| **Bot Protection** | HD-API | Custom bot manager implemented on verification endpoints |

## 3. Technical Analysis

### 3.1. Registration Flow
The registration process begins with fetching available fields and then acquiring a captcha identifier. A subsequent call to the `hd-api/verify` endpoint is made, which requires a large encrypted payload (sensor data) and returns a token used as `ImageText` in the final registration call.

#### Step 1: Captcha Acquisition
The app requests a captcha task for the registration method.
- **Endpoint**: `https://api.gooobet.com/captcha/v1/GetCaptcha`
- **Method**: `POST`

**Request**:
```json
{
  "AppGuid": "d718f045e1ce41e1_2",
  "Language": "en_GB",
  "Method": "Registration",
  "VersionGen": 2,
  "Login": ""
}
```

**Response**:
```json
{
  "id": "e4de21aa-c83b-461a-900c-10471759c38e",
  "tasks": [
    {
      "image": "OpenFrame",
      "count": 0,
      "letCount": 0,
      "type": 4
    }
  ]
}
```

#### Step 2: Bot Protection Verification (HD-API)
The app sends sensor data to the `hd-api/verify` endpoint to obtain a validation token.
- **Endpoint**: `https://api.gooobet.com/hd-api/verify`
- **Method**: `POST`

**Request Headers**:
```http
Content-Type: text/plain;charset=UTF-8
X-Captcha-Token: Z4Czz/ML5rtufpaT2ySt+eNJHw02XnP5IC0b+ANINJYhltAa2phq51ftl25RiS/9x69Fzv6k0eO2GpH/9IxWoOHc/Iw+BtTaJT5Jb9UBXCfCt0l1JxhvJOPGqVH5Qe/WddKBG6B1QzBdKvEu7P5PACXdzZSWajEa3YIHh9c832rcZa+V7ad9BFe1csPUrDzSYQIf1LasFuLPjbEjcslIPdDSHBfZV1snP8VrORY5SoTp/wS0xUj1106q5EDRxCDIv2b8NhBvKcnaKl0wdU/8MnjuRBvG4eL4VhtZrjTRPfKaDLLkvZJYE9NxSPFIMTCqn+d0GDuwUhO5FWtNM3Hxvf9wEMoBj2XscYGH1oAwcJcsRSeXKKJYH15C5/jNbSASgGc9TBAZ09IPZnaYbl95sQkSGv/CzGogTPVVP6U1Nzl+5Cj2/nYpz4vzvEItL9lx7Z3p7jBqLAn725xZkHSmR/cK31TfbQb8TlBGUKLbjKpnwQ==
X-Hd-Frame-Token: 1MTGzELeg/5M882Hs1krnj8kJYP64kAiZN7rp6MFEs4iIKIqqNye81v3Abusv/6/BtgCtd0Bj3FyKw9+ZrC7s/ZbYP4Xdw92fEUYQ4eI3yWJSE0Wa6UkmfFw6tf/QbGh9+NLVU+0LJCwy0NalXEPgk8L1GlpQek1uNB0rua6FaN0/mQyKY+9sCsMqRtQd33eAJOrzlQgWi03AQyesSOh352krQur/MuV6yK2RdsHZ3o+IZzaBxGs+dXQVp/frlf4aeYOmpdAXGpG9TACEamV4T/aTtSzDIkqM/Zm8ttxJdPF3uZ/D9bqA1kcWUg1QDMAqLwEO+WY0hmIW2n5xiKLKaHiq1GoolizWRcJlOd0rLzU/CzwuLpZgvRxMwlMo6/1z7dI8jbl0/RvZtKjURmmWhx9cBN3azohhtCUF+yAE6B5qIfjJRrVk7KziVAFfUFqLUxt84aScO7D1JJXMgTKvEK95wXD0YWyeV74VCJMFZ+xXdg+GNYyYN2wnD9m4updSn/hy50YXieoHGOibrWab/JFUQVWpoYiX4Qi3Q==
Referer: https://api.gooobet.com/hd-api/checker
```

**Response**:
```json
{
  "token": "6ur_76uArLkJH2OE689jsVdpygPvimaTAFI2v5W9PBN6hcQ-XVOWm0RDtnxOHQaGhq6aI437t85B79f52gsPCVMnP5fmY1arMdlzl-bwCGkYvnfA2Jnc7uiSV4FCMlRyrhg-hOBU0-Aq1PKXNrjzZ5GRNRVSqmxweKwW0tTRZ7mJZF6pQ6KeD3uzZngeY_35aO20akpQQUj-L5Xydl7wROI0XNVVm5xAzqQdwvS16qcRI0i0k9-b8KQO4yT9C3EvQkp51SVKuXZeGgZ9QCw5KAkNqZS7XnZHF-mwfljWiGt_AUGf8cUXmPp9OG8U3KnrkgLmjUwJ5h3SeD3C09URKi98XxpjaDocq9xJnlelhbmHDWsgP_0aJzRnAUiidmBRbd24os9jgOOZcDQPOdFoWVp97qlnLH2iFQDqJnxX5ZM7X75Yp0dksx35N7pQUIBH4aH6UfCV3NgvFahtuU2ZGtXCrNmsVYk262bRaQkoAz..."
}
```

#### Step 3: Registration Submission
The user's details and the HD-API token are submitted to create the account.
- **Endpoint**: `https://api.gooobet.com/Account/v1.1/Mb/Register/Registration`
- **Method**: `POST`

**Request Body**:
```json
{
  "CaptchaId": "e4de21aa-c83b-461a-900c-10471759c38e",
  "ImageText": "6ur_76uArLkJH2OE689jsVdpygPvimaTAFI2v5W9PBN6hcQ-XVOWm0RDtnxOHQaGhq6aI437t85B79f52gsPCVMnP5fmY1arMdlzl-bwCGkYvnfA2Jnc7uiSV4FCMlRyrhg-hOBU0-Aq1PKXNrjzZ5GRNRVSqmxweKwW0tTRZ7mJZF6pQ6KeD3uzZngeY_35aO20akpQQUj-L5Xydl7wROI0XNVVm5xAzqQdwvS16qcRI0i0k9-b8KQO4yT9C3EvQkp51SVKuXZeGgZ9QCw5KAkNqZS7XnZHF-mwfljWiGt_AUGf8cUXmPp9OG8U3KnrkgLmjUwJ5h3SeD3C09URKi98XxpjaDocq9xJnlelhbmHDWsgP_0aJzRnAUiidmBRbd24os9jgOOZcDQPOdFoWVp97qlnLH2iFQDqJnxX5ZM7X75Yp0dksx35N7pQUIBH4aH6UfCV3NgvFahtuU2ZGtXCrNmsVYk262bRaQkoAz...",
  "Data": {
    "RegType": 2,
    "CountryId": 71,
    "CurrencyId": 99,
    "Phone": "8319350528",
    "RulesConfirmation": 1,
    "SharePersonalDataConfirmation": 1,
    "TimeZone": "5.3"
  }
}
```
<!-- Phone Number is 8319350528 -->

**Response**:
```json
{
  "Success": true,
  "Value": {
    "Auth": {
      "CodeType": "Sms",
      "Guid": "7ade1410-fb18-4097-bdde-1a7dd7180c23",
      "Token": "6501516D81224ACFB8D90F3F6635C8DF",
      "Hash": "7ade1410-fb18-4097-bdde-1a7dd7180c23|6501516D81224ACFB8D90F3F6635C8DF"
    },
    "CodeTypes": [
      "Sms"
    ]
  }
}
```

### 3.2. OTP Flow

#### Step 4: SMS OTP Request
The app triggers the SMS OTP for the newly created account.
- **Endpoint**: `https://api.gooobet.com/Account/v1/SendCode`
- **Method**: `POST`

**Request Body**:
```json
{
  "Data": {},
  "Auth": {
    "Guid": "7ade1410-fb18-4097-bdde-1a7dd7180c23",
    "Token": "6501516D81224ACFB8D90F3F6635C8DF"
  }
}
```

**Response**:
```json
{
  "Success": true,
  "Value": {
    "RAS": 300,
    "Auth": {
      "Guid": "7ade1410-fb18-4097-bdde-1a7dd7180c23",
      "Token": "A4695C0D8B3E41D79AD01E533DB11971",
      "Hash": "7ade1410-fb18-4097-bdde-1a7dd7180c23|A4695C0D8B3E41D79AD01E533DB11971"
    }
  }
}
```

#### Step 5: OTP Verification
The user submits the received OTP code.
- **Endpoint**: `https://api.gooobet.com/Account/v1/CheckCode`
- **Method**: `POST`

**Request Body**:
```json
{
  "Data": {
    "Code": "3333"
  },
  "Auth": {
    "Guid": "7ade1410-fb18-4097-bdde-1a7dd7180c23",
    "Token": "A4695C0D8B3E41D79AD01E533DB11971"
  }
}
```
<!-- OTP Code is 3333 (Attempted) -->

**Response**:
```json
{
  "Success": false,
  "Error": "Verification code is incorrect.",
  "ErrorCode": 100371
}
```

## 4. Conclusion
The Gooobet application implements a robust registration flow protected by HD-API sensor-based bot detection. The requirement for a multi-kilobyte encrypted payload in the `hd-api/verify` step makes standard HTTP automation extremely difficult, as this payload likely contains device-specific identifiers and environmental checks. While the subsequent SMS OTP flow is standard, the initial registration hurdle is significant.

**Automation Feasibility: Low < 40%**
The main bottleneck is the HD-API bot protection. Without a way to generate or validly replay the sensor data payload, automated account creation is not feasible through direct API interaction. Recommendations include further research into the HD-API payload structure or using an automated browser/emulator environment to handle the challenge.

Researcher: Deepanshu Singh
Date: 2026-04-29
