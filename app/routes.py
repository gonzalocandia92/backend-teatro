from flask_cors import cross_origin
from flask_login import LoginManager
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app.models import Funcion, Grupo, Productor, User, Role
from app import app, db
from app.schemas import (
    funcion_schema,funciones_schema,
    grupo_schema, grupos_schema,
    productor_schema, productores_schema,
    user_schema, usuarios_schema
    )
from flask import Response, jsonify, make_response, render_template, request, redirect, session, url_for
from flask_security import login_user, logout_user, current_user, roles_required, login_required
from werkzeug.security import generate_password_hash, check_password_hash



def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # Verifica si el token está presente en la solicitud
            verify_jwt_in_request()

            # Obtiene la identidad del token (en este caso, el ID del usuario)
            user_id = get_jwt_identity()

            # Ejemplo de lógica (ajusta según tu implementación):
            user = User.query.get(user_id)
            user_roles = [role.name for role in user.roles]

            # Verifica si el usuario tiene el rol de administrador
            if 'administrador' in user_roles:
                return fn(*args, **kwargs)
            else:
                return jsonify({'message': 'Acceso no autorizado'}), 403

        except Exception as e:
            return jsonify({'message': 'Error de autenticación'}), 401

    return wrapper


@app.route('/', methods=['GET'])
def index():
    return jsonify({'Holamundo': 'Proyecto Backend para el TPO de Codo a Codo 4.0'})

# ================================ Lista de usuarios

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        if request.method == 'GET':
            usuarios = User.query.all()
            # Serializa usuarios con roles usando Marshmallow
            usuarios_serializados = usuarios_schema.dump(usuarios)
            return jsonify({'usuarios': usuarios_serializados})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ======================================= FUNCIONES =======================================

@app.route('/funciones', methods=['GET'])
def get_funciones():
    if request.method == 'GET':
        funciones = Funcion.query.all()
        return jsonify({'funciones': funciones_schema.dump(funciones)})
    
@app.route('/funciones/<int:funcion_id>', methods=['GET'])
def mostrar_funciones(funcion_id):
    funcion = Funcion.query.get(funcion_id)

    if not funcion:
        return jsonify({'message': 'Función no encontrada'}), 404

    if request.method == 'GET':
        return jsonify({'funcion': funcion_schema.dump(funcion)})
    
@app.route('/dashboard/funciones/crear', methods=['POST'])
@admin_required
def create_funciones():
    if request.method == 'POST':
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
    
@app.route('/dashboard/funciones/<int:funcion_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def modify_funcion(funcion_id):
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

# ======================================= GRUPOS =======================================

@app.route('/grupos', methods=['GET'])
def get_grupos():
    if request.method == 'GET':
        grupos = Grupo.query.all()
        return jsonify({'grupos': grupos_schema.dump(grupos)})

@app.route('/grupos/<int:grupo_id>', methods=['GET'])
def gestionar_grupo(grupo_id):
    grupo = Grupo.query.get(grupo_id)

    if not grupo:
        return jsonify({'message': 'Grupo no encontrado'}), 404

    if request.method == 'GET':
        return jsonify({'grupo': grupo_schema.dump(grupo)})    
    
@app.route('/dashboard/grupos', methods=['GET', 'POST'])
@admin_required
def get_grupos_admin():
    if request.method == 'POST':
        nuevo_grupo = Grupo(
            nombre=request.json['nombre'],
            integrantes=request.json['integrantes']
        )
        db.session.add(nuevo_grupo)
        db.session.commit()
        return jsonify({'message': 'Grupo creado'}), 201

@app.route('/dashboard/grupos/<int:grupo_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def gestionar_grupo_admin(grupo_id):
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

# ======================================= PRODUCTORES =======================================

@app.route('/productores', methods=['GET'])
def get_productores():
    if request.method == 'GET':
        productores = Productor.query.all()
        return jsonify({'productores': productores_schema.dump(productores)})

@app.route('/productores/<int:productor_id>', methods=['GET'])
def gestionar_productor(productor_id):
    productor = Productor.query.get(productor_id)

    if not productor:
        return jsonify({'message': 'Productor no encontrado'}), 404

    if request.method == 'GET':
        return jsonify({'productor': productor_schema.dump(productor)})

@app.route('/dashboard/productores', methods=['GET', 'POST'])
@admin_required
def get_productores_admin():
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
    
@app.route('/dashboard/productores/<int:productor_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def gestionar_productor_admin(productor_id):
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


# =============================================== Login =================================
# Ruta de registro
@app.route('/register', methods=['POST'])
def register():
    from app import user_datastore
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Verifica si el usuario ya existe por dirección de correo electrónico
    existing_user = user_datastore.find_user(email=email)
    if existing_user:
        return jsonify({'message': 'El usuario ya existe'}), 400

    # Crea el nuevo usuario
    new_user = user_datastore.create_user(email=email, password=generate_password_hash(password))
    user_datastore.add_role_to_user(new_user, 'usuario')
    user_datastore.add_role_to_user(new_user, 'administrador')  # Asigna el rol de administrador
    db.session.commit()

    # Genera un token de acceso
    access_token = create_access_token(identity=new_user.id)
    login_user(user)


    # Retorna el token junto con el mensaje de registro exitoso
    return jsonify({'message': 'Registro exitoso', 'access_token': access_token}), 201

# Ruta de inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    from app import user_datastore
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Obtén el usuario por dirección de correo electrónico
    user = user_datastore.find_user(email=email)

    if user and check_password_hash(user.password, password):
        # Inicia sesión utilizando Flask-Login
        login_user(user)

        # Obtén los roles del usuario
        user_roles = [role.name for role in user.roles]

        # Genera un token de acceso con información adicional (roles)
        access_token = create_access_token(identity=user.id, additional_claims={'roles': user_roles})


        # Retorna el token junto con el mensaje de inicio de sesión exitoso
        return jsonify({'message': 'Inicio de sesión exitoso', 'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Credenciales incorrectas'}), 401
    
# Ruta de logout
@app.route('/logout', methods=['POST'])
@login_required
@cross_origin(supports_credentials=True)
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({'message': 'Cierre de sesión exitoso'}), 200
    else:
        return jsonify({'message': 'No hay usuario autenticado'}), 401