import tkinter
import customtkinter
import bcrypt
import sqlite3

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
