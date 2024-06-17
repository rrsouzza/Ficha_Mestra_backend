import firebase_admin
import pyrebase
import json
from firebase_admin import credentials, auth
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

cred = credentials.Certificate("api/admin_sdk.json")
default_app = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open("api/key.json")))

def create_app():
  app = Flask(__name__)
  CORS(app)

  from .characterAPI import charactersAPI
  from .mesaAPI import mesaAPI

  app.register_blueprint(charactersAPI, url_prefix='/api/character')
  app.register_blueprint(mesaAPI, url_prefix='/api/mesa')

  @app.after_request
  def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

  @app.route('/api/signup', methods=['POST'])
  def signup():
    body = request.json
    email = body.get("email")
    password = body.get("password")
    name = body.get("name")

    if email is None or password is None or name is None:
      return { 'success': False, 'message': 'Error: missing email, password or name'}, 400
    
    try:
      user = auth.create_user(
        email = email,
        password = password,
        display_name = name,
      )

      return { 'success': True, 'message': 'User was created successfully', 'user': { 'id': '{0}'.format(user.uid), 'email': email, 'name': name } }, 200
    except Exception as e:
      print("Exception: ", e, "\n--------------\n")
      return { 'success': False, 'message': 'Error creating user', 'exception': e }, 400
      
  @app.route('/api/login', methods=['POST'])
  def login():
    body = request.json
    email = body.get('email')
    password = body.get('password')

    try:
      user = pb.auth().sign_in_with_email_and_password(email, password)
    except Exception as e:
      error = e.__str__()
      if error.__contains__('\"code\": 400,'):
        if error.__contains__('\"message\": \"INVALID_LOGIN_CREDENTIALS'):
          # return { 'success': False, 'message': 'Invalid login credentials', 'exception': e }, 401
          return jsonify(success = False, message = 'Invalid login credentials', exception = e ), 401
        if error.__contains__('\"message\": \"TOO_MANY_ATTEMPTS_TRY_LATER'):
          # return { 'success': False, 'message': 'Too many attempts. Account was temporarily disabled', 'exception': e }, 403
          return jsonify(success = False, message = 'Too many attempts. Account was temporarily disabled', exception = e), 403
      # return { 'success': False, 'message': 'There was an error logging in', 'exception': e }, 400
      return jsonify(success = False, message = 'There was an error logging in', exception = e), 400
    else:
      userInfo = {
        'id': user.get('localId'),
        'email': email,
        'displayName': user.get('displayName'),
      }
      jwt = user['idToken']

      return { 'success': True, 'token': jwt, 'user': userInfo }, 200
    
  @app.route('/api/validate-token/<token>', methods=['GET'])
  def validate_token(token):
    try:
      decoded_token = auth.verify_id_token(token)
      uid = decoded_token['uid']
      return { 'success': True, 'token': token, 'message': 'Token is valid' }, 200
    except Exception as e:
      print("Exception: ", e, "\n--------------\n")
      return { 'success': False, 'message': 'Token is not valid, or an error occurred' }, 401

  return app