from flask import jsonify, request
from app import app, db
from app.models import Funcion, Grupo, Productor
from app.schemas import (
    funcion_schema,funciones_schema,
    grupo_schema, grupos_schema,
    productor_schema, productores_schema,
    )

@app.route('/', methods=['GET'])
def index():
    return jsonify({'Holamundo': 'Proyecto Backend para el TPO de Codo a Codo 4.0'})

# Rutas para la API REST
@app.route('/funciones', methods=['GET', 'POST'])
def get_funciones():
    if request.method == 'GET':
        funciones = Funcion.query.all()
        return jsonify({'funciones': funciones_schema.dump(funciones)})

    elif request.method == 'POST':
        nueva_funcion = Funcion(
            titulo=request.json['titulo'],
            fecha=request.json['fecha'],
            hora=request.json['hora'],
            imagen=request.json['imagen'],
            grupo_id=request.json['grupo_id'],
            productor_id=request.json['productor_id']
        )
        db.session.add(nueva_funcion)
        db.session.commit()
        return jsonify({'message': 'Función creada'}), 201

@app.route('/funciones/<int:funcion_id>', methods=['GET', 'PUT', 'DELETE'])
def gestionar_funcion(funcion_id):
    funcion = Funcion.query.get(funcion_id)

    if not funcion:
        return jsonify({'message': 'Función no encontrada'}), 404

    if request.method == 'GET':
        return jsonify({'funcion': funcion_schema.dump(funcion)})

    elif request.method == 'PUT':
        funcion.titulo = request.json['titulo']
        funcion.fecha = request.json['fecha']
        funcion.hora = request.json['hora']
        funcion.imagen = request.json['imagen']
        funcion.grupo_id = request.json['grupo_id']
        funcion.productor_id = request.json['productor_id']
        db.session.commit()
        return jsonify({'message': 'Función actualizada'})

    elif request.method == 'DELETE':
        db.session.delete(funcion)
        db.session.commit()
        return jsonify({'message': 'Función eliminada'})

@app.route('/grupos', methods=['GET', 'POST'])
def get_grupos():
    if request.method == 'GET':
        grupos = Grupo.query.all()
        return jsonify({'grupos': grupos_schema.dump(grupos)})

    elif request.method == 'POST':
        nuevo_grupo = Grupo(
            nombre=request.json['nombre'],
            integrantes=request.json['integrantes']
        )
        db.session.add(nuevo_grupo)
        db.session.commit()
        return jsonify({'message': 'Grupo creado'}), 201

@app.route('/grupos/<int:grupo_id>', methods=['GET', 'PUT', 'DELETE'])
def gestionar_grupo(grupo_id):
    grupo = Grupo.query.get(grupo_id)

    if not grupo:
        return jsonify({'message': 'Grupo no encontrado'}), 404

    if request.method == 'GET':
        return jsonify({'grupo': grupo_schema.dump(grupo)})

    elif request.method == 'PUT':
        grupo.nombre = request.json['nombre']
        grupo.integrantes = request.json['integrantes']
        db.session.commit()
        return jsonify({'message': 'Grupo actualizado'})

    elif request.method == 'DELETE':
        db.session.delete(grupo)
        db.session.commit()
        return jsonify({'message': 'Grupo eliminado'})

@app.route('/productores', methods=['GET', 'POST'])
def get_productores():
    if request.method == 'GET':
        productores = Productor.query.all()
        return jsonify({'productores': productores_schema.dump(productores)})

    elif request.method == 'POST':
        nuevo_productor = Productor(
            nombre=request.json['nombre']
        )
        db.session.add(nuevo_productor)
        db.session.commit()
        return jsonify({'message': 'Productor creado'}), 201

@app.route('/productores/<int:productor_id>', methods=['GET', 'PUT', 'DELETE'])
def gestionar_productor(productor_id):
    productor = Productor.query.get(productor_id)

    if not productor:
        return jsonify({'message': 'Productor no encontrado'}), 404

    if request.method == 'GET':
        return jsonify({'productor': productor_schema.dump(productor)})

    elif request.method == 'PUT':
        productor.nombre = request.json['nombre']
        db.session.commit()
        return jsonify({'message': 'Productor actualizado'})

    elif request.method == 'DELETE':
        db.session.delete(productor)
        db.session.commit()
        return jsonify({'message': 'Productor eliminado'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)