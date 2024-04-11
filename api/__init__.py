import firebase_admin
import pyrebase
import json
from firebase_admin import credentials, auth
from flask import Flask, request

cred = credentials.Certificate("api/key.json")
default_app = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('api/key.json')))

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = '12345rtfescdvf'

  from .userAPI import userAPI
  from .fichaAPI import fichaAPI
  from .mesaAPI import mesaAPI

  app.register_blueprint(userAPI, url_prefix='/user')
  app.register_blueprint(fichaAPI, url_prefix='/ficha')
  app.register_blueprint(mesaAPI, url_prefix='/mesa')

  @app.route('/api/signup', methods=['POST'])
  def signup():
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or password is None:
      return { 'success': False, 'message': 'Error: missing email or password'}, 400
    
    try:
      user = auth.create_user(
        email = email,
        password = password,
      )
      return { 'success': True, 'message': 'User was created successfully', 'user': user }, 200
    except:
      return { 'success': False, 'message': 'Error creating user' }, 400
      
  @app.route('/api/login', methods=['POST'])
  def login():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
      user = pb.auth().sign_in_with_email_and_password(email, password)
      jwt = user['idToken']
      return { 'success': True, 'token': jwt }, 200
    except:
      return { 'success': False, 'message': 'There was an error logging in' }, 400

  return app