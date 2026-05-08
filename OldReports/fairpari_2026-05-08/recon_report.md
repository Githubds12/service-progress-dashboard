# Fairpari Reconnaissance Report

## 1. Project Information
- **App Name**: Fairpari
- **Package Name**: `org.fairpari.client`
- **Version**: `253.0.2`
- **Backend Host**: `andind2022.com`

## 2. Reconnaissance Findings

### Infrastructure
- **Main API Domain**: `andind2022.com`
- **Analytics/Telemetry**:
    - `Fatman` telemetry: `https://andind2022.com/Fatman/.../event.json`
    - Firebase/Google Analytics observed in traffic.
    - AppsFlyer integration for attribution.
- **Server Headers**:
    - Uses `br, gzip` encoding.
    - Custom headers like `X-Sign`, `X-Whence`, `X-Referral`, `X-Group`.

### Attack Surface Analysis
- **Registration Flow**: Exposed via `Account/v1.1/Mb/Register/Registration`.
- **OTP Delivery**: Handled via `Account/v1/SendCode`.
- **Bot Protection**:
    - **Captcha**: Custom image captcha implementation.
    - **Signing**: Mandatory `X-Sign` header for state-changing requests.
    - **Behavioral Tracking**: Sends detailed device information and user events to the backend.

### Vulnerability Assessment
| Vector | Risk | Notes |
| :--- | :--- | :--- |
| **OTP Brute Force** | Low | Protected by `X-Sign` and session-bound `Token`. |
| **SMS Pumping** | Medium | No explicit rate limiting (429) observed in HAR, but captcha prevents easy scale. |
| **Data Leakage** | Low | Payloads use standard JSON, but sensitive fields like passwords (not seen in HAR) are likely hashed. |
| **Bot Detection Bypass** | Medium | The custom captcha is the primary hurdle for automated scanners. |

## 3. Technical Summary
Fairpari's mobile application communicates with a robust backend hosted on `andind2022.com`. The security architecture is designed to prevent automated abuse through a combination of custom captchas, request signing, and behavioral analytics. Reconnaissance suggests that while the API structure is clear, the cryptographic implementation of `X-Sign` provides a significant layer of defense against generic replay attacks.
