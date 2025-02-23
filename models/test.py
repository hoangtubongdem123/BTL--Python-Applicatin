import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime


class Book:
    def __init__(self, book_id, title, author, category, quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.quantity = quantity


class Member:
    def __init__(self, member_id, name, phone, id_card, address):
        self.member_id = member_id
        self.name = name
        self.phone = phone
        self.id_card = id_card
        self.address = address
        self.borrowed_books = {}


class BorrowReturnRecord:
    def __init__(self, record_id, member_id, borrowed_books, borrow_date, due_date):
        self.record_id = record_id
        self.member_id = member_id
        self.borrowed_books = borrowed_books  # dict of {book_id: quantity}
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = None


class LibraryManagement:
    def __init__(self):
        self.books = {}
        self.members = {}
        self.records = {}

    def add_book(self, book):
        self.books[book.book_id] = book

    def update_book(self, book_id, title=None, author=None, quantity=None):
        if book_id in self.books:
            if title:
                self.books[book_id].title = title
            if author:
                self.books[book_id].author = author
            if quantity is not None:
                self.books[book_id].quantity = quantity

    def delete_book(self, book_id):
        if book_id in self.books and self.books[book_id].quantity == 0:
            del self.books[book_id]

    def add_member(self, member):
        self.members[member.member_id] = member

    def update_member(self, member_id, name=None, phone=None, address=None):
        if member_id in self.members:
            if name:
                self.members[member_id].name = name
            if phone:
                self.members[member_id].phone = phone
            if address:
                self.members[member_id].address = address

    def delete_member(self, member_id):
        if member_id in self.members and not self.members[member_id].borrowed_books:
            del self.members[member_id]

    def borrow_books(self, member_id, book_id, quantity, borrow_date, due_date):
        if member_id in self.members and book_id in self.books:
            if self.books[book_id].quantity >= quantity and quantity <= 5:
                self.books[book_id].quantity -= quantity
                self.members[member_id].borrowed_books[book_id] = self.members[member_id].borrowed_books.get(book_id,
                                                                                                             0) + quantity
                record_id = len(self.records) + 1
                self.records[record_id] = BorrowReturnRecord(record_id, member_id, {book_id: quantity}, borrow_date,
                                                             due_date)

    def return_books(self, member_id, book_id, quantity, return_date):
        if member_id in self.members and book_id in self.members[member_id].borrowed_books:
            if self.members[member_id].borrowed_books[book_id] >= quantity:
                self.members[member_id].borrowed_books[book_id] -= quantity
                self.books[book_id].quantity += quantity
                for record in self.records.values():
                    if record.member_id == member_id and book_id in record.borrowed_books:
                        record.return_date = return_date
                        break

    def search_books(self, title=None, author=None, category=None):
        results = []
        for book in self.books.values():
            if (title and title in book.title) or (author and author in book.author) or (
                    category and category == book.category):
                results.append(book)
        return results

    def search_members(self, name=None, member_id=None):
        results = []
        for member in self.members.values():
            if (name and name in member.name) or (member_id and member_id == member.member_id):
                results.append(member)
        return results


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống quản lý thư viện")
        self.library = LibraryManagement()

        # Giao diện chính
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        self.add_book_button = tk.Button(self.main_frame, text="Thêm sách", command=self.add_book)
        self.add_book_button.pack(fill=tk.X)

        self.update_book_button = tk.Button(self.main_frame, text="Sửa thông tin sách", command=self.update_book)
        self.update_book_button.pack(fill=tk.X)

        self.delete_book_button = tk.Button(self.main_frame, text="Xóa sách", command=self.delete_book)
        self.delete_book_button.pack(fill=tk.X)

        self.add_member_button = tk.Button(self.main_frame, text="Thêm thành viên", command=self.add_member)
        self.add_member_button.pack(fill=tk.X)

        self.update_member_button = tk.Button(self.main_frame, text="Sửa thông tin thành viên",
                                              command=self.update_member)
        self.update_member_button.pack(fill=tk.X)

        self.delete_member_button = tk.Button(self.main_frame, text="Xóa thành viên", command=self.delete_member)
        self.delete_member_button.pack(fill=tk.X)

        self.borrow_book_button = tk.Button(self.main_frame, text="Lập phiếu mượn sách", command=self.borrow_books)
        self.borrow_book_button.pack(fill=tk.X)

        self.return_book_button = tk.Button(self.main_frame, text="Lập phiếu trả sách", command=self.return_books)
        self.return_book_button.pack(fill=tk.X)

        self.search_book_button = tk.Button(self.main_frame, text="Tìm kiếm sách", command=self.search_books)
        self.search_book_button.pack(fill=tk.X)

        self.search_member_button = tk.Button(self.main_frame, text="Tìm kiếm thành viên", command=self.search_members)
        self.search_member_button.pack(fill=tk.X)

        self.exit_button = tk.Button(self.main_frame, text="Thoát", command=self.root.quit)
        self.exit_button.pack(fill=tk.X)

    def add_book(self):
        book_id = simpledialog.askstring("Mã sách", "Nhập mã sách:")
        title = simpledialog.askstring("Tên sách", "Nhập tên sách:")
        author = simpledialog.askstring("Tác giả", "Nhập tác giả:")
        category = simpledialog.askstring("Thể loại", "Nhập thể loại:")
        quantity = simpledialog.askinteger("Số lượng", "Nhập số lượng:")
        if book_id and title and author and category and quantity is not None:
            self.library.add_book(Book(book_id, title, author, category, quantity))
            messagebox.showinfo("Thành công", "Đã thêm sách thành công!")

    def update_book(self):
        book_id = simpledialog.askstring("Mã sách", "Nhập mã sách cần sửa:")
        title = simpledialog.askstring("Tên sách", "Nhập tên sách mới (để trống nếu không thay đổi):")
        author = simpledialog.askstring("Tác giả", "Nhập tác giả mới (để trống nếu không thay đổi):")
        quantity = simpledialog.askinteger("Số lượng", "Nhập số lượng mới (để trống nếu không thay đổi):")
        self.library.update_book(book_id, title, author, quantity)
        messagebox.showinfo("Thành công", "Đã cập nhật thông tin sách!")

    def delete_book(self):
        book_id = simpledialog.askstring("Mã sách", "Nhập mã sách cần xóa:")
        self.library.delete_book(book_id)
        messagebox.showinfo("Thành công", "Đã xóa sách thành công!")

    def add_member(self):
        member_id = simpledialog.askstring("Mã thành viên", "Nhập mã thành viên:")
        name = simpledialog.askstring("Họ tên", "Nhập họ tên:")
        phone = simpledialog.askstring("Số điện thoại", "Nhập số điện thoại:")
        id_card = simpledialog.askstring("Căn cước công dân", "Nhập căn cước công dân:")
        address = simpledialog.askstring("Địa chỉ", "Nhập địa chỉ:")
        if member_id and name and phone and id_card and address:
            self.library.add_member(Member(member_id, name, phone, id_card, address))
            messagebox.showinfo("Thành công", "Đã thêm thành viên thành công!")

    def update_member(self):
        member_id = simpledialog.askstring("Mã thành viên", "Nhập mã thành viên cần sửa:")
        name = simpledialog.askstring("Họ tên", "Nhập họ tên mới (để trống nếu không thay đổi):")
        phone = simpledialog.askstring("Số điện thoại", "Nhập số điện thoại mới (để trống nếu không thay đổi):")
        address = simpledialog.askstring("Địa chỉ", "Nhập địa chỉ mới (để trống nếu không thay đổi):")
        self.library.update_member(member_id, name, phone, address)
        messagebox.showinfo("Thành công", "Đã cập nhật thông tin thành viên!")

    def delete_member(self):
        member_id = simpledialog.askstring("Mã thành viên", "Nhập mã thành viên cần xóa:")
        self.library.delete_member(member_id)
        messagebox.showinfo("Thành công", "Đã xóa thành viên thành công!")

    def borrow_books(self):
        member_id = simpledialog.askstring("Mã thành viên", "Nhập mã thành viên:")
        book_id = simpledialog.askstring("Mã sách", "Nhập mã sách:")
        quantity = simpledialog.askinteger("Số lượng", "Nhập số lượng:")
        borrow_date = datetime.now().strftime("%Y-%m-%d")
        due_date = simpledialog.askstring("Ngày trả", "Nhập ngày trả (YYYY-MM-DD):")
        self.library.borrow_books(member_id, book_id, quantity, borrow_date, due_date)
        messagebox.showinfo("Thành công", "Đã lập phiếu mượn sách thành công!")

    def return_books(self):
        member_id = simpledialog.askstring("Mã thành viên", "Nhập mã thành viên:")
        book_id = simpledialog.askstring("Mã sách", "Nhập mã sách:")
        quantity = simpledialog.askinteger("Số lượng", "Nhập số lượng trả:")
        return_date = datetime.now().strftime("%Y-%m-%d")
        self.library.return_books(member_id, book_id, quantity, return_date)
        messagebox.showinfo("Thành công", "Đã lập phiếu trả sách thành công!")

    def search_books(self):
        title = simpledialog.askstring("Tìm kiếm sách", "Nhập tên sách:")
        results = self.library.search_books(title=title)
        if results:
            result_text = "\n".join(
                [f"{book.title} - {book.author} - {book.category} - {book.quantity}" for book in results])
            messagebox.showinfo("Kết quả tìm kiếm", result_text)
        else:
            messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy sách!")

    def search_members(self):
        name = simpledialog.askstring("Tìm kiếm thành viên", "Nhập tên thành viên:")
        results = self.library.search_members(name=name)
        if results:
            result_text = "\n".join([f"{member.name} - {member.member_id} - {member.phone}" for member in results])
            messagebox.showinfo("Kết quả tìm kiếm", result_text)
        else:
            messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy thành viên!")


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
