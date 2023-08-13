import unittest
from app.extensions import db
from app.models import User, Product
from app import app

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_creation(self):
        user = User(name='John Doe', email='john@example.com', password='password', phone='1234567890')
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.filter_by(email='john@example.com').first()
        self.assertEqual(retrieved_user.name, 'John Doe')
        self.assertEqual(retrieved_user.phone, '1234567890')

    def test_product_creation(self):
        product = Product(name='Product 1', description='Description 1', price=10.99, image='image.jpg', category='Category 1', product_id='12345')
        db.session.add(product)
        db.session.commit()

        retrieved_product = Product.query.filter_by(name='Product 1').first()
        self.assertEqual(retrieved_product.description, 'Description 1')
        self.assertEqual(retrieved_product.price, 10.99)

    # Add more test methods for other models

if __name__ == '__main__':
    unittest.main()
