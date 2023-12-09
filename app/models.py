from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT
from app import db
from flask_security import UserMixin, RoleMixin
# Modelos para la base de datos

class Funcion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    imagen = db.Column(LONGTEXT)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo.id'), nullable=False)
    productor_id = db.Column(db.Integer, db.ForeignKey('productor.id'), nullable=False)
    grupo = db.relationship('Grupo', backref='funciones')
    productor = db.relationship('Productor', backref='funciones')
    
    def __init__(self,titulo,fecha,hora,imagen,grupo_id,productor_id):
        self.titulo=titulo   
        self.fecha=fecha
        self.hora=hora
        self.imagen=imagen
        self.grupo_id=grupo_id
        self.productor_id=productor_id
        

class Grupo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    integrantes = db.Column(db.Integer, nullable=True)

class Productor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    nombre = db.Column(db.String(255), nullable=True)
    apellido = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True)  
    roles = db.relationship('Role', secondary='user_roles', backref='user_roles')
            
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.email, self.password)


class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

