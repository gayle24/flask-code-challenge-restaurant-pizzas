from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    #name, ingredients, created_at, updated_at
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurants = db.relationship('RestaurantPizza', backref='pizzas')

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    #name, address
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    pizzas = db.relationship('RestaurantPizza', backref='restaurants')

    # name must not have more than 50 characters & must be unique
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

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    # pizza_id(relationship), restaurant_id(relationship), price, created_at, updated_at
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #validations -> price must be between 1 and 30
    @validates('price')
    def validate_price(self, key, price):
        if price < 1 or price > 30:
            raise ValueError("Price must be between 1 and 30")
        return price