from application.extensions import db
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    
class Product(db.Model):
    __tablename__ = 'Product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': str(self.price),
            'image': self.image,
            'category': self.category
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
class Shipping(db.Model):
    __tablename__ = 'Shipping'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=True, default=None)
    full_name = db.Column(db.String(255), nullable=True, default=None)
    street_address = db.Column(db.String(255), nullable=True, default=None)
    city = db.Column(db.String(255), nullable=True, default=None)
    state_province = db.Column(db.String(255), nullable=True, default=None)
    postal_code = db.Column(db.String(255), nullable=True, default=None)
    country = db.Column(db.String(255), nullable=True, default=None)

class Cart(db.Model):
    __tablename__ = 'Cart'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    shipping_id = db.Column(db.Integer, db.ForeignKey('Shipping.id'), nullable=True, default=None)

class CartProduct(db.Model):
    __tablename__ = 'CartProduct'
    cart_id = db.Column(db.Integer, db.ForeignKey('Cart.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'), primary_key=True)

class Order(db.Model):
    __tablename__ = 'Order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    status = db.Column(db.String(255), nullable=False, default='processing')
    total = db.Column(db.Numeric(10, 2), nullable=False)

class OrderProduct(db.Model):
    __tablename__ = 'OrderProduct'
    order_id = db.Column(db.Integer, db.ForeignKey('Order.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'), primary_key=True)