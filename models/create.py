import sqlite3

import os
db_file = "{}/data.db".format(__file__[::-1].split("/",1)[1][::-1])
print("creating db at {}".format(db_file))
os.system("rm " + db_file.replace(" ", "\ "))

db = sqlite3.connect(db_file)
cur = db.cursor()
cur.execute("""CREATE TABLE videos (
    id INTEGER,
    category TEXT NOT NULL,
    likes INTEGER NOT NULL,
    dislikes INTEGER NOT NULL,
    title TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    length INTEGER NOT NULL,
    channel TEXT NOT NULL,
    PRIMARY KEY (id)
);""")

cur.execute("""CREATE TABLE votes (
    account TEXT NOT NULL,
    video INTEGER NOT NULL,
    FOREIGN KEY (video) REFERENCES videos (id)
);""")

db.commit()
db.close()