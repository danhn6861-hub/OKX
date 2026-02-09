import asyncio
import time
from gateway.rest_client import OKXRestClient
from risk.risk_engine import RiskEngine
from risk.latency_guard import LatencyGuard
from execution.state_reconciler import StateReconciler
from execution.order_manager import OrderManager

async def main():
    print("=== [SYSTEM INITIALIZING] ===")
    
    # Init hạ tầng
    rest = OKXRestClient("API_KEY", "SECRET", "PASS")
    risk = RiskEngine(max_drawdown=0.03, max_exposure_usd=50000)
    guard = LatencyGuard(max_allowed_latency_ms=100)
    reconciler = StateReconciler(rest)
    manager = OrderManager(rest, risk, guard)

    # Reconcile trước khi "vào việc"
    reconciler.sync()
    
    print("=== [SYSTEM LIVE] ===")
    
    # Giả lập: Thấy tín hiệu, check lag và vả lệnh
    fake_server_time = int(time.time() * 1000) - 20 
    manager.send_smart_order("BTC-USDT-SWAP", "buy", 0.1, fake_server_time, current_exposure=0)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[STOPPED] Hệ thống đã dừng.")