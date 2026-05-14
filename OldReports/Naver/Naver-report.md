# Naver - Research Report

## Metadata
- **Target URL/App**: `naver.com` / `com.nhn.android.search`
- **Researcher**: `Deepanshu Singh`
- **Date**: `2026-05-10`
- **Status**: `Completed`
- **HAR Files**: `Naver.har`

## 1. Executive Summary
Naver's authentication and registration flow was analyzed via the Android application (`com.nhn.android.search`). The investigation focused on the SMS verification mechanism used during account creation. The process involves multiple AJAX-based steps, including ID availability checks, password validation, and a multi-layered SMS request system. Notably, the SMS request (`sendAuthno`) includes an encrypted payload (`nid_kb2`) containing UUIDs and encoded data, suggesting client-side security measures or session tracking. The verification step is a simple GET request with the received code.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for identity verification |
| **Captcha** | undefined | No visible captcha was triggered during the analyzed flow |
| **Encryption** | Custom (nid_kb2) | Encrypted JSON payload in POST body |
| **Rate Limits** | Unknown | No rate limiting behavior was observed in the HAR |
| **Endpoints Involved** | 3 | `/user2/joinAjax?m=checkId`, `/user2/joinAjax?m=sendAuthno`, `/user2/joinAjax?m=checkAuthno` |
| **Bot Protection** | Custom | Encrypted payloads and session keys (`token_sjoin`) |

## 3. Technical Traces

### 3.1 ID Availability Check
Initial step to verify if the desired username is available.

**Request**:
```http
GET https://nid.naver.com/user2/joinAjax?m=checkId&id=deepanshu29&key=NYEnbyJolM6u5zr1 HTTP/1.1
Host: nid.naver.com
User-Agent: Mozilla/5.0 (Linux; Android 15; Pixel 7) ... com.nhn.android.search/12.20.11
Referer: https://nid.naver.com/user2/join/begin?token_sjoin=NYEnbyJolM6u5zr1...
```

**Response**:
```http
HTTP/1.1 200 OK
Content-Type: text/html;charset=UTF-8

NNNNY
```

### 3.2 SMS Verification Code Request
This endpoint triggers the sending of the OTP to the provided mobile number. Note the presence of the `nid_kb2` encrypted payload.

**Request**:
```http
POST https://nid.naver.com/user2/joinAjax?m=sendAuthno&tp=normal&nationNo=39&mobno=3522291526&lang=en_US&key=NYEnbyJolM6u5zr1&id=deepanshu29 HTTP/1.1
Host: nid.naver.com
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
User-Agent: Mozilla/5.0 (Linux; Android 15; Pixel 7) ... com.nhn.android.search/12.20.11

nid_kb2={"uuid":"286534ef-4f34-4952-81c8-742be7398e43-0","encData":"N4IghiBcIE..."}&nid_kb3=kNeiW26TNuBGzMf9jU3A3yoDpeNq1sW03Xv3Md0SBQc%3D
```
<!-- Phone Number: 3522291526 -->

**Response**:
```http
HTTP/1.1 200 OK
Content-Type: text/html;charset=UTF-8

NNNNS
```
<!-- Status: NNNNS (Success) -->

### 3.3 SMS Verification Code Submission
Submission of the 4-digit code received via SMS.

**Request**:
```http
GET https://nid.naver.com/user2/joinAjax?m=checkAuthno&authno=2555&key=NYEnbyJolM6u5zr1 HTTP/1.1
Host: nid.naver.com
User-Agent: Mozilla/5.0 (Linux; Android 15; Pixel 7) ... com.nhn.android.search/12.20.11
```
<!-- OTP Code: 2555 -->

**Response**:
```http
HTTP/1.1 200 OK
Content-Type: text/html;charset=UTF-8

NNNNF
```
<!-- Status: NNNNF (Failure - Invalid or Expired) -->

## 4. Automation Feasibility
- **Feasibility**: Medium (40-70%)
- **Reasoning**: The flow uses standard HTTP/HTTPS protocols, but the `nid_kb2` encrypted payload in the `sendAuthno` request presents a challenge. The payload seems to be generated client-side (possibly in JavaScript/WebView) and likely contains a signature or timestamp-based encryption. Without reversing the encryption logic, automating the SMS trigger will be difficult. However, once the code is triggered, submission is straightforward.

## 5. Conclusion
The Naver Android registration flow is well-structured and utilizes a multi-step AJAX approach within a WebView. While the final OTP submission is a simple GET request, the preceding SMS trigger is protected by an encrypted payload (`nid_kb2`). This suggests a layer of bot protection aimed at preventing bulk SMS requests. Further research into the `nid_kb2` generation logic is required for full automation.
