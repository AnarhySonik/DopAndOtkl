import sqlite3
#sql_query = f"SELECT {letter}{digit}_max, {letter}{digit}_min FROM temp_{system} WHERE diameter_range = '{diameter_size}'"

sql_query = "SELECT h13_min, h13_max FROM temp_ne_otv WHERE diameter_range = 'от 1 до 3 вкл'"
conn = sqlite3.connect("output2.db")
cur = conn.cursor()
cur.execute(sql_query)
row = cur.fetchone()
print(row)