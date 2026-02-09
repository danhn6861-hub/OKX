class RiskEngine:
    def __init__(self, max_drawdown=0.05, max_exposure_usd=100000):
        self.max_drawdown = max_drawdown
        self.max_exposure = max_exposure_usd
        self.peak_equity = 0
        self.is_emergency_stop = False

    def check_health(self, current_equity):
        """Cơ chế Kill-switch: Chặn đứng mọi hoạt động nếu chạm ngưỡng Drawdown"""
        if self.is_emergency_stop:
            return False, "SYSTEM LOCKED: Cần can thiệp thủ công."

        # Cập nhật đỉnh vốn để tính sụt giảm tài sản chuẩn xác
        if current_equity > self.peak_equity:
            self.peak_equity = current_equity
        
        if self.peak_equity > 0:
            drawdown = (self.peak_equity - current_equity) / self.peak_equity
            if drawdown >= self.max_drawdown:
                self.is_emergency_stop = True 
                return False, f"CRITICAL: Drawdown {drawdown:.2%} chạm ngưỡng chặn. KHÓA HỆ THỐNG!"
        
        return True, "Safe"

    def validate_order(self, size_usd, current_exposure_usd):
        """Pre-trade risk check: Chặn lệnh ngay tại cửa ngõ nếu vi phạm exposure"""
        if self.is_emergency_stop:
            return False, "Lệnh bị từ chối: Hệ thống đang trạng thái khóa rủi ro."
        
        if current_exposure_usd + size_usd > self.max_exposure:
            return False, f"Lệnh bị từ chối: Vượt ngưỡng exposure tối đa ({self.max_exposure}$)."
            
        return True, "Valid"