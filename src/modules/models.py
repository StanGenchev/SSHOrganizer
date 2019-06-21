from pony.orm import *
from os.path import expanduser
from os import makedirs

db_path = expanduser("~") + "/.local/share/sshorganizer"
makedirs(db_path, exist_ok=True)
db_file = db_path + "/organizer.sqlite"

db = Database("sqlite", db_file, create_db=True)

class Account(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    password = Optional(str)

class SessionType(db.Entity):
    id = PrimaryKey(int)
    name = Required(str, unique=True)
    arguments = Optional(str)
    connections = Set('Connection')

class FileFolder(db.Entity):
    id = PrimaryKey(int, auto=True)
    source = Required(str)
    connections = Set('Connection')

class Group(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    description = Optional(str)
    connections = Set('Connection')

class Connection(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    user = Required(str)
    password = Optional(str)
    host = Required(str)
    port = Optional(int)
    forward_local = Optional(int)
    forward_remote = Optional(int)
    arguments = Optional(str)
    commands = Optional(str)
    group = Required(Group)
    session_type = Required(SessionType)
    files_folders = Set(FileFolder)

sql_debug(False)
db.generate_mapping(create_tables=True)

@db_session
def populate_database():
    st1 = SessionType(id=0, name='Shell session', arguments='')
    st2 = SessionType(id=1, name='Port forwarding', arguments='-N -L')
    st3 = SessionType(id=2, name='File transfer', arguments='-rp')

with db_session:
    if SessionType.select().first() is None:
        populate_database()
