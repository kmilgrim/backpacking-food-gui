import tkinter
from typing import List
from global_state import GlobalState
import customtkinter
import bcrypt
import sqlite3
import time

DB_NAME = "backpacking_food.db"


def create_user_table():

    # create database and cursor
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # create all tables
    c.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()

    conn.close()


def create_meal_table():

    # create database and cursor
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # create all tables
    c.execute("""
        CREATE TABLE IF NOT EXISTS meal (
            id INTEGER PRIMARY KEY,
            mealName TEXT NOT NULL,
            mealRecipe TEXT NOT NULL,
            mealCalsPerServe INTEGER,
            mealNumOfServe INTEGER, 
            userId INTEGER NOT NULL,
            createdAt TEXT NOT NULL,
            updatedAt TEXT NOT NULL
        )
    """)

    conn.commit()

    conn.close()


def db_add_meal(meal_name, meal_recipe, cals_per_serve, num_of_serve) -> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    curr_time = str(time.localtime())
    # Insert a new meal into the table
    cursor.execute('INSERT INTO meal (mealName, mealRecipe, mealCalsPerServe, mealNumOfServe, userId, createdAt, updatedAt) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (meal_name, meal_recipe, cals_per_serve, num_of_serve, GlobalState.get_instance().get_current_user_id(), curr_time, curr_time))

    # Get ID of new meal
    meal_id = cursor.lastrowid

    conn.commit()
    conn.close()
    return meal_id


def get_all_meals() -> List[any]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Select specific columns from the meal table
    cursor.execute(
        'SELECT id, mealName, mealRecipe, mealCalsPerServe, mealNumOfServe, userId, createdAt, updatedAt FROM meal')
    rows = cursor.fetchall()

    conn.close()

    return rows


def get_all_meal_names() -> List[any]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Select only the mealName column from the meal table
    cursor.execute('SELECT mealName FROM meal ORDER BY createdAt DESC')
    rows = cursor.fetchall()

    conn.close()

    if rows is None:
        return []
    # Extract meal names from each row tuple
    meal_names = [row[0] for row in rows]

    return meal_names


def get_meal_name_from_db(meal_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT mealName FROM meal WHERE id = ?', (meal_id,))
    meal_data = cursor.fetchone()

    conn.close()

    if meal_data is not None:
        return meal_data[0]
    else:
        return None


def get_concatenated_meal_recipe(meal_ids: List[int]):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Build a query to retrieve the concatenated meal recipe for the specified meal IDs
    query = f"SELECT GROUP_CONCAT(mealRecipe, '\n') FROM meal WHERE id IN ({','.join(map(str, meal_ids))})"
    cursor.execute(query)

    result = cursor.fetchone()

    conn.close()

    return result
