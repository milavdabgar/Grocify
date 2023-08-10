from flask import Blueprint, render_template, session, redirect, url_for
import sqlite3

bp = Blueprint('order_confirmation', __name__)

@bp.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    # Check if the user is authenticated
    if 'email' not in session:
        return redirect(url_for('signin'))

    # Connect to the SQLite database
    cnx = sqlite3.connect('databases/fresh_basket_sample.db')
    cursor = cnx.cursor()

    # Retrieve the order details from the database
    select_order_query = """
    SELECT O.Id, P.Name, P.Description, P.Price, P.Image, P.Category
    FROM "Order" O
    JOIN OrderProduct OP ON O.Id = OP.OrderId
    JOIN Product P ON OP.ProductId = P.Id
    JOIN User U ON O.UserId = U.Id
    WHERE U.Email = ? AND O.Id = ?
    """
    cursor.execute(select_order_query, (session['email'], order_id))
    order_products = cursor.fetchall()

    # Calculate the total price of the order
    total_query = """
    SELECT SUM(P.Price)
    FROM "Order" O
    JOIN OrderProduct OP ON O.Id = OP.OrderId
    JOIN Product P ON OP.ProductId = P.Id
    JOIN User U ON O.UserId = U.Id
    WHERE U.Email = ? AND O.Id = ?
    """
    cursor.execute(total_query, (session['email'], order_id))
    total_price = cursor.fetchone()[0]

    # Retrieve shipping info from database
    select_shipping_query = """
    SELECT * FROM Shipping
    INNER JOIN User ON Shipping.UserId = User.Id
    WHERE User.Email = ?
    """
    cursor.execute(select_shipping_query, (session['email'],))
    shipping_info = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # checks items on the cart
    cart_count = get_cart_count()

    # Render the template and pass the order data to it
    return render_template('order_confirmation.html',
                           order_id=order_id,
                           order_products=order_products,
                           total_price=total_price,
                           shipping_info=shipping_info,
                           cart_count=cart_count)
