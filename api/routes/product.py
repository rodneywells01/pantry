import logging
from flask import Flask, request, redirect, url_for, jsonify, Blueprint
from models.models import create_object, Product
import requests

UPC_API_URL = "https://api.upcitemdb.com/prod/trial/lookup?upc="
product = Blueprint('product', __name__)

@product.route("/product", methods=["GET"])
def get_products():
    # List all Products
    products = Product.query.all()
    return {
        "count": len(products),
        "inventory": [product.to_dict() for product in products],
    }

@product.route("/product/<item_id>")
def get_product_by_id(item_id):
    """
    - Verifiy Item ID is valid UPC
    - Check if it's in our database
    - Perform Lookup
    """

    if not is_valid_upc(item_id):
        # TODO proper API error handling
        return jsonify({"error": "item is not valid UPC"}), 400

    # Check if it's in our database.
    item = Product.query.filter_by(upc=item_id).first()
    if not item:
        logging.info("Searching for item in the UPC database")

        # Let's attempt to fetch it from the UPC API
        response = requests.get(f"{UPC_API_URL}{item_id}").json()
        print(response)
        if response.get("CODE") == "INVALID_UPC":
            return jsonify({"Error": "Invalide upc provided"}), 400

        if response["total"] != 1:
            raise Exception(
                f"We found multiple entries for {item_id} in following json {response}"
            )
        if response["items"][0]["upc"] != item_id:
            logging.info(f"Could not find item {item_id}")
            return {"count": 0, "items": list()}

        # We found our item. Save to DB.
        product = response["items"][0]
        image_url = None
        if product["images"]:
            image_url = product["images"][0]

        new_product = Product(
            title=product["title"],
            description=product["description"],
            ean=product["ean"],
            upc=product["upc"],
            brand=product["brand"],
            model=product["model"],
            category=product["category"],
            image_url=image_url,
        )
        create_object(new_product)
        return {"count": 1,"items": [new_product.to_dict()]}

    logging.info("We had this stored!")
    return {"count": 1,"items": [item.to_dict()]}


def is_valid_upc(upc):
    # UPCs have 12 numeric digits.
    return len(upc) == 12 and upc.isnumeric()
