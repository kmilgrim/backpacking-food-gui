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

    c.execute('INSERT INTO meal VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
              [None, mealName, mealRecipe, mealCalsPerServe,
               mealNumOfServe, userId, createdAt, updatedAt])
    conn.commit()
    tkinter.messagebox.showinfo('Success', 'Meal has been added.')

    conn.close()

# update a meal


def updateMeal(meal: Meal, attributeName, newValue, mealId):
    conn = sqlite3.connect("backpacking_food.db")
    c = conn.cursor()

    try:
        c.execute(f'UPDATE meal SET {attributeName} = ? WHERE id = ?',
                  [newValue, mealId])
        conn.commit()
        print(
            f"Meal attribute '{attributeName}' for meal with ID {mealId} has been updated.")
    except sqlite3.Error as e:
        print(f"Error updating meal attribute: {e}")
    finally:
        conn.close()


# delete meals
def deleteMeal(mealId):
    conn = sqlite3.connect("backpacking_food.db")
    c = conn.cursor()

    try:
        c.execute('DELETE FROM meal WHERE id = ?', [mealId])
        conn.commit()
        print(f"Meal with ID {mealId} has been deleted.")
    except sqlite3.Error as e:
        print(f"Error deleting meal: {e}")
    finally:
        conn.close()


def searchMeal(mealName):
    conn = sqlite3.connect("backpacking_food.db")
    c = conn.cursor()

    try:
        c.execute('SELECT * FROM meal WHERE mealName LIKE ?',
                  ['%' + mealName + '%'])
        results = c.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"Error searching for meal: {e}")
    finally:
        conn.close()
