# Shop Apotheke API Request/Response Logs

### POST https://api.sa-tech.de/auth/v2/com/register
**Status**: 201

#### Request
```json
{
  "dateOfBirth": "1998-04-15",
  "email": "deepanshusinghdigitalheroes@gmail.com",
  "firstName": "Deepanshu",
  "lastName": "Singh",
  "newsletterAccepted": false,
  "password": "Facebook@ds12,",
  "preferredLanguage": "de",
  "registrationOrigin": "app",
  "salutation": "mr",
  "tosAccepted": true
}
```

#### Response
```json
{
  "tokenType": "bearer",
  "token": "eyJraWQiOiJmMjI3MGU4OS1iOGJjLTQ1ODAtOTA2MC01OTBmMTNiYjkyMjEiLCJhbGciOiJSUzM4NCJ9.eyJleHAiOjE4MDg4NDAxNzcsInN1YiI6IjI1MTQ2Mjk4NDgiLCJyb2xlIjoiUkVHSVNURVJFRCIsInRlbmFudCI6ImNvbSIsInR5cGUiOiJBQ0NFU1MiLCJrZXlWZXJzaW9uIjoiZjIyNzBlODktYjhiYy00NTgwLTkwNjAtNTkwZjEzYmI5MjIxIiwiZGV2aWNlVHlwZSI6ImFuZHJvaWRBcHAiLCJleHBSZWZyZXNoIjoiMjAyNi0wNC0yN1QxMDowMjoxNy45NDRaIiwiZXhwU2Vuc2l0aXZlIjoiMjAyNy0wNC0yN1QxNTozNjoxNy45NDRaIiwianRpIjoiNjA4ODQwOTItODcxNi00NmNhLWE5ZTItMDFkNzJjYmM1YTI2IiwiaXNzIjoiYXV0aC5yZWR0ZWNsYWIuY29tIiwiaWF0IjoxNzc3MjgzMjM3fQ.QIevGI0VQ0a42BV_NNBSKvNcBiEsDE-i_xiGldChkW0bPUUMdTlxzZ8zCPXoFT9XI1JZ3js3g7pirIrC-Zw_2PrcSUGKpj61DF-JqvYmK4WUh6SqKpO2xeboUIxQ3V_hEXy7DbwBCflIzoXW0HChaJDUmafm_W44luyLKqDcCCvv5vjTP2g8WnVDhpIwxsZdIpOMr2upN6Niq8Ff3zdmHLdRFlfNooF2Zehzgc-5n-43kKQ0hC4ZjCMB36Yby_zgFMXhCrXT_pRh4hzJPffC3O2FiXK3K4aKEgjYXeaSeus_banSJWE4pxAysSOKPtvCTf5Xu5GW0c8iXf9WtpSqYDMOMCTWKJTzAnoKI6pXlARRw558M-vJn3_zNmxC9HwbblCfng1BUOIKijxN2VyAO8Arg759INct-VcpFeARPblKyhbx0qLNGShHkb15Jb54_lW3MW_bONt_Rw6iXHawkUThU81pAMnR1MRwXS3SpHSfbs0kYXRfLGMU6tg9ZJRu"
}
```

---

### GET https://api.sa-tech.de/session/v1/com/erx-session-status/2514629848
**Status**: 404

#### Request
*No Body*

#### Response
```json
{
  "statusCode": 404,
  "error": "Not Found",
  "message": "customer-data-service.error.not_found"
}
```

---

### POST https://api.sa-tech.de/nfc-health-card-position/api/v1/nfc-position
**Status**: 200

#### Request
```json
{
  "manufacturer": "Google",
  "marketingName": "Pixel 7",
  "modelName": "Pixel 7",
  "os": "Android"
}
```

#### Response
```json
{
  "nfcPos": {
    "x0": 0.35,
    "y0": 0.25,
    "x1": 0.65,
    "y1": 0.4
  },
  "source": "CACHE",
  "found": true,
  "datasetVersion": "1777023147000",
  "modelVersion": "1777023147000",
  "updatedAt": "2026-04-24T09:32:27Z",
  "searchPolicy": "upper_scan"
}
```

---

### POST https://api.sa-tech.de/customer/v1/com/mfa/2514629848/phone-verification/request
**Status**: 204

#### Request
```json
{
  "phoneNumber": "+491765550123"
}
```

#### Response
```json

```

---

### POST https://api.sa-tech.de/customer/v1/com/mfa/2514629848/phone-verification/confirmation
**Status**: 400

#### Request
```json
{
  "code": "222222"
}
```

#### Response
```json
{
  "statusCode": 400,
  "error": "Bad Request",
  "message": "erx.phone_verification.password_rejected"
}
```

---

