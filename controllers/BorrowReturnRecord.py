from datetime import datetime

class BorrowReturnRecord:
    def __init__(self, record_id, member_id, borrowed_books, borrow_date, return_due_date):
        self.record_id = record_id
        self.member_id = member_id
        self.borrowed_books = borrowed_books  # {book_id: quantity}
        self.borrow_date = borrow_date
        self.return_due_date = return_due_date
        self.actual_return_date = None  # Ngày trả thực tế

    def return_books(self, return_date):
        """Trả sách và tính phí trễ hạn"""
        self.actual_return_date = return_date
        late_days = (return_date - self.return_due_date).days
        late_fee = max(0, late_days * 5000)  # 5000đ/ngày trễ
        return late_fee

    def __str__(self):
        return f"Phiếu {self.record_id} | Thành viên {self.member_id} | Ngày mượn: {self.borrow_date} | Ngày trả dự kiến: {self.return_due_date} | Sách: {self.borrowed_books}"
