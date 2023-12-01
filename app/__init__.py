# app/__init__.py
import os
import secrets
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from envs.var import DATABASE_URI
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flask_cors import CORS
from flask_login import LoginManager
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

# La variable DATABASE_URI contiene la URL de conexión a la base de datos MySQL.
# El formato general es 'mysql://usuario:contraseña@localhost/nombre_de_la_base_de_datos'.
# Asegúrate de reemplazar 'usuario', 'contraseña' y 'nombre_de_la_base_de_datos' con tus propias credenciales.
# DATABASE_URI = 'mysql://usuario:contraseña@localhost/nombre_de_la_base_de_datos'

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_urlsafe(32)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Configuración de JWT
app.config['JWT_SECRET_KEY'] = 'ASDKNQWR234OGIV234NM!Q#SAK234DFNASDOFAS453DBN4F'  # Reemplaza con tu propia clave secreta

# flask-login
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"

app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hora

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

def create_default_user():
    admin_user = user_datastore.find_user(email='admin@example.com')
    if admin_user:
        # Si el usuario existe, actualiza la contraseña
        admin_user.password = generate_password_hash('new_password')
    else:
        # Si el usuario no existe, crea uno nuevo
        admin_user = user_datastore.create_user(email='admin@admin.com', password=generate_password_hash('admin'))
        for role_name in ['administrador', 'usuario']:
            role = user_datastore.find_role(role_name)
            user_datastore.add_role_to_user(admin_user, role)
    db.session.commit()

def create_admin_user():
    # Datos del usuario administrador
    email = 'administrador@administrador.com'
    password = 'administrador'

    # Verifica si el usuario ya existe por dirección de correo electrónico
    existing_user = user_datastore.find_user(email=email)
    if existing_user:
        user_datastore.add_role_to_user(admin_user, 'administrador')
        db.session.commit()
        print('El usuario administrador ya existe.')
        return

    # Crea el nuevo usuario administrador
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
