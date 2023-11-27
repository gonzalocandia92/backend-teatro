from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT
from app import db

# Modelos para la base de datos

class Funcion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    imagen = db.Column(LONGTEXT)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo.id'), nullable=False)
    productor_id = db.Column(db.Integer, db.ForeignKey('productor.id'), nullable=False)

    # Definiciones de relaciones
    grupo = db.relationship('Grupo', backref='funciones')
    productor = db.relationship('Productor', backref='funciones')

class Grupo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    integrantes = db.Column(db.Integer, nullable=True)

class Productor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)

