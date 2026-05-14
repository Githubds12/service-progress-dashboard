import json
import sys

har_path = r'c:\Users\Gorri\Documents\Reports\Grab\Grab.har'
output_path = r'c:\Users\Gorri\Documents\Reports\Grab\Grab_fixed.har'

with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Request body provided by user
req_body = {
    "adrID":"3346dff226996b4a",
    "adrIMEI":"3346dff226996b4a",
    "adrIMSI":"",
    "adrMEID":"",
    "adrSERIAL":"unknown",
    "adrUDID":"18a64fb3-79ce-441b-8c1f-680134e7b745",
    "advertisingID":"f51ee336-e489-4882-8c21-95ff06ed4a9a",
    "applicationVersion":"5.408.0(54080000) Build ; Build 151667694",
    "cellularOperator":"",
    "challengeID":"700a4967-985e-48d3-a82a-739563b154a7",
    "cli":"",
    "countryCode":"IT",
    "deviceManufacturer":"Google",
    "deviceModel":"Pixel 7",
    "hints":"newAccount",
    "iosUDID":"",
    "latitude":1.361216711,
    "longitude":103.989443071381,
    "otp":"333333",
    "otpAutoFilled":False,
    "phoneNumber":"393720513142",
    "scenario":"signup",
    "snaCarrier":None,
    "snaChallengeID":None,
    "snaErrorDescription":None,
    "snaExecutionCode":None,
    "snaToken":None,
    "source":"android2",
    "sourceID":"",
    "tmSessionID":"",
    "tpToken":{
        "type":"Google",
        "value":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjgwNzZkZGJhYjQxNTU1NmUxNjkxNTRjNmE0YTBiZGJkNDQ2OWI3OWMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIxNDEyNTUxMTM5NzMtMWNybHBucDFkZnJhbmluaGpmNmJ1bDljNDhnbDZzYTYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiIxNDEyNTUxMTM5NzMtazNzY2l1Nzl0NWM1MXJuajloZmp0MmhhcHMwNDM2Z2ouYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTY1OTc2MTM3Njk0MDIxMzIwMzIiLCJlbWFpbCI6ImRlZXBhbnNodXNpbmdoZGlnaXRhbGhlcm9lc0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkRlZXBhbnNodSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NKdS1rWmRfX3g1aDBnZWk2NGVDYUczaEpYdUs5U3pnSi1DWFk2VmhFTktfdkQzaUE9czk2LWMiLCJnaXZlbl9uYW1lIjoiRGVlcGFuc2h1IiwiaWF0IjoxNzc4NTY2MzkwLCJleHAiOjE3Nzg1Njk5OTB9.t6QJv59TnTSmYX0INXJ4n4JZlrfwo8jVQ6uUmlMMzR8E7RWMNW18SctjDiaMjl4r-ZLzugE2p8_crSamCIxS9ew53r6A7qM9S3S2bwncRa_yZhG7fSYtcxznC1muZS6eqe2e9_f8ApIt8FOk2aanwHzWmkbQBAvuqhx6qf7gu_wnlZ_yJUR1I4xonfUZaVeezNcCTUkvcqLt_Jwz0zaD8xj0qSLaO0kc6wlgJPImdx_Uu2mMrpd2uhlyCz7Q8z7wkT-zCf4Ft1uShsqkQpipMBcnj38WyQrC4EDNvXduSoBKfueLBZGIOgEaN48D6SQMtNfE_ac23-C79JgcgNqdqg"
    }
}

# Response body provided by user
res_body = {
  "errors": [
    {
      "code": 16000,
      "message": "Something went wrong and we can't verify the code. Try again later.",
      "details": {
        "numAttemptsLeft": 2
      }
    }
  ]
}

# Find the entry (it was around index 688)
entry_index = 688
entry = data['log']['entries'][entry_index]
print(f"Modifying entry: {entry['request']['url']}")

# Update request
entry['request']['postData'] = {
    "mimeType": "application/json",
    "text": json.dumps(req_body)
}

# Update response
entry['response']['content'] = {
    "mimeType": "application/json; charset=utf-8",
    "size": len(json.dumps(res_body)),
    "text": json.dumps(res_body)
}

# Save fixed HAR
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Saved fixed HAR to {output_path}")
