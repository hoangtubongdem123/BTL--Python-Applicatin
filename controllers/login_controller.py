from models.user_model import UserModel
from views.login_view import LoginView


from controllers.home_controller import HomeController

class LoginController:
    def __init__(self):
        self.model = UserModel()
        self.view = LoginView(self)
        self.home_controller = None

    def login(self):
        """Xử lý đăng nhập"""
        username = self.view.entry_username.get()
        password = self.view.entry_password.get()

        if self.model.check_credentials(username, password):
            self.view.show_message(f"Chào mừng {username}!", success=True)
            self.view.destroy()

            self.home_controller = HomeController(username)

        else:
            self.view.show_message("Sai tên đăng nhập hoặc mật khẩu!")

    def run(self):

        self.view.mainloop()

