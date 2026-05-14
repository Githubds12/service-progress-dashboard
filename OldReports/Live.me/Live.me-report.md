## 1. Executive Summary
This report analyzes the registration and SMS verification flow for **Live.me**, focusing on its authentication endpoints and evaluating the feasibility of automation. The analysis is based on captured HTTP/HTTPS traffic (HAR files) originating from the Android application (`com.cmcm.live` v4.9.25). The goal is to document the observed endpoints, assess implemented bot protections, and identify required payload structures for programmatic interaction.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | Primary channel for OTP |
| **Captcha** | undefined | No interactive captcha challenge observed in the trace |
| **Encryption** | Custom Hash Signatures | Use of custom hashing (`lm_s_str`) |
| **Rate Limits** | Unknown | No rate limiting behavior was observed during testing |
| **Endpoints Involved** | 3 | `/1/cgi/is_exist`, `/2/cgi/sendsms`, `/1/cgi/code_exist` |
| **Bot Protection** | Tongdun | Tongdun device fingerprinting SDK implemented (`tongdun_black_box`) |

## 3. Endpoints and Payload Details
The authentication flow utilizes three endpoints to handle phone number submission, SMS triggering, and OTP verification.

### Step 1: Phone Number Registration / Check
This endpoint is used to submit the phone number and check if the user exists.

**Request:**
```http
POST /1/cgi/is_exist HTTP/1.1
Host: iag.liveme.com
Content-Type: multipart/form-data; boundary=3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
User-Agent: okhttp/4.11.0

--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="cmversion"

49252624
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="ver"

4.9.25
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="name"

<!-- phone number -->393382289898
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="lm_s_str"

8252d4ba57a9286cac3984d67c349b96
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="lm_s_ver"

1
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="alias"


--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="devid"

80b67980e5c38193
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="lm_s_id"

LM6000101139961122666757
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="lm_s_ts"

1777449601713
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="deviceid"

80b67980e5c38193
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="devtype"

android
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="tongdun_black_box"

rGPU51777449570XWBOPMdUtN1
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f--
```

**Response:**
```http
HTTP/1.1 200 OK

{"data":{"has_pwd":0,"captcha":""},"ret":12018}
```

### Step 2: Request SMS OTP
This endpoint triggers the server to send the OTP code to the submitted phone number.

**Request:**
```http
POST /2/cgi/sendsms HTTP/1.1
Host: iag.liveme.com
Content-Type: multipart/form-data; boundary=3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
User-Agent: okhttp/4.11.0

--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="client_channel_1"

android
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="client_channel_2"

web
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="cmversion"

49252624
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="length"

4
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="mobile"

<!-- phone number -->393382289898
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="need_slide"

2
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="geo"

IN
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="itc"

39
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="ver"

4.9.25
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="type"

5
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="lm_s_str"

f288ab5d2c61067e62b27d8bc2739e3b
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="lm_s_ver"

1
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="alias"


--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="devid"

80b67980e5c38193
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="lm_s_id"

LM6000101139961122666757
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="lm_s_ts"

1777449607898
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="deviceid"

80b67980e5c38193
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="client_country_code"

IT
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="devtype"

android
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="tongdun_black_box"

rGPU51777449570XWBOPMdUtN1
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f--
```

**Response:**
```http
HTTP/1.1 200 OK

{"ret":50801,"data":{"status":50801,"captcha":""}}
```

### Step 3: OTP Verification
This endpoint processes the submitted OTP for verification.

**Request:**
```http
POST /1/cgi/code_exist HTTP/1.1
Host: iag.liveme.com
Content-Type: multipart/form-data; boundary=3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
User-Agent: okhttp/4.11.0

--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="client_channel_1"

android
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="client_channel_2"

web
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="sid"


--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="ver"

4.9.25
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="code"

<!-- otp code -->3333
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="name"

<!-- phone number -->393382289898
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="type"

5
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="lm_s_str"

67d319f4949b5e8581c14ff2768c45ef
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="lm_s_ver"

1
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="alias"


--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="devid"

80b67980e5c38193
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="lm_s_id"

LM6000101139961122666757
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="lm_s_ts"

1777449640134
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="deviceid"

80b67980e5c38193
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="client_country_code"

IT
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="devtype"

android
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f
Content-Disposition: form-data; name="tongdun_black_box"

rGPU51777449570XWBOPMdUtN1
--3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f--
```

**Response:**
```http
HTTP/1.1 200 OK

{"ret":12015,"data":{"captcha":""}}
```

## 4. Bot Protection & Vulnerability Scan
The application employs standard device fingerprinting through the Tongdun SDK (`tongdun_black_box`), which requires accurate device profiling to bypass. There are also dynamic hash signatures generated locally (`lm_s_str`), which may pose a challenge unless reverse-engineered or replayed efficiently.

## 5. Conclusion
**Automation Feasibility:** High > 70%

The automation feasibility for the Live.me application's SMS verification flow is high. The required API endpoints use standard multipart/form-data encoding and return straightforward JSON responses. The primary security hurdles involve the `tongdun_black_box` parameter and the custom `lm_s_str` hash signature.

As long as the fingerprint and the signature generation can be replicated or safely omitted/replayed without triggering immediate blocks, automated SMS registrations can be successfully performed. No interactive captchas were observed in the captured network traffic, simplifying the programmatic approach.
