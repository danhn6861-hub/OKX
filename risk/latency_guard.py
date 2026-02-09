import time
import statistics

class LatencyGuard:
    def __init__(self, max_allowed_latency_ms=150, window_size=20):
        self.max_latency = max_allowed_latency_ms
        self.history = []
        self.window_size = window_size

    def validate_network(self, server_time_ms):
        """Dùng Standard Deviation để đo Jitter - mạng chập chờn là nghỉ chơi"""
        if not server_time_ms: return False, "Thiếu Server Time."
        
        latency = int(time.time() * 1000) - server_time_ms
        self.history.append(latency)
        
        if len(self.history) > self.window_size:
            self.history.pop(0)

        jitter = statistics.stdev(self.history) if len(self.history) > 1 else 0

        if latency > self.max_latency:
            return False, f"Lag tức thời quá cao: {latency}ms"
        if jitter > (self.max_latency * 0.4):
            return False, f"Mạng chập chờn (Jitter: {jitter:.2f}ms)"

        return True, f"Stable ({latency}ms)"