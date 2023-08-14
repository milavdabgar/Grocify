from flask import Blueprint, render_template, request
from flask_restful import Resource, reqparse
from app.models import Product

class ProductResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='Name is required.')
    parser.add_argument('description', type=str, required=True, help='Description is required.')
    parser.add_argument('price', type=float, required=True, help='Price is required.')
    parser.add_argument('image', type=str, required=True, help='Image is required.')
    parser.add_argument('category', type=str, required=True, help='Category is required.')

    def get(self, product_id):
        product = Product.query.get(product_id)
        if product:
            return product.json()
        return {'message': 'Product not found'}, 404

    def post(self):
        data = ProductResource.parser.parse_args()
        product = Product(**data)
        product.save_to_db()
        return product.json(), 201

    def put(self, product_id):
        data = ProductResource.parser.parse_args()
        product = Product.query.get(product_id)
        if product:
            product.name = data['name']
            product.description = data['description']
            product.price = data['price']
            product.image = data['image']
            product.category = data['category']
            product.save_to_db()
            return product.json()
        return {'message': 'Product not found'}, 404

    def delete(self, product_id):
        product = Product.query.get(product_id)
        if product:
            product.delete_from_db()
            return {'message': 'Product deleted'}
        return {'message': 'Product not found'}, 404