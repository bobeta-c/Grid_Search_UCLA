import sqlite3

con = sqlite3.connect("random.db")
cur = con.cursor()
res = cur.execute("SELECT * FROM buildings")
print(res.fetchone())
print("DONE")
cur.execute("INSERT INTO buildings (name) VALUES(?)", ("room1",))
con.commit()
con.close()


