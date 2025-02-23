import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from controllers.LibraryManagement import LibraryManagement


class HomeView(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.controller = LibraryManagement(self)
        self.title("Trang Chủ - Quản Lý Thư Viện")


        self.configure(bg="#f0f0f0")  # Màu nền

        # Căn giữa cửa sổ
        self.center_window(1200, 800)

        # Sidebar menu (chức năng)
        self.sidebar = tk.Frame(self, width=200, bg="#4CAF50")
        self.sidebar.pack(side="left", fill="y")

        # Nội dung chính
        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(side="right", expand=True, fill="both")

        # Danh sách các chức năng
        self.buttons = [
            ("📚 Quản lý Sách", self.show_books),
            ("📖 Phiếu Mượn Sách", self.show_borrow),
            ("📜 Phiếu Trả Sách", self.show_return),
            ("👤 Thành Viên", self.show_members),
            ("📊 Thống Kê", self.show_statistics),
            ("🔴 Đăng Xuất", self.logout)
        ]

        # Hiển thị các nút trong sidebar
        for text, command in self.buttons:
            btn = tk.Button(self.sidebar, text=text, command=command, bg="#ffffff", fg="black", font=("Arial", 12), padx=10, pady=5)
            btn.pack(fill="x", pady=5)

        # Hiển thị màn hình mặc định là quản lý sách
        self.show_books()

    def center_window(self, width, height):
        """Căn giữa cửa sổ"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def clear_main_frame(self):
        """Xóa nội dung hiện tại"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_books(self):
        """Hiển thị danh sách sách từ file Excel"""
        self.clear_main_frame()

        # Tạo frame chứa tiêu đề và nút thêm sách
        header_frame = tk.Frame(self.main_frame, bg="white")
        header_frame.pack(fill="x", pady=10, padx=10)

        tk.Label(header_frame, text="📚 Quản lý Sách", font=("Arial", 16, "bold"), bg="white").pack(side="left")

        add_book_btn = tk.Button(header_frame, text="➕ Thêm Sách", command=self.controller.add_book, bg="blue",
                                 fg="white", font=("Arial", 12))
        add_book_btn.pack(side="right")

        # Tạo bảng danh sách sách
        columns = ("ID", "Tên Sách", "Tác Giả", "Thể Loại","Số Lượng ")
        self.book_table = ttk.Treeview(self.main_frame, columns=columns, show="headings")

        for col in columns:
            self.book_table.heading(col, text=col)
            self.book_table.column(col, anchor="center")

        self.book_table.pack(fill="both", expand=True, padx=10, pady=5)

        # Tạo menu chuột phải
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="✏️ Sửa", command=self.edit_book)
        self.context_menu.add_command(label="❌ Xóa", command=self.delete_book)

        # Gán sự kiện chuột phải cho bảng
        self.book_table.bind("<Button-2>", self.show_context_menu)

        # Đọc dữ liệu từ file Excel
        try:
            df = pd.read_excel("books.xlsx")  # Đọc file Excel
            for _, row in df.iterrows():
                self.book_table.insert("", "end", values=(row["ID"], row["Tên Sách"], row["Tác Giả"], row["Thể Loại"],row["Số Lượng"]))
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file books.xlsx!")

    def show_context_menu(self, event):
        """Hiển thị menu chuột phải khi click vào một dòng trong bảng"""
        selected_item = self.book_table.identify_row(event.y)  # Lấy ID dòng được click
        if selected_item:
            self.book_table.selection_set(selected_item)  # Chọn dòng
            self.context_menu.post(event.x_root, event.y_root)  # Hiển thị menu tại vị trí chuột


    def edit_book(self):
        """Hàm xử lý khi nhấn Sửa sách"""
        selected_item = self.book_table.selection()
        if selected_item:
            item_values = self.book_table.item(selected_item, "values")
            book_id = item_values[0]  # ID của sách cần sửa
            messagebox.showinfo("Sửa Sách", f"Bạn muốn sửa sách có ID: {book_id}")
            # Bạn có thể mở cửa sổ sửa sách ở đâyf

    def delete_book(self):
        """Hàm xử lý khi nhấn Xóa sách"""
        selected_item = self.book_table.selection()
        if selected_item:
            item_values = self.book_table.item(selected_item, "values")
            book_id = item_values[0]  # ID của sách cần xóa

            confirm = messagebox.askyesno("Xóa Sách", f"Bạn có chắc chắn muốn xóa sách có ID: {book_id}?")
            if confirm:
                self.book_table.delete(selected_item)  # Xóa trên giao diện
                # Xử lý xóa trong file Excel tại đây (đọc file, xóa dòng, lưu lại)
                messagebox.showinfo("Xóa Thành Công", f"Đã xóa sách có ID: {book_id}")

    def show_borrow(self):
        """Hiển thị danh sách phiếu mượn/trả sách"""
        self.clear_main_frame()
        tk.Label(self.main_frame, text="📖 Danh Sách Phiếu Mượn", font=("Arial", 16, "bold")).pack(pady=10)

        # Tạo bảng danh sách phiếu mượn
        columns = ("Mã Phiếu", "Mã Thành Viên", "Mã Sách", "Số Lượng","Ngày Mượn","Ngày Trả Dự Kiến")
        borrow_table = ttk.Treeview(self.main_frame, columns=columns, show="headings")
        btn_add_borrow = tk.Button(self.main_frame, text="➕ Thêm Phiếu Mượn", command=self.controller.borrow_books,
                                   bg="blue", fg="white")

        btn_add_borrow.pack(pady=5)
        for col in columns:
            borrow_table.heading(col, text=col)
            borrow_table.column(col, anchor="center")

        borrow_table.pack(fill="both", expand=True, padx=10, pady=5)

        # Đọc dữ liệu từ file Excel
        try:
            df = pd.read_excel("borrow_records.xlsx")  # Đọc file Excel
            for _, row in df.iterrows():
                borrow_table.insert("", "end",
                                    values=(row["Mã Phiếu"], row["Mã Thành Viên"], row["Mã Sách"], row["Số Lượng"],row["Ngày Mượn"],row["Ngày Trả Dự Kiến"]))
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file borrow_records.xlsx!")

    def show_context_menu_cua_phieutra(self, event):
        """Hiển thị menu chuột phải trên danh sách phiếu trả"""
        if not hasattr(self, "return_table") or self.return_table is None:
            return  # Nếu bảng không tồn tại, thoát luôn

        selected_item = self.return_table.identify_row(event.y)
        if not selected_item:
            return  # Nếu không có dòng nào, không hiển thị menu

        self.context_menu.post(event.x_root, event.y_root)

    def show_return(self):
        """Hiển thị danh sách phiếu trả từ file Excel"""
        self.clear_main_frame()


        # Tạo frame chứa tiêu đề


        header_frame = tk.Frame(self.main_frame, bg="white")
        header_frame.pack(fill="x", pady=10, padx=10)

        tk.Label(header_frame, text="📄 Quản lý Phiếu Trả", font=("Arial", 16, "bold"), bg="white").pack(side="left")

        add_return_btn = tk.Button(header_frame, text="➕ Thêm Phiếu Trả", command=self.controller.return_books, bg="blue",
                                 fg="white", font=("Arial", 12))
        add_return_btn.pack(side="right")

        # Tạo bảng danh sách phiếu trả
        columns = (
        "Mã Phiếu", "Mã Thành Viên", "Mã Sách", "Số Lượng", "Ngày Mượn", "Ngày Trả Dự Kiến", "Ngày Trả Thực Tế")
        self.return_table = ttk.Treeview(self.main_frame, columns=columns, show="headings")

        for col in columns:
            self.return_table.heading(col, text=col)
            self.return_table.column(col, anchor="center")

        self.return_table.pack(fill="both", expand=True, padx=10, pady=5)

        # Tạo menu chuột phải
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="✏️ Sửa")
        self.context_menu.add_command(label="❌ Xóa")


        # Gán sự kiện chuột phải cho bảng
        self.return_table.bind("<Button-2>", self.show_context_menu_cua_phieutra)

        # Đọc dữ liệu từ file Excel
        try:
            df = pd.read_excel("return_records.xlsx")  # Đọc file Excel
            for _, row in df.iterrows():
                self.return_table.insert("", "end", values=(
                    row["Mã Phiếu"], row["Mã Thành Viên"], row["Mã Sách"], row["Số Lượng"],
                    row["Ngày Mượn"], row["Ngày Trả Dự Kiến"], row["Ngày Trả Thực Tế"]
                ))
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file return_records.xlsx!")
    def show_members(self):
        """Hiển thị danh sách thành viên"""
        self.clear_main_frame()
        tk.Label(self.main_frame, text="👤 Thành Viên", font=("Arial", 16, "bold")).pack(pady=10)

    def show_statistics(self):
        """Hiển thị thống kê thư viện"""
        self.clear_main_frame()
        tk.Label(self.main_frame, text="📊 Thống Kê", font=("Arial", 16, "bold")).pack(pady=10)

    def show_members(self):
        """Hiển thị danh sách thành viên"""
        self.clear_main_frame()
        tk.Label(self.main_frame, text="👤 Danh Sách Thành Viên", font=("Arial", 16, "bold")).pack(pady=10)

        # Tạo bảng danh sách thành viên
        columns = ("ID", "Tên Thành Viên", "Email", "Số Điện Thoại")
        self.member_table = ttk.Treeview(self.main_frame, columns=columns, show="headings")

        for col in columns:
            self.member_table.heading(col, text=col)
            self.member_table.column(col, anchor="center")

        self.member_table.pack(fill="both", expand=True, padx=10, pady=5)

        # Nút thêm thành viên
        tk.Button(self.main_frame, text="➕ Thêm Thành Viên",command=self.controller.add_member, bg="blue", fg="white",
                  font=("Arial", 12)).pack(pady=10)

        # Đọc dữ liệu từ file Excel
        try:
            df = pd.read_excel("members.xlsx")  # Đọc file Excel
            for _, row in df.iterrows():
                self.member_table.insert("", "end", values=(row["ID"], row["Tên"], row["Email"], row["SĐT"]))
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file members.xlsx!")

    def logout(self):
        """Đăng xuất và quay lại đăng nhập"""
        self.destroy()
        messagebox.showinfo("Thông báo", "Bạn đã đăng xuất thành công!")


a = HomeView("tung")

a.mainloop()





