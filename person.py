from db import get_cursor
from simpleorm import SimpleBean, SimpleRepo


class Person(SimpleBean):

    columns = ('id', 'name', 'male')

    def sex_string(self):
        return 'male' if self.male else 'female'


class PeopleRepo(SimpleRepo):

    table_name = 'people'
    bean_class = Person
    create_query = """
        CREATE TABLE {{table_name}} (
            id SERIAL NOT NULL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            male BOOLEAN
        )
    """

    @classmethod
    def find_by_name(cls, name):
        return cls.fetch_by_condition("name=%s", (name,))[0]
