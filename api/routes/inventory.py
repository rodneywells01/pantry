import logging
from flask import Flask, request, redirect, url_for, jsonify, Blueprint
from models.models import Inventory, Product

inventory = Blueprint('inventory', __name__)

@inventory.route("/inventory", methods=["GET"])
def get_inventory():
    # List all inventory
    order_by = request.args.get("order_by")
    user_id = request.args.get("user_id")
    populate_details = request.args.get("populate_details")
    logging.info(f"populate_details: {populate_details}")
    items = list()

    # if user_id:
    #     # All of this needs to be in the ORM.
    #     items_in_inventory = Inventory.query.filter_by(user_id=user_id).all()

    #     detailed_items_in_inventory = (
    #         Product.query.join(
    #             Inventory, Product.upc == Inventory.upc
    #         )
    #         .filter(Inventory.user_id == user_id)
    #         .add_columns(
    #             Inventory.user_id, Inventory.qty_percentage_remaining
    #         )
    #         .all()
    #     )

    #     items = detailed_items_in_inventory
    #     for item in detailed_items_in_inventory:
    #         logging.info(item)
    inventories = Inventory.getAll()

    response = {
        "count": len(inventories),
        "inventories": [inventory.to_dict() for inventory in inventories]
    }

    # if order_by == "category":
    #     # Order items by category.
    #     # TODO - Can I use SQLAlchemy to do this more effectively?
    #     # TODO - Should this be done on clients side?
    #     categories = dict()
    #     for item in items:
    #         if item.category in categories:
    #             categories[item.category].append(item)
    #         else:
    #             categories[item.category] = [item]

    #     for item_category in categories:
    #         response["inventory"][item.category] = [item.to_dict() for item in categories[item_category]]

    # else:
    #     response["inventory"] = [item.to_dict() for item in items]

    return response

@inventory.route("/inventory", methods=["POST"])
def create_inventory():
    # List all inventory
    logging.info("Creating Inventory")

    # Updating the users inventory
    data = request.get_json()
    inventory = Inventory(
        dynamo_item=data
    )
    inventory.save()

    return jsonify(inventory.to_dict()) , 201
