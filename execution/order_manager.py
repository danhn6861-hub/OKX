import uuid, time

class OrderManager:
    def __init__(self, rest_client, risk_engine, latency_guard):
        self.client = rest_client
        self.risk = risk_engine
        self.guard = latency_guard

    def send_smart_order(self, symbol, side, sz, server_time_ms, current_exposure):
        # Lớp 1: Check mạng
        net_ok, net_msg = self.guard.validate_network(server_time_ms)
        if not net_ok: 
            return print(f"❌ CHẶN LỆNH: {net_msg}")

        # Lớp 2: Check rủi ro (Giả lập giá BTC=60k để tính exposure)
        order_val = sz * 60000 
        risk_ok, risk_msg = self.risk.validate_order(order_val, current_exposure)
        if not risk_ok:
            return print(f"🛑 CHẶN RỦI RO: {risk_msg}")

        # Lớp 3: Thực thi với ID duy nhất chống trùng lệnh (Idempotency)
        cl_id = f"PRO_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        res = self.client.place_order(symbol, side, sz, cl_id)

        if res.get("code") == "0":
            print(f"✅ KHỚP: {symbol} {side} {sz} | ID: {res['data'][0]['ordId']}")
        else:
            print(f"❌ SÀN TỪ CHỐI: {res.get('msg')}")