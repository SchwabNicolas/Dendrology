from flask import Flask, render_template, url_for, redirect, request
from flask_login import LoginManager
from .config import config
from mongoengine import *

app = Flask(__name__)
app.debug = True
app.template_folder = 'templates'
app.secret_key = config.SECRET_KEY
login = LoginManager(app)
login.login_view = 'login'

connect("Dendrology")

from app import views

if __name__ == '__main__':
    app.run()