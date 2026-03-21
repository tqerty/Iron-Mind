import sqlite3

def create_table():
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT, 
                login TEXT,
                password INTEGER)''')
    con.commit()
    con.close()