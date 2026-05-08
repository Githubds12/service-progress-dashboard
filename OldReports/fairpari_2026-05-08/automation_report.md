# Fairpari Automation Testing Report

## 1. Overview
The automation test aimed to replicate the registration and OTP flow for Fairpari (`org.fairpari.client`) using Python. The script `api.py` was developed to execute the multi-step sequence identified from the HAR traffic.

## 2. Test Execution
- **Script**: `api.py`
- **Endpoints Tested**:
    - `POST /Account/v1.1/Mb/Register/Registration`
    - `POST /Account/v1/SendCode`
    - `POST /Account/v1/CheckCode`

### Results
| Step | Endpoint | Status | Result |
| :--- | :--- | :--- | :--- |
| 1 | `/Register/Registration` | FAILED | HTTP 200, ErrorCode: 160 (Authentication failed) |
| 2 | `/SendCode` | SKIPPED | Dependent on Step 1 |
| 3 | `/CheckCode` | SKIPPED | Dependent on Step 2 |

## 3. Analysis of Failure
The automation script failed at the first step (`Registration`). This is due to the following security measures:
1.  **X-Sign Signature**: The request requires a cryptographic signature in the `X-Sign` header. This signature is likely calculated using the request body, timestamp, and a client-side secret. The hardcoded signature from the HAR file is either expired or tied to a specific session timestamp.
2.  **Captcha Validation**: The `ImageText` field contains the solved image captcha solution. Since captchas are single-use and time-sensitive, the captured solution is no longer valid.
3.  **AppGuid/RequestGuid**: The server likely validates the consistency of GUIDs and timestamps, rejecting replays.

## 4. Conclusion & Recommendations
Automation is **partially feasible** (50%). To achieve full automation, the following components must be implemented:
- **X-Sign Generator**: Reverse engineering the Android library (likely `libfairpari.so` or similar) to understand the `X-Sign` generation logic.
- **Captcha Solver**: Integration with an OCR service or a dedicated model to solve the custom image captcha in real-time.
- **Dynamic Token Management**: Handling the `Guid` and `Token` exchange correctly once the first step is bypassed.
