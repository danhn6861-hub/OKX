import hmac, hashlib, base64, requests, json
from datetime import datetime

class OKXRestClient:
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.base_url = "https://www.okx.com"

    def _get_timestamp(self):
        # Format chuẩn: YYYY-MM-DDTHH:mm:ss.sssZ
        return datetime.utcnow().isoformat(timespec="milliseconds") + "Z"

    def _sign(self, timestamp, method, request_path, body=""):
        message = str(timestamp) + str.upper(method) + request_path + str(body)
        mac = hmac.new(bytes(self.secret_key, 'utf-8'), bytes(message, 'utf-8'), hashlib.sha256)
        return base64.b64encode(mac.digest()).decode('utf-8')

    def _request(self, method, request_path, params=None):
        ts = self._get_timestamp()
        body = json.dumps(params) if params else ""
        headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': self._sign(ts, method, request_path, body),
            'OK-ACCESS-TIMESTAMP': ts,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
        try:
            res = requests.request(method, self.base_url + request_path, headers=headers, data=body, timeout=5)
            return res.json()
        except Exception as e:
            return {"code": "-1", "msg": str(e)}

    def place_order(self, symbol, side, sz, cl_ord_id):
        params = {"instId": symbol, "tdMode": "cross", "side": side, "ordType": "market", "sz": str(sz), "clOrdId": cl_ord_id}
        return self._request("POST", "/api/v5/trade/order", params)

    def fetch_positions(self): return self._request("GET", "/api/v5/account/positions")