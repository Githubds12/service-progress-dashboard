import requests

url = "https://api-base.soulchill.live/api/session/sendVerifyCode"

headers = {
    "User-Agent": "SoulChill/4.24_b2604233 Android/4252 (Pixel7; Android 15; en; google; Gapps 0)",
    "Content-Encoding": "gzip",
    "fr": "ba9aeb5b148803764a3da68cad2f7e062e622b35",
    "isEncryption": "true",
    "x-req-compress": "gzip",
    "Content-Type": "application/x-www-form-urlencoded"
}

def trigger_sms(mzip_payload):
    # This payload is encrypted and compressed
    print("[*] Attempting to trigger SMS with encrypted payload...")
    try:
        response = requests.post(url, headers=headers, data={"mzip": mzip_payload}, timeout=10)
        print("Status Code:", response.status_code)
        print("Response (Encrypted):", response.text[:100] + "...")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    # Example encrypted payload from HAR
    trigger_sms("IpnQAJ6i9BpfuhzDeKv87Isfxu+zrfOolPafyI1qBvEVczCXzVmkiy2yU4i9utQ0MJ9EZhdazEdRShUfrOxR/1D1HlGPPxQDuIpDpSErNZi0ItxplhKsFISvBuNZw7yMz+Pwnb88Nt/bkmRgCVfxpfaYpKNyOEYaropCX3ZIEE0a/o4OMawndnVtxw2HRq0iqiH023g56jceryVV6Pk3pqW3+Qx0f5UTEblYEMAXr/Y=")
