import sqlite3


def cre():
    conn = sqlite3.connect(f'Database/sentences.db')
    c = conn.cursor()
    c.execute(f'''CREATE TABLE IF NOT EXISTS sentences (
                                                             id INTEGER PRIMARY KEY,
                                                             sentence TEXT,
                                                             times TEXT
                                                             )''')

    conn.commit()
    conn.close()
def inra():
    conn = sqlite3.connect('Database/sentences.db')
    c = conn.cursor()
    c.execute('''
            SELECT id, sentence, times 
            FROM sentences
            ORDER BY times ASC
            LIMIT 1
        ''')
    result = c.fetchone()
    if result:
        id, sentence, times = result
        times = int(times)
        new_times = times + 1
        c.execute('''
                UPDATE sentences
                SET times = ?
                WHERE id = ?
            ''', (new_times, id))
        conn.commit()
    conn.close()
    print(result)
def ad():
    conn = sqlite3.connect(f'Database/sentences.db')
    c = conn.cursor()
    c.execute("INSERT INTO sentences (sentence, times) VALUES (?, ?)", ('ban cc', '3'))

    conn.commit()
    conn.close()
#cre()
#ad()
inra()