# import os
# from app import create_app, db
# from app.models import User, FAQEntry, PDFDocument, VisitLog, AdminActionLog

# app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# @app.cli.command('initdb')
# def initdb_command():
#     """Initialize the database"""
#     db.create_all()
#     admin = User(username='admin', email='admin@example.com', is_admin=True)
#     admin.set_password('adminpassword')
#     db.session.add(admin)
#     db.session.commit()
#     print('Initialized the database with admin user')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)