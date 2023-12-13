import sqlite3
import uuid
from sqlite3 import Connection

# create a connection pool to the database
conn: Connection = sqlite3.connect('users.db', check_same_thread=False, uri=True)

# create a cursor object to execute SQL commands
c = conn.cursor()

# create a table to store user information with a unique user ID
c.execute('CREATE TABLE IF NOT EXISTS users (id TEXT, name TEXT, email TEXT, password TEXT)')

# define a function to add a user to the database
def add_user(name:str, email:str, password:str):
    # generate a unique user ID
    user_id = str(uuid.uuid4())
    c.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (user_id, name, email, password))
    conn.commit()
    print('User added to database.')

# define a function to retrieve a user's information from the database
def get_user(user_id):
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    if user:
        print('Name:', user[1])
        print('Email:', user[2])
        print('Password:', user[3])
    else:
        print('User not found in database.')

# define a function to update a user's information in the database
def update_user(user_id, name=None, password=None):
    params = []
    query = 'UPDATE users SET '
    if name:
        query += 'name = ?, '
        params.append(name)
    if password:
        query += 'password = ?, '
        params.append(password)
    # remove the trailing comma and space from the query string
    query = query[:-2]
    query += 'WHERE id = ?'
    params.append(user_id)
    c.execute(query, tuple(params))
    conn.commit()
    print('User information updated.')

# define a function to delete a user from the database
def delete_user(user_id):
    c.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    print('User deleted from database.')

#This function gets all users in the database
def get_all_users():
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    for user in users:
        print('ID:', user[0])
        print('Name:', user[1])
        print('Email:', user[2])
        print('Password:', user[3])

def check_user(name: str, password: str) -> bool:
    c.execute('SELECT * FROM users WHERE name = ? AND password = ?', (name, password))
    user = c.fetchone()
    
    if user:
        return True
    else:
        return False

get_all_users()  # Now this function can be called without any issues
