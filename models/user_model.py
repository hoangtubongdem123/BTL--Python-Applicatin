class UserModel:
    def __init__(self):
        # Danh sách tài khoản mẫu (username, password)
        self.users = {
            "admin": "1234",
            "1": "1",
            "test": "test123"
        }

    def check_credentials(self, username, password):
        """Kiểm tra xem tài khoản có tồn tại không"""
        return self.users.get(username) == password
