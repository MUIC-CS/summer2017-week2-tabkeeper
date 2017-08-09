from db import get_cursor


class SimpleBean:
    columns = ()

    def __init__(self, *args, **kwds):
        # TODO: make it set
        tmp = {k: v for k, v in zip(self.columns, args)}
        tmp.update(kwds)
        self.__dict__ = self.filter_params(tmp)

    @classmethod
    def filter_params(cls, d):
        ret = {}
        for col in cls.columns:
            if(col not in d):
                ret[col] = None
            else:
                ret[col] = d[col]
        return ret

    @classmethod
    def from_dict(cls, d):
        dd = {k: v for k, v in d.items() if k in cls.columns}
        return cls(**cls.filter_params(d))

    @classmethod
    def id_col(cls):
        return cls.columns[0]

    def tuple_values(self, with_id=False):
        start = 0 if with_id else 1
        return tuple(self.__dict__[col] for col in self.columns[start:])

    def __repr__(self):
        values = ['{c}={v}'.format(c=col, v=self.__dict__[col])
                  for col in self.columns]
        vals = ', '.join(values)
        classname = self.__class__.__name__
        return '<{classname} {vals}>'.format(classname=classname, vals=vals)


class SimpleRepo:
    table_name = ''
    bean_class = None
    create_query = ''

    @classmethod
    def create_table(cls, drop=False):
        if drop:
            cls.drop_table()
        with get_cursor() as cur:
            cur.execute(cls.create_query.format(table_name=cls.table_name))
            cur.connection.commit()

    @classmethod
    def find_by_col(cls, col, value):
        with get_cursor() as cur:
            cur.execute(
                """
                SELECT * from {table_name} where {col}=%s
                """.format(table_name=cls.table_name, col=col),
                (value,)
            )
            rs = cur.fetchone()
            return bean_class.from_dict(rs)

    @classmethod
    def find_all(cls):
        with get_cursor() as cur:
            cur.execute(
                """
                SELECT * from {table_name}
                """.format(table_name=cls.table_name)
            )
            return [cls.bean_class.from_dict(d) for d in cur.fetchall()]

    @classmethod
    def find_by_id(cls, value):
        return cls.find_by_col(bean_class.id_col(), value)

    @classmethod
    def delete_by_id(cls, id):
        with get_cursor() as cur:
            cur.execute(
                """
                DELETE FROM {table_name} where {id_col}=%s
                """.format(
                    table_name=cls.table_name,
                    id_col=bean_class.id_col()),
                (id,)
            )
            cur.connection.commit()

    @classmethod
    def add(cls, obj):
        col_tuple = ', '.join(cls.bean_class.columns[1:])
        ph = ', '.join(['%s'] * (len(cls.bean_class.columns) - 1))
        id_col = cls.bean_class.id_col()
        print obj.tuple_values()
        with get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO {table_name}({col_tuple})
                VALUES ({ph}) RETURNING {id_col}
                """.format(table_name=cls.table_name,
                           col_tuple=col_tuple,
                           ph=ph,
                           id_col=id_col),
                obj.tuple_values()
            )
            id = cur.fetchone()[id_col]
            cur.connection.commit()
            obj.id = id
            return obj

    @classmethod
    def add_all(cls, objs):
        return [cls.add(obj) for obj in objs]

    @classmethod
    def drop_table(cls):
        with get_cursor() as cur:
            cur.execute(
                """
                DROP TABLE IF EXISTS {table_name}
                """.format(table_name=cls.table_name)
            )
            cur.connection.commit()

    @classmethod
    def delete_table(cls):
        with get_cursor() as cur:
            cur.execute(
                """
                DELETE FROM {table_name}
                """.format(table_name=cls.table_name)
            )
            cur.connection.commit()

    @classmethod
    def fetch_by_condition(cls, cond, args):
        with get_cursor() as cur:
            cur.execute(
                """SELECT *
                   FROM {table_name}
                   WHERE {cond}
                """.format(cond=cond, table_name=cls.table_name),
                args
            )
            rs = cur.fetchall()
            return [cls.bean_class.from_dict(row) for row in rs]
