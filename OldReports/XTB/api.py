import requests

class XTBAPI:
    """
    XTB uses gRPC-web over HTTP. This class provides the endpoint structure.
    Automation requires encoding payloads in Protobuf format.
    """
    def __init__(self):
        self.base_url = "https://ipax.xtb.com/pl.xtb.ipax.pub.grpc.onboarding.activation.v3.CustomerDataService"
        self.headers = {
            "Content-Type": "application/grpc",
            "User-Agent": "xStation Mobile Android/2.167.0 15 grpc-java-okhttp/1.77.0",
            "te": "trailers"
        }

    def send_phone_number(self, phone_proto_bytes):
        """
        Sends the phone number to trigger OTP.
        Requires binary protobuf data.
        """
        url = f"{self.base_url}/SendPhoneNumber"
        response = requests.post(url, data=phone_proto_bytes, headers=self.headers)
        return response.content

    def post_verification_config(self, config_proto_bytes):
        """
        Configures the phone verification session.
        """
        url = f"{self.base_url}/PostPhoneVerificationConfiguration"
        response = requests.post(url, data=config_proto_bytes, headers=self.headers)
        return response.content

    def send_verification_confirmation(self, otp_proto_bytes):
        """
        Submits the 6-digit OTP for confirmation.
        """
        url = f"{self.base_url}/SendPhoneVerificationConfirmation"
        response = requests.post(url, data=otp_proto_bytes, headers=self.headers)
        return response.content

if __name__ == "__main__":
    # Example usage (Requires valid binary payloads)
    api = XTBAPI()
    print("[!] XTB uses gRPC. Automation requires Protobuf binary construction.")
    print("[*] Protobuf Field Mappings for Confirmation:")
    print("    Field 1: Session/Customer ID (e.g., 69f5990380c6477a46e49034)")
    print("    Field 2: SMS OTP (e.g., 121212)")
    print("    Field 3: Phone Number (e.g., +393522050181)")
    # response = api.send_phone_number(b'\x00\x00\x00\x00\x1a...')
    # print(response)
