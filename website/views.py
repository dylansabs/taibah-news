from flask import Flask, Blueprint, request, render_template

app = Flask(__name__)

views = Blueprint('views', __name__)

@views.route("/")
@views.route("/home", methods=['POST','GET'])
def home():
    return render_template('home.html')
