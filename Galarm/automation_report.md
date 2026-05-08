# Galarm Automation Testing Report

## 1. Overview
The automation test for Galarm (`com.galarmapp`) aimed to replicate the OTP request and verification flow using Firebase Cloud Functions. The script `api.py` was developed to execute the sequence captured in the HAR traffic.

## 2. Test Execution
- **Script**: `api.py`
- **Endpoints Tested**:
    - `POST /sendVerificationCodeHttps`
    - `POST /verifyCodeHttps`

### Results
| Step | Endpoint | Status | Result |
| :--- | :--- | :--- | :--- |
| 1 | `/sendVerificationCodeHttps` | FAILED | HTTP 200, "status":"failure" (Invalid request) |
| 2 | `/verifyCodeHttps` | SKIPPED | Dependent on Step 1 |

## 3. Analysis of Failure
The script failed at the first step (`sendVerificationCodeHttps`) due to the following factors:
1.  **reCAPTCHA Expiration**: The `token` field requires a fresh Google reCAPTCHA v2 token. The captured token in the HAR is single-use and has a very short TTL (usually 2 minutes).
2.  **Cipher Data**: The `cipher` field contains AES-encrypted metadata. The server likely checks for unique session identifiers or timestamps within this blob.
3.  **Firebase Instance ID**: The `Firebase-Instance-ID-Token` header and `X-Firebase-AppCheck` are likely validated against current app state.

## 4. Conclusion & Recommendations
Automation feasibility is **low (15%)**. Successful automation would require:
- **reCAPTCHA Bypass**: Integration with a captcha-solving service to provide fresh tokens.
- **Cipher Reversing**: Extracting the AES key and IV from the APK to generate valid `cipher` blobs dynamically.
- **Session Management**: Properly managing Firebase session state and AppCheck tokens.
