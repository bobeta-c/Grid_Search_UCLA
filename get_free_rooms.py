import sys
import sqlite3

SQL_PATH = "UCLA_BUILDING_STRUCTURE.db"
DT = 120
if(len(sys.argv) != 5):
    print("ERROR: please type python get_free_rooms.py <BUILDING> <DAY> <CURRENT_TIME> <DELTA TIME>")
    exit()

building = sys.argv[1].upper()
day = int(sys.argv[2])
current_time = int(sys.argv[3])
DT = int(sys.argv[4])

if not (day < 5 and day >=0):
    print(f"ERROR {day} is not a valid day (0,1,2,3,4)")
    exit()
if not (current_time >= (8*60) and current_time <= (24*60)):
    print(f"ERROR {current_time} is not a valid time 8:00am to midnight")
    exit()


con = sqlite3.connect(SQL_PATH)
cur = con.cursor()
res = cur.execute("SELECT name FROM buildings")

buildings = res.fetchall()

if (building,) not in buildings:
    print(f"ERROR {building} not found")
    exit()

res = cur.execute("SELECT id FROM buildings WHERE name = ?", (building,))

bldg_id = res.fetchone()[0]

res = cur.execute("SELECT id, room_number FROM rooms WHERE building_id = ?", (bldg_id,))

room_ids = res.fetchall()

for room_id in room_ids:
    room_empty = True
    res = cur.execute("SELECT start_time, end_time, day_of_week, room_id FROM classes WHERE room_id = ? AND day_of_week = ?", (room_id[0], day))
    
    busy_times = res.fetchall()

    if(len(busy_times) == 0):
        continue

    end_time = current_time + DT
    for time_stamp in busy_times:
        if time_stamp[0] > end_time or time_stamp[1] < current_time:
            continue
        else:
            room_empty = False
            print("Conflict " + str(time_stamp[0]) + " " +  str(time_stamp[1]))
    if(room_empty):
        print(room_id[1] + f" is empty at this time for the next {DT} minutes")






con.close()
