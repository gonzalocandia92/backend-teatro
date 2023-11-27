# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from envs.var import DATABASE_URI

# La variable DATABASE_URI contiene la URL de conexión a la base de datos MySQL.
# El formato general es 'mysql://usuario:contraseña@localhost/nombre_de_la_base_de_datos'.
# Asegúrate de reemplazar 'usuario', 'contraseña' y 'nombre_de_la_base_de_datos' con tus propias credenciales.
# DATABASE_URI = 'mysql://usuario:contraseña@localhost/nombre_de_la_base_de_datos'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

from app import routes

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()