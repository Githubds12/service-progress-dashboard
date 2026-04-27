# iHerb API Logs

## 1. OTP Send Request
```json
POST https://checkout2.iherb.com/auth/api/otp/send
Headers: {
  "Content-Type": "application/json",
  "g-recaptcha": "0cAFcWeA4AqdlP24gpvrQyB5kJ3JKxoCQYA9gIrLOErFvCKuWc...",
  "x-application-id": "androidglobal:12.4.0416:2",
  "deviceuuid": "3dcdbde3-efea-4baa-8ebe-32419c0c0a19"
}
Body: {
  "username": "+918791267460",
  "claim": "registerMobile",
  "mobileCountry": "IN"
}
Response (200): {}
```

## 2. OTP Validate Request
```json
POST https://checkout2.iherb.com/auth/api/otp/validate
Body: {
  "username": "+918791267460",
  "claim": "registerMobile",
  "code": "663349",
  "mobileCountry": "IN"
}
Response (200): {
  "state": "CfDJ8ApAsakMnoZEq0_E73QEzD9pVVLG_4S9KbDQxGK_rin5Gi__YOZTkGCT7W-P3Eqn5r9thyqTE6FUCLM15qig_0RF6Fu6iq3UvB9SOYz8xhEpAm1fzR_5aU9_dJ-awOwCEyX2YMhiMOfjICY5JwQhD3ofwpzBjWujyVAq7jpUqgR9ekTjY0YMnV3JQb6kIqdf_FtiIQCNac69q8hXTsqoSLm2WtEAEZT0ehWIEkj7-H4uhQLVTQ2aZ1RqvFI7MxJsZvLxvd6V9HuhHN1hsP7VSHsdg0-w1eYPs_rrjQ9k9K6zFtPC45iNNhxT8sPKsDy7A5FkbVIRT9rGwOGDIYC7kPmIyLHdXnch7iSETFIB2nOgOQWa21Jsd1x4NuWaowYlD2S5j6wBXnv26-U9JpEUSJ5NpwFOUoZ3-FSQg4qWq0Tue9dm5y0a1L8rpB7EdDZFcyEuQz2PYMFckqh35FQJ7avnLy2aOEsIxlZAl3..."
}
```

## 3. Register Request
```json
POST https://checkout2.iherb.com/auth/api/register
Body: {
  "username": "+918791267460",
  "password": "Facebook@ds12,",
  "isSubscribe": true,
  "mobileCountry": "IN",
  "state": "CfDJ8ApAsakMnoZEq0_E73QEzD9pVVLG_4S9KbDQxGK_rin5Gi__YOZTkGCT7W-P3Eqn5r9thyqTE6FUCLM15qig_0RF6Fu6iq3UvB9SOYz8xhEpAm1fzR_5aU9_dJ-awOwCEyX2YMhiMOfjICY5JwQhD3ofwpzBjWujyVAq7jpUqgR9ekTjY0YMnV3JQb6kIqdf_FtiIQCNac69q8hXTsqoSLm2WtEAEZT0ehWIEkj7-H4uhQLVTQ2aZ1RqvFI7MxJsZvLxvd6V9HuhHN1hsP7VSHsdg0-w1eYPs_rrjQ9k9K6zFtPC45iNNhxT8sPKsDy7A5FkbVIRT9rGwOGDIYC7kPmIyLHdXnch7iSETFIB2nOgOQWa21Jsd1x4NuWaowYlD2S5j6wBXnv26-U9JpEUSJ5NpwFOUoZ3-FSQg4qWq0Tue9dm5y0a1L8rpB7EdDZFcyEuQz2PYMFckqh35FQJ7avnLy2aOEsIxlZAl3Fk3otzGXOOxc6BxprAUynhkKzORg"
}
Response (200): {
  "redirect": "/auth/connect/authorize/callback?redirect_uri=..."
}
```
