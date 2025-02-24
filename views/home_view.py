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


        self.configure(bg="#f0f0f0")


        self.center_window(1200, 800)


        self.sidebar = tk.Frame(self, width=200, bg="#4CAF50")
        self.sidebar.pack(side="left", fill="y")


        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(side="right", expand=True, fill="both")


        self.buttons = [
            ("📚 Quản lý Sách", self.show_books),
            ("📖 Phiếu Mượn Sách", self.show_borrow),
            ("📜 Phiếu Trả Sách", self.show_return),
            ("👤 Thành Viên", self.show_members),
            ("📊 Thống Kê", self.show_statistics),
            ("🔴 Đăng Xuất", self.logout)
        ]


        for text, command in self.buttons:
            btn = tk.Button(self.sidebar, text=text, command=command, bg="#ffffff", fg="black", font=("Arial", 12), padx=10, pady=5)
            btn.pack(fill="x", pady=5)


        self.show_books()

    def center_window(self, width, height):

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def clear_main_frame(self):

        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_books(self):

        self.clear_main_frame()


        header_frame = tk.Frame(self.main_frame, bg="white")
        header_frame.pack(fill="x", pady=10, padx=10)

        tk.Label(header_frame, text="📚 Quản lý Sách", font=("Arial", 16, "bold"), bg="white").pack(side="left")

        add_book_btn = tk.Button(header_frame, text="➕ Thêm Sách", command=self.controller.add_book, bg="blue",
                                 fg="white", font=("Arial", 12))
        add_book_btn.pack(side="right")


        columns = ("ID", "Tên Sách", "Tác Giả", "Thể Loại","Số Lượng ")
        self.book_table = ttk.Treeview(self.main_frame, columns=columns, show="headings")

        for col in columns:
            self.book_table.heading(col, text=col)
            self.book_table.column(col, anchor="center")

        self.book_table.pack(fill="both", expand=True, padx=10, pady=5)


        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="✏️ Sửa", command=self.edit_book)
        self.context_menu.add_command(label="❌ Xóa", command=self.delete_book)


        self.book_table.bind("<Button-2>", self.show_context_menu)


        try:
            df = pd.read_excel("books.xlsx")
            for _, row in df.iterrows():
                self.book_table.insert("", "end", values=(row["ID"], row["Tên Sách"], row["Tác Giả"], row["Thể Loại"],row["Số Lượng"]))
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file books.xlsx!")

    def show_context_menu(self, event):

        selected_item = self.book_table.identify_row(event.y)
        if selected_item:
            self.book_table.selection_set(selected_item)
            self.context_menu.post(event.x_root, event.y_root)


    def edit_book(self):

        selected_item = self.book_table.selection()
        if selected_item:
            item_values = self.book_table.item(selected_item, "values")
            book_id = item_values[0]
            messagebox.showinfo("Sửa Sách", f"Bạn muốn sửa sách có ID: {book_id}")


    def delete_book(self):
        """Hàm xử lý khi nhấn Xóa sách"""
        selected_item = self.book_table.selection()
        if selected_item:
            item_values = self.book_table.item(selected_item, "values")
            book_id = item_values[0]

            confirm = messagebox.askyesno("Xóa Sách", f"Bạn có chắc chắn muốn xóa sách có ID: {book_id}?")
            if confirm:
                self.book_table.delete(selected_item)

                messagebox.showinfo("Xóa Thành Công", f"Đã xóa sách có ID: {book_id}")

    def show_borrow(self):

        self.clear_main_frame()
        tk.Label(self.main_frame, text="📖 Danh Sách Phiếu Mượn", font=("Arial", 16, "bold")).pack(pady=10)


        columns = ("Mã Phiếu", "Mã Thành Viên", "Mã Sách", "Số Lượng","Ngày Mượn","Ngày Trả Dự Kiến")
        borrow_table = ttk.Treeview(self.main_frame, columns=columns, show="headings")
        btn_add_borrow = tk.Button(self.main_frame, text="➕ Thêm Phiếu Mượn", command=self.controller.borrow_books,
                                   bg="blue", fg="white")

        btn_add_borrow.pack(pady=5)
        for col in columns:
            borrow_table.heading(col, text=col)
            borrow_table.column(col, anchor="center")

        borrow_table.pack(fill="both", expand=True, padx=10, pady=5)


        try:
            df = pd.read_excel("borrow_records.xlsx")
            for _, row in df.iterrows():
                borrow_table.insert("", "end",
                                    values=(row["Mã Phiếu"], row["Mã Thành Viên"], row["Mã Sách"], row["Số Lượng"],row["Ngày Mượn"],row["Ngày Trả Dự Kiến"]))
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file borrow_records.xlsx!")

    def show_context_menu_cua_phieutra(self, event):

        if not hasattr(self, "return_table") or self.return_table is None:
            return

        selected_item = self.return_table.identify_row(event.y)
        if not selected_item:
            return

        self.context_menu.post(event.x_root, event.y_root)

    def show_return(self):

        self.clear_main_frame()





        header_frame = tk.Frame(self.main_frame, bg="white")
        header_frame.pack(fill="x", pady=10, padx=10)

        tk.Label(header_frame, text="📄 Quản lý Phiếu Trả", font=("Arial", 16, "bold"), bg="white").pack(side="left")

        add_return_btn = tk.Button(header_frame, text="➕ Thêm Phiếu Trả", command=self.controller.return_books, bg="blue",
                                 fg="white", font=("Arial", 12))
        add_return_btn.pack(side="right")


        columns = (
        "Mã Phiếu", "Mã Thành Viên", "Mã Sách", "Số Lượng", "Ngày Mượn", "Ngày Trả Dự Kiến", "Ngày Trả Thực Tế")
        self.return_table = ttk.Treeview(self.main_frame, columns=columns, show="headings")

        for col in columns:
            self.return_table.heading(col, text=col)
            self.return_table.column(col, anchor="center")

        self.return_table.pack(fill="both", expand=True, padx=10, pady=5)


        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="✏️ Sửa")
        self.context_menu.add_command(label="❌ Xóa")


        self.return_table.bind("<Button-2>", self.show_context_menu_cua_phieutra)

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

        self.clear_main_frame()
        tk.Label(self.main_frame, text="👤 Thành Viên", font=("Arial", 16, "bold")).pack(pady=10)

    def show_statistics(self):

        self.clear_main_frame()
        tk.Label(self.main_frame, text="📊 Thống Kê", font=("Arial", 16, "bold")).pack(pady=10)

    def show_members(self):

        self.clear_main_frame()
        tk.Label(self.main_frame, text="👤 Danh Sách Thành Viên", font=("Arial", 16, "bold")).pack(pady=10)


        columns = ("ID", "Tên Thành Viên", "Email", "Số Điện Thoại")
        self.member_table = ttk.Treeview(self.main_frame, columns=columns, show="headings")

        for col in columns:
            self.member_table.heading(col, text=col)
            self.member_table.column(col, anchor="center")

        self.member_table.pack(fill="both", expand=True, padx=10, pady=5)


        tk.Button(self.main_frame, text="➕ Thêm Thành Viên",command=self.controller.add_member, bg="blue", fg="white",
                  font=("Arial", 12)).pack(pady=10)


        try:
            df = pd.read_excel("members.xlsx")  # Đọc file Excel
            for _, row in df.iterrows():
                self.member_table.insert("", "end", values=(row["ID"], row["Tên"], row["Email"], row["SĐT"]))
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file members.xlsx!")

    def logout(self):

        self.destroy()
        messagebox.showinfo("Thông báo", "Bạn đã đăng xuất thành công!")


a = HomeView("tung")

a.mainloop()





