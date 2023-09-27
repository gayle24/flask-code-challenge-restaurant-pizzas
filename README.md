# Flask Code Challenge - Restaurant Pizzas

<p>This Flask app is designed to manage and explore information about restaurants and their pizza offerings. It allows users to retrieve details about restaurants, their addresses, and the pizzas they serve. Additionally, users can post new information about restaurant-pizza associations, including the price of each pizza offered by a restaurant.</p>

<p>Explore the delicious world of restaurant pizzas with this simple and intuitive Flask web application.</p>

## API Endpoints
GET /: Retrieve information about the application.

GET /restaurants: Get a list of all restaurants.

GET /restaurants/<int:id>: Get information about a specific restaurant, including its name, address, and the pizzas it serves.

DELETE /restaurants/<int:id>: Delete a restaurant by its ID. This also deletes any associated records in the RestaurantPizza table.

## Data Validation
The application enforces data validation rules to ensure the integrity of the data:

<li>Restaurant names must be unique and have a maximum length of 50 characters.</li>
Pizza ingredients are randomly generated from a predefined list.
Restaurant pizzas have a price between 1 and 30.

## Seed Data
A seed script (seed.py) is included to populate the database with sample data. You can run it using the following command:

```bash
Copy code
python seed.py
```
## Contributing
If you would like to contribute to this project, please follow these steps:

<li>Fork the repository.
<li>Create a new branch for your feature or bug fix.
Make your changes and commit them.
<li>Push the changes to your fork.
<li>Submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

```bash
vbnet
Copy code
```

Feel free to modify this template to suit your project's specific details and requirements.
