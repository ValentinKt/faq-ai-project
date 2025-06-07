import unittest
from app import create_app
from modules.auth.services import AuthService
from core.database import db, database_manager
from config.settings import settings

class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        database_manager.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_register_user(self):
        with self.app.app_context():
            data = {
                'email': 'test@example.com',
                'password': 'testpassword123',
                'first_name': 'Test',
                'last_name': 'User'
            }
            user = AuthService.register_user(data)
            self.assertEqual(user['email'], data['email'])
            self.assertEqual(user['first_name'], data['first_name'])
            self.assertEqual(user['last_name'], data['last_name'])

    def test_login_user(self):
        with self.app.app_context():
            data = {
                'email': 'test@example.com',
                'password': 'testpassword123'
            }
            AuthService.register_user({**data, 'first_name': 'Test', 'last_name': 'User'})
            token = AuthService.login_user(data)
            self.assertIsNotNone(token)
            self.assertTrue(isinstance(token, str))