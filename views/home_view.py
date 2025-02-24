import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from datetime import datetime
from controllers.LibraryManagement import LibraryManagement
import platform





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
            ("🚀 Thành Viên Muộn", self.show_late_returns),
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

        # Header Frame
        header_frame = tk.Frame(self.main_frame, bg="white")
        header_frame.pack(fill="x", pady=10, padx=10)

        tk.Label(header_frame, text="📚 Quản lý Sách", font=("Arial", 16, "bold"), bg="white").pack(side="left")

        add_book_btn = tk.Button(header_frame, text="➕ Thêm Sách", command=self.controller.add_book, bg="blue",
                                 fg="black", font=("Arial", 12))
        add_book_btn.pack(side="right")

        # Tìm kiếm Frame
        search_frame = tk.Frame(self.main_frame, bg="white")
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="🔍 Tìm kiếm:", font=("Arial", 12), bg="white").pack(side="left", padx=5)

        self.search_entry = tk.Entry(search_frame, font=("Arial", 12))
        self.search_entry.pack(side="left", padx=5)

        search_btn = tk.Button(search_frame, text="Tìm", command=self.search_books, bg="green", fg="black",
                               font=("Arial", 12))
        search_btn.pack(side="left", padx=5)

        reset_btn = tk.Button(search_frame, text="🔄 Reset", command=self.load_books, bg="gray", fg="black",
                              font=("Arial", 12))
        reset_btn.pack(side="left", padx=5)

        # Bảng hiển thị sách
        self.columns = ("ID", "Tên Sách", "Tác Giả", "Thể Loại", "Số Lượng")
        self.book_table = ttk.Treeview(self.main_frame, columns=self.columns, show="headings")

        for col in self.columns:
            self.book_table.heading(col, text=col, command=lambda c=col: self.sort_books(c, False))  # Nhấn để sắp xếp
            self.book_table.column(col, anchor="center")

        self.book_table.pack(fill="both", expand=True, padx=10, pady=5)

        # Menu chuột phải
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="✏️ Sửa", command=self.edit_book)
        self.context_menu.add_command(label="❌ Xóa", command=self.delete_book)

        import platform

        # Kiểm tra hệ điều hành
        if platform.system() == "Darwin":  # macOS
            right_click_event = "<Button-2>"
        else:  # Windows & Linux
            right_click_event = "<Button-3>"

        self.book_table.bind(right_click_event, self.show_context_menu)

        # Tải dữ liệu từ file Excel
        self.load_books()

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
                                   bg="blue", fg="black")

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
                                 fg="black", font=("Arial", 12))
        add_return_btn.pack(side="right")


        columns = (
        "Mã Phiếu", "Mã Thành Viên", "Mã Sách", "Số Lượng", "Ngày Mượn", "Ngày Trả Dự Kiến", "Ngày Trả Thực Tế")
        self.return_table = ttk.Treeview(self.main_frame, columns=columns, show="headings")

        for col in columns:
            self.return_table.heading(col, text=col)
            self.return_table.column(col, anchor="center")

        self.return_table.pack(fill="both", expand=True, padx=10, pady=5)




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

    def show_late_returns(self):



        self.clear_main_frame()

        tk.Label(self.main_frame, text="📌 Danh Sách Thành Viên Trả Sách Muộn", font=("Arial", 14, "bold")).pack(pady=10)

        try:

            borrow_df = pd.read_excel("borrow_records.xlsx", dtype={"Mã Thành Viên": str})
            return_df = pd.read_excel("return_records.xlsx", dtype={"Mã Thành Viên": str})
            members_df = pd.read_excel("members.xlsx", dtype={"ID": str})


            borrow_df["Mã Thành Viên"] = borrow_df["Mã Thành Viên"].astype(str).str.strip()
            return_df["Mã Thành Viên"] = return_df["Mã Thành Viên"].astype(str).str.strip()
            members_df["ID"] = members_df["ID"].astype(str).str.strip()
            members_df["Tên"] = members_df["Tên"].str.strip()


            columns = ("Mã Thành Viên", "Tên Thành Viên", "Số Ngày Trễ", "Tổng Phí Phạt")
            late_table = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=7)

            for col in columns:
                late_table.heading(col, text=col)
                late_table.column(col, anchor="center")

            late_table.pack(fill="both", expand=True, padx=10, pady=5)


            late_fees = {}

            today = datetime.now()
            late_fee_per_day = 5000

            for _, row in return_df.iterrows():
                try:
                    due_date = datetime.strptime(str(row["Ngày Trả Dự Kiến"]).strip(), "%Y-%m-%d")
                    return_date = datetime.strptime(str(row["Ngày Trả Thực Tế"]).strip(), "%Y-%m-%d")

                    if return_date > due_date:
                        late_days = (return_date - due_date).days
                        fine = late_days * late_fee_per_day

                        member_id = row["Mã Thành Viên"]

                        if member_id in late_fees:
                            late_fees[member_id]["Số Ngày Trễ"] += late_days
                            late_fees[member_id]["Tổng Phí Phạt"] += fine
                        else:
                            late_fees[member_id] = {
                                "Số Ngày Trễ": late_days,
                                "Tổng Phí Phạt": fine
                            }
                except Exception as e:
                    print(f"Lỗi xử lý ngày tháng: {e}")


            for member_id, data in late_fees.items():
                member_name = members_df.loc[members_df["ID"] == member_id, "Tên"].values
                member_name = member_name[0] if len(member_name) > 0 else "Không rõ"

                late_table.insert("", "end",
                                  values=(member_id, member_name, data["Số Ngày Trễ"], data["Tổng Phí Phạt"]))

            if not late_fees:
                messagebox.showinfo("Thông báo", "Không có thành viên nào trả sách muộn!")

        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file dữ liệu!")

    def show_statistics(self):

        """Thống kê tổng số sách, sách được mượn nhiều nhất, thành viên mượn nhiều nhất với giao diện trực quan."""
        self.clear_main_frame()

        tk.Label(self.main_frame, text="📊 Thống Kê Thư Viện", font=("Arial", 16, "bold")).pack(pady=10)

        try:
            books_df = pd.read_excel("books.xlsx", dtype={"ID": str})
            borrow_df = pd.read_excel("borrow_records.xlsx",
                                      dtype={"Mã Phiếu": str, "Mã Thành Viên": str, "Mã Sách": str})
            members_df = pd.read_excel("members.xlsx", dtype={"Mã Thành Viên": str})
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file dữ liệu!")
            return


        total_books = books_df["Số Lượng"].sum()


        most_borrowed_book = borrow_df["Mã Sách"].value_counts().idxmax() if not borrow_df.empty else "Không có"
        book_title = books_df.loc[books_df["ID"] == most_borrowed_book, "Tên Sách"].values






        summary_frame = tk.Frame(self.main_frame, bg="white", bd=2, relief="groove")
        summary_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(summary_frame, text=f"📚 Tổng số sách: {total_books}", font=("Arial", 14, "bold"), bg="white").pack(
            pady=5)


        books_df = pd.read_excel("books.xlsx", dtype={"ID": str})


        top_books_df = books_df.nlargest(5, "Số Lần Mượn")[["ID", "Tên Sách", "Số Lần Mượn"]]


        top_books_frame = tk.Frame(self.main_frame)
        top_books_frame.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Label(top_books_frame, text="📌 Top 5 Sách Mượn Nhiều Nhất", font=("Arial", 12, "bold")).pack()


        columns = ("Mã Sách", "Tên Sách", "Số Lần Mượn")
        book_table = ttk.Treeview(top_books_frame, columns=columns, show="headings", height=5)

        for col in columns:
            book_table.heading(col, text=col)
            book_table.column(col, anchor="center")

        book_table.pack(fill="both", expand=True)


        for _, row in top_books_df.iterrows():
            book_table.insert("", "end", values=(row["ID"], row["Tên Sách"], row["Số Lần Mượn"]))

        members_df["ID"] = members_df["ID"].astype(str).str.strip()
        members_df["Tên"] = members_df["Tên"].str.strip()
        borrow_df["Mã Thành Viên"] = borrow_df["Mã Thành Viên"].astype(str).str.strip()


        top_members = borrow_df["Mã Thành Viên"].value_counts().head(5)


        top_members_frame = tk.Frame(self.main_frame)
        top_members_frame.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Label(top_members_frame, text="🏆 Top 5 Thành Viên Mượn Nhiều Nhất", font=("Arial", 12, "bold")).pack()

        member_columns = ("Mã Thành Viên", "Tên Thành Viên", "Số Lần Mượn")
        member_table = ttk.Treeview(top_members_frame, columns=member_columns, show="headings", height=5)

        for col in member_columns:
            member_table.heading(col, text=col)
            member_table.column(col, anchor="center")

        member_table.pack(fill="both", expand=True)


        for member_id, count in top_members.items():
            member_name = members_df.loc[members_df["ID"] == member_id, "Tên"].values
            member_name = member_name[0] if len(member_name) > 0 else "Không xác định"

            member_table.insert("", "end", values=(member_id, member_name, count))

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

    def sort_books(self, column, reverse):

        data = [(self.book_table.item(item, "values"), item) for item in self.book_table.get_children()]


        if column == "Số Lượng":
            data.sort(key=lambda x: int(x[0][4]), reverse=reverse)
        else:
            data.sort(key=lambda x: x[0][self.columns.index(column)], reverse=reverse)


        for index, (_, item) in enumerate(data):
            self.book_table.move(item, "", index)


        self.book_table.heading(column, command=lambda c=column: self.sort_books(c, not reverse))

    def load_books(self):

        for row in self.book_table.get_children():
            self.book_table.delete(row)

        try:
            df = pd.read_excel("books.xlsx", engine="openpyxl")
            for _, row in df.iterrows():
                self.book_table.insert("", "end", values=(
                    row["ID"], row["Tên Sách"], row["Tác Giả"], row["Thể Loại"], row["Số Lượng"]))
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file books.xlsx!")

    def search_books(self):

        keyword = self.search_entry.get().strip().lower()

        if not keyword:
            messagebox.showwarning("Lỗi", "Vui lòng nhập từ khóa tìm kiếm!")
            return

        try:
            df = pd.read_excel("books.xlsx", engine="openpyxl")
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file books.xlsx!")
            return


        filtered_df = df[df.apply(lambda row: keyword in str(row["ID"]).lower() or
                                              keyword in str(row["Tên Sách"]).lower() or
                                              keyword in str(row["Tác Giả"]).lower() or
                                              keyword in str(row["Thể Loại"]).lower(), axis=1)]


        for row in self.book_table.get_children():
            self.book_table.delete(row)


        if filtered_df.empty:
            messagebox.showinfo("Kết quả", f"Không tìm thấy sách với từ khóa: {keyword}")
        else:
            for _, row in filtered_df.iterrows():
                self.book_table.insert("", "end", values=(
                    row["ID"], row["Tên Sách"], row["Tác Giả"], row["Thể Loại"], row["Số Lượng"]))

    def edit_book(self):

        selected_item = self.book_table.selection()
        if selected_item:
            item_values = self.book_table.item(selected_item, "values")
            book_id = item_values[0]
            confirm = messagebox.askyesno("Sửa Sách", f"Bạn muốn sửa sách có ID: {book_id}")
            if confirm:
                self.controller.update_info(book_id)

    def logout(self):

        self.destroy()
        messagebox.showinfo("Thông báo", "Bạn đã đăng xuất thành công!")


a = HomeView("tung")

a.mainloop()





