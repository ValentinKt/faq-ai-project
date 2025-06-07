import unittest
from app import create_app
from flask.testing import FlaskClient
from core.database import db, database_manager
from config.settings import settings

class TestAuthEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        database_manager.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_register_and_login(self):
        register_data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post('/api/auth/register', json=register_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['status'], 'success')

        login_data = {
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post('/api/auth/login', json=login_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertIn('access_token', response.json['data'])