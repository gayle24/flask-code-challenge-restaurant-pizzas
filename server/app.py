from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rest-pizza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Index(Resource):
    def get(self):
        response_dict = {
            "index": "Restaurant Pizza Code Challenge"
        }

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response
api.add_resource(Index, '/')

class Restaurants(Resource):
    def get(self):
        response_dict_list = [item.to_dict() for item in Restaurant.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200
        )

        return response
api.add_resource(Index, '/restaurants')

# get first restaurant that matches the id, its name, address and pizzas that it serves (restaurantpizza)
# in json format; else if the restaurant doesn't exist return "error": {"Restaurant not found"} in json format
# along with status code
class RestaurantByID(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant:
            response_dict = {
                "name": restaurant.name,
                "address": restaurant.address,
                "pizzas": [rp.pizza.to_dict() for rp in restaurant.restaurant_pizzas]
            }
            status_code = 200
        
        else:
            response_dict = {"error": "Restaurant not found"}
            status_code = 404

        response = make_response(
            jsonify(response_dict),
            status_code
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