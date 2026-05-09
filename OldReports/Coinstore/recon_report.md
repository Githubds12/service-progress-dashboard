# Coinstore Reconnaissance Report

## 1. Executive Summary
Reconnaissance of the Coinstore Android application (`com.io.coinstore`) has revealed a robust security architecture for account management. The platform uses a "gateway" system for sending verification codes and enforces multi-factor authentication (MFA) for sensitive operations such as binding a phone number.

## 2. Infrastructure Details
- **Main API Host**: `api.coinstore.com`
- **Futures API Host**: `futures.coinstore.com`
- **Encryption Host**: `coinstore-sg-encryption.coinstore.com`
- **Captcha Provider**: GeeTest (`geevisit.com`).
- **Notification Service**: Firebase FCM (`cJBWAcR3TXO...`).

## 3. Critical Endpoints
| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/v2/user/common/gateway/send/email` | POST | Sends an email verification code for security scenes. |
| `/v2/user/common/gateway/send/sms` | POST | Sends an SMS verification code to a new phone number. |
| `/v2/user/strategy/validCode` | POST | Validates codes (Email/Google/SMS) for a specific scene. |
| `/v2/user/mobile/binding/save` | POST | Finalizes the linking of a phone number to an account. |

## 4. Observed Payloads
### Phone Binding (Scene 6)
Requests for phone binding consistently use `scene: 6`. The payloads include the country code (e.g., `+82`), mobile number, and the verification codes.

## 5. Security Posture
- **GeeTest Integration**: Behavioral captcha is used to mitigate automated SMS requests.
- **Scene-Based Logic**: Verification codes are tied to specific operation "scenes", preventing cross-endpoint reuse.
- **FCM Token Binding**: The app binds the device's FCM token to the user session for notification security.

## 6. Conclusion
Coinstore exhibits a mature security posture with clear separation of concerns via its gateway-based verification system. The multi-step binding flow effectively prevents unauthorized account modifications.
