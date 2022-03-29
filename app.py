from crypt import methods
from flask import Flask
from connection import connection, cursor
import json

app = Flask(__name__)

@app.route('/')
def index():
    cursor.execute("select * from Products;")
    products = []
    for product in cursor:
        products.append(product)
    return json.dumps(product)


@app.route('/add', methods=['POST'])
def create(request):
    product_id = request.form.get("product_id")
    restaurant_id = request.form.get("restaurant_id")
    product_name = request.form.get("product_name")
    image_path = request.form.get("image_path")
    rate = request.form.get("rate")
    is_available = request.form.get("is_available")

    cursor.execute(
        "insert into Products (product_id, restaurant_id, product_name, image_path, rate, is_available, created_at, updated_at) VALUES (?,?,?,?,?,?,NOW(), NULL);",
        (product_id, restaurant_id, product_name, image_path, rate, is_available,))
    products = []
    for product in cursor:
        products.append(product)
    return json.dumps(products)


@app.route('/search', methods=['POST', 'GET'])
def search(request):
    product_id = request.form.get("product_id")

    cursor.execute(
        "select * from Products where product_id = (product_id) VALUES (?);",
        (product_id))
    products = []
    for product in cursor:
        products.append(product)
    return json.dumps(products)

@app.route('/delete', methods=['DELETE'])
def delete(request):
    product_id = request.form.get("product_id")

    cursor.execute(
        "delete from Products where product_id = (product_id) VALUES (?);",
        (product_id))


if __name__ == '__main__':
    app.run()