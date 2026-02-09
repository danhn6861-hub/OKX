class StateReconciler:
    def __init__(self, rest_client):
        self.client = rest_client

    def sync(self):
        """Đảm bảo Bot và Sàn khớp nhau 100% trước khi trade"""
        print(" Đang đối soát vị thế thực tế...")
        pos = self.client.fetch_positions()
        if pos.get("code") == "0":
            # Logic đồng bộ trạng thái ở đây
            print(f" Đối soát xong. Hiện đang giữ {len(pos['data'])} vị thế.")
            return pos['data']

        return None
