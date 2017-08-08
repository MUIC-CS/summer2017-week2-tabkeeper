from db import get_cursor
from datetime import datetime


class Borrowal:

    def __init__(self, id, lender, borrower, amount, description, borrow_date):
        self.id = id
        self.lender = lender
        self.borrower = borrower
        self.amount = float(amount)
        self.description = description
        self.borrow_date = borrow_date

    def __repr__(self):
        return 'Borrowal(%s, %s, %s, %s, %s, %s)' % (
            self.id,
            self.lender,
            self.borrower,
            self.amount,
            self.description,
            self.borrow_date
        )

    @staticmethod
    def from_dict(d):
        return Borrowal(
            d['id'],
            d['lender'],
            d['borrower'],
            d['amount'],
            d['description'],
            d['borrow_date']
        )


class BorrowalRepo:

    @staticmethod
    def find_by_id(id):
        with get_cursor() as cur:
            cur.execute("SELECT * from borrowal WHERE id=%s", (id,))
            rs = cur.fetchone()
            return Borrowal.from_dict(rs)

    @staticmethod
    def add(borrowal):
        b = borrowal
        with get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO borrowals
                (lender, borrower, amount, description, borrow_date)
                VALUES
                (%s, %s, %s, %s ,%s)
                RETURNING id
                """,
                (b.lender, b.borrower, b.amount, b.description, b.borrow_date))
            rs = cur.fetchone()
            b.id = rs['id']
            cur.connection.commit()
            return b

    @staticmethod
    def create_transaction(lender, borrower, amount, description):
        borrowal = Borrowal(
            None,
            lender.id,
            borrower.id,
            amount,
            description,
            datetime.now()
        )
        return BorrowalRepo.add(borrowal)

    @staticmethod
    def find_all():
        with get_cursor() as cur:
            cur.execute(
                "SELECT * FROM borrowals"
            )
            rs = cur.fetchall()
            return [Borrowal.from_dict(row) for row in rs]

    @staticmethod
    def find_by_lender_borrower(lender, borrower):
        with get_cursor() as cur:
            cur.execute(
                """SELECT *
                   FROM borrowals
                   WHERE borrower=%s AND lender=%s""",
                (borrower.id, lender.id)
            )
            rs = cur.fetchall()
            return [Borrowal.from_dict(row) for row in rs]

    @staticmethod
    def find_transaction_between(lender, borrower):
        with get_cursor() as cur:
            cur.execute(
                """SELECT *
                   FROM borrowals
                   WHERE borrower=%s OR lender=%s""",
                (borrower.id, lender.id)
            )
            rs = cur.fetchall()
            return [Borrowal.from_dict(row) for row in rs]

    @staticmethod
    def find_sum_by_lender_borrower(lender, borrower):
        with get_cursor() as cur:
            cur.execute(
                """SELECT COALESCE(sum(amount),0) as s
                   FROM borrowals
                   WHERE borrower=%s AND lender=%s""",
                (borrower.id, lender.id)
            )
            rs = cur.fetchone()
            return rs['s']

    @staticmethod
    def summarize_debt(left, right):  # positive = left lend right
        left_lend = BorrowalRepo.find_sum_by_lender_borrower(left, right)
        left_borrow = BorrowalRepo.find_sum_by_lender_borrower(right, left)
        return left_lend - left_borrow

    @staticmethod
    def clear_table():
        with get_cursor() as cur:
            cur.execute('DELETE from borrowals')
            cur.connection.commit()
