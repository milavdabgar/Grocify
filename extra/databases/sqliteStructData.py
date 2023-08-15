import sqlite3

# Connect to the database (create it if it doesn't exist)
conn = sqlite3.connect('databases/grocify_sample.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Execute the SQL statements to create the tables
cursor.executescript(
'''
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
INSERT INTO "Cart" VALUES (1,17,0);
INSERT INTO "Cart" VALUES (2,18,0);
INSERT INTO "Cart" VALUES (3,16,0);
INSERT INTO "Cart" VALUES (5,20,NULL);
INSERT INTO "Cart" VALUES (6,21,NULL);
INSERT INTO "Cart" VALUES (7,22,NULL);
INSERT INTO "Cart" VALUES (8,23,NULL);
INSERT INTO "Cart" VALUES (9,24,NULL);
INSERT INTO "CartProduct" VALUES (1,8);
INSERT INTO "CartProduct" VALUES (1,7);
INSERT INTO "CartProduct" VALUES (1,17);
INSERT INTO "CartProduct" VALUES (1,14);
INSERT INTO "Order" VALUES (4,1,'processing',2089.45);
INSERT INTO "Order" VALUES (5,1,'processing',768.47);
INSERT INTO "Order" VALUES (6,1,'processing',768.47);
INSERT INTO "Order" VALUES (7,1,'processing',218.99);
INSERT INTO "Order" VALUES (8,1,'processing',209.48);
INSERT INTO "Order" VALUES (9,1,'processing',579.47);
INSERT INTO "Order" VALUES (15,18,'processing',2469.96);
INSERT INTO "Order" VALUES (16,16,'processing',648.48);
INSERT INTO "Order" VALUES (17,16,'processing',889.47);
INSERT INTO "Order" VALUES (18,16,'processing',549.48);
INSERT INTO "Order" VALUES (19,18,'processing',3372.95);
INSERT INTO "Order" VALUES (20,16,'processing',2159.97);
INSERT INTO "Order" VALUES (21,16,'processing',119.99);
INSERT INTO "Order" VALUES (22,18,'processing',218.99);
INSERT INTO "Order" VALUES (23,20,'processing',1389.48);
INSERT INTO "Order" VALUES (24,21,'processing',949.46);
INSERT INTO "Order" VALUES (25,16,'processing',549.48);
INSERT INTO "Order" VALUES (26,16,'processing',119.99);
INSERT INTO "Order" VALUES (27,22,'processing',1559.46);
INSERT INTO "Order" VALUES (28,16,'processing',4522.89);
INSERT INTO "Order" VALUES (29,16,'processing',388.97);
INSERT INTO "Order" VALUES (30,16,'processing',218.99);
INSERT INTO "Order" VALUES (31,23,'processing',768.47);
INSERT INTO "Order" VALUES (32,23,'processing',2584.46);
INSERT INTO "Order" VALUES (33,24,'processing',1608.47);
INSERT INTO "Order" VALUES (34,24,'processing',1518.98);
INSERT INTO "Order" VALUES (35,24,'processing',2105.46);
INSERT INTO "OrderProduct" VALUES (8,6);
INSERT INTO "OrderProduct" VALUES (8,8);
INSERT INTO "OrderProduct" VALUES (9,16);
INSERT INTO "OrderProduct" VALUES (9,11);
INSERT INTO "OrderProduct" VALUES (9,8);
INSERT INTO "OrderProduct" VALUES (15,11);
INSERT INTO "OrderProduct" VALUES (15,10);
INSERT INTO "OrderProduct" VALUES (15,12);
INSERT INTO "OrderProduct" VALUES (15,6);
INSERT INTO "OrderProduct" VALUES (16,5);
INSERT INTO "OrderProduct" VALUES (16,8);
INSERT INTO "OrderProduct" VALUES (16,7);
INSERT INTO "OrderProduct" VALUES (17,8);
INSERT INTO "OrderProduct" VALUES (17,12);
INSERT INTO "OrderProduct" VALUES (17,17);
INSERT INTO "OrderProduct" VALUES (18,7);
INSERT INTO "OrderProduct" VALUES (18,8);
INSERT INTO "OrderProduct" VALUES (19,8);
INSERT INTO "OrderProduct" VALUES (19,12);
INSERT INTO "OrderProduct" VALUES (19,10);
INSERT INTO "OrderProduct" VALUES (19,11);
INSERT INTO "OrderProduct" VALUES (19,9);
INSERT INTO "OrderProduct" VALUES (19,14);
INSERT INTO "OrderProduct" VALUES (19,5);
INSERT INTO "OrderProduct" VALUES (20,7);
INSERT INTO "OrderProduct" VALUES (20,11);
INSERT INTO "OrderProduct" VALUES (20,10);
INSERT INTO "OrderProduct" VALUES (21,6);
INSERT INTO "OrderProduct" VALUES (22,5);
INSERT INTO "OrderProduct" VALUES (22,6);
INSERT INTO "OrderProduct" VALUES (23,10);
INSERT INTO "OrderProduct" VALUES (23,8);
INSERT INTO "OrderProduct" VALUES (24,16);
INSERT INTO "OrderProduct" VALUES (24,12);
INSERT INTO "OrderProduct" VALUES (24,6);
INSERT INTO "OrderProduct" VALUES (24,8);
INSERT INTO "OrderProduct" VALUES (25,8);
INSERT INTO "OrderProduct" VALUES (25,7);
INSERT INTO "OrderProduct" VALUES (26,6);
INSERT INTO "OrderProduct" VALUES (27,10);
INSERT INTO "OrderProduct" VALUES (27,16);
INSERT INTO "OrderProduct" VALUES (27,8);
INSERT INTO "OrderProduct" VALUES (27,15);
INSERT INTO "OrderProduct" VALUES (28,5);
INSERT INTO "OrderProduct" VALUES (28,6);
INSERT INTO "OrderProduct" VALUES (28,7);
INSERT INTO "OrderProduct" VALUES (28,8);
INSERT INTO "OrderProduct" VALUES (28,9);
INSERT INTO "OrderProduct" VALUES (28,10);
INSERT INTO "OrderProduct" VALUES (28,11);
INSERT INTO "OrderProduct" VALUES (28,12);
INSERT INTO "OrderProduct" VALUES (28,13);
INSERT INTO "OrderProduct" VALUES (28,14);
INSERT INTO "OrderProduct" VALUES (28,15);
INSERT INTO "OrderProduct" VALUES (28,16);
INSERT INTO "OrderProduct" VALUES (28,17);
INSERT INTO "OrderProduct" VALUES (29,5);
INSERT INTO "OrderProduct" VALUES (29,6);
INSERT INTO "OrderProduct" VALUES (29,16);
INSERT INTO "OrderProduct" VALUES (29,15);
INSERT INTO "OrderProduct" VALUES (30,5);
INSERT INTO "OrderProduct" VALUES (30,6);
INSERT INTO "OrderProduct" VALUES (31,5);
INSERT INTO "OrderProduct" VALUES (31,6);
INSERT INTO "OrderProduct" VALUES (31,8);
INSERT INTO "OrderProduct" VALUES (31,7);
INSERT INTO "OrderProduct" VALUES (32,5);
INSERT INTO "OrderProduct" VALUES (32,7);
INSERT INTO "OrderProduct" VALUES (32,10);
INSERT INTO "OrderProduct" VALUES (32,12);
INSERT INTO "OrderProduct" VALUES (32,14);
INSERT INTO "OrderProduct" VALUES (33,5);
INSERT INTO "OrderProduct" VALUES (33,6);
INSERT INTO "OrderProduct" VALUES (33,8);
INSERT INTO "OrderProduct" VALUES (33,10);
INSERT INTO "OrderProduct" VALUES (34,5);
INSERT INTO "OrderProduct" VALUES (34,6);
INSERT INTO "OrderProduct" VALUES (34,10);
INSERT INTO "OrderProduct" VALUES (35,12);
INSERT INTO "OrderProduct" VALUES (35,15);
INSERT INTO "OrderProduct" VALUES (35,14);
INSERT INTO "OrderProduct" VALUES (35,10);
INSERT INTO "Product" VALUES (5,'Bananas','Deliciously sweet and rich in potassium, bananas are a nutritious and energizing fruit that satisfies your taste buds and supports your active lifestyle.',99,'product-images/bananas.jpg','Fruit','3');
INSERT INTO "Product" VALUES (6,'Milk','Milk is a nutrient-rich food that is an excellent source of protein, calcium, and other essential vitamins and minerals.',119.99,'product-images/milk.jpg','Dairy','4');
INSERT INTO "Product" VALUES (7,'Eggs','Nutritious and versatile, these protein-rich gems are perfect for breakfast or baking, adding delicious flavor to your meals.',459.99,'product-images/eggs.jpg','Dairy','5');
INSERT INTO "Product" VALUES (8,'Bread','Wholesome and comforting, bread is a staple food that complements any meal with its soft texture and versatile flavors.',89.49,'product-images/bread.jpg','Bread','6');
INSERT INTO "Product" VALUES (9,'Cheese','Indulge in the delightful world of cheese, a diverse range of flavors and textures that adds a creamy and savory touch to your dishes.',759,'product-images/cheese.jpg','Dairy','7');
INSERT INTO "Product" VALUES (10,'Chicken','Tender and protein-packed, chicken is a versatile white meat that offers a lean and delicious option for your everyday meals.',1299.99,'product-images/chicken.jpg','Meat','8');
INSERT INTO "Product" VALUES (11,'Beef','Savor the rich taste of beef, a succulent red meat that brings a hearty and satisfying flavor to your favorite recipes.',399.99,'product-images/beef.jpg','Meat','9');
INSERT INTO "Product" VALUES (12,'Salmon','Dive into the goodness of salmon, a pink fish renowned for its delicate taste and abundant omega-3 fatty acids, promoting a healthy heart and brain.',649.99,'product-images/salmon.jpg','Fish','10');
INSERT INTO "Product" VALUES (13,'Apples','Enjoy the crisp and refreshing nature of apples, a delicious and nutritious fruit that adds a touch of sweetness to your snacks and recipes.',249.99,'product-images/apples.jpg','Fruit','1');
INSERT INTO "Product" VALUES (14,'Oranges','Experience the zesty and invigorating flavors of oranges, a citrus fruit bursting with vitamin C and a refreshing burst of citrusy goodness.',75.49,'product-images/oranges.jpg','Fruit','2');
INSERT INTO "Product" VALUES (15,'Grapes','Enjoy the sweet and refreshing taste of grapes, a versatile fruit that is perfect for snacking or adding to salads and desserts.',79.99,'product-images/grapes.jpg','Fruit','15');
INSERT INTO "Product" VALUES (16,'Tomatoes','Versatile and vibrant, tomatoes are a staple ingredient that adds a tangy and savory touch to your salads, sauces, and more.',89.99,'product-images/tomatoes.jpg','Vegetable','16');
INSERT INTO "Product" VALUES (17,'Strawberries','Sweet and juicy, strawberries are a delightful fruit that brings a burst of flavor to your desserts and snacks.',149.99,'product-images/strawberries.jpg','Fruit','17');
INSERT INTO "Shipping" VALUES (10,17,'Teddy G','Langas','Nakuru','Mombasa','20200','Kenya');
INSERT INTO "Shipping" VALUES (11,18,'James W','Kiamunyi','Molo','Rift-Valley','20100','Kenya');
INSERT INTO "Shipping" VALUES (13,20,'John Kelly','Mangu','Kericho','Rift-Valley','011000','South Africa');
INSERT INTO "Shipping" VALUES (14,21,'Motty Blue','Wall street','New York','Boston','120543','United States');
INSERT INTO "Shipping" VALUES (31,16,'John Foe','Kiamunyi','Meru','Central','40320','Kenya');
INSERT INTO "Shipping" VALUES (32,22,'Joe Kamau','Karen','Nairobi','Central','00100','Kenya');
INSERT INTO "Shipping" VALUES (34,23,'Kate Mambo','Kiamunyi','Mombasa','Mombasa','00500','Kenya');
INSERT INTO "User" VALUES (11,'Gregory Kibs','gregkibs@example.com','Greg','0741123123');
INSERT INTO "User" VALUES (12,'Martin Luther','martinluther@example.com','Martin','0712345678');
INSERT INTO "User" VALUES (13,'Roy Martin','roymartin@example.com','Roy','0106320609');
INSERT INTO "User" VALUES (14,'Lawrence Kibs','lawrencekibs@example.com','Larry','0792123123');
INSERT INTO "User" VALUES (15,'Gregory Remmie','gregrem@you.com','Remy','0741321321');
INSERT INTO "User" VALUES (16,'John Foe','johnfoe@gmail.com','$2b$12$6lafyk5ULE2xwv.FqyzyHuntN8VMwNRkae7mForvet9FgCz/p.0Aq','0790320320');
INSERT INTO "User" VALUES (17,'Teddy Gift','teddyg@you.com','$2b$12$AH3cEuTI0ru3Amkj3LIVJOp40QTycsjIfT9I9WqQsxsTrezUCiG1a','0790192324');
INSERT INTO "User" VALUES (18,'James W','wjames@you.com','$2b$12$7OIWlRTvdlnv6UEZ7Y888uwqADlhEHj6b9NOmAtDwkV2ZHt5nUly6','0722123123');
INSERT INTO "User" VALUES (19,'Gregory Remmie','remmiegreg@you.com','$2b$12$hZGNYxCVEaX7qH.TNt4GhuAgI5rKEDmHE6dFlyseEKU0g5v6GnoNy','0741123123');
INSERT INTO "User" VALUES (20,'Kelly John','johnkelly@you.com','$2b$12$HqVye1GyzqVucrGFUzeyDOGH.Wy.m8FCMCvbZDUnfzUXkqy4oMoPy','0790234234');
INSERT INTO "User" VALUES (21,'Motty Blue','mottyb@you.com','$2b$12$7YvOEYT0H2oF8VG9C1UzTeKO62OTWc2niFOczWQd89FoodvO/RCS6','0102030405');
INSERT INTO "User" VALUES (22,'Joe Kamau','joekamau@gmail.com','$2b$12$IMrW/4bFYS8Orff8MJA2g.AFHK4VAnzV90D7anpWR7rFimMT2ox.C','0790500500');
INSERT INTO "User" VALUES (23,'Kate Mambo','mambokate@you.com','$2b$12$xKRNgh//QHxoeVqlvEvdceUVjLCl9a4xjwGM7sIm3G91xGf2SwgBC','0790192324');
INSERT INTO "User" VALUES (24,'Milav Dabgar','milav.dabgar@gmail.com','$2b$12$kcUWehIw5OTvx1JTrhqEv.miEa/i4XbuRloLrHQ32YaJXwtxh0qRW','8128576285');
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
