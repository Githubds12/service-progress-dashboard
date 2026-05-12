# Wallester - Research Report

## Metadata
- **Target URL/App**: `com.wallester.whitelabel` (2.9.69)
- **Researcher**: `Deepanshu Singh`
- **Date**: `12 May 2026`
- **Status**: `Completed`
- **HAR Files**: `Wallest.har`

## 1. Executive Summary
Wallester implements a multi-step SMS verification flow to authenticate users. The platform uses a `/sign-up` endpoint to initiate registration followed by `/sign-in` which requires solving a Friendly Captcha (FRC API) to proceed. The OTP is requested by passing the captcha solution and verified via the `/sign-in/challenge` endpoint. No complex encryption or device fingerprinting was observed on the mobile endpoints, but the presence of Friendly Captcha enforces interaction and anti-bot verification during the sign-in phase.

## 2. Quick Analysis
| Feature | Status | Details |
| :--- | :--- | :--- |
| **Verification Type** | SMS | primary channel for OTP |
| **Captcha** | Custom | Friendly Captcha (FRC API) implemented on the sign-in endpoint |
| **Encryption** | None | Standard JSON payloads over HTTPS |
| **Rate Limits** | Unknown | No rate limiting behavior was explicitly observed in the provided traces, though attempts are tracked |
| **Endpoints Involved** | 4 | `/v1/sign-up`, `/v1/sign-in`, `/v1/sign-in/challenge` (GET & POST) |
| **Bot Protection** | Friendly Captcha | Friendly Captcha solution required during `/sign-in` |

## 3. Flow Details

### Flow 1: Sign Up & OTP Trigger

**Step 1: Sign Up Initialization**
- **Endpoint**: `POST https://api-auth.wallester.com/v1/sign-up`
- **Purpose**: Submitting the phone number for registration.
- **Request Headers**:
```http
Host: api-auth.wallester.com
Connection: keep-alive
Content-Length: 72
sec-ch-ua-platform: "Android"
User-Agent: Mozilla/5.0 (Linux; Android 15; Pixel 7 Build/AP4A.250205.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/147.0.7727.137 Mobile Safari/537.36
Accept: application/json, text/plain, */*
sec-ch-ua: "Android WebView";v="147", "Not.A/Brand";v="8", "Chromium";v="147"
Content-Type: application/json
sec-ch-ua-mobile: ?1
Origin: https://client.wallester.com
X-Requested-With: com.wallester.whitelabel
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en,en-IN;q=0.9,en-GB;q=0.8,fil-PH;q=0.7,fil;q=0.6,en-SG;q=0.5,nb-NO;q=0.4,nb;q=0.3,sv-SE;q=0.2,sv;q=0.1,gsw-CH;q=0.1,gsw;q=0.1,en-US;q=0.1,de-DE;q=0.1,de;q=0.1,ja-JP;q=0.1,ja;q=0.1,da-DK;q=0.1,da;q=0.1,fi-FI;q=0.1,fi;q=0.1,nl-NL;q=0.1,nl;q=0.1,ko-KR;q=0.1,ko;q=0.1,zh-CN;q=0.1,zh;q=0.1,it-IT;q=0.1,it;q=0.1
```
- **Request Body**:
<!-- Phone number submitted for registration -->
```json
{"mobile":"+393720513805","locale":"en","timezone_name":"Asia/Calcutta"}
```
- **Response Headers**:
```http
Date: Tue, 12 May 2026 09:25:23 GMT
Content-Type: application/json
Content-Length: 4
Connection: keep-alive
access-control-allow-origin: *
access-control-expose-headers: X-Request-Id
vary: Origin
x-request-id: 352f676d-61ef-412f-af18-a48fc9f719ed
cf-cache-status: DYNAMIC
Server: cloudflare
CF-RAY: 9fa860325b8d79e6-HYD
alt-svc: h3=":443"; ma=86400
```
- **Response Body**:
```json
"ok"
```

