from flask import Flask, Blueprint, request, render_template, session
from flask import redirect, url_for, jsonify
from website import add_flash_message
from database import get_user_data, update_user 
from apis import music_news as ms 
from bs4 import BeautifulSoup
from operator import itemgetter
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

views = Blueprint('views', __name__)

# Initialize an empty list to store added URLs
added_urls = []

@views.route('/profile')
def profile():
    logged_in = session.get('logged_in')
    if not logged_in:
        return redirect(url_for('auth.login'))
    
    user_data = get_user_data(user_id=logged_in)
    id = user_data['id']
    name = user_data['name']
    email = user_data['email']
    avatar = user_data['user_avatar']
    user_authenticated = True
    
    return render_template('user.html', user_name=name, id=id, email=email, avatar=avatar, user_authenticated=user_authenticated)

@views.route("/")
@views.route("/home", methods=['POST', 'GET'])
def home():
    logged_in = session.get('logged_in')
    print(f"Logged In:{logged_in}")

    # Check if the user is logged in
    if logged_in:
        user_data = get_user_data(user_id=logged_in)

        # Fetch data from each URL
        data = []
        for url in added_urls:
            html_content = ms.get_html_content(url)
            site = BeautifulSoup(html_content, 'html.parser')
            tags = site.find_all(['div'], class_="a-story-grid")

            for entry in ms.extract_data_from_tags(tags):
                data.append({'title': entry['title'], 'time': entry['time'], 'new_time': entry['new_time'], 'mtitle': entry['m_title']})

        # Sort data by 'new_time' in descending order
        sorted_data = sorted(data, key=itemgetter('new_time'), reverse=True)

        # Check if user_data is not None and 'id' key exists
        if user_data:
            id = user_data['id']
            name = user_data['name']
            email = user_data['email']
            avatar = user_data['user_avatar']
            user_authenticated = 'logged_in' in session
            return render_template('home.html', user_authenticated=user_authenticated, user_name=name, id=id, email=email, avatar=avatar, data=sorted_data)
        else:
            # Handle the case when user_data is None or 'id' key doesn't exist
            return redirect(url_for('auth.login'))
    else:
        # User is not logged in, redirect to the login page
        return redirect(url_for('auth.login'))


@views.route("/upload-profile-picture", methods=['POST'])
def upload_profile_picture():
    logged_in = session.get('logged_in')
    if logged_in:
        user_data = get_user_data(user_id=logged_in)
        if user_data:
            file = request.files.get('profile_picture')
            if file:
                # Save the uploaded file to a location on your server
                filename = secure_filename(file.filename)  # Ensure a secure filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                # Update the user's profile picture in the database
                update_user(user_id=logged_in, user_avatar=file_path)
                
                # Return success response
                return jsonify({'success': True}), 200
            else:
                return jsonify({'success': False, 'error': 'No file provided.'}), 400
        else:
            return jsonify({'success': False, 'error': 'User data not found.'}), 404
    else:
        return jsonify({'success': False, 'error': 'User not logged in.'}), 401



@views.route('/process-url', methods=['POST'])
def process_url():
    url = request.json.get('url')
    if url:
        if url in added_urls:
            # If URL is already added, remove it
            added_urls.remove(url)
            action = 'removed'
        else:
            # If URL is not added, add it
            added_urls.append(url)
            action = 'added'

        # For demonstration purposes, just print the URL and the action
        print(f'URL {url} {action}')
        
        return jsonify({'success': True, 'action': action})
    else:
        return jsonify({'success': False, 'error': 'No URL received'})