import asyncio
import time
import os
from dotenv import load_dotenv # Cần: pip install python-dotenv

from gateway.rest_client import OKXRestClient
from risk.risk_engine import RiskEngine
from risk.latency_guard import LatencyGuard
from execution.state_reconciler import StateReconciler
from execution.order_manager import OrderManager

# Load biến môi trường từ file .env
load_dotenv()

async def main():
    print("\n=== [SYSTEM INITIALIZING] ===")
    
    # Đọc cấu hình từ môi trường
    api_key = os.getenv("OKX_API_KEY", "YOUR_KEY")
    secret = os.getenv("OKX_SECRET", "YOUR_SECRET")
    passphrase = os.getenv("OKX_PASSPHRASE", "YOUR_PASS")
    
    # Init hạ tầng
    rest = OKXRestClient(api_key, secret, passphrase)
    risk = RiskEngine(max_drawdown=0.03, max_exposure_usd=50000)
    guard = LatencyGuard(max_allowed_latency_ms=100)
    reconciler = StateReconciler(rest)
    manager = OrderManager(rest, risk, guard)

    # 1. Reconcile (Sẽ báo lỗi Key nếu chưa cấu hình đúng)
    sync_data = reconciler.sync()
    if sync_data is None:
        print("❌ KHỞI TẠO THẤT BẠI: Vui lòng kiểm tra API Key trong file .env")
        return
    
    print("=== [SYSTEM LIVE: MONITORING] ===")
    
    # Giả lập: Thấy tín hiệu, check lag và vả lệnh
    fake_server_time = int(time.time() * 1000) - 20 
    manager.send_smart_order("BTC-USDT-SWAP", "buy", 0.1, fake_server_time, current_exposure=0)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[STOPPED] Bot đã dừng thủ công.")
