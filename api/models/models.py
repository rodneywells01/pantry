# from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import current_app, g

def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        client = MongoClient(current_app.config["MONGO_URI"])
        pantry_db = client.get_database("pantry")
        db = pantry_db
        g._database = db

    return db

class BaseModel():
    __abstract__ = True

    def save(self):
        pass


class Product(BaseModel):
    __tablename__ = "product_info"

    def __init__(self, *, dynamo_item, title=None, description=None, ean=None, upc=None, brand=None, model=None, category=None, image_url=None):
        self.title = title or dynamo_item["title"]
        self.description = description or dynamo_item["description"]
        self.ean = ean or dynamo_item["ean"]
        self.upc = upc or dynamo_item["upc"]
        self.brand = brand or dynamo_item["brand"]
        self.model = model or dynamo_item["model"]
        self.category = category or dynamo_item["category"]
        self.image_url = image_url or dynamo_item["image_url"]
        self.category = category or dynamo_item["category"]

    def getAll():
        db = get_db()
        results = list(db.products.find())
        return [Product(dynamo_item=result) for result in results]

    def save(self):
        db = get_db()
        db.products.insert_one(self.to_dict())

    def __repr__(self):
        return f"<Inventory {self.item_name} />"

    def get_precise_category(self):
        return self.category.split(">")[-1].strip()

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "ean": self.ean,
            "upc": self.upc,
            "brand": self.brand,
            "model": self.model,
            "category": self.category,
            "image_url": self.image_url,
            "category": self.category,
        }


class Inventory(BaseModel):
    __tablename__ = "inventory"

    def __init__(self, user_id, upc, qty_percentage_remaining):
        self.id = None
        self.user_id = user_id
        self.upc = upc
        self.qty_percentage_remaining = qty_percentage_remaining

    def save(self):
        db = get_db()
        db.Inventory.insert_one(self.to_dict())

    def __repr__(self):
        return f"<Inventory {self.upc} />"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "upc": self.upc,
            "qty_percentage_remaining": self.qty_percentage_remaining,
        }


class User(BaseModel):
    __tablename__ = "users"

    def __init__(self, user_id, email, first_name, last_name):
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = first_name + " " + last_name

    def save(self):
        db = get_db()
        db.User.insert_one(self.to_dict())

    def __repr__(self):
        return f"<User {self.full_name} />"
