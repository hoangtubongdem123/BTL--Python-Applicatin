class UserModel:
    def __init__(self):

        self.users = {
            "admin": "1234",
            "1": "1",
            "test": "test123"
        }

    def check_credentials(self, username, password):

        return self.users.get(username) == password
