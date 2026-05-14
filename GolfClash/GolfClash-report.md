# GolfClash Security Reconnaissance Report

## Service Metadata
- **Service Name**: Golf Clash
- **Package Name**: `com.playdemic.golf.android`
- **Version**: `3.4.3`
- **Service ID**: `c81a0f61-f580-49fe-b650-ab54aea72b15`
- **Developer**: Playdemic (Glu Mobile)

## Authentication Flow Summary
Golf Clash utilizes a proprietary binary protocol for its primary client-server communication, including authentication and session management. The app supports multiple login methods (Apple ID, Facebook, Google Play Games), but also maintains a direct mobile number + OTP flow.

### 1. Session Initialization
The app first establishes a session with the Glu Central Services.

**Request:**
```http
GET /v1/sessions/games/com.playdemic.golf/devices/F51EE336-E489-4882-8C21-95FF06ED4A9A HTTP/1.1
Host: prd1.session.centech.glulive.com
User-Agent: Dalvik/2.1.0 (Linux; U; Android 15; Pixel 7 Build/AP4A.250205.002)
Connection: Keep-Alive
Accept-Encoding: gzip
```

**Response:**
```json
{
  "status": {
    "code": 2000,
    "type": null,
    "errorMessage": null
  },
  "data": {
    "sessionId": "40e8ee8d-0356-46bb-8b8c-6ed9b250ea74"
  }
}
```

---

### 2. OTP Generation (Mobile Number Submission)
The phone number is submitted to the Playdemic backend. The request is sent as a binary `application/octet-stream` payload.

**Request:**
```http
POST //Client/Home HTTP/1.1
Host: playgk.playdemic.com
Content-Type: application/octet-stream
Content-Length: 215
User-Agent: okhttp/5.3.0
Connection: Keep-Alive

[Binary Payload: Encrypted/Proprietary]
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/octet-stream
Content-Length: 297

[Binary Payload: Encrypted/Proprietary]
```

---

### 3. OTP Verification
The received 4-digit code (e.g., `6197`) is submitted back to the same endpoint.

**Request:**
```http
POST //Client/Home HTTP/1.1
Host: playgk.playdemic.com
Content-Type: application/octet-stream
Content-Length: 200
User-Agent: okhttp/5.3.0
Connection: Keep-Alive

[Binary Payload: Encrypted/Proprietary]
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/octet-stream
Content-Length: 255

[Binary Payload: Encrypted/Proprietary]
```

---

## Secondary Services & SDKs

### Facebook SDK Analytics
Used for tracking app launches and attribution.
**Endpoint**: `https://graph.facebook.com/v16.0/app/mobile_sdk_gk`

### Singular Analytics
Used for marketing attribution.
**Endpoint**: `https://sdk-api-v1.singular.net/api/v1/config`

### AWS Kinesis Logging
The app streams real-time event data to AWS Kinesis.
**Endpoint**: `https://kinesis.us-east-1.amazonaws.com/`

## Observations
- The use of a double slash `//` in the URL path (`//Client/Home`) suggests a possible misconfiguration or a specific routing logic on the backend.
- The binary protocol is highly resilient to simple inspection, likely requiring dynamic instrumentation (hooking `okhttp` or native methods) to recover cleartext parameters.
- Session IDs are managed separately via the `centech.glulive.com` infrastructure.
