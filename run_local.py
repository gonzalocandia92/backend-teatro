from app import app, create_admin_user, db, create_default_roles

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_roles()
        create_admin_user()
        app.run(debug=True)
