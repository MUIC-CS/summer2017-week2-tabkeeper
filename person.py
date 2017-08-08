from db import get_cursor


class Person:

    def __init__(self, id, name, male):
        self.id = id
        self.name = name
        self.male = male

    def __repr__(self):
        return 'Person(%s, %s, %s)' % (self.id, self.name, self.male)

    def sex_string(self):
        return 'male' if self.male else 'female'

    @staticmethod
    def from_dict(d):
        return Person(d['id'], d['name'], d['male'])


class PeopleRepo:

    @staticmethod
    def find_by_id(id):
        with get_cursor() as cur:
            cur.execute("SELECT * from people WHERE id=%s", (id,))
        if rs is None:
            return None
        else:
            return Person(rs['id'], rs['name'], rs['male'])

    @staticmethod
    def find_by_name(name):
        with get_cursor() as cur:
            cur.execute("SELECT * from people WHERE name=%s", (name,))
            rs = cur.fetchone()
            if rs is None:
                return None
            else:
                return Person(rs['id'], rs['name'], rs['male'])

    @staticmethod
    def add(person):
        with get_cursor() as cur:
            cur.execute(
                "INSERT INTO people(name, male) VALUES(%s, %s) RETURNING id",
                (person.name, person.male))
            rs = cur.fetchone()
            cur.connection.commit()
            person.id = rs['id']
            return person

    @staticmethod
    def find_all():
        with get_cursor() as cur:
            cur.execute(
                "SELECT * from people"
            )
            rs = cur.fetchall()
            return [Person(row['id'], row['name'], row['male'])for row in rs]

    @staticmethod
    def clear_table():
        with get_cursor() as cur:
            cur.execute('DELETE from people')
            cur.connection.commit()

if __name__ == '__main__':
    print PeopleRepo.find_all()
