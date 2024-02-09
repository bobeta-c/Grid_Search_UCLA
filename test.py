import sqlite3

con = sqlite3.connect("UCLA_BUILDING_STRUCTURE.db")
cur = con.cursor()
res = cur.execute("SELECT * FROM buildings")
print(res.fetchone())
print("DONE")
con.close()


