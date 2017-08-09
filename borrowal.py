from db import get_cursor
from datetime import datetime
from simpleorm import SimpleBean, SimpleRepo


class Borrowal(SimpleBean):
    columns = ('id',
               'lender',
               'borrower',
               'amount',
               'description',
               'borrow_date')


class BorrowalRepo(SimpleRepo):

    table_name = 'borrowals'
    bean_class = Borrowal
    create_query = """
        CREATE TABLE {{table_name}} (
            id SERIAL NOT NULL PRIMARY KEY,
            lender INTEGER NOT NULL,
            borrower INTEGER NOT NULL,
            amount REAL NOT NULL,
            description VARCHAR(255) NOT NULL,
            borrow_date timestamp NOT NULL
        )
    """

    @classmethod
    def create_transaction(cls, lender, borrower, amount, description):
        borrowal = Borrowal(
            id=None,
            lender=lender.id,
            borrower=borrower.id,
            amount=amount,
            description=description,
            borrow_date=datetime.now()
        )
        return cls.add(borrowal)

    @classmethod
    def find_by_lender_borrower(cls, lender, borrower):
        return cls.fetch_by_condition(
            "borrower=%s AND lender=%s",
            (borrower.id, lender.id)
        )

    @classmethod
    def find_transaction_between(cls, lender, borrower):
        return cls.fetch_by_condition(
            "borrower=%s OR lender=%s",
            (borrower.id, lender.id)
        )

    @classmethod
    def find_sum_by_lender_borrower(cls, lender, borrower):
        with get_cursor() as cur:
            cur.execute(
                """SELECT COALESCE(sum(amount),0) as s
                   FROM {table_name}
                   WHERE borrower=%s AND lender=%s
                """.format(table_name=cls.table_name),
                (borrower.id, lender.id)
            )
            rs = cur.fetchone()
            return rs['s']

    @classmethod
    def summarize_debt(cls, left, right):  # positive = left lend right
        left_lend = BorrowalRepo.find_sum_by_lender_borrower(left, right)
        left_borrow = BorrowalRepo.find_sum_by_lender_borrower(right, left)
        return left_lend - left_borrow
