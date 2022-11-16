import sqlite3 as sl
connect = sl.connect('app.db')

with connect:
    connect.execute("""DROP TABLE IF EXISTS use_history;""")
    
    connect.execute("""
                CREATE TABLE use_history
                (
                    use FLOAT,
                    time FLOAT,
                    day INTEGER
                );""")
    
    # default data
    for i in range(5):# days
        for j in range(24): # hours
            for k in range(4):
                connect.execute('''INSERT INTO use_history (use, time, day) VALUES (6220, %f, %d)'''%(j+k*.25,i))