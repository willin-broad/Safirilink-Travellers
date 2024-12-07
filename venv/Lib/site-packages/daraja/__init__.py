import base64
import json
import datetime
import urllib.request
import urllib.parse

class Mpesa():
    def __init__(self, config_file: str, env: str):
        self._config_file = config_file
        self.env = env

        if self.env == "prod":
            self.API_BASE = "https://api.safaricom.co.ke"
        elif self.env == "dev":
            self.API_BASE = "https://sandbox.safaricom.co.ke"
        else:
            raise ValueError("env parameter should be 'prod' or 'dev")

        with open(config_file, 'r') as f:
            data = json.load(f)
            self._consumerKey = data.get('consumerKey')
            self._consumerSecret = data.get('consumerSecret')
            self._passKey = data.get('passKey')
            self._shortCode = data.get('shortCode')
            self._tillNumber = data.get('tillNumber')
            self._callbackUrl = data.get('callbackUrl')
            self._transactionType = data.get('transactionType')
            self._accountRef = data.get('accountReference')
            self._transactionDesc = data.get('transactionDescription')

    async def get_auth(self):
        auth_str = f"{self._consumerKey}:{self._consumerSecret}"
        base64_auth = base64.b64encode(auth_str.encode()).decode()
        headers = {"Authorization": f"Basic {base64_auth}"}

        try:
            url = f"{self.API_BASE}/oauth/v1/generate?grant_type=client_credentials"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
            return data["access_token"]
        except Exception as e:
            print(e)

    @staticmethod
    async def get_time():
        utc_time = datetime.datetime.utcnow()
        ke_time = utc_time + datetime.timedelta(hours=3)
        return ke_time.strftime("%Y%m%d%H%M%S")

    async def _get_password(self):
        shortcode = str(self._shortCode)
        data_to_encode = f"{shortcode}{self._passKey}{await self.get_time()}"
        encoded_bytes = base64.b64encode(data_to_encode.encode())
        password = encoded_bytes.decode("utf-8")
        return password

    async def stk(self, receiver: str, amount: int):
        auth_token = await self.get_auth()
        password = await self._get_password()
        timestamp = await self.get_time()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}",
        }

        payload = {
            "BusinessShortCode": self._shortCode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": self._transactionType,
            "Amount": amount,
            "PartyA": receiver,
            "PartyB": self._tillNumber,
            "PhoneNumber": receiver,
            "CallBackURL": self._callbackUrl,
            "AccountReference": self._accountRef,
            "TransactionDesc": self._transactionDesc,
        }

        try:
            data = json.dumps(payload).encode('utf-8')
            url = f"{self.API_BASE}/mpesa/stkpush/v1/processrequest"
            req = urllib.request.Request(url, data=data, headers=headers, method='POST')
            with urllib.request.urlopen(req) as response:
                response_json = json.loads(response.read().decode())
                return response_json
        except Exception as e:
            print(e)

