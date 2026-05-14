# Paybis Security & Authentication Analysis

## Metadata
- **Target URL/App**: `com.paybis` / `paybis.com`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-30 10:10`
- **Status**: `Completed`
- **HAR Files**: `Paybis.har`

## 1. Executive Summary
Paybis (com.paybis) is a highly secured cryptocurrency exchange platform. The authentication flow involves an initial email/session setup followed by phone number registration and OTP verification. The platform implements multi-layered bot protection, including **Cloudflare** for edge security and **reCaptcha v3** for validating the SMS request (`/register`) action. Automation is considered high-friction due to the requirement of a valid reCaptcha token for triggering the OTP.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | 6-digit OTP code |
| **Captcha** | reCaptcha v3 | Required for triggering SMS via `/register` |
| **Encryption** | Standard TLS | No proprietary payload encryption observed |
| **Rate Limits** | Dynamic | `canBeResentAfter` and `expirationTime` provided in response |
| **Endpoints Involved** | 2 | `/register` (SMS trigger), `/confirm` (OTP verify) |
| **Bot Protection** | High | Cloudflare WAF + reCaptcha v3 |

## 3. Flow Details

### Flow 1: Registration & SMS Verification

**Step 1: Request SMS OTP**
- **Endpoint**: `POST /public/authentication-service/v1/session/{sessionId}/register`
- **Purpose**: Triggers an SMS OTP to the provided phone number.
- **Request Payload**:
    <!-- Phone Submission -->
    ```json
    {
      "phone": "+393518085457",
      "locale": "en",
      "reCaptcha": "0cAFcWeA5XLqI6hKgqiZplAa4HZKmiElSP_sQ0rS-7Zg6A3iEc7_l572I7Z9T--aJCKDELz7XjoqE5uinm7rCe3sTAm-DM1x3r6LWKftg1gI239TCyjwjEWXu1O63E9vHWILlqhTH4HYMYpFGocHU_gUN1OsSHiV6Kc2FMcA5OOx2wWsHd3PcwWCM-Vz-wKuBocfOi7KIcbNCLnbMzqVfWHu1HRN_kjTptQF8efr_-aivINzD69fs8vLKhkO0KRqpmt79nh4UJfVz_kxwFJjjAHvrl8kTpxSgg_GXCx4tQ7vZKRFCZSKA8gO-mFIy8RIrBp6xaNA0LK6e3zdiHvuUDvub3WvnUE5LoNoSzkzZxB6VC3OXbIO81tH1z51l3lsQOB221U1g1tHQSx0xDHK84BqUWjSwSfbzCqXOLr89ljp90AxrcAf5re3uNcUxKAUrw0N9Jd4xfJOIhz-NxuTk9doIOi4mdGw_ZOstqnHQlIYrRLONyFgI-4hyjoP0Z8FgyFezW6p29E8lQovNqpK9l4VutCqS-hg4oFbpQ7H_6bL2Kb2ZjQbEvoNGoK1oGsHHXBuRa-Nt6TRG24qnevAmlBukyG4Qm_SctCt4bDdVTeWWlC9pi4gdT8pnT63fV_1Vz7hgpiiGywbDIcNd7eBkj86dITMpiSkOe2AMlwOj1KfHc5K1f4yCzGyzDJJIwiLreCixonf8BXcR9H343qEk5cv3S4vQhlIkrBPxLyAOX9hG_2UpwO9PrNi9XR-8Y17rle9FMTvZXsoT16W3FJd3mFMOZKBjMtxZXluUr8-DYXxMkIJLN2pRmcb0I1GLxv0_X12AdYPSpoDic9uS-ucp4gNzG4YJ3ngLRASHZ5XXvR7aTUFBS24X108BBLGXJB5n-gKdLSCO5mA8YTbA60FbauOlH-fc6YZQswyhmGMcv5MU5Cuah2EhvgbihuDQkrD1_6sDlca9Zj3M6h44tM8PhaxpoX_J9hdrEgUS0zfIbVB6hECksQu8hUCB75IZGrYrfqqDCGYSn2M33l80EfmXvkzi99hl-7XfHuO5HykfKTYVt9YkZ4a0P1va4Z5Du8OSJb09uQL7rsKZzFtrj3K5nKao9NliNvLisnIWacn6fwQRKvFxYQYohboMp8WLfSiRtyJjT0ayJWdgTI091Ff-cQvT9eX8eXwsKiKv2J6p6ac7U_wsJDYeAkCDqA-xIBO1f9RAh9fuOqolQ9BnL3whO5OWMRvDKa_ck4NCpmITguMXzr2Yn-em_YIwBtxiLStQxpmFqqnEyF6R7N1PB2RC5U84sA2Eb_B2jTqiHeT8qLu0PGNwOe0xlOqeUjsxGcwAv3Agov81nt3N-2gyOLrDuECwx13TepnPUCwiQblaYcRNidcPlz_YeMN6zRqCYIsA6LO0xUirebHwrp7WnpSIMPTijPWkYVUiVwvwCJ6fAm-6I4zRQrTDMP0RobmY3F93FON9uBr537QW1BGiOdCF8IY2A-PtkAJe56z7gwqoZSSdFUoDHRehYP5xKRAs_IgHq3G-pLwRSiMS0NNe6_3fwdaT-jDCFZBAOcR6oNxNiNP4WelSBuwrSNJKDmeVcXEwFf0MpDAbeVI0UDQZFZHagJJAzsWBG7tQJH4CYW_fVNJperpBAqBk6CRY5ZZAqfcUVfjnpSIG3fWer0QeQDR4XUtFIi4s8ETp82i5eYWF3NZbTYrvW4EXnvDfSsEnkyJ2DAVCxUCjisI11r1fIavYNRfaztNcPhyI3kObGbYlRp09UFuqMZyGxPCdU7QWhdCP7EW9eFfRy-qOUtenIZ-pb1DHucRRl481w6Vs9AZ61ZAESX7jGee-AKimOEKUXel_lqMTOeMGbscnIXLMcj58-Jmip-wtY3sjNTuuYMIIez4B2mw3sjaNFTcPe1f20bwXPOf0nv1Fns6IVkLTDWrwrtluZFZoZQQ0Tz6AqWFEk3ZvUc6CC13TTC-2bJgMR9lWFx4dqm29gGOO-YYl0GJRhRvA0DTdO3ugupSPOPrMBMbVaVca5vK8U0t-RgtjGb-wXChaOG7hWWsHNMFhd0Fx2FSlsRg0KFD7_tosUz96_c5kGgVWbuWOyA_WNEH5DDTnX2_c6DzTKivQ_2xlpXrAwTX3znKnBRpEx4XBMZHStXoDpZNuFcC00NVldAHiDpiVdCv6oPpdLYZWwuGAsNG8sJQl1e7uHQFZ1e3YA2-e4cuMyXT5miVqLxaEgpwX13KSw6gboKQhj_RGiER55lbJtxPoOxURHteP6e3bH1uhgJDqPI2Dd_cSrQ7i8DG6J00nAct6cMnDWZRskrFOLHJuCgRBJCO7mLfIYXiRYzYxTrLtP6zFtMRqPnKLE9g7fJj0c-AKa9M-_TtFczvZLDJBtp02aRaZsecQdknehF2loTCdWJcxbjQgGSoRHefd_O87_aI54wNvLuGjsYhDglYJIEHOJyEiBsCHnqw",
      "faxNumber": "",
      "formInteractionMs": 65408
    }
    ```
- **Response**:
    ```json
    {
      "expirationTime": "2026-04-30T04:39:56+00:00",
      "canBeResentAfter": "2026-04-30T04:35:56+00:00",
      "attempts": 5
    }
    ```

**Step 2: Verify OTP**
- **Endpoint**: `POST /public/authentication-service/v1/session/{sessionId}/confirm`
- **Purpose**: Validates the 6-digit OTP code to complete registration.
- **Request Payload**:
    <!-- OTP Submission -->
    ```json
    {
      "otp": "236416",
      "isTosAccepted": true,
      "channel": "phone"
    }
    ```
- **Response**:
    ```json
    {
      "code": "wrong-otp",
      "attempts": 4,
      "expirationTime": "2026-04-30T04:39:56+00:00",
      "canBeResentAt": "2026-04-30T04:35:56+00:00"
    }
    ```

## 4. Security & Reversing Notes

### reCaptcha v3 Validation
The platform uses Google reCaptcha v3. The `reCaptcha` token in the `/register` request is long-lived but must be generated via a valid browser context. Automated tools will need a Captcha-solving service (like 2Captcha or Anti-Captcha) to generate this token dynamically.

### Session Lifecycle
The `sessionId` (e.g., `1f1444db-28a3-6ed2-935f-1d6a4c83e8a9`) is mandatory and appears to be initialized during the landing page load. It remains consistent across the registration lifecycle.

## 5. Conclusion

### Automation Feasibility: 35% (Low)

### Detailed Conclusion:
Automation is significantly hindered by the mandatory reCaptcha v3 validation and Cloudflare edge protection. While the API structure is clear, triggering the SMS requires a fresh, high-score reCaptcha token. Successful automation would require a hybrid approach using `Playwright` or `Puppeteer` to handle the JS-heavy reCaptcha generation, or the integration of a specialized solving API. Headless REST-only automation is likely to be flagged as fraudulent by the reCaptcha scoring system.
