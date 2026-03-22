from app import create_app

app = create_app()

with app.app_context():
    from models import db
    from models.user import User

    # Find admin
    admin = User.query.filter_by(role='admin').first()

    if admin:
        admin.set_password('Admin123')
        db.session.commit()
        print(f"Password reset for {admin.email}")
        print("New password: Admin123")
    else:
        print("No admin user found!")