**Step 2: Sign In (OTP Trigger via Captcha)**
- **Endpoint**: `POST https://api-auth.wallester.com/v1/sign-in?out_of_band_allowed=true`
- **Purpose**: Authenticates the phone number by providing the captcha solution and triggers the OTP challenge.
- **Request Headers**:
```http
Host: api-auth.wallester.com
Connection: keep-alive
Content-Length: 6917
sec-ch-ua-platform: "Android"
User-Agent: Mozilla/5.0 (Linux; Android 15; Pixel 7 Build/AP4A.250205.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/147.0.7727.137 Mobile Safari/537.36
Accept: application/json, text/plain, */*
sec-ch-ua: "Android WebView";v="147", "Not.A/Brand";v="8", "Chromium";v="147"
Content-Type: application/json
sec-ch-ua-mobile: ?1
Origin: https://client.wallester.com
X-Requested-With: com.wallester.whitelabel
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en,en-IN;q=0.9,en-GB;q=0.8,fil-PH;q=0.7,fil;q=0.6,en-SG;q=0.5,nb-NO;q=0.4,nb;q=0.3,sv-SE;q=0.2,sv;q=0.1,gsw-CH;q=0.1,gsw;q=0.1,en-US;q=0.1,de-DE;q=0.1,de;q=0.1,ja-JP;q=0.1,ja;q=0.1,da-DK;q=0.1,da;q=0.1,fi-FI;q=0.1,fi;q=0.1,nl-NL;q=0.1,nl;q=0.1,ko-KR;q=0.1,ko;q=0.1,zh-CN;q=0.1,zh;q=0.1,it-IT;q=0.1,it;q=0.1
```
- **Request Body**:
<!-- Phone number submitted with captcha solution -->
```json
{"mobile":"+393720513805","captcha_solution":"AQQA.p53oZBdtnaHIjFd7saVaI6RW3tQwK551Kq_p-RPxRj6kRPd9K4Y-oKNLs4omkESAG3GNclauyXsfjYJP7hPac8bC8drwHS4zw4AenhHRR-QBYw3H5R92A4oJ9jua2xxPxI7pv0uUrkpdoNRj1KFSR2_q1cjsfTX9uzmS0nr9s58bMAy3ESHqx7J2x75tgIpRnnozkVabTx5iCNKZgB0eP9bJvvtbJJpmdqDmbtC5w17b0lpar9ULYDqXMAxiwYr9k-VL_4E8_Wrh30K9RzWisJo4o_61gtJByJfJg5p100noMPlUxmzZCfiO27r1jnC4hqRWmp7DdAUVranC04f-KuMdwDRUTk0fLQWyx5PbUFQFlZjnIBWSvObFEARf7XbLR86ynB2EeMRbkPCdS_MNDelyHQFz98JzxKo8q2lzUA3g81uWzEKyBMgGTXc-f7ZovGsNS5Zu0mtLDztAEJ6ztRmShIXioqBZQX2TWAQQPvrQ3jHy8Ry5sNRRZqDsjqHL42iFffvyQiucln1d3UXqgv6-JRZqRJdLF7iZ9aGBBIZGx0XrPjTDABLlx2fiiKJBv3MxpSiYfWx-U57fdnpphS-S_nCC6b_ubAgXcqcBoq_KGHehP2RO5jxGzNb8ahVAgB0_Jq5v0OY5C2wlG1-W8S6N1eXb8qrhxzMqkZQDbq83bWy7ABLsibvpIjL1ZnkS0zWw5wgzUj7-l0amNX78_yuONL3AdNjqOCHh_GRbpcjdaiiZUqu-GcSA7Ks57_TQpVhhWfusS-1fvJX2Vt5j8MxXFr2zmlft1Faih1oZL786ls3ot4SL0ux1hyscYjYIlrtoJ-w4Sj4_QogqUEssHNGz11SULngTQzXWdAXkXzD0DxkXVIzDkOrc8tXCiv-uHIs8yTMVlXbg2ZsyyfQT_2shzw6b8TP98GasZfVwfax8XxaDTcE2CZkrJT-hZD2eqW8JPsyjVepKaecyafVBUhBXbgenS74HSAAEfaBd6fk-WTX0oxZAre6YXhHARuOBOy_xlxnFe2ouOlgASBWN3DGSwbAHK3ggfvrez-v3ErxkVS6m7dEo3oewXSDSYguVqzOYy1eqJHgw-IpzD9K84i3iiws8kfQLvekDsbLqBeNkbdEfl-zXvC6suBNVEKNZbj0f3A_3ch3PvwhquixbhB5PJWMV4pCwwNK5Sk-xQTWvRrYAlSUwnk_WUIJhSrbV0Cixa7YK2NLe3BmMZITwKGEBR17eR8My_ZndF4gN9MjVURk-nz10ckHTtCn3nmkolxAcdL3FsK5_v6fS2Hsoc9t5duu7Tw6Rha-FiDK-YS8GKDoTr2O8EApQvV38wizkammOFLVOCEOG_qxUUQuDQn0YZhbeBXUUWFla0sqk3x_8wIe40l6FpjFZNLib46g1K5Mtfd4l7isAox8XKZ7Ztbph4UcPnxz8xNib4Vl5ZywQl7OEim_bzR5GTb2Twx3Lq-tMS9zP08Q-jEecvEG_Zptp_xLTDB4UvKnre0ZpkIfwa3ZawuZ6qi1DYnJ_dz1O-PBK3qIlCX6HTG5eyxt7JSqLAA1uszCuReRakWtg7qLAJ8OX81bR4P3U1abw-2BSKUVjLXoA4kA4vnDFMH5MSpwiTkNcEaLRr0nbDXqtYYZRD28guFzYEFGvDONbq_0gJr0JA4EprrdPPOOv4RTxIQyfy_B-QpvfShs65dfPlCmiA_CiIylOSCMIX_Usl4CGwlLrJOV9LYhJNn5NcnsTWwStI6B9wchFbyZ1oEL3QLD_L4V50jsamp0E6UMz16mbCXnsEFirC8AGvOpaVQNQdPDTFU7ZMKmKe3rWHF-0twgx2hjErKktWldYb2Gxq0oPYQcZ2Hn7GWiiV2GYXN0t2k7ULJk3jD3iHwTDY50y5Rb873u2A8d8LbiVh7clQ3suwuwbClVyffMbKBV8Xt92C2N46pShiYRm5fBHZDdQCaS30Duv_cykibwNcGbmLcx_cHez1iOjOpazVcn_iYOVzDLHR-F8ZjUnhnQh6I9YiJnJi-_sDfiAwb7n-sN2EJiVL_JqdBltYRpKVvWg2fCwr7OFl9y0OpZ9rPoO8X23BBhoSWEnPKVnK3FVrt6y2OQBK6dYa5IuDro1rMyg78L6SbkY3hhsrCYE3Gjn86YwWV-1Nqorl67gEUZvztLw2JSMJIZyjH1LX7wTOCSC2y-HOBTKtI0huLmJrvvvOr0zywd2J-1JbSpV0eB1YfKtXpgjCgJu4ofxPsik5Q70XfxFCLpGC43k64AjOb35CzlETJTYzEaw4oCdgVmkW-mt_H6lmdfiv37ZUWPIv4EhBJ8RSMmQgcCuRwwGQMYvuV8n1YPNVWFOC5PDZgT4MVgYk1i5OxgFmd0REO5v2KiDr4rxNN3hIVzi6ZoExEmnCKsOPNwFNpEjgrDOC-GMaCqrM738d73jbAKn3ErijbT2TGERX4fA-nj3RMbuLkFJrWS_cqW5FC5RtyHx1gr3SaeaULQrPdTuossKnaP9ejdyvbhYFsOLhTxQV-rpqeprGPkS5ADBJJ--QI8QDz95gJb66OvhVw_A4gWP6qNbtaVFO10VyaJE3TUq0RE6koyyzL8uUh2nIsQv6ARQqFxILv2nIpy2LT23oM526RsAr7gS79SP_vwveyNviKjcNjW5q8yF45UtAaFME3jQPEeMuBXJJLhNeIvuftOCMWuBNCmnSJqIJr7eUyB-WpSe1iK52g9gt4eSrTTgRKjGBqGacqokPCe1ORNESQ8Y6qedUJhSRWGak6U0kkSf-aW8nF31w5wcDQyjkBmM3MK2u_fan2QpTsu64LLLBlsodkLnB9cT1q-tIxqRGxBPIUbv_e3SJChGf78Hdxb2YbSX2zB0PkBvzH2UcWGwa--RJJLbvknUrLANUJ8zAKmmFwwQJAhpRn4UDTq96flXCENmpMe5HnLSpB0YRarESBQZRJ1SOMuLCtbMqBCpISs4pMbpX4ciZFOCXL7RjmGctuDC2plIpoIEpXtXwnbns-ZNzqSHJ9kEpanWKCP2SpMaE1Be47xt7318t5ynkt-riEy-nAlsI94QhhozRxx7cUfDpBEZD00XWJ346Cx3PR7WT0qbxUQ-glLkNvJNZCpRTcD8Ac7xYGE7yLtPIeNf9DL-Gc-nNDO22YvtBIdnNpRsPTFNcb6MHvpG-uPAez_tUeChPSF0hy0azaQBG5MyPR-k_WQ5IVcoTkqwxmQ2JVyAsIu0ASj39fAxfcYyamgjoirM3vuOuraxgogP_9ZTTfTzQbbZqfIR8GoRHrz--2H4ZWawin0NnggnQscTMiMwxXZVvzZ_PxZ6VDNQwP6sxlHQewXe4GbrRC6WS2hfd1oK4cU2857WjQf_CRmyxMEEUGshTN2Ou7BvZQIafV_aPP5-d1bQ16UemS_MGPwn4DmuDjs2bsaPpIE27ISTm1xg3omF1lWKHx3wZ3-OLdBm_M9s0sI__ObEQKjqUEXsJwqN4EO0L7q6zaPjPmSrh_W30o700NbqpYUH0v-7mqE8EArXBmn2rdmgFG6z9P0t7HGsVlR7p_apYbx1IqQcpwNIaq4CzssYxiF3koMv-G2oA5iIy2xJERHlsay0C0JD1RIFl2QMKo_WiOC3wo6-MvRBa5J_rD9OCvMFIGO0Pz5pHw7626Gllz7jscQ1NnNIEApHSEQNu6lEKLxMPiyV7QL30Kuuwawf5zXw3oUSRPb1c7qKkYzviaozDyhKrIIymWVMdDrDqyHV8h1Kank5Jci3PYmmFZ3RmdxUGPTszmC0ZJGussLtJUeQV0kl_9Vfj0uTqQS9xKrfMGDzG3ajs1Yc9vbanmclmcPysbWG4QlLw7s9EX_oVF9qEfMmpCmTsAWttV486oiIAu3N3BcboNik5XRT1vUS3rO6J1Zxih8OevIBp-PMsuYfTriUhFAKHM8NzLGQGfaU3vJzhEkL6syrPyZtKpJoNvbD_fzeQqok1EZGfY8_xkybdb9qCXdMmiO2WHqdsAS2OF1AIgg6OZS3lrmt6JyhLHD6Rt7QlTCeMZq1zbzGawmZZTRriusG4WfdfE1ewYx84O7WJsIeCYkSSQiyPTPSgPgOXWs9hf9hI8FGWG9tXMAjA-1JZeYd1Oe6ze-c7iBNYV7zQKEnQELvBnmkGqLGcyvgblnnzZtK5782ulxoFuzyjtIpkn_IVBzuMBDcIxjoq8iLy8oi_A8guWWkLRBtcXqOnsFkHA5jLXymVwkJU-PhKunFdoK0WDEBataqdiR_N3u3HtI2RYYXf5iBRakpCe1OAAQlMzmarVVNQ9-Yn4VFJjDDviGxbaKoDCxZWEvgyP2ThlmSHutlbmuHdg3VkNq9pFsXh-KhrU-IhRFVxanBtKC5DtUE1V1xJ5zOpmhbBLI1XzIbFNPmntQI6gJBHAdsW1f8ggThdOyV4qUsbbys3uyMMF6aAaH4MQC-AcVtERqX4rGGUhKIW9n_scKxFG1y4F5rRXI1P9mWmseqf36PmYS-SFXv-3xE_CorUMhbe4H1Fi6QoAJBj_18ZQ-XtkoTdRZsEpTsGGYkT_J2u5er5E1prokEa8Mf4QX32CyI8hAG14KdvzocW4ipu1fHlYew2aE9wGmIu0DP7XT6AMy5jt_d8cH5L2wUDJqm0lQMx6oF7EXBqjNL9kT-XEHzbjrUxxgGS1G41ebqnue7oqpNtjbeGVgXMk2WHuIYdw3OYWFiVbo2fnXDpa5X99OfRl8lRcKG5lU2QOUVXxcWa1Na_AvjmZxY-MUcI-1z38iRxvYxP6bcT6i6JeHoxi4f8Zmoc6_nrmkeyE-iNZd5e_HTE-kTJyxyDMJmImCD6ut0lpY_mGf80-dJbGyYzq_b-N_Z9kdHPZhqWu1ymAXKhY6jPL4NRoBYZKal_lyvW9v4x3gqMlHgY5i4CITDjTi7qxEPf1bX26NtC2VHCi0NGDeexREyt5VRruFS6FqY65hK7jUNAaNl3Ael34l-LKX0IbjHnWlFHCFqk06F_QNYa77I7U9pPhLTcgHgrSdWLLdvdsA69t2tnmKA4MjG7oPbCdhtuRM9fq3eX9MWoEF17CoOm1a4pdFLnyfvm9PkTSXkJEC8Qgm_3VEpDlXyVfdW7bO7NpI3Mm5SQJ3kqDlvIODoKJJY-t4mbDQBp-qI6avssbA3sjiqePHa95AaEMZGEeG_BLYP1es31tQOrXtzu0rpY6wyjV4zQ_vLg83eUkl2MwCRhJC9yozPSRAjzpCR5xxPRNPLTerFFDJUZh_XQuXBlpM2wf90vczIVrhmbLDSxCIasAJIfAaEneT_T9q6ITPmjXFA1lpo4ofXejD5s35M1J61_76Bj8Xgu06WnJgp2OeqHjIqm40ims_B2sMdZaoVWqkEyVQQ-IpypHX3DVS2IKLdJ8DyZdOUYNVNAValzIIgzOlJV4BgQhOYanIzoCbrV_ao9zomOlCzWErWAy4aVzuBaItpCYakRgpvv3wkEIqlVuLyMW2ra15lZmx08_8rFWrvc5qlK3JlsDtoIDqPQW1-3dE9Y30m5VIrAlwvJS5wx-Q_dJv4OaQtgIwvOiGdE7ESSCmPvk8gdMAvXgH7w8tV-QcWkCiqRxF6ae_ppKOPKYQB_Dih8byIPhV2sWQPMmWP80oftWYpd9TtNqTJajfB8BFtHrQvhI_LNDyORZiRnS_qGEeyI93wpmafyd9NkKfzs3M4IN-IEaq0nSBqX7MaxI1cKJ3R1G0ln-rGH02-svqi6aHw9y6rb5vmgUkNNfnEiQC2NvOUmn90GU4XQlI5Lgh4hDGdbrXsPfeYssaaWIkJ6Uja13xMzwGMXhykLJi9C4yiu1JqQFUcyeFNllFOVCDvbR2967yGhhswLo4QjaX5mA8b2iup1_SGDF0CxWTqq0VjzqNSaKx0kh8l63VVf-svUxd7_F10meHS7qvHJRSKr17yrTqxQoLStE9wIC2iWGUnoMhwfhn1zdutB9W9qibLvPb_D8sLM7H2qst3mStiH1AuGe1qYltYJLWr0vIgJgR9aBONoBqOQia2CsY9KBEkkI_dhiw-LZjI3pUNU6FqvKpYluU3KJla9AwIYCT3hxpC5lUIHVqLikOL5h9aAyMbTKexPifxLQU7j1YPZyfz603NCAwO6VQUXlYrypc5HQJS5iOO7uFFPSBL_IYTm2zl8BRwpYu3SLScNq0Vgd3PVlmpVKXki1lI1VoHy0CkXn8JULfd9sb5PnAAcTITn8_XWl8WXxGV4ZQha6xcRzS76Vo6lqPGrwz0_WU0icVegIUaD6xUnKK8-dad2NgxXDMcwREAzpoOFuufo7i3IRUlmlSqkvV8vBwi2qPtGn04ARRdionabwTL3vG6hWlcyLaYK9jVLjW08b_QdWxcbHkzgpI-bWzxHPpZQusN55hkhMXrd97wLTgr-Ox98mrgKC4WdwOivWOWus9hrd9t9RLw_u2-7VKLeEx8-rWgWLNgxsxswPqHh5cU_ru1o46VywHJtDYc80ZiMPahxjg=","captcha_solution_decision_seconds":3,"meta":{"user_agent":"Mozilla/5.0 (Linux; Android 15; Pixel 7 Build/AP4A.250205.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/147.0.7727.137 Mobile Safari/537.36","ip":"127.0.0.1","audit_source_type":"Backend","js_enabled":true,"cookies_enabled":true,"language":"ENG","browser_page_resolution":"1x1"}}
```
- **Response Headers**:
```http
Date: Tue, 12 May 2026 09:25:23 GMT
Content-Type: application/json
Transfer-Encoding: chunked
Connection: keep-alive
access-control-allow-origin: *
access-control-expose-headers: X-Request-Id
vary: Origin
x-request-id: 063aea7e-0413-4f29-811c-3739bab90ffa
cf-cache-status: DYNAMIC
Content-Encoding: br
Server: cloudflare
CF-RAY: 9fa86036c86079e6-HYD
alt-svc: h3=":443"; ma=86400
```
- **Response Body**:
```json
{"auth_token":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYXV0aCIsImV4cCI6MTc3ODU3OTcyMywiaWQiOiJmOWEzMjM5Ny01MGI5LTRkNmYtODhhYi1lNWEzZjY5Y2ExZGIiLCJtb2JpbGUiOiIrMzkzNzIwNTEzODA1IiwiZGV2aWNlX2lkIjpudWxsLCJkb25lIjpudWxsLCJjdXJyZW50IjpbIm1vYmlsZV9vdHAiLCJvdXRfb2ZfYmFuZCJdLCJtZXRhIjp7InVzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgMTU7IFBpeGVsIDcgQnVpbGQvQVA0QS4yNTAyMDUuMDAyOyB3dikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzE0Ny4wLjc3MjcuMTM3IE1vYmlsZSBTYWZhcmkvNTM3LjM2IiwiaXAiOiIxNTIuNTkuODYuMTQ3IiwiYXVkaXRfc291cmNlX3R5cGUiOiJCYWNrZW5kIiwianNfZW5hYmxlZCI6dHJ1ZSwiY29va2llc19lbmFibGVkIjp0cnVlLCJsYW5ndWFnZSI6IkVORyIsImJyb3dzZXJfcGFnZV9yZXNvbHV0aW9uIjoiMXgxIn0sImlzX2FkZGl0aW9uYWxfc3RlcF9uZWVkZWQiOmZhbHNlfQ.eT9cXOIIrx4hm64btWC79olb8ObVuYGf8vVsJuzas-eFv0Qx3EVI0kT3stRbnFLlisLrInfB7uhnd8q0nxJHfDK_296YVq1dZ-XTeSOWkOLs-N1HiZAGBrSymH292wt8QBtp5GIFAaQH_u2mAWLdEBl5kNIFPU8cRTThi5AhnjhJ8BYsZtuBCvAalI-SA5MgkY7EZ7W_L56sgsMvCSuCvoWXZMGu8Ws5cOZ5xqBWWjoSMwAWuZKOUDjWsvEXicK0OMeYz6xdSMOnxJMIMu8iauv20kkkqdhbP88hDWZICz8B5cV_EkiA1D19FoerjM125-ufxlb_HvjBRCitGvg68SCuNieWv-kyOgVJ0zxci746DzIAPEst0EUv7mkz8Izxtb0nY_WbKS_RO1LbI48YLeFBEU5dBqnRxcCVepKu13Sh0gTBqi6yCoFqMzIDVethHlcNx3CW5CUOyPqFsRFDJY6nwssalo47qXUc6mmVLQtgOho7uM9gVONVZgtMKFeZj9SNo5YdMRgGT62ZfeTZeLQ3inz9L2KKQh0nGrB7mFLENuNs_SvtZ2sy2adznaV7sKV_kOF_V-zXZPhnkRJ6mI8JDfhUAcLUCEGHUbBR6I88OKrrAI72cnfOViuoM4wzqCebb0EjWczDYkPpuskSMlnP-S_mO2Eso04-YHIbuS8","challenges":["mobile_otp","out_of_band"]}
```

