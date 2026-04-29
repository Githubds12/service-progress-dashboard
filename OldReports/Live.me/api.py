import requests
import json
import time

def send_sms(phone_number, country_code="39", country_iso="IT"):
    url = "https://iag.liveme.com/2/cgi/sendsms"
    
    headers = {
        "User-Agent": "okhttp/4.11.0",
        "Connection": "keep-alive"
    }

    # Multipart boundary from the HAR
    boundary = "3i2ndDfv2rTHiSisAbouNdArYfORhtTPEefj3q2f"
    headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"

    payload = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"client_channel_1\"\r\n\r\n"
        f"android\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"client_channel_2\"\r\n\r\n"
        f"web\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"cmversion\"\r\n\r\n"
        f"49252624\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"length\"\r\n\r\n"
        f"4\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"mobile\"\r\n\r\n"
        f"{country_code}{phone_number}\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"need_slide\"\r\n\r\n"
        f"2\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"geo\"\r\n\r\n"
        f"IN\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"itc\"\r\n\r\n"
        f"{country_code}\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"ver\"\r\n\r\n"
        f"4.9.25\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"type\"\r\n\r\n"
        f"5\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"lm_s_str\"\r\n\r\n"
        f"f288ab5d2c61067e62b27d8bc2739e3b\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"lm_s_ver\"\r\n\r\n"
        f"1\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"alias\"\r\n\r\n"
        f"\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"devid\"\r\n\r\n"
        f"80b67980e5c38193\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"lm_s_id\"\r\n\r\n"
        f"LM6000101139961122666757\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"lm_s_ts\"\r\n\r\n"
        f"{int(time.time()*1000)}\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"deviceid\"\r\n\r\n"
        f"80b67980e5c38193\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"client_country_code\"\r\n\r\n"
        f"{country_iso}\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"devtype\"\r\n\r\n"
        f"android\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"tongdun_black_box\"\r\n\r\n"
        f"rGPU51777449570XWBOPMdUtN1\r\n"
        f"--{boundary}--\r\n"
    )

    try:
        response = requests.post(url, headers=headers, data=payload)
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        return response.status_code, response.text
    except Exception as e:
        print("Error:", str(e))
        return None, str(e)

if __name__ == "__main__":
    send_sms("3382289898")
