from math import prod
from flask import Flask, request
from connection import connection, cursor
import json

app = Flask(__name__)


@app.route("/")
def handler():
    response = ['/products/ , GET,  , List products',
                '/products/ , POST,  product_id | restaurant_id | product_name | image_path | rate | is_available , Add a new product',
                '/products/<int:product_id> , GET,  , Show a specific product',
                '/products/<int:product_id> , POST,  product_name | image_path | rate | is_available , Update a product',
                '/products/<int:product_id> , DELETE,  , Remove a product']
    return json.dumps(response)


# products
@app.route('/products/', methods=['GET', 'POST'])
def index():
    # List all products
    if request.method == "GET":
        cursor.execute("SELECT * FROM products;")
        products = []
        for product in cursor:
            products.append(product)
        return json.dumps(products)

    # Add a product
    elif request.method == "POST":
        product_id = request.form.get("product_id")
        restaurant_id = request.form.get("restaurant_id")
        product_name = request.form.get("product_name")
        image_path = request.form.get("image_path")
        rate = request.form.get("rate")
        is_available = request.form.get("is_available")
    
        cursor.execute(
            "INSERT INTO products (product_id, restaurant_id, product_name, image_path, rate, is_available) VALUES (%s,%s,%s,%s,%s,%s);",
            (product_id, restaurant_id, product_name, image_path, rate, is_available,))

        connection.commit()
        return json.dumps({'success: 1'})


@app.route('/products/<int:product_id>', methods=['GET', 'POST', 'DELETE'])
def fetch(product_id):
    cursor.execute("SELECT * FROM products WHERE product_id=%s", (product_id,))
    product = cursor.fetchone()

    # Show a product
    if request.method == 'GET':
        return json.dumps(product)

    # Update products
    elif request.method == 'POST':
        restaurant_id = request.form.get("restaurant_id") if request.form.get("restaurant_id") else product[2]
        product_name = request.form.get("product_name") if request.form.get("product_name") else product[3]
        image_path = request.form.get("image_path") if request.form.get("image_path") else product[4]
        rate = request.form.get("rate") if request.form.get("rate") else product[5]
        is_available = request.form.get("is_available") if request.form.get("is_available") else product[6]

        cursor.execute(
            "UPDATE products SET restaurant_id=%s, product_name=%s, image_path=%s, rate=%s, is_available=%s WHERE product_id=%s",
            (product_id, restaurant_id, product_name, image_path, rate, is_available,)
        )

        connection.commit()
        return json.dumps({
                "success": 1
            })

    # Delete products
    elif request.method == "DELETE":
        cursor.execute(
            "DELETE FROM products WHERE product_id=%s",
            (product_id,)
        )
        if cursor:
            response = {
                "success": 1
            }
        else:
            response = {
                "success": 0
            }
        connection.commit()
        return json.dumps(response)


if __name__ == '__main__':
    app.run()
