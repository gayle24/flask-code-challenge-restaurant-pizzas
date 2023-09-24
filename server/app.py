from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rest-pizza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return 'Restaurant Pizzas Code Challenge'

@app.route('/restaurants')
def restaurants(self):
    pass
    # get all restaurants in json format with id, name, address

@app.route('/restaurants/<int:id>')
def restaurant_by_id(self, id):
    pass
    # get first restaurant that matches the id, its name, address and pizzas that it serves (restaurantpizza)
    # in json format; else if the restaurant doesn't exist return "error": {"Restaurant not found"} in json format
    # along with status code

def delete_restaurant_by_id(self):
    pass
    # delete the restaurant that matches the id in the http request

@app.route('/pizzas')
def pizzas(self):
    pass
    # get all pizzas in json format with id, name, ingredients

@app.route('/restaurant_pizzas')
def restaurant_pizzas(self):
    pass
    # post a new instance of RestaurantPizza that is associated with 
    # existing Pizza and Restaurant (price, pizza_id, restaurant_id)
    # if successful, return data related to the pizza(name, ingredients)
    # if not successful, return {"error": ["validation errors"]} along with status code



if __name__ == '__main__':
    app.run(port=5555, debug=True)