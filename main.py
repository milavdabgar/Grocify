from app import create_app
from app.api.products_api import ProductResource

app, api = create_app()

api.add_resource(
    ProductResource,
    "/shop",
    "/product_list",
    "/products/<int:product_id>",
    "/products/add",
    "/products/edit/<int:product_id>",
    "/products/delete/<int:product_id>",
)


if __name__ == "__main__":
    app.run(debug=True)