**Step 3: Verification Status Check**
- **Endpoint**: `GET https://api-auth.wallester.com/v1/sign-in/challenge?type=mobile_otp`
- **Purpose**: Checking OTP generation attempts and status.
- **Request Headers**:
```http
Host: api-auth.wallester.com
Connection: keep-alive
sec-ch-ua-platform: "Android"
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYXV0aCIsImV4cCI6MTc3ODU3OTcyMywiaWQiOiJmOWEzMjM5Ny01MGI5LTRkNmYtODhhYi1lNWEzZjY5Y2ExZGIiLCJtb2JpbGUiOiIrMzkzNzIwNTEzODA1IiwiZGV2aWNlX2lkIjpudWxsLCJkb25lIjpudWxsLCJjdXJyZW50IjpbIm1vYmlsZV9vdHAiLCJvdXRfb2ZfYmFuZCJdLCJtZXRhIjp7InVzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgMTU7IFBpeGVsIDcgQnVpbGQvQVA0QS4yNTAyMDUuMDAyOyB3dikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzE0Ny4wLjc3MjcuMTM3IE1vYmlsZSBTYWZhcmkvNTM3LjM2IiwiaXAiOiIxNTIuNTkuODYuMTQ3IiwiYXVkaXRfc291cmNlX3R5cGUiOiJCYWNrZW5kIiwianNfZW5hYmxlZCI6dHJ1ZSwiY29va2llc19lbmFibGVkIjp0cnVlLCJsYW5ndWFnZSI6IkVORyIsImJyb3dzZXJfcGFnZV9yZXNvbHV0aW9uIjoiMXgxIn0sImlzX2FkZGl0aW9uYWxfc3RlcF9uZWVkZWQiOmZhbHNlfQ.eT9cXOIIrx4hm64btWC79olb8ObVuYGf8vVsJuzas-eFv0Qx3EVI0kT3stRbnFLlisLrInfB7uhnd8q0nxJHfDK_296YVq1dZ-XTeSOWkOLs-N1HiZAGBrSymH292wt8QBtp5GIFAaQH_u2mAWLdEBl5kNIFPU8cRTThi5AhnjhJ8BYsZtuBCvAalI-SA5MgkY7EZ7W_L56sgsMvCSuCvoWXZMGu8Ws5cOZ5xqBWWjoSMwAWuZKOUDjWsvEXicK0OMeYz6xdSMOnxJMIMu8iauv20kkkqdhbP88hDWZICz8B5cV_EkiA1D19FoerjM125-ufxlb_HvjBRCitGvg68SCuNieWv-kyOgVJ0zxci746DzIAPEst0EUv7mkz8Izxtb0nY_WbKS_RO1LbI48YLeFBEU5dBqnRxcCVepKu13Sh0gTBqi6yCoFqMzIDVethHlcNx3CW5CUOyPqFsRFDJY6nwssalo47qXUc6mmVLQtgOho7uM9gVONVZgtMKFeZj9SNo5YdMRgGT62ZfeTZeLQ3inz9L2KKQh0nGrB7mFLENuNs_SvtZ2sy2adznaV7sKV_kOF_V-zXZPhnkRJ6mI8JDfhUAcLUCEGHUbBR6I88OKrrAI72cnfOViuoM4wzqCebb0EjWczDYkPpuskSMlnP-S_mO2Eso04-YHIbuS8
User-Agent: Mozilla/5.0 (Linux; Android 15; Pixel 7 Build/AP4A.250205.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/147.0.7727.137 Mobile Safari/537.36
Accept: application/json, text/plain, */*
sec-ch-ua: "Android WebView";v="147", "Not.A/Brand";v="8", "Chromium";v="147"
Content-Type: application/json
sec-ch-ua-mobile: ?1
Origin: https://client.wallester.com
X-Requested-With: com.wallester.whitelabel
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en,en-IN;q=0.9,en-GB;q=0.8,fil-PH;q=0.7,fil;q=0.6,en-SG;q=0.5,nb-NO;q=0.4,nb;q=0.3,sv-SE;q=0.2,sv;q=0.1,gsw-CH;q=0.1,gsw;q=0.1,en-US;q=0.1,de-DE;q=0.1,de;q=0.1,ja-JP;q=0.1,ja;q=0.1,da-DK;q=0.1,da;q=0.1,fi-FI;q=0.1,fi;q=0.1,nl-NL;q=0.1,nl;q=0.1,ko-KR;q=0.1,ko;q=0.1,zh-CN;q=0.1,zh;q=0.1,it-IT;q=0.1,it;q=0.1
```
- **Response Headers**:
```http
Date: Tue, 12 May 2026 09:25:24 GMT
Content-Type: application/json
Transfer-Encoding: chunked
Connection: keep-alive
access-control-allow-origin: *
access-control-expose-headers: X-Request-Id
vary: Origin
x-request-id: 299f3907-1559-49a9-8594-dcd0c362cb78
cf-cache-status: DYNAMIC
Content-Encoding: br
Server: cloudflare
CF-RAY: 9fa8603b1d1179e6-HYD
alt-svc: h3=":443"; ma=86400
```
- **Response Body**:
```json
{"masked_mobile":"*******3805","attempts_left":6,"next_attempt_after":60}
```

