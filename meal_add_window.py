import tkinter
import customtkinter
from PIL import ImageTk, Image
import sqlite3
import bcrypt
from database import *


class MealAddWindow(customtkinter.CTkToplevel):
    def __init__(self, new_meal_callback, **kwargs):
        super().__init__(**kwargs)
        self.geometry("800x600")

        self.new_meal_callback = new_meal_callback

        self.title = "Add a new meal"

        self.label = customtkinter.CTkLabel(
            self, text="Backpacking Meals").grid(row=0, column=1, columnspan=3, padx=5, pady=5)

        # Meal Name
        self.label_meal_name = customtkinter.CTkLabel(
            self, text="Meal Name:").grid(row=1, column=0)
        self.entry_meal_name = customtkinter.CTkEntry(
            self, width=140, corner_radius=6, placeholder_text='Enter a meal name...')
        self.entry_meal_name.grid(row=1, column=3, columnspan=2)

        # Calories
        self.entry_calories = customtkinter.CTkEntry(
            self, width=100, corner_radius=6, placeholder_text='Enter calorie count')
        self.entry_calories.grid(row=2, column=3, columnspan=2)
        self.label_calorie_count = customtkinter.CTkLabel(
            self, text="Calorie Count").grid(row=2, column=0)
        # Servings
        self.entry_serving_count = customtkinter.CTkEntry(
            self, width=100, corner_radius=6, placeholder_text='Enter number of servings')
        self.entry_serving_count.grid(row=3, column=3, columnspan=2)
        self.label_serving_count = customtkinter.CTkLabel(
            self, text="Serving Count:").grid(row=3, column=0)
        # Ingrediants
        self.entry_ingredient_list = customtkinter.CTkEntry(
            self, width=350, height=300, placeholder_text="Enter list of ingredients")
        self.entry_ingredient_list.grid(row=4, column=3, columnspan=2)
        self.label_meal_name = customtkinter.CTkLabel(
            self, text="Ingrediants:").grid(row=4, column=0)

        self.button_add_meal = customtkinter.CTkButton(
            master=self, width=100, text='Add a Meal', command=self.create_meal, corner_radius=6).grid(row=10, column=10, columnspan=2, sticky="S")

    def create_meal(self):
        # Get values from entry fields
        meal_name = self.entry_meal_name.get()
        calorie_count = self.entry_calories.get()
        serving_count = self.entry_serving_count.get()
        ingredients = self.entry_ingredient_list.get()

        # Verify that things entered are valid
        if meal_name == "":
            tkinter.messagebox.showinfo('Error', 'Meal name cannot be empty')
            return

        if calorie_count == "":
            tkinter.messagebox.showinfo(
                'Error', 'Calorie count cannot be empty')
            return

        if not calorie_count.isdigit():
            tkinter.messagebox.showinfo(
                'Error', 'Calorie count must be a number')
            return

        if serving_count == "":
            tkinter.messagebox.showinfo(
                'Error', 'Serving count cannot be empty')
            return

        if not serving_count.isdigit():
            tkinter.messagebox.showinfo(
                'Error', 'Serving count must be a number')
            return

        if ingredients == "":
            tkinter.messagebox.showinfo('Error', 'Ingredients cannot be empty')
            return

        # All fields are valid, create a new meal
        new_meal_id = db_add_meal(
            meal_name, ingredients, calorie_count, serving_count)
        self.new_meal_callback(new_meal_id)
        self.destroy()
