from app import app, db, create_default_roles, create_default_user

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_roles()
        create_default_user()
        app.run(debug=False)