import logging

# logging.basicConfig(level=logging.development)

from flask import Flask, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import requests


app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:postgres@postgres:5432/pantry"  # TODO - do not store here
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
UPC_API_URL = "https://api.upcitemdb.com/prod/trial/lookup?upc="


@app.route("/")
def hello_world():
    logging.info("Hello, world!!")
    return "Index Page"


@app.route("/hello")
def hello():
    logging.info("Hello, world!1")
    return {
        "message": "hello, world!"
    }


@app.route("/inventory", methods=["GET", "POST"])
def handle_inventory():
    # List all inventory
    print("HANDLE Inventory")
    logging.info("HANDLE Inventory")
    if request.method == "GET":
        print("It's a GET")
        order_by = request.args.get("order_by")
        for_user = request.args.get("for_user")
        populate_details = request.args.get("populate_details")
        logging.info(f"populate_details: {populate_details}")
        items = None
        if for_user:
            items_in_inventory = InventoryModel.query.filter_by(user_id=for_user).all()

            detailed_items_in_inventory = (
                ProductModel.query.join(
                    InventoryModel, ProductModel.upc == InventoryModel.upc
                )
                .filter(InventoryModel.user_id == for_user)
                .add_columns(
                    InventoryModel.user_id, InventoryModel.qty_percentage_remaining
                )
                .all()
            )

            # .add_columns(ProductModel)
            # .add_columns(users.userId, users.name, users.email, friends.userId, friendId)\
            # .filter(users.id == friendships.friend_id)\
            # .filter(friendships.user_id == userID)\
            # .paginate(page, 1, False)

            items = detailed_items_in_inventory
            for item in detailed_items_in_inventory:
                logging.info(item)
        else:
            try:
                items = InventoryModel.query.all()
            except Exception as ex:
                return jsonify({"error": "Couldn't handle", "developer_text": str(ex)}), 500

        response = {"count": len(items), "inventory": None}

        if order_by == "category":
            # Order items by category.
            # TODO - Can I use SQLAlchemy to do this more effectively?
            # TODO - Should this be done on clients side?
            categories = dict()
            for item in items:
                if item.category in categories:
                    categories[item.category].append(item)
                else:
                    categories[item.category] = [item]

            for item_category in categories:
                response["inventory"][item.category] = [
                    {
                        "id": item.id,
                        "user_id": item.user_id,
                        "upc": item.upc,
                        "qty_percentage_remaining": item.qty_percentage_remaining,
                    }
                    for item in categories[item_category]
                ]

        else:
            response["inventory"] = [
                {
                    "id": item.id,
                    "user_id": item.user_id,
                    "upc": item.upc,
                    "qty_percentage_remaining": item.qty_percentage_remaining,
                }
                for item in items
            ]

        return response

    elif request.method == "POST":
        # Updating the users inventory
        data = request.get_json()
        logging.info(f"IT'S A POST!")
        inventory = InventoryModel(
            user_id=data["user_id"],
            upc=data["upc"],
            qty_percentage_remaining=data["qty_percentage_remaining"],
        )
        db.session.add(inventory)
        db.session.commit()

        return str(inventory), 201

    else:
        raise Exception("Method was not GET OR POST!")


def is_valid_upc(upc):
    # UPCs have 12 numeric digits.
    return len(upc) == 12 and upc.isnumeric()


@app.route("/product")
def get_products():
    # List all Products
    if request.method == "GET":
        items = ProductModel.query.all()
        return {
            "count": len(items),
            "inventory": [
                {
                    "title": item.title,
                    "description": item.description,
                    "ean": item.ean,
                    "upc": item.upc,
                    "brand": item.brand,
                    "model": item.model,
                    "category": item.category,
                    "image_url": item.image_url,
                }
                for item in items
            ],
        }
    else:
        raise Exception("Method was not GET!")


@app.route("/product/<item_id>")
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

    # filter_by(username='admin').first()
    item = ProductModel.query.filter_by(upc=item_id).first()
    if not item:
        logging.info("Searching for item in the UPC database")

        # Let's attempt to fetch it from the UPC API
        response = requests.get(f"{UPC_API_URL}{item_id}").json()
        if response["total"] != 1:
            raise Exception(
                f"We found multiple entries for {item_id} in following json {response}"
            )
        if response["items"][0]["upc"] == item_id:
            # We found our item.
            # Let's save this to our database.
            product = response["items"][0]

            image_url = None
            if product["images"]:
                image_url = product["images"][0]

            new_product = ProductModel(
                title=product["title"],
                description=product["description"],
                ean=product["ean"],
                upc=product["upc"],
                brand=product["brand"],
                model=product["model"],
                category=product["category"],
                image_url=image_url,
            )
            db.session.add(new_product)
            db.session.commit()

            return {
                "count": 1,
                "items": {
                    "title": new_product.title,
                    "description": new_product.description,
                    "ean": new_product.ean,
                    "upc": new_product.upc,
                    "brand": new_product.brand,
                    "model": new_product.model,
                    "category": new_product.category,
                    "image_url": new_product.image_url,
                },
            }

        return {"count": 0, "items": None}

    elif item:
        logging.info("We had this stored!")
        return {
            "count": 1,
            "items": {
                "title": item.title,
                "description": item.description,
                "ean": item.ean,
                "upc": item.upc,
                "brand": item.brand,
                "model": item.model,
                "category": item.category,
                "image_url": item.image_url,
            },
        }


class ProductModel(db.Model):
    __tablename__ = "product_info"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    ean = db.Column(db.String())
    upc = db.Column(db.String())
    brand = db.Column(db.String())
    model = db.Column(db.String())
    category = db.Column(db.String())
    image_url = db.Column(db.String())

    def __init__(self, title, description, ean, upc, brand, model, category, image_url):
        self.title = title
        self.description = description
        self.ean = ean
        self.upc = upc
        self.brand = brand
        self.model = model
        self.category = category
        self.image_url = image_url

        self.category = self.get_precise_category()  # TODO reconsider how this is done

    def __repr__(self):
        return f"<Inventory {self.item_name} />"

    def get_precise_category(self):
        return self.category.split(">")[-1].strip()


class InventoryModel(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String())
    upc = db.Column(db.String())
    qty_percentage_remaining = db.Column(db.Float())

    # children = relationship("Child")

    def __init__(self, user_id, upc, qty_percentage_remaining):
        self.user_id = user_id
        self.upc = upc
        self.qty_percentage_remaining = qty_percentage_remaining

    def __repr__(self):
        return f"<Inventory {self.upc} />"


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String())
    email = db.Column(db.String())
    first_name = db.Column(db.String())
    last_name = db.Column(db.Float())

    def __init__(self, user_id, email, first_name, last_name):
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = first_name + " " + last_name

    def __repr__(self):
        return f"<User {self.full_name} />"


print("IN MAIN")
app.run(host="0.0.0.0", port=8080)
