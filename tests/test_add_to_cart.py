import unittest
from flask import Flask
from flask_testing import TestCase
from app import create_app, db
from app.models import Cart, User, CartProduct

class TestAddToCart(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_to_cart_with_existing_cart(self):
        with self.client:
            # Create a user and cart
            user = User(email='test@example.com')
            db.session.add(user)
            db.session.commit()
            cart = Cart(user_id=user.id)
            db.session.add(cart)
            db.session.commit()

            # Make a POST request to add a product to the cart
            response = self.client.post('/add_to_cart', data={'product_id': '123'})

            # Assert that the response status code is 200
            self.assert200(response)
            # Assert that the product was inserted into the cart
            cart_product = CartProduct.query.filter_by(cart_id=cart.id, product_id='123').first()
            self.assertIsNotNone(cart_product)

    def test_add_to_cart_without_existing_cart(self):
        with self.client:
            # Create a user
            user = User(email='test@example.com')
            db.session.add(user)
            db.session.commit()

            # Make a POST request to add a product to the cart
            response = self.client.post('/add_to_cart', data={'product_id': '123'})

            # Assert that the response status code is 200
            self.assert200(response)
            # Assert that a new cart was created and the product was inserted into it
            cart = Cart.query.filter_by(user_id=user.id).first()
            self.assertIsNotNone(cart)
            cart_product = CartProduct.query.filter_by(cart_id=cart.id, product_id='123').first()
            self.assertIsNotNone(cart_product)


if __name__ == '__main__':
    unittest.main()
