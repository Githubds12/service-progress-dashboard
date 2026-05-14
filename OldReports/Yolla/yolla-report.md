# Yolla - Security Analysis Report

## Metadata
- **Target URL/App**: `com.yollacalls`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-04-25`
- **Status**: `Completed`
- **HAR Files**: `Yolla.har`

## 1. Executive Summary
Yolla implements a standard OTP-based authentication flow for mobile registration. The application employs security measures including request integrity signing (the `sign` parameter) and Google Play Integrity Standard for bot protection. The registration flow consists of two primary steps: submitting the phone number to receive an SMS OTP and subsequently verifying that code. While the API communication is over HTTPS, the presence of request signing and integrity tokens suggests a focus on preventing unauthorized API access and ensuring requests originate from a legitimate app instance.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for OTP delivery |
| **Captcha** | Google Play Integrity Standard | Used during the registration step |
| **Encryption** | Request Signing | MD5/Hex signature in the `sign` parameter |
| **Rate Limits** | Unknown | No explicit rate limiting observed in the provided traces |
| **Endpoints Involved** | 2 | `/register`, `/verify` |
| **Bot Protection** | Google Play Integrity | Standard integrity checks for Android devices |

## 3. Flow Details

### Flow 1: User Registration / Login

**Step 1: Request SMS OTP**
- **Endpoint**: `POST https://api.yollacalls.com/register`
- **Purpose**: Submit phone number and request verification code via SMS.
- **Host**: `api.yollacalls.com`
- **Request Headers**:
    - `Accept-Encoding`: `gzip`
    - `Accept`: `application/json`
    - `User-Agent`: `com.yollacalls/4.81 (Pixel 7; Android 15; en_IN)`
    - `Content-Type`: `application/x-www-form-urlencoded; charset=UTF-8`
- **Request Body**:
    ```text
    country=IN&device[hardware]=panther&device[app_version_code]=5334&device[model]=Pixel+7&sign=B8F79851FFAC7D6D2266D09032E3A66B&device[timezone]=GMT%2B5&language=en&device[language]=en&device[ad_id]=f51ee336-e489-4882-8c21-95ff06ed4a9a&device[rooted]=false&integrity_token=CowDARCnMGu4CRZ_AYqEsNHrNwqnqUwX-oqN9idShRHmCcgnEBhHEyMLGV3DU4jx9RIgC0_4lSuD0ib8RQ3nByagAGJtc6440J7jhY0TJxUsBlsd4IEpDvX70WoYX738fnR-emIYk5LAC5743Dlh5Zofd3NQNhbGhX7eAiKrxxYbZr9Q-MRmoXGL2dVwIOJMn29WZjfyAk03_wsIoqY_LhYSAMaQJXeDhiV00B-RdAqI0wgGE2WrDJTSUO8yaXiXqjgXavU82_pinmQZiVGw6mZHDQ-5bY_YmrHqSspVyMJIy2i0gXLU9oADPHwrmQ_q-i5PWDMbZTtGZCV5ajLcsaDPKIBMf9Yl71I-XT6Bg022_mSuCwPyCoThhifGX5DePrOARPM2IdosDdIecm-Epoi0-pxnkd7KeT3FqFTwb_pJSijOenn_cHfqTCjcoVbQiVTrV1wwY8GLxGaHIvjmdzJtWn1hDjQZs303dzvAIfk-qDu8s2GLwEZFS8KMvsi8Poe0k8YhYbByDF1gtZIiGl4B4PVZxR-H7QNwoj5mmdDTUhiB10aOO3SRZF_hXzt8mG_gvpqz5GW2O-oUgr03pz67k5kVvgp9q6vfhk6GbhsVO1ILFPOAbcmlPHbHYjd7Xf5DlGLvr-dG64wGxz7OIkMB4PVZxXQwI311Vomt6gRjeaOO96ZoRXJDF0HgndV_0np_OJoQBR7feeKkMPoh1LUgoCOiu5qOvX8r8Ppi0HnpsCP_&device[product]=panther&device[android_id]=2c969a3eff46d674&phone=<!-- phone -->918791267460<!-- /phone -->&verify_by=sms&device[emulator_flags]=telephony&device[platform]=android&device[device_id]=ccd1624fb6ad624bdd08e02086063486d6dd135b&device[system_version]=15&device[emulator]=false
    ```
- **Response Status**: `200 OK`
- **Response Headers**:
    - `Content-Type`: `application/json`
    - `x-powered-by`: `Express`
- **Response Body**:
    ```json
    {
      "data": {
        "already_devices_count": 1,
        "verification_type": "sms"
      }
    }
    ```

**Step 2: Verify OTP**
- **Endpoint**: `POST https://api.yollacalls.com/verify`
- **Purpose**: Submit the received OTP code to authenticate the session.
- **Host**: `api.yollacalls.com`
- **Request Headers**:
    - `Accept`: `application/json`
    - `User-Agent`: `com.yollacalls/4.81 (Pixel 7; Android 15; en_IN)`
    - `Content-Type`: `application/x-www-form-urlencoded; charset=UTF-8`
- **Request Body**:
    ```text
    code=<!-- otp -->6336<!-- /otp -->&device[android_id]=2c969a3eff46d674&phone=<!-- phone -->918791267460<!-- /phone -->&sign=BCA4081F97FB057D35B79934279DEA17&ad[device_advertising_id]=f51ee336-e489-4882-8c21-95ff06ed4a9a&device[timezone]=GMT%2B5&device[device_id]=ccd1624fb6ad624bdd08e02086063486d6dd135b&device[language]=en&device[ad_id]=f51ee336-e489-4882-8c21-95ff06ed4a9a&device[system_version]=15&device[rooted]=false
    ```
- **Response Status**: `200 OK`
- **Response Headers**:
    - `Content-Type`: `application/json`
- **Response Body**:
    ```json
    {
      "error": {
        "code": 1151,
        "messages": {
          "error": "[1151] Incorrect code"
        }
      }
    }
    ```

## 4. Security & Reversing Notes

### Request Integrity (Sign Parameter)
All critical requests to `api.yollacalls.com` include a `sign` parameter. This is a hexadecimal string (likely MD5 or SHA1) used to verify that the request body has not been tampered with. Reversing the application would be necessary to identify the exact hashing algorithm and the secret salt used to generate this signature.

### Google Play Integrity Standard
The registration endpoint requires an `integrity_token`. This indicates the use of Google Play Integrity API to ensure that the request is coming from a genuine Android device and an unmodified version of the Yolla app. This is a significant hurdle for automation as it requires a valid token from a real device.

### Device Fingerprinting
The app collects various device details including `android_id`, `hardware`, `model`, `timezone`, and `advertising_id`. These parameters are bundled into the request bodies and are likely checked against the `sign` and `integrity_token`.

## 5. Conclusion

### Automation Feasibility: Medium 50%

The authentication flow in Yolla is straightforward in terms of endpoint sequence but presents technical challenges for full automation. The primary blockers are the custom request signing (`sign` parameter) and the integration of Google Play Integrity (`integrity_token`). 

Automation can be achieved by:
1. Reversing the Android APK to extract the signing logic and salt.
2. Utilizing a real device or a specialized service to generate valid Google Play Integrity tokens.
3. Mimicking the device fingerprinting parameters consistently.

Overall, while not trivial, the flow is verifiable and standard for high-quality mobile applications.
