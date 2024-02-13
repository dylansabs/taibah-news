from flask import Flask, flash

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1234567890'
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

def add_flash_message(message, category='info'):
    """
    Add a flash message to be displayed on the next request.

    Parameters:
    - message: The message text.
    - category: The message category (default is 'info').
    """
    flash(message, category)