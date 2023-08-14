import unittest
from app.models import Product
from flask_restful import reqparse
from unittest.mock import patch
from grocify import app

class TestProductResource(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='Name is required.')
        self.parser.add_argument('description', type=str, required=True, help='Description is required.')
        self.parser.add_argument('price', type=float, required=True, help='Price is required.')
        self.parser.add_argument('image', type=str, required=True, help='Image is required.')
        self.parser.add_argument('category', type=str, required=True, help='Category is required.')

    def test_get_existing_product(self):
        with app.app_context():
            with patch('app.models.Product.query.get') as mock_query_get:
                mock_query_get.return_value = Product(id=17, name='Strawberries', description='Sweet and juicy, strawberries are a delightful fruit that brings a burst of flavor to your desserts and snacks.', price=149.99, image='product-images/strawberries.jpg', category='Fruit')
                response = self.client.get('/product/1')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json, {'id': 17, 'name': 'Strawberries', 'description': 'Sweet and juicy, strawberries are a delightful fruit that brings a burst of flavor to your desserts and snacks.', 'price': 149.99, 'image': 'product-images/strawberries.jpg', 'category': 'Fruit'})

    def test_get_non_existing_product(self):
        with app.app_context():
            with patch('app.models.Product.query.get') as mock_query_get:
                mock_query_get.return_value = None
                response = self.client.get('/product/100')
                self.assertEqual(response.status_code, 404)
                self.assertEqual(response.json, {'message': 'Product not found'})

    def test_post_product(self):
        with app.app_context():
            with patch.object(Product, 'save_to_db') as mock_save_to_db:
                response = self.client.post('/product', json={'name': 'New Product', 'description': 'New Description', 'price': 10.0, 'image': 'new_image.jpg', 'category': 'New Category'})
                self.assertEqual(response.status_code, 201)
                self.assertEqual(response.json, {'id': 1, 'name': 'New Product', 'description': 'New Description', 'price': 10.0, 'image': 'new_image.jpg', 'category': 'New Category'})
                mock_save_to_db.assert_called_once()

    # Add more unit tests for the remaining methods (put, delete) as needed

if __name__ == '__main__':
    unittest.main()
