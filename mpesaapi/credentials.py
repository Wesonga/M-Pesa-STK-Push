import os
import base64
import requests
from pathlib import Path
from datetime import datetime
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env', override=True)


class MpesaC2bCredential:
    consumer_key = os.getenv('MPESA_CONSUMER_KEY')
    consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


class MpesaAccessToken:
    @staticmethod
    def get_access_token():
        load_dotenv(BASE_DIR / '.env', override=True)
        consumer_key = os.getenv('MPESA_CONSUMER_KEY')
        consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')

        if not consumer_key or not consumer_secret:
            raise ValueError(f"Missing MPESA_CONSUMER_KEY or MPESA_CONSUMER_SECRET in {BASE_DIR / '.env'}")

        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(
            MpesaC2bCredential.api_URL,
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
            headers=headers
        )
        r.raise_for_status()
        return r.json().get('access_token')


class LipanaMpesaPpassword:
    Business_short_code = os.getenv('MPESA_SHORTCODE', '174379')
    Test_c2b_shortcode = "600984"
    passkey = os.getenv('MPESA_PASSKEY', 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919')

    @classmethod
    def generate_password(cls):
        lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
        data_to_encode = cls.Business_short_code + cls.passkey + lipa_time
        decode_password = base64.b64encode(data_to_encode.encode()).decode('utf-8')
        return decode_password, lipa_time