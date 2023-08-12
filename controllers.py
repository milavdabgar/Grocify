from flask import session
import mysql.connector
from config import *

def get_cart_count():
    # Check if the user is authenticated
    if 'email' in session:
        # Connect to the MySQL database
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Retrieve the cart count for the user
        select_query = """
        SELECT COUNT(CP.ProductId)
        FROM CartProduct CP
        JOIN Cart C ON CP.CartId = C.Id
        JOIN User U ON C.UserId = U.Id
        WHERE U.Email = %s
        """
        cursor.execute(select_query, (session['email'],))
        cart_count = cursor.fetchone()[0]

        # Close the cursor and connection
        cursor.close()
        cnx.close()

        return cart_count

    pass
