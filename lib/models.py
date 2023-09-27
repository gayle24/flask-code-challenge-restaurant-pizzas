from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurants = db.relationship('Restaurant', secondary='restaurant_pizzas', back_populates='pizzas')

    # serialize_rules = ('-restaurant_pizzas.pizzas',)
    serialize_rules = ('-restaurants.pizzas',)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    pizzas = db.relationship('Pizza', secondary='restaurant_pizzas', back_populates='restaurants')

    @validates('name')
    def validate_name(self, key, name):
        if len(name) >= 50:
            raise ValueError("Name cannot be greater than 50 characters")
        
        if (
            self.query
            .filter(Restaurant.name == name)
            .filter(Restaurant.id != self.id)
            .first()
        ):
            raise ValueError("Restaurant is already registered")
        return name

    # serialize_rules = ('-restaurant_pizzas.restaurants',)
    serialize_rules = ('-pizzas.restaurants',)

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('price')
    def validate_price(self, key, price):
        if price < 1 or price > 30:
            raise ValueError("Price must be between 1 and 30")
        return price

    # serialize_rules = ('-restaurants.restaurant_pizzas', '-pizzas.restaurant_pizzas',)