**Step 4: Verify OTP**
- **Endpoint**: `POST https://api-auth.wallester.com/v1/sign-in/challenge`
- **Purpose**: Checking the received OTP code.
- **Request Headers**:
```http
Host: api-auth.wallester.com
Connection: keep-alive
Content-Length: 38
sec-ch-ua-platform: "Android"
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYXV0aCIsImV4cCI6MTc3ODU3OTcyMywiaWQiOiJmOWEzMjM5Ny01MGI5LTRkNmYtODhhYi1lNWEzZjY5Y2ExZGIiLCJtb2JpbGUiOiIrMzkzNzIwNTEzODA1IiwiZGV2aWNlX2lkIjpudWxsLCJkb25lIjpudWxsLCJjdXJyZW50IjpbIm1vYmlsZV9vdHAiLCJvdXRfb2ZfYmFuZCJdLCJtZXRhIjp7InVzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgMTU7IFBpeGVsIDcgQnVpbGQvQVA0QS4yNTAyMDUuMDAyOyB3dikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzE0Ny4wLjc3MjcuMTM3IE1vYmlsZSBTYWZhcmkvNTM3LjM2IiwiaXAiOiIxNTIuNTkuODYuMTQ3IiwiYXVkaXRfc291cmNlX3R5cGUiOiJCYWNrZW5kIiwianNfZW5hYmxlZCI6dHJ1ZSwiY29va2llc19lbmFibGVkIjp0cnVlLCJsYW5ndWFnZSI6IkVORyIsImJyb3dzZXJfcGFnZV9yZXNvbHV0aW9uIjoiMXgxIn0sImlzX2FkZGl0aW9uYWxfc3RlcF9uZWVkZWQiOmZhbHNlfQ.eT9cXOIIrx4hm64btWC79olb8ObVuYGf8vVsJuzas-eFv0Qx3EVI0kT3stRbnFLlisLrInfB7uhnd8q0nxJHfDK_296YVq1dZ-XTeSOWkOLs-N1HiZAGBrSymH292wt8QBtp5GIFAaQH_u2mAWLdEBl5kNIFPU8cRTThi5AhnjhJ8BYsZtuBCvAalI-SA5MgkY7EZ7W_L56sgsMvCSuCvoWXZMGu8Ws5cOZ5xqBWWjoSMwAWuZKOUDjWsvEXicK0OMeYz6xdSMOnxJMIMu8iauv20kkkqdhbP88hDWZICz8B5cV_EkiA1D19FoerjM125-ufxlb_HvjBRCitGvg68SCuNieWv-kyOgVJ0zxci746DzIAPEst0EUv7mkz8Izxtb0nY_WbKS_RO1LbI48YLeFBEU5dBqnRxcCVepKu13Sh0gTBqi6yCoFqMzIDVethHlcNx3CW5CUOyPqFsRFDJY6nwssalo47qXUc6mmVLQtgOho7uM9gVONVZgtMKFeZj9SNo5YdMRgGT62ZfeTZeLQ3inz9L2KKQh0nGrB7mFLENuNs_SvtZ2sy2adznaV7sKV_kOF_V-zXZPhnkRJ6mI8JDfhUAcLUCEGHUbBR6I88OKrrAI72cnfOViuoM4wzqCebb0EjWczDYkPpuskSMlnP-S_mO2Eso04-YHIbuS8
User-Agent: Mozilla/5.0 (Linux; Android 15; Pixel 7 Build/AP4A.250205.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/147.0.7727.137 Mobile Safari/537.36
Accept: application/json, text/plain, */*
sec-ch-ua: "Android WebView";v="147", "Not.A/Brand";v="8", "Chromium";v="147"
Content-Type: application/json
sec-ch-ua-mobile: ?1
Origin: https://client.wallester.com
X-Requested-With: com.wallester.whitelabel
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en,en-IN;q=0.9,en-GB;q=0.8,fil-PH;q=0.7,fil;q=0.6,en-SG;q=0.5,nb-NO;q=0.4,nb;q=0.3,sv-SE;q=0.2,sv;q=0.1,gsw-CH;q=0.1,gsw;q=0.1,en-US;q=0.1,de-DE;q=0.1,de;q=0.1,ja-JP;q=0.1,ja;q=0.1,da-DK;q=0.1,da;q=0.1,fi-FI;q=0.1,fi;q=0.1,nl-NL;q=0.1,nl;q=0.1,ko-KR;q=0.1,ko;q=0.1,zh-CN;q=0.1,zh;q=0.1,it-IT;q=0.1,it;q=0.1
```
- **Request Body**:
<!-- OTP code submitted for verification -->
```json
{"type":"mobile_otp","value":"333333"}
```
- **Response Headers**:
```http
Date: Tue, 12 May 2026 09:26:09 GMT
Content-Type: application/json
Content-Length: 19
Connection: keep-alive
access-control-allow-origin: *
access-control-expose-headers: X-Request-Id
vary: Origin
x-request-id: a17185c2-528c-454c-9041-f218d6c7499f
cf-cache-status: DYNAMIC
Server: cloudflare
CF-RAY: 9fa86151b9bc79e6-HYD
alt-svc: h3=":443"; ma=86400
```
- **Response Body**:
```json
{"attempts_left":4}
```

## 4. Security & Reversing Notes

### Bot Detection & Captcha
- **Friendly Captcha**: The application uses the Friendly Captcha (eu.frcapi.com) service. The captcha solution `captcha_solution` must be submitted alongside the mobile number during the `/v1/sign-in` step.
- The `meta` block contains fingerprinting data, including user-agent, IP, and local settings. If the captcha is missing or invalid, the API rejects the request with HTTP 422 `{"message":"Unprocessable Entity","error_code":90810,"error_text":"wrong CAPTCHA result"}`.

### Flow Mechanisms
- A bearer `auth_token` is generated from the `/sign-in` step and is used to authenticate further requests such as OTP verification.
- Rate limiting or maximum attempts tracking is handled server-side, returning the current count of `attempts_left` on each failed OTP verification attempt.

## 5. Conclusion

### Automation Feasibility: Medium 40-70%
The application leverages a standard JSON-based API interface with no device encryption payloads. However, to fully automate the OTP transmission, a valid Friendly Captcha solution is required. If a mechanism to programmatically fetch and solve Friendly Captchas is available, automation of this SMS flow is highly feasible due to the lack of other intricate security components.
