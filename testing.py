import logging
logging.basicConfig(level=logging.DEBUG)

from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate

import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
"postgresql://postgres:postgres@postgres:5432/pantry" #TODO - do not store here 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
UPC_API_URL = "https://api.upcitemdb.com/prod/trial/lookup?upc="


def handle_inventory():
    # List all inventory 
    for_user="rodneywells01"
    
    items_in_inventory = InventoryModel.query.filter_by(user_id=for_user).all()

    detailed_items_in_inventory = ProductModel.query\
        .join(InventoryModel, ProductModel.upc==InventoryModel.upc)\
        .filter(InventoryModel.user_id == for_user)\
        .add_columns(
            InventoryModel.user_id,
            InventoryModel.qty_percentage_remaining
        )

        # .add_columns(ProductModel)
        # .add_columns(users.userId, users.name, users.email, friends.userId, friendId)\
        # .filter(users.id == friendships.friend_id)\
        # .filter(friendships.user_id == userID)\
        # .paginate(page, 1, False)

    items = detailed_items_in_inventory
    for item in detailed_items_in_inventory: 
        logging.info(item) 

    response = {
        "count": len(items),
        "inventory": None
    }

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
                } for item in categories[item_category]
            ]

    else:
        response["inventory"] = [
            {
                "id": item.id, 
                "user_id": item.user_id,
                "upc": item.upc,
                "qty_percentage_remaining": item.qty_percentage_remaining,
            } for item in items
        ]
    
    return response




class ProductModel(db.Model):
    __tablename__ = 'product_info'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    ean = db.Column(db.String())
    upc = db.Column(db.String())
    brand = db.Column(db.String())
    model = db.Column(db.String())
    category = db.Column(db.String())
    image_url = db.Column(db.String())

    def __init__(self,title,description,ean,upc,brand,model,category,image_url):
        self.title = title
        self.description = description
        self.ean = ean
        self.upc = upc
        self.brand = brand
        self.model = model
        self.category = category
        self.image_url = image_url

        self.category = self.get_precise_category() #TODO reconsider how this is done 

    def __repr__(self):
        return f"<Inventory {self.item_name} />"

    def get_precise_category(self): 
        return self.category.split(">")[-1].strip()


class InventoryModel(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String())
    upc = db.Column(db.String())
    qty_percentage_remaining = db.Column(db.Float())

    # children = relationship("Child")


    def __init__(self, user_id,upc,qty_percentage_remaining):
        self.user_id = user_id
        self.upc = upc
        self.qty_percentage_remaining = qty_percentage_remaining

    def __repr__(self):
        return f"<Inventory {self.upc} />"



class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String())
    email = db.Column(db.String())
    first_name = db.Column(db.String())
    last_name = db.Column(db.Float())

    def __init__(self, user_id,email,first_name,last_name):
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = first_name + " " + last_name

    def __repr__(self):
        return f"<User {self.full_name} />"

handle_inventory()