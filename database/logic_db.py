import sqlite3

def create_tables():
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT, 
                login TEXT,
                password TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS data(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                login TEXT,
                role TEXT,
                answer TEXT
                )''')
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

def insert_data(login, role, answer):
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    values = (login, role, answer)
    cur.execute('''INSERT INTO data(login, role, answer) VALUES (?, ?, ?)
''', values)
    con.commit()
    con.close()

def get_data(login):
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    result = cur.execute('''SELECT role, answer FROM data where login = ?''', (login,)).fetchall()
    if result is None:
        return 'Ошибочка'
    ls = []
    for role, answer in result:
        ls.append({'role': role, 'text': answer})
    return ls





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

def get_hash(login):
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    result = cur.execute('''SELECT password FROM users where login = ?''', (login,)).fetchone()
    con.close()
    if result == None:
        return None 
    return result[0]
    
def get_name(login):
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    result = cur.execute('''SELECT name FROM users where login = ?''', (login,)).fetchone()
    if result is None:
        return 'Ошибочка'
    return result[0]

if __name__ == '__main__':
    create_tables()