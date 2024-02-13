import sqlite3
import uuid
from sqlite3 import Connection
import datetime
from flask import url_for

# create a connection pool to the database
conn: Connection = sqlite3.connect('website/databases/users.db', check_same_thread=False, uri=True)

# create a cursor object to execute SQL commands
c = conn.cursor()

# create a table to store user information with a unique user ID
c.execute('CREATE TABLE IF NOT EXISTS users (id TEXT, name TEXT, email TEXT, password TEXT, user_avatar TEXT)')

# define a function to add a user to the database
def add_user(name:str, email:str, password:str, user_avatar:str='default.jpeg'):
    # generate a unique user ID
    user_id = str(uuid.uuid4())
    # Use url_for to generate the URL for the default avatar image
    default_avatar_path = url_for('static', filename='imgs/' + user_avatar)
    c.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?)', (user_id, name, email, password, default_avatar_path))
    conn.commit()
    print('User added to database.')


#Function to retrieve a user's information from the database via the user_id
def get_user(user_id):
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    for user in c.fetchall():
        yield user

# define a function to update a user's information in the database
def update_user(user_id, name=None, password=None, user_avatar=None):
    params = []
    query = 'UPDATE users SET '
    if name:
        query += 'name = ?, '
        params.append(name)
    if password:
        query += 'password = ?, '
        params.append(password)
    if user_avatar:
        query += 'user_avatar = ?, '
        params.append(user_avatar)
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

def check_user(name: str) -> bool:
    c.execute('SELECT * FROM users WHERE name = ?', (name,))
    user = c.fetchone()
    
    if user:
        return True
    else:
        return False
    
def check_email(email: str) -> bool:
    c.execute('SELECT * FROM users WHERE name = ?', (email,))
    user = c.fetchone()
    
    if user:
        return True
    else:
        return False
    
def check_user_for_login(name: str, password: str) -> bool:
    c.execute('SELECT * FROM users WHERE name = ? AND password = ?', (name, password))
    user = c.fetchone() 
    
    if user:
        return True
    else:
        return False
    
# Function to authenticate user and return user_id
def authenticate_user(name, passwd):
    c.execute('SELECT id FROM users WHERE name = ? AND password = ?', (name, passwd))
    user = c.fetchone()
    
    if user:
        return user[0]
    else:
        return None  # Return None if authentication fails
    
# Create a table to store user-generated content
c.execute('CREATE TABLE IF NOT EXISTS user_content (id TEXT, user_id TEXT, content_type TEXT, content TEXT, timestamp TEXT)')

def add_user_content(user_id, content_type, content):
    # Generate a unique content ID
    content_id = str(uuid.uuid4())
    # Get the current timestamp
    timestamp = str(datetime.datetime.now())
    
    # Insert the user content into the table
    c.execute('INSERT INTO user_content VALUES (?, ?, ?, ?, ?)', (content_id, user_id, content_type, content, timestamp))
    conn.commit()
    print('User content added to the database.')


# Example usage:
# add_user_content('user_id_123', 'image', 'path/to/image.jpg')
# add_user_content('user_id_123', 'video', 'path/to/video.mp4')
# add_user_content('user_id_123', 'text', 'Some text content')

# Retrieve user-generated content for a specific user
# get_user_content('user_id_123')
    
def get_user_data(user_id):
    conn = sqlite3.connect('website/databases/users.db', check_same_thread=False, uri=True)
    c = conn.cursor()

    # Fetch user data based on the user ID
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = c.fetchone()

    if user_data:
        user_dict = {
            'id': user_data[0],
            'name': user_data[1],
            'email': user_data[2],
            'password': user_data[3],
            'user_avatar': user_data[4]
        }

        # Fetch user-generated content
        c.execute('SELECT * FROM user_content WHERE user_id = ?', (user_id,))
        user_content = c.fetchall()

        user_dict['content'] = []
        for content in user_content:
            content_dict = {
                'content_id': content[0],
                'content_type': content[2],
                'content': content[3],
                'timestamp': content[4]
            }
            user_dict['content'].append(content_dict)

        conn.close()
        return user_dict
    else:
        conn.close()
        return None

'''
# Example usage:
user_id = 'f4ffd50b-15a9-44d2-abd9-20fafe1007ae'
user_data = get_user_data(user_id)

if user_data:
    print("User data:")
    print(f"ID: {user_data['id']}")
    print(f"Name: {user_data['name']}")
    print(f"Email: {user_data['email']}")
    print(f"Avatar: {user_data['user_avatar']}")

    print("\nUser content:")
    for content in user_data['content']:
        print(f"\nContent ID: {content['content_id']}")
        print(f"Content Type: {content['content_type']}")
        print(f"Content: {content['content']}")
        print(f"Timestamp: {content['timestamp']}")
else:
    print("User not found.")
'''
get_all_users()  # Now this function can be called without any issues
