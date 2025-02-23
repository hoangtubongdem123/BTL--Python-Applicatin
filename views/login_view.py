import tkinter as tk
from tkinter import messagebox

class LoginView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Đăng Nhập")
        self.geometry("300x200")

        # Nhãn tên đăng nhập
        self.label_username = tk.Label(self, text="Tên đăng nhập:")
        self.label_username.pack(pady=5)

        # Ô nhập tên đăng nhập
        self.entry_username = tk.Entry(self)
        self.entry_username.pack(pady=5)

        # Nhãn mật khẩu
        self.label_password = tk.Label(self, text="Mật khẩu:")
        self.label_password.pack(pady=5)

        # Ô nhập mật khẩu
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)

        # Nút đăng nhập
        self.login_button = tk.Button(self, text="Đăng Nhập", command=self.controller.login)
        self.login_button.pack(pady=10)

    def show_message(self, message, success=False):
        """Hiển thị thông báo"""
        if success:
            messagebox.showinfo("Thông báo", message)
        else:
            messagebox.showerror("Lỗi", message)
