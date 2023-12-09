from flask_cors import cross_origin
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, create_access_token, jwt_required
from app.models import Funcion, Grupo, Productor, User, Venta
from app import app, db
from app.schemas import (
    funcion_schema,funciones_schema,
    grupo_schema, grupos_schema,
    productor_schema, productores_schema,
    usuarios_schema, user_schema, venta_schema, ventas_schema
    )
from flask import jsonify, request
from flask_security import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError



def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            user_roles = [role.name for role in user.roles]
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
    
@app.route('/dashboard/funciones/crear', methods=['GET', 'POST'])
@admin_required
def create_funciones():
    if request.method == 'POST':
        nueva_funcion = Funcion(
            titulo=request.json['titulo'],
            fecha=request.json['fecha'],
            hora=request.json['hora'],
            imagen=request.json['imagen'],
            precio=request.json['precio'],
            activa=True,
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
        try:
            funcion.titulo = request.json.get('titulo')
            funcion.fecha = request.json.get('fecha')
            funcion.hora = request.json.get('hora')
            funcion.imagen = request.json.get('imagen')
            funcion.precio = request.json.get('precio')
            funcion.activa = request.json.get('activa')
            funcion.grupo_id = request.json.get('grupo_id')
            funcion.productor_id = request.json.get('productor_id')
            db.session.commit()
            return jsonify({'message': 'Función actualizada', 'funcion_id': funcion.id})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

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

# =============================================== Usuarios =================================
@app.route('/dashboard/usuarios', methods=['GET', 'POST'])
@admin_required
def get_usuarios_admin():
    from app import user_datastore

    if request.method == 'GET':
        usuarios = User.query.all()
        return jsonify({'usuarios': usuarios_schema.dump(usuarios)})

    elif request.method == 'POST':
        try:
            data = request.get_json()
            email = data.get('email')
            nombre = data.get('nombre')
            apellido = data.get('apellido')
            password = data.get('password')

            # Validación de datos de entrada
            if not email or not password:
                return jsonify({'message': 'Datos de usuario incompletos'}), 400

            existing_user = user_datastore.find_user(email=email)
            if existing_user:
                return jsonify({'message': 'El usuario ya existe'}), 400

            new_user = user_datastore.create_user(
                email=email,
                nombre=nombre,
                apellido=apellido,
                password=generate_password_hash(password)
            )
            user_datastore.add_role_to_user(new_user, 'usuario')
            db.session.commit()
            return jsonify({'message': 'Usuario creado'}), 201

        except Exception as e:
            return jsonify({'message': f'Error al crear usuario: {str(e)}'}), 500

@app.route('/dashboard/usuarios/<int:usuario_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def gestionar_usuario(usuario_id):
    from app import user_datastore

    usuario = User.query.get(usuario_id)

    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    if request.method == 'GET':
        return jsonify({'usuario': user_schema.dump(usuario)})

    elif request.method == 'PUT':
        try:
            usuario = User.query.get(usuario_id)

            if not usuario:
                return jsonify({'message': 'Usuario no encontrado'}), 404


            usuario.nombre = request.json['nombre']
            usuario.apellido = request.json['apellido']
            usuario.email = request.json['email']
            db.session.commit()
            


            print('aaaaaaaaaaa')
            db.session.commit()
            return jsonify({'message': 'Usuario actualizado'}), 200

        except SQLAlchemyError as e:
            # Manejo de errores específicos de SQLAlchemy
            db.session.rollback()  # Revierte los cambios en caso de error
            print(str(e))
            return jsonify({'message': f'Error de SQLAlchemy al actualizar usuario: {str(e)}'}), 500

        except Exception as e:
            # Manejo de otros errores no especificados
            print(str(e))
            return jsonify({'message': f'Error al actualizar usuario: {str(e)}'}), 500

    elif request.method == 'DELETE':
        try:
            # Eliminar cualquier asignación de roles asociada con el usuario
            user_datastore.remove_role_from_user(usuario, 'usuario')
            user_datastore.remove_role_from_user(usuario, 'administrador')

            db.session.delete(usuario)
            db.session.commit()
            return jsonify({'message': 'Usuario eliminado'}), 200

        except Exception as e:
            return jsonify({'message': f'Error al eliminar usuario: {str(e)}'}), 500
    
# =============================================== Sesiones =================================
# Ruta de registro
@app.route('/register', methods=['POST'])
def register():
    from app import user_datastore
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        
        if not email or not password:
            return jsonify({'message': 'Correo electrónico y contraseña son obligatorios'}), 400
        existing_user = user_datastore.find_user(email=email)
        if existing_user:
            return jsonify({'message': 'El usuario ya existe'}), 400
        new_user = user_datastore.create_user(
            email=email,
            nombre=nombre,
            apellido=apellido,
            password=generate_password_hash(password)
            )
        user_datastore.add_role_to_user(new_user, 'usuario')
        db.session.commit()
        user_roles = [role.name for role in new_user.roles]
        access_token = create_access_token(identity=new_user.id, additional_claims={'roles': user_roles})
        return jsonify({'message': 'Registro exitoso', 'access_token': access_token}), 201

# Ruta de inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    from app import user_datastore
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = user_datastore.find_user(email=email)

    if user and check_password_hash(user.password, password):
        login_user(user)
        user_roles = [role.name for role in user.roles]
        access_token = create_access_token(identity=user.id, additional_claims={'roles': user_roles})
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

# ============================================ VENTAS ============================================
# Ruta para usuarios logueados
@app.route('/ventas', methods=['POST'])
@jwt_required()
def create_venta():
    try:
        # Obtener la identidad del usuario desde el token JWT
        usuario_id = get_jwt_identity()

        nueva_venta = Venta(
            funcion_id=request.json['funcion_id'],
            productor_id=request.json['productor_id'],
            grupo_id=request.json['grupo_id'],
            usuario_id=usuario_id,
            fecha_venta=request.json['fecha_venta'],
            hora_venta=request.json['hora_venta'],
            monto=request.json['monto']
        )
        db.session.add(nueva_venta)
        db.session.commit()
        return jsonify({'message': 'Venta creada'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Rutas para administradores desde el dashboard
@app.route('/dashboard/ventas', methods=['GET'])
@admin_required
def get_ventas_admin():
    if request.method == 'GET':
        ventas = Venta.query.all()
        return jsonify({'ventas': usuarios_schema.dump(ventas)})
    
@app.route('/dashboard/ventas/<int:venta_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def manage_venta(venta_id):
    venta = Venta.query.get(venta_id)
    if not venta:
        return jsonify({'message': 'Venta no encontrada'}), 404

    if request.method == 'GET':
        return jsonify({'venta': venta_schema.dump(venta)})

    elif request.method == 'PUT':
        try:
            # Actualizar los campos necesarios
            venta.funcion_id = request.json.get('funcion_id')
            venta.productor_id = request.json.get('productor_id')
            venta.grupo_id = request.json.get('grupo_id')
            venta.usuario_id = request.json.get('usuario_id')
            venta.fecha_venta = request.json.get('fecha_venta')
            venta.hora_venta = request.json.get('hora_venta')
            venta.monto = request.json.get('monto')

            db.session.commit()
            return jsonify({'message': 'Venta actualizada', 'venta_id': venta.id})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    elif request.method == 'DELETE':
        db.session.delete(venta)
        db.session.commit()
        return jsonify({'message': 'Venta eliminada'})