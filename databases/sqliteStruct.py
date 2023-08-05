import sqlite3

# Connect to the database (create it if it doesn't exist)
conn = sqlite3.connect('databases/fresh_basket.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Execute the SQL statements to create the tables
cursor.executescript('''
DROP TABLE IF EXISTS "Cart";
CREATE TABLE IF NOT EXISTS "Cart" (
	"Id"	integer NOT NULL,
	"UserId"	integer NOT NULL,
	"ShippingId"	integer DEFAULT NULL,
	CONSTRAINT "Cart_ibfk_1" FOREIGN KEY("UserId") REFERENCES "User"("Id"),
	PRIMARY KEY("Id" AUTOINCREMENT),
	CONSTRAINT "Cart_ibfk_2" FOREIGN KEY("ShippingId") REFERENCES "Shipping"("Id")
);
DROP TABLE IF EXISTS "CartProduct";
CREATE TABLE IF NOT EXISTS "CartProduct" (
	"CartId"	integer NOT NULL,
	"ProductId"	integer NOT NULL,
	CONSTRAINT "CartProduct_ibfk_1" FOREIGN KEY("CartId") REFERENCES "Cart"("Id"),
	CONSTRAINT "CartProduct_ibfk_2" FOREIGN KEY("ProductId") REFERENCES "Product"("Id")
);
DROP TABLE IF EXISTS "Order";
CREATE TABLE IF NOT EXISTS "Order" (
	"Id"	integer NOT NULL,
	"UserId"	integer NOT NULL,
	"Status"	varchar(255) NOT NULL DEFAULT 'processing',
	"Total"	decimal(10, 2) NOT NULL,
	CONSTRAINT "Order_ibfk_1" FOREIGN KEY("UserId") REFERENCES "User"("Id"),
	PRIMARY KEY("Id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "OrderProduct";
CREATE TABLE IF NOT EXISTS "OrderProduct" (
	"OrderId"	integer NOT NULL,
	"ProductId"	integer NOT NULL,
	CONSTRAINT "OrderProduct_ibfk_2" FOREIGN KEY("ProductId") REFERENCES "Product"("Id"),
	CONSTRAINT "OrderProduct_ibfk_1" FOREIGN KEY("OrderId") REFERENCES "Order"("Id")
);
DROP TABLE IF EXISTS "Product";
CREATE TABLE IF NOT EXISTS "Product" (
	"Id"	integer NOT NULL,
	"Name"	varchar(255) NOT NULL,
	"Description"	varchar(255) NOT NULL,
	"Price"	decimal(10, 2) NOT NULL,
	"Image"	varchar(255) NOT NULL,
	"Category"	varchar(255) NOT NULL,
	"product_id"	varchar(255) NOT NULL,
	PRIMARY KEY("Id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "Shipping";
CREATE TABLE IF NOT EXISTS "Shipping" (
	"Id"	integer NOT NULL,
	"UserId"	integer DEFAULT NULL,
	"Full_Name"	varchar(255) DEFAULT NULL,
	"Street_Address"	varchar(255) DEFAULT NULL,
	"City"	varchar(255) DEFAULT NULL,
	"State_Province"	varchar(255) DEFAULT NULL,
	"Postal_Code"	varchar(255) DEFAULT NULL,
	"Country"	varchar(255) DEFAULT NULL,
	CONSTRAINT "Shipping_ibfk_1" FOREIGN KEY("UserId") REFERENCES "User"("Id"),
	PRIMARY KEY("Id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "User";
CREATE TABLE IF NOT EXISTS "User" (
	"Id"	integer NOT NULL,
	"Name"	varchar(255) NOT NULL,
	"Email"	varchar(255) NOT NULL,
	"Password"	varchar(255) NOT NULL,
	"Phone"	varchar(20) NOT NULL,
	PRIMARY KEY("Id" AUTOINCREMENT),
	UNIQUE("Email")
);
DROP INDEX IF EXISTS "idx_CartProduct_CartId";
CREATE INDEX IF NOT EXISTS "idx_CartProduct_CartId" ON "CartProduct" (
	"CartId"
);
DROP INDEX IF EXISTS "idx_CartProduct_ProductId";
CREATE INDEX IF NOT EXISTS "idx_CartProduct_ProductId" ON "CartProduct" (
	"ProductId"
);
DROP INDEX IF EXISTS "idx_Shipping_UserId";
CREATE INDEX IF NOT EXISTS "idx_Shipping_UserId" ON "Shipping" (
	"UserId"
);
DROP INDEX IF EXISTS "idx_OrderProduct_OrderId";
CREATE INDEX IF NOT EXISTS "idx_OrderProduct_OrderId" ON "OrderProduct" (
	"OrderId"
);
DROP INDEX IF EXISTS "idx_OrderProduct_ProductId";
CREATE INDEX IF NOT EXISTS "idx_OrderProduct_ProductId" ON "OrderProduct" (
	"ProductId"
);
DROP INDEX IF EXISTS "idx_Cart_UserId";
CREATE INDEX IF NOT EXISTS "idx_Cart_UserId" ON "Cart" (
	"UserId"
);
DROP INDEX IF EXISTS "idx_Cart_ShippingId";
CREATE INDEX IF NOT EXISTS "idx_Cart_ShippingId" ON "Cart" (
	"ShippingId"
);
DROP INDEX IF EXISTS "idx_Order_UserId";
CREATE INDEX IF NOT EXISTS "idx_Order_UserId" ON "Order" (
	"UserId"
);
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
