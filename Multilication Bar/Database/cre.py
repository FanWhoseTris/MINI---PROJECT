import sqlite3
def insert(name, place):
    conn = sqlite3.connect('databar.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM databar')
    ans = cursor.fetchall()
    print(ans)
    cursor.execute('''
    INSERT INTO databar (name, place)
    VALUES (?, ?)
    ''', (name, place))
    conn.commit()
    conn.close()

conn = sqlite3.connect('databar.db')
cursor = conn.cursor()
#cursor.execute('''
#CREATE TABLE IF NOT EXISTS databar (
#    ID INTEGER PRIMARY KEY,
#    name TEXT,
#    place TEXT
#)
#''')

cursor.execute('SELECT * FROM databar')
ans = cursor.fetchall()
print(ans)



conn.commit()
conn.close()
insert("vd","ok")
