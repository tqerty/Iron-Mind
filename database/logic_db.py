import sqlite3

def create_table():
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT, 
                login TEXT,
                password TEXT)''')
    con.commit()
    con.close()

def insert_user(name, login, password):
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    data = (name, login, password)
    cur.execute('''INSERT INTO users(name, login, password) VALUES (?, ?, ?)
''', data)
    con.commit()
    con.close()

def check_user(user):
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    result = cur.execute('''SELECT * FROM users where login = ? ''', (user,)).fetchone()
    con.commit()
    con.close()
    if result:
        return True
    else:
        return False

def check_l_p(login, password):
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    result = cur.execute('''SELECT * FROM users where login = ? AND password = ?''', (login, password)).fetchone()
    con.close()
    if result:
        return True
    else:
        return False