import sqlite3

db = sqlite3.connect("models/data.db")
cursor = db.cursor()

def query(command, args=None, findmethod="one", executemethod="normal"):
    assert(findmethod in ["all", "one"])
    assert(executemethod in ["normal", "many"])
    if args == None:
        args = []
    if executemethod == "normal":
        cursor.execute(command, args)
    else:
        cursor.exexutemany(command, args)

    if findmethod == "all":
        result = cursor.fetchall()
    else:
        result = cursor.fetchone()
    db.commit()
    return result

def queryall(command, args=None, executemethod="normal"):
    return query(command, args, "all", executemethod)

def queryone(command, args=None, executemethod="normal"):
    return query(command, args, "one", executemethod)