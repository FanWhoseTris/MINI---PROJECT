import sqlite3
conn = sqlite3.connect('todolist.db')
cursor = conn.cursor()
cursor.execute("DELETE FROM tasks WHERE task = ?",("xs co dk ",))
conn.commit()
conn.close()