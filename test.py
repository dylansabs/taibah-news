from database import get_user
'''
    if user:
        print('Name:', user[1])
        print('Email:', user[2])
        print('Password:', user[3])
    else:
        print('User not found in database.')
'''

for user_data in get_user('f275b595-f0a2-4feb-b529-35f7f6234108'):
    user_name = user_data[2]  # Access the name directly from the tuple
    print(f"User name: {user_name}")