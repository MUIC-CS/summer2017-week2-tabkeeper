from db import get_cursor


def create_borrowals(cur):
    query = """
    DROP TABLE IF EXISTS borrowals;
    CREATE TABLE borrowals
    (
        id SERIAL NOT NULL PRIMARY KEY,
        lender int NOT NULL,
        borrower int NOT NULL,
        amount decimal(10,2) NOT NULL,
        description text NOT NULL,
        borrow_date timestamp NOT NULL
    );
    """
    cur.execute(query)


def create_people(cur):

    query = """
    DROP TABLE IF EXISTS people;
    CREATE TABLE people
    (
        id SERIAL NOT NULL PRIMARY KEY,
        name varchar(255) NOT NULL UNIQUE,
        male boolean NOT NULL
    );
    """
    cur.execute(query)


with get_cursor() as cur:
    create_borrowals(cur)
    create_people(cur)
    cur.connection.commit()
