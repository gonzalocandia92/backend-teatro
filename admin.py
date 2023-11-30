from werkzeug.security import generate_password_hash
from app import db, user_datastore

def create_admin_user():
    email = 'admin@admin.com'
    password = 'admin123'

    admin_user = user_datastore.find_user(email=email)
    if admin_user:
        # Si el usuario ya existe, actualiza la contraseña
        admin_user.password = generate_password_hash(password)
    else:
        # Si el usuario no existe, crea uno nuevo como administrador
        admin_user = user_datastore.create_user(email=email, password=generate_password_hash(password))
        admin_role = user_datastore.find_role('administrador')
        user_datastore.add_role_to_user(admin_user, admin_role)

    db.session.commit()
    print('Usuario administrador creado o actualizado exitosamente.')

if __name__ == '__main__':
    create_admin_user()
