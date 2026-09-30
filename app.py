from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Application configuration using environment variables
APP_ENV = os.getenv("APP_ENV", "development")
DB_HOST = os.getenv("DB_HOST", "localhost")
APP_PORT = int(os.getenv("APP_PORT", "8080"))

# Temporary in-memory product data
products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 55000,
        "category": "Electronics"
    },
    {
        "id": 2,
        "name": "Mobile Phone",
        "price": 25000,
        "category": "Electronics"
    }
]


# Health endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "environment": APP_ENV
    }), 200


# Get all products
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products), 200


# Get product by ID
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):

    for product in products:
        if product["id"] == product_id:
            return jsonify(product), 200

    return jsonify({
        "error": "Product not found"
    }), 404


# Add a new product
@app.route("/products", methods=["POST"])
def add_product():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    if "name" not in data or "price" not in data or "category" not in data:
        return jsonify({
            "error": "name, price and category are required"
        }), 400

    new_id = max([product["id"] for product in products], default=0) + 1

    new_product = {
        "id": new_id,
        "name": data["name"],
        "price": data["price"],
        "category": data["category"]
    }

    products.append(new_product)

    return jsonify(new_product), 201


# Update a product
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):

    data = request.get_json()

    for product in products:

        if product["id"] == product_id:

            if "name" in data:
                product["name"] = data["name"]

            if "price" in data:
                product["price"] = data["price"]

            if "category" in data:
                product["category"] = data["category"]

            return jsonify(product), 200

    return jsonify({
        "error": "Product not found"
    }), 404


# Delete a product
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):

    for product in products:

        if product["id"] == product_id:

            products.remove(product)

            return jsonify({
                "message": "Product deleted successfully"
            }), 200

    return jsonify({
        "error": "Product not found"
    }), 404


# Start application
if __name__ == "__main__":

    print(f"Application Environment: {APP_ENV}")
    print(f"Database Host: {DB_HOST}")
    print(f"Application Port: {APP_PORT}")

    app.run(
        host="0.0.0.0",
        port=APP_PORT
    )