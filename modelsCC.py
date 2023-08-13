from extensions import db

class User(db.Model):
    __tablename__ = 'User'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    Phone = db.Column(db.String(20), nullable=False)
    
class Product(db.Model):
    __tablename__ = 'Product'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.String(255), nullable=False)
    Price = db.Column(db.Numeric(10, 2), nullable=False)
    Image = db.Column(db.String(255), nullable=False)
    Category = db.Column(db.String(255), nullable=False)
    product_id = db.Column(db.String(255), nullable=False)
    
class Shipping(db.Model):
    __tablename__ = 'Shipping'
    Id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.Id'), nullable=True)
    Full_Name = db.Column(db.String(255), nullable=True)
    Street_Address = db.Column(db.String(255), nullable=True)
    City = db.Column(db.String(255), nullable=True)
    State_Province = db.Column(db.String(255), nullable=True)
    Postal_Code = db.Column(db.String(255), nullable=True)
    Country = db.Column(db.String(255), nullable=True)    

class Cart(db.Model):
    __tablename__ = 'Cart'
    Id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.Id'), nullable=False)
    ShippingId = db.Column(db.Integer, db.ForeignKey('Shipping.Id'), nullable=True)

class CartProduct(db.Model):
    __tablename__ = 'CartProduct'
    CartId = db.Column(db.Integer, db.ForeignKey('Cart.Id'), primary_key=True)
    ProductId = db.Column(db.Integer, db.ForeignKey('Product.Id'), primary_key=True)

class Order(db.Model):
    __tablename__ = 'Order'
    Id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.Id'), nullable=False)
    Status = db.Column(db.String(255), nullable=False, default='processing')
    Total = db.Column(db.Numeric(10, 2), nullable=False)

class OrderProduct(db.Model):
    __tablename__ = 'OrderProduct'
    OrderId = db.Column(db.Integer, db.ForeignKey('Order.Id'), primary_key=True)
    ProductId = db.Column(db.Integer, db.ForeignKey('Product.Id'), primary_key=True)
