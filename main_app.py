import tkinter
from typing import Optional
import customtkinter
from PIL import ImageTk, Image
import sqlite3
import bcrypt
from database import *
from meal_add_window import *
from meal_api import *
from user_handle import *

MAIN_APP = None

DEBUG = False

# create check box frame for showing all meals


class ScrollableCheckBoxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = customtkinter.CTkCheckBox(self, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10))
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]

    def add_meal_to_checkbox_frame(self, meal_id):
        meal_data = get_meal_name_from_db(meal_id)

        if meal_data is not None:
            self.add_item(meal_data)
        else:
            print(f"No meal found with ID {meal_id}")


class App(customtkinter.CTk):

    def handle_login(self, username: str, password: str) -> None:
        if login(username, password):
            self.create_main_frame()

        else:
            tkinter.messagebox.showinfo(
                'Error', 'Username and Password are not valid')

    # initialize the app with the login page
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")

        self.geometry("720x480")
        self.title('Backpacking Food Planner')

        # prepare the database to check for a user or add a new one
        create_user_table()

        self.login_frame = customtkinter.CTkFrame(
            master=self, width=320, height=360)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.l_login = customtkinter.CTkLabel(
            master=self.login_frame, text="Log into your account", font=('Century Gothic', 20))
        self.l_login.place(x=50, y=45)

        self.entry_username = customtkinter.CTkEntry(
            master=self.login_frame, width=120, placeholder_text="username")
        self.entry_username.place(x=50, y=110)

        self.entry_password = customtkinter.CTkEntry(
            master=self.login_frame, width=120, placeholder_text="password", show="*")
        self.entry_password.place(x=50, y=165)

        # signup and login buttons perform similar tasks
        # signup adds user to database, login checks and matches user in database.
        self.button_login = customtkinter.CTkButton(master=self.login_frame, command=lambda: self.handle_login(
            self.entry_username.get(), self.entry_password.get()), width=220, text='Login', corner_radius=6)
        self.button_login.place(x=50, y=240)

        self.button_signup = customtkinter.CTkButton(master=self.login_frame, command=lambda: signup(self.entry_username.get(
        ), self.entry_password.get()), width=220, text='Sign Up', corner_radius=6, fg_color=("black", "gray"))
        self.button_signup.place(x=50, y=280)

        self.window_add_meal = None
        if DEBUG:
            self.create_main_frame()

    def checkbox_frame_event(self):
        print(
            f"checkbox frame modified: {self.scrollable_checkbox_frame.get_checked_items()}")

    def create_main_frame(self):
        self.login_frame.destroy()

        # create/load the meal table from the database
        create_meal_table()

        # create scrollable checkbox frame to show meals
        self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=self, width=200, height=300, command=self.checkbox_frame_event,
                                                                 item_list=get_all_meal_names())
        self.scrollable_checkbox_frame.grid(
            row=0, column=0, padx=15, pady=15, sticky="ns")
        self.scrollable_checkbox_frame.add_item("new item")

        # button to add meals
        self.button_add_meal = customtkinter.CTkButton(
            master=self, command=self.open_meal_add, width=220, text='Add a Meal', corner_radius=6)
        self.button_add_meal.grid(
            row=1, column=0, padx=15, pady=5, sticky="ns")

        # buttons to generate ingredient list and delete meals from database
        self.button_generate_ingredients = customtkinter.CTkButton(
            master=self, width=220, text='Generate Ingredients', command=lambda: self.generate_ingredients(), corner_radius=6, fg_color=("black", "gray"))
        self.button_generate_ingredients.grid(
            row=2, column=0, padx=15, pady=5, sticky="ns")

        self.button_delete_meal = customtkinter.CTkButton(
            master=self, width=220, text='Delete Meals', command=lambda: self.delete_meals(), corner_radius=6, fg_color=("black", "gray"))
        self.button_delete_meal.grid(
            row=3, column=0, padx=15, pady=5, sticky="ns")

        # insert text box for the ingredients list
        self.textbox = customtkinter.CTkTextbox(
            master=self, width=300, corner_radius=0)
        self.textbox.grid(
            row=0, column=1, padx=15, pady=15, sticky="ns")
        self.textbox.insert("0.0", "Ingredients List..." * 1)

        # get the details entered by user

        # create meal with details
        # createMeal("fried pickes", "pickles and fries",
        #
        #
        #  10000, 3, 78, "today", "today")

    def open_meal_add(self):
        if self.window_add_meal is None or not self.window_add_meal.winfo_exists():
            # create window if its None or destroyed
            self.window_add_meal = MealAddWindow(
                new_meal_callback=self.scrollable_checkbox_frame.add_meal_to_checkbox_frame)
        self.window_add_meal.focus()  # if window exists focus it

    def generate_ingredients(self):
        meal_list = []
        ingredient_list = []

        try:
            # get all selected meals
            meals = self.scrollable_checkbox_frame.get_checked_items()

            i = 0
            for meal in meals:
                meal_data = searchMeal(meal)
                if meal_data:
                    meal_list.append(meal_data)
                    ingredient_list.append(meal_data[0][2])
                    i += 1
                else:
                    print(f"No data found for meal {meal}")
        except Exception as e:
            print(f"Error generating ingredients: {e}")

        print(ingredient_list)
        self.generate_cal_count(ingredient_list)

    def update_textbox(self, ingredient_list):
        self.textbox.delete("0.0", "end")  # delete all text

        for ingredient in ingredient_list:
            self.textbox.insert("end", ingredient + "\n")

    def delete_meals(self):
        meal_list = []

        try:
            # get all selected meals
            meals = self.scrollable_checkbox_frame.get_checked_items()

            # find id of meals with the correct name
            for meal in meals:
                meal_data = searchMeal(meal)
                if meal_data:
                    meal_list.append(meal_data)
                else:
                    print(f"No data found for meal {meal}")
        except Exception as e:
            print(f"Error generating ingredients: {e}")

        for meal in meal_list:
            self.scrollable_checkbox_frame.remove_item(meal[0][1])
            deleteMeal(meal[0][0])

    def generate_cal_count(self, ingredient_list):
        meal_list = []
        calorie_count = 0

        try:
            # get all selected meals
            meals = self.scrollable_checkbox_frame.get_checked_items()

            for meal in meals:
                meal_data = searchMeal(meal)
                if meal_data:
                    calorie_count += meal_data[0][3]
                else:
                    print(f"No data found for meal {meal}")
        except Exception as e:
            print(f"Error adding up calorie count of all meals: {e}")

        print(calorie_count)
        ingredient_list.append(
            f"\nTotal Calories: {str(calorie_count)}")
        self.update_textbox(ingredient_list)


if __name__ == "__main__":
    app = App()
    app.mainloop()
