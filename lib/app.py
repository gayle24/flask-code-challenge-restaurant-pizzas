from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rest-pizza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    response_dict = {
        "index": "Restaurant Pizza Code Challenge"
    }

    response = make_response(
        jsonify(response_dict),
        200
    )
    return response


class Restaurants(Resource):
    def get(self):
        rest = Restaurant.query.all()
        response_dict_list = []
        # response_dict_list = [item.to_dict() for item in Restaurant.query.all()]
        for item in rest:
            response_dict= {
                "id": item.id,
                "name": item.name,
                "address": item.address 
            }
            response_dict_list.append(response_dict)
        response = make_response(
            jsonify(response_dict_list),
            200
        )
        return response
api.add_resource(Restaurants, '/restaurants')

# get first restaurant that matches the id, its name, address and pizzas that it serves (restaurantpizza)
# in json format; else if the restaurant doesn't exist return "error": {"Restaurant not found"} in json format
# along with status code
class RestaurantByID(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        # response_dict_list = [Restaurant.query.filter_by(id=id).first().to_dict()]
        if restaurant:
            response_dict = {
                "name": restaurant.name,
                "address": restaurant.address,
                # "pizzas": [pizza.to_dict() for pizza in restaurant.pizzas] 
            }
            status_code = 200
        else:
            response_dict = {"error": "Restaurant not found"}
            status_code = 404

        response = make_response(
            jsonify(response_dict),
            200
        )
        return response
    
    def delete(self, id):
        record = Restaurant.query.filter_by(id=id).first()

        if record:
            RestaurantPizza.query.filter_by(restaurant_id=id).delete()
            db.session.delete(record)
            db.session.commit()

            response_dict = {"message": "Record successfully deleted"}
            status_code = 200

        else:
            response_dict = {"error": "Restaurant not found"}
            status_code = 404

        response = make_response(
            jsonify(response_dict),
            status_code
        )
        return response
api.add_resource(RestaurantByID, '/restaurants/<int:id>')

@app.route('/pizzas')
# get all pizzas in json format with id, name, ingredients
def pizzas():
    response_dict_list = []
    pizza = Pizza.query.all()
    response_dict_list = []
    for item in pizza:
        response_dict= {
            "id": item.id,
            "name": item.name,
            "ingredients": item.ingredients
        }
        response_dict_list.append(response_dict)

    response = make_response(
        jsonify(response_dict_list),
        200
    )
    return response

# post a new instance of RestaurantPizza that is associated with 
    # existing Pizza and Restaurant (price, pizza_id, restaurant_id)
    # if successful, return data related to the pizza(name, ingredients)
    # if not successful, return {"error": ["validation errors"]} along with status code
class RestaurantPizzas(Resource):
    def post(self):
        data = request.json

        pizza_id = data.get('pizza_id')
        restaurant_id = data.get('restaurant_id')
        price = data.get('price')

        if None in (pizza_id, restaurant_id, price):
            return {"error": ["Missing required fields"]}, 400

        pizza = Pizza.query.get(pizza_id)
        restaurant = Restaurant.query.get(restaurant_id)

        if not (pizza and restaurant):
            return {"error": ["Pizza or Restaurant not found"]}, 404

        if not (1 <= price <= 30):
            return {"error": ["Price must be between 1 and 30"]}, 400

        restaurant_pizza = RestaurantPizza(
            pizza_id=pizza_id,
            restaurant_id=restaurant_id,
            price=price
        )
        db.session.add(restaurant_pizza)
        db.session.commit()

        pizza_data = {
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }
        return pizza_data, 201
api.add_resource(RestaurantPizzas, '/restaurant_pizzas')

if __name__ == '__main__':
    app.run(port=5555, debug=True)