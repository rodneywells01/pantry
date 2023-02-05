from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    def save(self):
        db.session.add(self)
        db.session.commit()


class Product(BaseModel):
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

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "ean": self.ean,
            "upc": self.upc,
            "brand": self.brand,
            "model": self.model,
            "category": self.category,
            "image_url": self.image_url,
        }


class Inventory(BaseModel):
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

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "upc": self.upc,
            "qty_percentage_remaining": self.qty_percentage_remaining,
        }


class User(BaseModel):
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
