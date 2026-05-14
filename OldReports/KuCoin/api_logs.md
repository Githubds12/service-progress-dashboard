# KuCoin API Logs

## 1. Check User Account
```text
POST https://appapi-v2.xcoinsystem.com/app/v1/auth/check-user-account
Headers: {
  "X-APP-VERSION": "4.24.0",
  "X-APP_ID": "com.kubi.kucoin",
  "token_sm": "BtibO20dIgoWjn3eP0NJZu980PIFmr6TVnEFZdIgIlq3w+B+Jdy+kutOGCN/lRjK..."
}
Body: account=91-8791267460
Response (200): {"success":true,"code":"200","msg":"success","retry":false,"data":false}
```

## 2. Captcha Required (Error 40011)
```json
POST https://appapi-v2.xcoinsystem.com/app/v1/auth/validation-code
Body: {"channel":"SMS","loginToken":"","receiver":"+91-8791267460","validationBiz":"REGISTER"}
Response (200): {"success":false,"code":"40011","msg":"reCAPTCHA or GeeTest required.","retry":false,"data":null}
```

## 3. Captcha Validation
```text
POST https://appapi-v2.xcoinsystem.com/app/v1/auth/captcha-validation
Body: bizType=PHONE_REGISTER&captchaType=GEETEST&response=%7B%22captcha_id%22%3A%22d8a78f9ef7db4fcf864cfd257a728e39%22%2C%22lot_number%22%3A%22c3efb8648d8148a1bc9bb0c41f37b109%22%2C%22pass_token%22%3A%22ee005690c9c85d1afd7d2efc81a2654e5e7daf1442723cc1f2011928685d8660%22%2C%22gen_time%22%3A%221777288711%22%2C%22captcha_output%22%3A%228JNNelbm2j8YqQkdSJB_rFDNDPmdJqBc5AERug4...%22%7D&secret=d8a78f9ef7db4fcf864cfd257a728e39
Response (200): {"success":true,"code":"200","msg":"success","retry":false,"data":null}
```

## 4. OTP Verify
```json
POST https://appapi-v2.xcoinsystem.com/app/v1/auth/verify-validation-code
Body: {"bizType":"REGISTER","receiver":"+91-8791267460","seq":1,"validations":{"SMS":"449935"}}
Response (200): {"success":true,"code":"200","msg":"success","retry":false,"data":null}
```

## 5. Sign Up
```text
POST https://appapi-v2.xcoinsystem.com/app/v1/auth/sign-up
Body: password=910c7b07a7e92470fa5cd730cc21da62&utm_campaign=&referralCode=&userName2=&timeZone=19800&userName=%2B91-8791267460&userAccountType=PHONE&utm_source=GOOGLE&anonymousId=410e33d01629a331&userTermSubRequests=%5B%7B%22termId%22%3A%2247185419968079%22%7D%2C%7B%22termId%22%3A%2247497300093764%22%7D%5D&registerFlagRequests=
Response (200): {"success":true,"code":"200","msg":"success","retry":false,"data":{"id":"69ef462616150500016afeb6","uid":255882134,...}}
```
