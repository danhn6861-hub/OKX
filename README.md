Hệ thống thực thi lệnh tập trung vào tính toàn vẹn và quản trị rủi ro hạ tầng. 

 Triết lý thiết kế (Design Philosophy)
- Defensive Execution: Không bao giờ tin tưởng hoàn toàn vào phản hồi từ API. Sử dụng `clOrdId` (Idempotency) để chống double-spending/double-ordering khi mạng không ổn định.
- Fail-Safe Mechanism: Tích hợp `Kill-switch` dựa trên Drawdown thực tế (High-Water Mark), tự động khóa hệ thống khi rủi ro vượt ngưỡng.
- Microstructure Awareness: `LatencyGuard` đo lường cả độ trễ và Jitter, đảm bảo lệnh chỉ được gửi khi điều kiện mạng tối ưu để tránh trượt giá (Slippage).

 Vận hành
1. Cài đặt dependencies: `pip install requests`
2. Chỉnh sửa API Key trong `main.py`.
3. Chạy demo: `python main.py`


Lưu ý: code tập trung vào lớp Core Execution. WebSocket Layer được tối giản để demo tư duy xử lý lệnh sạch
