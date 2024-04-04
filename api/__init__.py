from flask import Flask
from firebase_admin import credentials, initialize_app

cred = credentials.Certificate("api/key.json")
default_app = initialize_app(cred)

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = '12345rtfescdvf'

  from .userAPI import userAPI
  from .fichaAPI import fichaAPI
  from .mesaAPI import mesaAPI

  app.register_blueprint(userAPI, url_prefix='/user')
  app.register_blueprint(fichaAPI, url_prefix='/ficha')
  app.register_blueprint(mesaAPI, url_prefix='/mesa')

  return app