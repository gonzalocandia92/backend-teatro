from marshmallow import fields
from app import ma
from app.models import Grupo, Productor, Funcion, User

class GrupoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Grupo

class ProductorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Productor

# Esquema con Marshmallow para Funcion
class FuncionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Funcion

    id = ma.auto_field()
    titulo = ma.auto_field()
    fecha = ma.auto_field()
    hora = ma.auto_field()
    imagen = ma.auto_field()
    grupo = ma.Nested(GrupoSchema)
    productor = ma.Nested(ProductorSchema)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

user_schema = UserSchema()
usuarios_schema = UserSchema(many=True)

funcion_schema = FuncionSchema()
funciones_schema = FuncionSchema(many=True)

grupo_schema = GrupoSchema()
grupos_schema = GrupoSchema(many=True)

productor_schema = ProductorSchema()
productores_schema = ProductorSchema(many=True)