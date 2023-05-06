# Backpacking Food Planner GUI

This application is meant to help users keep track of their backpacking meals and ingredients, and generate ingredient lists for grocery store shopping.

## Installation

Clone the repository /backpacking-food-gui, cd into the directory, and the app can be run with the script main_app.py

```bash
>> cd /backpacking-food-gui
>> python main_app.py
```

## Usage

Once the application is started, a login page will pop up for the user to authenticate themselves before reaching app functionality:
![image](https://user-images.githubusercontent.com/61169077/236593439-433fb900-e4a0-46db-ba14-c8814d5343c8.png)

At this point, the user can enter credentials to login, if they already exist, or sign up if they don't.

Once logged in, a main console window will open with options to add meals to the user's list, generate a list of ingredients for all the meals selected, and delete meals from the list. In the list of ingredients, a calorie count is also generated to help the user gauge whether they have enough food for their trip. 

![image](https://user-images.githubusercontent.com/61169077/236594739-ef0acc5b-80f5-4f8a-84d1-30c6f574d5fb.png)

The user can select which meals they want to generate the ingredients for with the check boxes, and click on the "Generate Ingredients" button. 

When adding a meal, the user can enter details in a separate window. Once the details are entered and "Add Meal" is pressed, the new meal will appear in the main console checkbox list along with previously added meals. 
![image](https://user-images.githubusercontent.com/61169077/236594776-bd2f7d95-4c29-44c1-82ff-e45b67e51fe5.png)

## Function

### database.py

This Python file contains functions that interact with a SQLite database that stores information about backpacking meals. The functions utilize the sqlite3 module to connect to and query the database. The create_user_table and create_meal_table functions create tables in the database to store information about users and meals, respectively.

The db_add_meal function adds a new meal to the meal table, while get_all_meals and get_all_meal_names retrieve information about all meals and their names. The get_meal_name_from_db function retrieves the name of a meal with a specified ID. Finally, the get_concatenated_meal_recipe function returns a concatenated recipe for a list of meal IDs. Overall, this Python file provides functionality for managing a database of backpacking meals.

### meal_api.py

This file contains functions and a class to handle everything related to meals in the Backpacking Food application. To use this file, you will need to import the following modules:

#### Meal Class

The Meal class is defined with the following attributes:

- mealName
- mealRecipe
- mealCalsPerServe
- mealNumOfServe
- userId
- createdAt
- updatedAt

To create a new meal object, call the Meal constructor with the corresponding attribute values.

```python
newMeal = Meal(mealName, mealRecipe, mealCalsPerServe, mealNumOfServe, userId, createdAt, updatedAt)
```

**createMeal**
The createMeal() function will add a new meal to the database. To use this function, provide the corresponding attribute values for the new meal.

```python
createMeal(mealName, mealRecipe, mealCalsPerServe, mealNumOfServe, userId, createdAt, updatedAt)
```

**updateMeal**
The updateMeal() function will update an existing meal's attribute value in the database. To use this function, provide the meal object, the name of the attribute to be updated, the new value for the attribute, and the meal ID.

```python
updateMeal(meal, attributeName, newValue, mealId)
```

**deleteMeal**
The deleteMeal() function will delete an existing meal from the database. To use this function, provide the meal ID.

```python
deleteMeal(mealId)
```

**searchMeal**
The searchMeal() function will search for meals in the database that contain the provided string in their name. To use this function, provide the search string for the meal name.

```python
searchMeal(mealName)
```

### user_handle.py

```python
login(username: str, password: str) -> bool
```

This function takes in a username and password as string parameters and returns a boolean indicating whether the login attempt was successful or not.

The function checks if username and password are not empty strings, queries the user table in the backpacking_food.db SQLite database to retrieve the hashed password associated with the input username, and compares it with the hashed input password using the bcrypt.checkpw function.

If the comparison is successful, meaning the password is correct, the function updates the current user ID in the GlobalState class using the GlobalState.get_instance().set_current_user_id(user_id) method and returns True. If the comparison fails, the function returns False.

```python
signup(username, password)
```

This function takes in a username and password as string parameters and creates a new user account in the user table of the backpacking_food.db SQLite database.

The function first checks if username and password are not empty strings. If the username already exists in the user table, an error message is displayed using the tkinter.messagebox.showerror method. If the username is new, the function checks if the password meets certain complexity requirements (at least 8 characters long and contains at least one uppercase letter, one lowercase letter, one number, and one special character).

If the password meets the requirements, it is encoded using utf-8 encoding and hashed using the bcrypt.hashpw function. The hashed password and the username are then inserted into the user table using the INSERT INTO SQL statement. If either the username or password is empty, an error message is displayed using the tkinter.messagebox.showerror method. If the account creation is successful, a success message is displayed using the tkinter.messagebox.showinfo method.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
