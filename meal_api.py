import tkinter
import customtkinter
from PIL import ImageTk, Image
import sqlite3
import bcrypt
from database import *
from meal_add_window import *

# This is an api that will handle everything having to do with the meal class and objects.
# meal structure (class)


class Meal:

    # meal creation and read
    def __init__(self, mealName, mealRecipe, mealCalsPerServe, mealNumOfServe, userId, createdAt, updatedAt):
        self.mealName = mealName
        self.mealRecipe = mealRecipe
        self.mealCalsPerServe = mealCalsPerServe
        self.mealNumOfServe = mealNumOfServe
        self.userId = userId
        self.createdAt = createdAt
        self.updatedAt = updatedAt


def createMeal(mealName, mealRecipe, mealCalsPerServe, mealNumOfServe, userId, createdAt, updatedAt):
    newMeal = Meal(mealName, mealRecipe, mealCalsPerServe,
                   mealNumOfServe, userId, createdAt, updatedAt)

    # add new meal to the database
    conn = sqlite3.connect("backpacking_food.db")
    c = conn.cursor()

    c.execute('INSERT INTO meal VALUES (?, ?, ?, ?, ?, ?, ?)',
              [mealName, mealRecipe, mealCalsPerServe,
               mealNumOfServe, userId, createdAt, updatedAt])
    conn.commit()
    tkinter.messagebox.showinfo('Success', 'Meal has been added.')

    conn.close()
