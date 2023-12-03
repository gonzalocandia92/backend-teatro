# app/__init__.py
import os
import secrets
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from envs.var import DATABASE_URI
from flask_security import Security, SQLAlchemyUserDatastore
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_urlsafe(32)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

app.config['JWT_SECRET_KEY'] = 'ASDKNQWR234OGIV234NM!Q#SAK234DFNASDOFAS453DBN4F'

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"

app.config['PERMANENT_SESSION_LIFETIME'] = 360000

CORS(app, supports_credentials=True)

db = SQLAlchemy(app)
ma = Marshmallow(app)

def create_default_roles():
    roles = ['administrador', 'usuario']  
    for role_name in roles:
        role = user_datastore.find_or_create_role(name=role_name, description=role_name)
        if role:
            print(f"Role {role_name} creado correctamente.")
        else:
            print(f"Error al crear el rol {role_name}.")
    db.session.commit()

def create_admin_user():
    email = 'administrador@administrador.com'
    password = 'administrador'
    existing_user = user_datastore.find_user(email=email)
    if existing_user:
        user_datastore.add_role_to_user(existing_user, 'administrador')
        db.session.commit()
        print('El usuario administrador ya existe.')
        return
    admin_user = user_datastore.create_user(email=email, password=generate_password_hash(password))
    if admin_user:
        user_datastore.add_role_to_user(admin_user, 'administrador')
    db.session.commit()

from app import routes
from app.models import User, Role      
  
def get_user(user_id):
    return User.query.get(int(user_id))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
user_datastore.get_user = get_user 
security = Security(app, user_datastore, user_model=User)
jwt = JWTManager(app)      
@app.teardown_appcontext

def shutdown_session(exception=None):
    db.session.remove()
 
migrate = Migrate(app, db)
