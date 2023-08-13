import unittest
from flask import Flask
from flask_testing import TestCase
from app import create_app, db
from app.extensions import db
from app.models import User

class SignInTestCase(TestCase):
    def create_app(self):
        """Create and configure a Flask app instance for testing"""
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        """Create the test database and insert test data"""
        db.create_all()
        user = User(email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """Remove the test database"""
        db.session.remove()
        db.drop_all()

    def test_signin_valid_credentials(self):
        """Test signing in with valid credentials"""
        response = self.client.post('/signin', data={'email': 'test@example.com', 'password': 'password'})
        self.assertRedirects(response, '/home')

    def test_signin_invalid_credentials(self):
        """Test signing in with invalid credentials"""
        response = self.client.post('/signin', data={'email': 'test@example.com', 'password': 'wrong_password'})
        self.assert200(response)
        self.assertTemplateUsed('signin.html')

    def test_signin_already_signed_in(self):
        """Test accessing the sign-in page while already signed in"""
        with self.client.session_transaction() as session:
            session['email'] = 'test@example.com'
        response = self.client.get('/signin')
        self.assertRedirects(response, '/home')

    def test_signin_get_request(self):
        """Test accessing the sign-in page with a GET request"""
        response = self.client.get('/signin')
        self.assert200(response)
        self.assertTemplateUsed('signin.html')

if __name__ == '__main__':
    unittest.main()
