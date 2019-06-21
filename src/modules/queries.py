from pony.orm import *
from .models import *

@db_session
def get_account(qid: int):
    if qid is None:
        return select(a for a in Account)[:]
    else:
        return select(a for a in Account if a.id == qid)[:]

@db_session
def add_account(name: str, password: str):
    new_account = Accounts(name=name, password=password)
    return new_account

@db_session
def change_account(qid: int, name: str, password: str):
    account = Accounts[qid]
    account.name = name
    account.password = password

@db_session
def delete_account(qid: int):
    Account[qid].delete()

@db_session
def get_session_type(qid: int):
    if qid is None:
        return select(s for s in SessionType)[:]
    else:
        return select(s for s in SessionType if s.id == qid)[:]

@db_session
def get_file_folder(qid: int, cid: int):
    if qid is None:
        if cid is None:
            return select(ff for ff in FileFolder)[:]
        else:
            conn = get_connection(cid, None)[0]
            ids = []
            for i in conn.files_folders:
                ids.append(i.id)
            return select(ff for ff in FileFolder if ff.id in ids)[:]
    else:
        return select(ff for ff in FileFolder if ff.id == qid)[:]

@db_session
def add_file_folder(source: str):
    new_ff = FileFolder(source=source)

@db_session
def delete_file_folder(qid: int):
    FileFolder[qid].delete()

@db_session
def get_group(qid: int):
    if qid is None:
        return select(g for g in Group)[:]
    else:
        return select(g for g in Group if g.id == qid)[:]

@db_session
def add_group(name: str, desc: str):
    new_group = Group(name=name, description=desc)

@db_session
def change_group(qid, args):
    group = Group[qid]
    if "name" in args:
        group.name = args['name']
    if "desc" in args:
        group.description = args['desc']

@db_session
def delete_group(qid: int):
    Group[qid].delete()

@db_session
def get_connection(qid: int, gid: int):
    if qid is None:
        if gid is None:
            return select(c for c in Connection)[:]
        else:
            g = get_group(gid)
            return select(c for c in Connection if c.group == g[0])[:]
    else:
        return select(c for c in Connection if c.id == qid)[:]

@db_session
def add_connection(name, host, port, username, password, group, session_type):
    group = get_group(group)[0]
    session_type = get_session_type(session_type)[0]
    if port == '':
        port = 22
    c1 = Connection(name=name,
                    user=username,
                    password=password,
                    host=host,
                    port=port,
                    group=group,
                    session_type=session_type)

@db_session
def add_file_folder_connection(qid: int, source: str):
    c = Connection[qid]
    f = FileFolder(source=source)
    c.files_folders.add(f)

@db_session
def change_connection(qid, args):
    c = Connection[qid]
    if "port" in args:
        if args['port'] == '':
            c.port = 22
        else:
            c.port = args['port']
    if "forward_local" in args:
        if args['forward_local'] == '':
            c.forward_local = None
        else:
            c.forward_local = args['forward_local']
    if "forward_remote" in args:
        if args['forward_remote'] == '':
            c.forward_remote = None
        else:
            c.forward_remote = args['forward_remote']
    if "name" in args:
        c.name=args['name']
    if "username" in args:
        c.user=args['username']
    if "password" in args:
        c.password=args['password']
    if "host" in args:
        c.host=args['host']
    if "arguments" in args:
        c.arguments=args['arguments']
    if "commands" in args:
        c.commands=args['commands']
    if "session_type" in args:
        c.session_type = get_session_type(args['session_type'])[0]

@db_session
def delete_connection(qid: int):
    Connection[qid].delete()
