class Member:
    def __init__(self, member_id, name, phone, id_card, address):
        self.member_id = member_id
        self.name = name
        self.phone = phone
        self.id_card = id_card
        self.address = address
        self.borrowed_books = {}  # {book_id: quantity}

    def borrow_book(self, book_id, quantity):
        """Thêm sách vào danh sách đang mượn"""
        if book_id in self.borrowed_books:
            self.borrowed_books[book_id] += quantity
        else:
            self.borrowed_books[book_id] = quantity

    def return_book(self, book_id, quantity):
        """Xóa sách khỏi danh sách mượn"""
        if book_id in self.borrowed_books:
            self.borrowed_books[book_id] -= quantity
            if self.borrowed_books[book_id] <= 0:
                del self.borrowed_books[book_id]

    def __str__(self):
        return f"{self.member_id} - {self.name} | SĐT: {self.phone} | Địa chỉ: {self.address} | Đang mượn: {self.borrowed_books}"
