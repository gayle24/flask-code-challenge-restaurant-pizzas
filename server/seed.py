from random import randint, sample, choice as rc
from faker import Faker
import random

from app import app
from models import db, Restaurant, RestaurantPizza, Pizza

pizza_ingredients = [
    "pizza dough",
    "tomato sauce",
    "mozzarella cheese",
    "cheddar cheese",
    "parmesan cheese",
    "pepperoni",
    "sausage",
    "mushrooms",
    "green peppers",
    "onions",
    "black olives",
    "green olives",
    "sliced tomatoes",
    "artichoke hearts",
    "spinach",
    "pineapple",
    "bacon",
    "ham",
    "anchovies",
    "garlic",
    "red pepper flakes",
    "oregano",
    "olive oil",
    "fresh basil leaves",
    "crushed red pepper",
    "sundried tomatoes",
    "feta cheese",
]

pizza_restaurant_names = [
    "Pizza Paradise",
    "Slice of Heaven",
    "Cheesy Delights Pizzeria",
    "Mama Mia's Pizza Palace",
    "The Pizza Planet",
    "Crispy Crust Pizzeria",
    "Saucy Slices",
    "Pizza Picasso",
    "Doughy Delights",
    "Pepperoni Perfection",
    "Pizzarella's",
    "The Pizza Pinnacle",
    "Pizza Panorama",
    "Oven Fresh Pies",
    "Pizza Pie Panache",
    "Slice It Right Pizzeria",
    "Pizzamania",
    "The Sizzle Slice",
    "Pizza Alchemy",
    "Rustic Wood-Fired Pies",
]

pizza_names = [
    "Margherita",
    "Hawaiian",
    "Supreme",
    "Vegetarian",
    "Mediterranean",
    "BBQ Chicken",
    "Buffalo Chicken",
    "White Pizza",
    "Pesto Delight",
    "Four Cheese",
    "Meat Lovers",
    "Veggie Delight",
    "California Dream",
    "Neapolitan",
    "Sicilian",
    "Greek Delight",
    "Rustic Italian",
    "Tuscan Feast",
    "Farmhouse",
    "Savory Sicilian",
]

fake = Faker()
with app.app_context():
    Restaurant.query.delete()
    Pizza.query.delete()
    RestaurantPizza.query.delete()

    pizzas = []

    for i in range(20):
        num_ingredients = randint(3, 6)
        ingredients = sample(pizza_ingredients, num_ingredients)

        pizza = Pizza(
            name=rc(pizza_names),
            ingredients=", ".join(ingredients)
        )
        pizzas.append(pizza)
    db.session.add_all(pizzas)


    restaurants = []
    for i in range(20):
        rst = Restaurant(
            name=rc(pizza_restaurant_names),
            address=fake.address(),
        )
        restaurants.append(rst)
    db.session.add_all(restaurants)

    restaurant_pizzas = []
    num_restaurants = Restaurant.query.count()
    num_pizzas = Pizza.query.count()
    for i in range(60):
        rst_pizza = RestaurantPizza(
            restaurant_id=randint(1, num_restaurants),
            pizza_id=randint(1, num_pizzas),
            price=randint(1, 30)
        )
        restaurant_pizzas.append(rst_pizza)
    db.session.add_all(restaurant_pizzas)  
    db.session.commit()

