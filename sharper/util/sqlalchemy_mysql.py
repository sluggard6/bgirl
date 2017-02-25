# -*- coding:utf-8 -*-

__author__ = [
    '"liubo" <liubo@51domi.com>'
]

tables = ["page_content"]

HOST = "106.75.97.108"
USER = "admin"
PASSWORD = "admin$bgirl#2016!"
DB = "bgirl"


# DB = "linkedin"

class Column():
    def __init__(self, name, type, nullable, is_primary_key, default, is_auto_increment):
        self.name = name
        self.type = self.type_convert(type)
        self.extras = []
        if nullable == "YES":
            self.extras.append("nullable=True")
        else:
            self.extras.append("nullable=False")
        if is_primary_key == "PRI":
            self.extras.append("primary_key=True")
        if is_auto_increment == "auto_increment":
            self.extras.append("autoincrement=True")

        if default == "":
            self.extras.append("default=''")
        elif default is not None and name not in ['create_time', 'modify_time']:
            self.extras.append("default=%s" % default)
        elif name in ['create_time', 'modify_time']:
            self.extras.append("default=datetime.now")

    def __repr__(self):
        return "    %s = Column(u'%s', %s, %s)" % (self.name, self.name, self.type, ",".join(self.extras))

        # print type(r)

    @classmethod
    def type_convert(cls, type):
        if type.find("int") != -1:
            return "INTEGER()"
        elif type.find("varchar(") != -1:
            return "VARCHAR(length=%s)" % type[8:-1]
        elif type.find("datetime") != -1:
            return "DATETIME()"
        elif type.find("timestamp") != -1:
            return "TIMESTAMP()"
        elif type.find("date") != -1:
            return "DATE()"


def to_camel_case(name):
    if name.find("_") != -1:
        names = name.split("_")
        new_name = ""
        for n in names:
            new_name += n.title()
        return new_name
    return name.title()


def get_columns(table):
    import MySQLdb

    db = MySQLdb.connect(host=HOST, user=USER,
                         passwd=PASSWORD, db=DB)
    c = db.cursor()
    ret = c.execute("""desc `%s`""" % table)
    columns = []

    for d in c.fetchall():
        columns.append(Column(d[0], d[1], d[2], d[3], d[4], d[5]))
    return columns


def print_table_class(table):
    columns = get_columns(table)
    print '''
class %s(BaseModel):
    __tablename__ = '%s'
    __table_args__ = {}
''' % (to_camel_case(table), table)
    for column in columns:
        print column.__repr__()


def print_table_wiki(table):
    import MySQLdb

    db = MySQLdb.connect(host=HOST, user=USER,
                         passwd=PASSWORD, db=DB)
    c = db.cursor()
    ret = c.execute("""show full columns from %s""" % table)
    columns = []
    print "=== %s ===" % table
    print "||= 字段名 =||= 类型 =||= 备注 =|| "
    for d in c.fetchall():
        print "|| %s \t|| %s \t|| %s || " % (d[0], d[1], d[8])


for table in tables:
    print_table_class(table)
    print "\n"
    print_table_wiki(table)
