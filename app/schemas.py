from marshmallow import fields
from app import ma
from app.models import Grupo, Productor, Funcion, User, Role, Venta

class GrupoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Grupo

class ProductorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Productor

class FuncionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Funcion

    id = ma.auto_field()
    titulo = ma.auto_field()
    fecha = ma.auto_field()
    hora = ma.auto_field()
    imagen = ma.auto_field()
    activa = ma.auto_field()
    precio = ma.auto_field()
    grupo = ma.Nested(GrupoSchema)
    productor = ma.Nested(ProductorSchema)

class RolSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        
class UserSchema(ma.SQLAlchemySchema):
    roles = fields.Nested(RolSchema, many=True)  

    class Meta:
        model = User

    id = ma.auto_field()
    email = ma.auto_field()
    nombre = ma.auto_field()
    apellido = ma.auto_field()
    
class VentaSchema(ma.SQLAlchemyAutoSchema):
    funcion = fields.Nested(FuncionSchema)
    productor = fields.Nested(ProductorSchema)
    grupo = fields.Nested(GrupoSchema)
    usuario = fields.Nested(UserSchema)

    class Meta:
        model = Venta
        include_fk = True  # Incluye automáticamente las claves foráneas

venta_schema = VentaSchema()
ventas_schema = VentaSchema(many=True)

user_schema = UserSchema()
usuarios_schema = UserSchema(many=True)

funcion_schema = FuncionSchema()
funciones_schema = FuncionSchema(many=True)

grupo_schema = GrupoSchema()
grupos_schema = GrupoSchema(many=True)

productor_schema = ProductorSchema()
productores_schema = ProductorSchema(many=True)