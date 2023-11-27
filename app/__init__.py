# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from envs.var import DATABASE_URI
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin

# La variable DATABASE_URI contiene la URL de conexión a la base de datos MySQL.
# El formato general es 'mysql://usuario:contraseña@localhost/nombre_de_la_base_de_datos'.
# Asegúrate de reemplazar 'usuario', 'contraseña' y 'nombre_de_la_base_de_datos' con tus propias credenciales.
# DATABASE_URI = 'mysql://usuario:contraseña@localhost/nombre_de_la_base_de_datos'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

app.config['SECRET_KEY'] = 'tu_clave_secreta_aleatoria'

db = SQLAlchemy(app)
ma = Marshmallow(app)

from app import routes
from app.models import User, Role

# Creación de grupos y usuario administración por defecto
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

def create_default_roles():
    roles = ['administrador', 'usuario']  
    for role_name in roles:
        role = user_datastore.find_role(role_name)
        if not role:
            role = user_datastore.create_role(name=role_name, description=role_name)
    db.session.commit()

def create_default_user():
    admin_user = user_datastore.find_user(email='admin@example.com')
    if not admin_user:
        admin_user = user_datastore.create_user(email='admin@example.com', password='password')
        user_datastore.add_role_to_user(admin_user, 'administrador')
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_roles()
        create_default_user()
        
        
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()