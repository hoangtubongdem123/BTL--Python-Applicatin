from datetime import datetime
from controllers.BorrowReturnRecord import BorrowReturnRecord
import tkinter as tk
from datetime import datetime, timedelta

import pandas as pd
from tkinter import messagebox

class LibraryManagement:
    def __init__(self,view=None):
        self.books = {}  # {book_id: Book}
        self.members = {}  # {member_id: Member}
        self.records = {}  # {record_id: BorrowReturnRecord}
        self.record_counter = 1  # Đếm số lượng phiếu mượn
        self.view = view  # Lưu HomeView để gọi lại khi cần



    def add_book(self):
        """Mở cửa sổ nhập thông tin sách"""
        add_window = tk.Toplevel()  # Sửa self → self.view
        add_window.title("Thêm Sách")
        add_window.geometry("300x250")

        tk.Label(add_window, text="Tên Sách:").pack(pady=5)
        entry_name = tk.Entry(add_window)
        entry_name.pack(pady=5)

        tk.Label(add_window, text="Tác Giả:").pack(pady=5)
        entry_author = tk.Entry(add_window)
        entry_author.pack(pady=5)

        tk.Label(add_window, text="Thể Loại:").pack(pady=5)
        entry_category = tk.Entry(add_window)
        entry_category.pack(pady=5)

        tk.Button(add_window, text="Lưu",
                  command=lambda: self.save_book(entry_name.get(), entry_author.get(), entry_category.get(), add_window)
                  ).pack(pady=10)

    def save_book(self, name, author, category, window):
        """Lưu sách vào file Excel"""
        if not name or not author or not category:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            df = pd.read_excel("books.xlsx")  # Đọc file Excel
        except FileNotFoundError:
            df = pd.DataFrame(columns=["ID", "Tên Sách", "Tác Giả", "Thể Loại"])

        # Thêm sách vào DataFrame
        new_id = df["ID"].max() + 1 if not df.empty else 1  # Sinh ID tự động
        new_book = pd.DataFrame([[new_id, name, author, category]], columns=df.columns)
        df = pd.concat([df, new_book], ignore_index=True)

        df.to_excel("books.xlsx", index=False)  # Lưu lại file
        messagebox.showinfo("Thành công", "Thêm sách thành công!")

        window.destroy()  # Đóng cửa sổ nhập sách
        self.view.show_books()  # Cập nhật danh sách sách

    def update_book(self, book_id, **kwargs):
        if book_id in self.books:
            self.books[book_id].update_info(**kwargs)

    def delete_book(self, book_id):
        if book_id in self.books:
            # Kiểm tra xem sách có trong phiếu mượn nào không
            for record in self.records.values():
                if book_id in record.borrowed_books:
                    print("Không thể xóa sách vì có trong phiếu mượn!")
                    return False
            del self.books[book_id]
            return True
        return False

    def add_member(self):
        """Mở cửa sổ nhập thông tin thành viên mới"""
        add_window = tk.Toplevel(self.view)
        add_window.title("Thêm Thành Viên")
        add_window.geometry("400x300")
        add_window.configure(bg="white")

        tk.Label(add_window, text="ID:", font=("Arial", 12)).pack(pady=5)
        entry_id = tk.Entry(add_window, font=("Arial", 12))
        entry_id.pack(pady=5)

        tk.Label(add_window, text="Tên:", font=("Arial", 12)).pack(pady=5)
        entry_name = tk.Entry(add_window, font=("Arial", 12))
        entry_name.pack(pady=5)

        tk.Label(add_window, text="Email:", font=("Arial", 12)).pack(pady=5)
        entry_email = tk.Entry(add_window, font=("Arial", 12))
        entry_email.pack(pady=5)

        tk.Label(add_window, text="Số Điện Thoại:", font=("Arial", 12)).pack(pady=5)
        entry_phone = tk.Entry(add_window, font=("Arial", 12))
        entry_phone.pack(pady=5)

        def save_member():
            """Lưu thông tin thành viên vào file Excel"""
            member_id = entry_id.get()
            member_name = entry_name.get()
            member_email = entry_email.get()
            member_phone = entry_phone.get()

            if not (member_id and member_name and member_email and member_phone):
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return

            try:
                df = pd.read_excel("members.xlsx")
            except FileNotFoundError:
                df = pd.DataFrame(columns=["ID", "Tên", "Email", "SĐT"])

            # Thêm dữ liệu mới
            new_member = pd.DataFrame(
                {"ID": [member_id], "Tên": [member_name], "Email": [member_email], "SĐT": [member_phone]})
            df = pd.concat([df, new_member], ignore_index=True)

            # Ghi vào file Excel
            df.to_excel("members.xlsx", index=False)

            messagebox.showinfo("Thành công", "Thêm thành viên thành công!")
            add_window.destroy()
            self.view.show_members()  # Cập nhật danh sách

        tk.Button(add_window, text="Lưu", command=save_member, bg="green", fg="white", font=("Arial", 12)).pack(pady=10)

    def delete_member(self, member_id):
        if member_id in self.members:
            if self.members[member_id].borrowed_books:
                print("Không thể xóa thành viên vì còn sách đang mượn!")
                return False
            del self.members[member_id]
            return True
        return False

    def borrow_books(self):
        """Giao diện thêm phiếu mượn"""
        self.view.clear_main_frame()

        tk.Label(self.view.main_frame, text="➕ Thêm Phiếu Mượn", font=("Arial", 16, "bold")).pack(pady=10)

        # Mã phiếu
        tk.Label(self.view.main_frame, text="Mã Phiếu:").pack()
        entry_borrow_id = tk.Entry(self.view.main_frame)
        entry_borrow_id.pack()

        # Mã thành viên
        tk.Label(self.view.main_frame, text="Mã Thành Viên:").pack()
        entry_member_id = tk.Entry(self.view.main_frame)
        entry_member_id.pack()

        # Mã sách và số lượng
        book_entries = []

        def add_book_entry():
            frame = tk.Frame(self.view.main_frame)
            frame.pack()
            tk.Label(frame, text="Mã Sách:").pack(side="left")
            entry_book_id = tk.Entry(frame, width=10)
            entry_book_id.pack(side="left")
            tk.Label(frame, text="Số Lượng:").pack(side="left")
            entry_quantity = tk.Entry(frame, width=5)
            entry_quantity.pack(side="left")
            book_entries.append((entry_book_id, entry_quantity))

        tk.Button(self.view.main_frame, text="➕ Thêm Sách", command=add_book_entry).pack(pady=5)

        # Lưu phiếu mượn
        def save_borrow_record():
            borrow_id = entry_borrow_id.get()
            member_id = entry_member_id.get()
            book_list = []

            for entry_book_id, entry_quantity in book_entries:
                book_id = entry_book_id.get()
                quantity = entry_quantity.get()
                if book_id and quantity.isdigit():
                    book_list.append((book_id, int(quantity)))

            if not borrow_id or not member_id or not book_list:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return

            try:
                borrow_df = pd.read_excel("borrow_records.xlsx")
            except FileNotFoundError:
                borrow_df = pd.DataFrame(
                    columns=["Mã Phiếu", "Mã Thành Viên", "Mã Sách", "Số Lượng", "Ngày Mượn", "Ngày Trả Dự Kiến"])

            try:
                books_df = pd.read_excel("books.xlsx")
                books_df.columns = books_df.columns.str.strip()  # Xóa khoảng trắng ở tên cột
                books_df["ID"] = books_df["ID"].astype(str)  # Chuyển ID thành dạng chuỗi
            except FileNotFoundError:
                messagebox.showerror("Lỗi", "Không tìm thấy file books.xlsx!")
                return

            borrow_date = datetime.now().strftime("%Y-%m-%d")
            return_due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")  # Mặc định 14 ngày

            for book_id, quantity in book_list:
                # Kiểm tra xem sách có tồn tại không
                if book_id not in books_df["ID"].values:
                    messagebox.showerror("Lỗi", f"Sách có ID {book_id} không tồn tại!")
                    return

                available_quantity = books_df.loc[books_df["ID"] == book_id, "Số Lượng"].values[0]

                # Kiểm tra số lượng sách có đủ để mượn không
                if quantity > available_quantity:
                    messagebox.showerror("Lỗi",
                                         f"Sách ID {book_id} chỉ còn {available_quantity}, không đủ để mượn {quantity}!")
                    return

            # Nếu đủ sách, cập nhật dữ liệu
            for book_id, quantity in book_list:
                books_df.loc[books_df["ID"] == book_id, "Số Lượng"] -= quantity  # Trừ số lượng sách

                new_row = pd.DataFrame({"Mã Phiếu": [borrow_id], "Mã Thành Viên": [member_id], "Mã Sách": [book_id],
                                        "Số Lượng": [quantity], "Ngày Mượn": [borrow_date],
                                        "Ngày Trả Dự Kiến": [return_due_date]})
                borrow_df = pd.concat([borrow_df, new_row], ignore_index=True)

            # Lưu file
            borrow_df.to_excel("borrow_records.xlsx", index=False)
            books_df.to_excel("books.xlsx", index=False)

            messagebox.showinfo("Thành Công", "Phiếu mượn đã được thêm và số lượng sách đã được cập nhật!")

        tk.Button(self.view.main_frame, text="Lưu Phiếu Mượn", command=save_borrow_record, bg="green", fg="white").pack(
            pady=10)

    def return_books(self):
        """Giao diện trả sách"""
        self.view.clear_main_frame()

        tk.Label(self.view.main_frame, text="🔄 Trả Sách", font=("Arial", 16, "bold")).pack(pady=10)

        # Mã phiếu
        tk.Label(self.view.main_frame, text="Mã Phiếu:").pack()
        entry_borrow_id = tk.Entry(self.view.main_frame)
        entry_borrow_id.pack()

        def process_return():
            borrow_id = entry_borrow_id.get().strip()  # Loại bỏ khoảng trắng
            if not borrow_id:
                messagebox.showerror("Lỗi", "Vui lòng nhập mã phiếu!")
                return

            try:
                borrow_df = pd.read_excel("borrow_records.xlsx", dtype={"Mã Phiếu": str})  # Đọc file phiếu mượn
                books_df = pd.read_excel("books.xlsx", dtype={"ID": str})  # Đọc danh sách sách
                return_df = pd.read_excel("return_records.xlsx", dtype={"Mã Phiếu": str})  # Đọc file phiếu trả
            except FileNotFoundError:
                messagebox.showerror("Lỗi", "Không tìm thấy file dữ liệu!")
                return

            # Chuẩn hóa dữ liệu
            borrow_df["Mã Phiếu"] = borrow_df["Mã Phiếu"].astype(str).str.strip()
            books_df["ID"] = books_df["ID"].astype(str).str.strip()

            # Lọc danh sách các phiếu mượn có cùng mã phiếu
            borrow_records = borrow_df[borrow_df["Mã Phiếu"] == borrow_id]
            if borrow_records.empty:
                messagebox.showerror("Lỗi", f"Không tìm thấy phiếu mượn có mã {borrow_id}!")
                return

            total_late_fee = 0
            return_date = datetime.now().strftime("%Y-%m-%d")
            return_data = []  # Danh sách phiếu trả

            # Xử lý từng quyển sách trong phiếu mượn
            for _, row in borrow_records.iterrows():
                book_id = str(row["Mã Sách"]).strip()
                quantity = row["Số Lượng"]
                member_id = row["Mã Thành Viên"]

                # Chuyển đổi ngày trả dự kiến về dạng đúng
                due_date_str = str(row["Ngày Trả Dự Kiến"]).strip()
                due_date = datetime.strptime(due_date_str.split()[0], "%Y-%m-%d")

                # Tính phí trễ hạn
                actual_return_date = datetime.strptime(return_date, "%Y-%m-%d")
                late_days = (actual_return_date - due_date).days
                late_fee = max(0, late_days * 5000)
                total_late_fee += late_fee

                # Cập nhật số lượng sách
                if book_id in books_df["ID"].values:
                    books_df.loc[books_df["ID"] == book_id, "Số Lượng"] += quantity
                else:
                    messagebox.showerror("Lỗi", f"Sách có ID {book_id} không tồn tại!")
                    return

                # Thêm vào danh sách phiếu trả
                return_data.append(
                    [borrow_id, member_id, book_id, quantity, row["Ngày Mượn"], due_date_str, return_date, late_fee])

            # Xóa tất cả các phiếu mượn có cùng mã phiếu
            borrow_df = borrow_df[borrow_df["Mã Phiếu"] != borrow_id]

            # Ghi dữ liệu mới vào return_records.xlsx
            new_return_df = pd.DataFrame(return_data, columns=["Mã Phiếu", "Mã Thành Viên", "Mã Sách", "Số Lượng",
                                                               "Ngày Mượn", "Ngày Trả Dự Kiến", "Ngày Trả Thực Tế",
                                                               "Phí Trễ Hạn"])
            return_df = pd.concat([return_df, new_return_df], ignore_index=True)

            # Lưu lại dữ liệu
            borrow_df.to_excel("borrow_records.xlsx", index=False)
            books_df.to_excel("books.xlsx", index=False)
            return_df.to_excel("return_records.xlsx", index=False)

            messagebox.showinfo("Thành Công", f"Sách đã được trả thành công!\nPhí trễ hạn: {total_late_fee:,} VND")

        tk.Button(self.view.main_frame, text="Trả Sách", command=process_return, bg="blue", fg="white").pack(pady=10)

    def search_book(self, keyword):
        """Tìm kiếm sách theo tên, tác giả, thể loại"""
        results = [book for book in self.books.values() if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower()]
        return results

    def statistics(self):
        """Thống kê sách theo thể loại"""
        genre_count = {}
        for book in self.books.values():
            genre_count[book.genre] = genre_count.get(book.genre, 0) + book.quantity
        return genre_count

    def top_borrowed_books(self, top_n=5):
        """Danh sách sách được mượn nhiều nhất"""
        borrow_counts = {}
        for record in self.records.values():
            for book_id, quantity in record.borrowed_books.items():
                borrow_counts[book_id] = borrow_counts.get(book_id, 0) + quantity

        sorted_books = sorted(borrow_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_books[:top_n]
