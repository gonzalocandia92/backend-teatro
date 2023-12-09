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
    funcion = fields.Nested(FuncionSchema, many=True)  
    productor = fields.Nested(ProductorSchema, many=True)  
    grupo = fields.Nested(GrupoSchema, many=True)  
    usuario = fields.Nested(UserSchema, many=True)  

    class Meta:
        model = Venta
        
    id = ma.auto_field()
    funcion_id = ma.auto_field()
    productor_id = ma.auto_field()
    grupo_id = ma.auto_field()
    usuario_id = ma.auto_field()
    fecha_venta = ma.auto_field()
    hora_venta = ma.auto_field()
    monto = ma.auto_field()

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