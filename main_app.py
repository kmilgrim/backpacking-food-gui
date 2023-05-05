import tkinter
import customtkinter
from PIL import ImageTk, Image
import sqlite3
import bcrypt
from database import *
from meal_add_window import *
from meal_api import *
from user_handle import *

MAIN_APP = None


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


class App(customtkinter.CTk):

    def handle_login(self, username: str, password: str) -> None:
        if login(username, password):
            tkinter.messagebox.showinfo('Success', 'Login Success')

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

    def main_frame(self):
        create_meal_table()

    def checkbox_frame_event(self):
        print(
            f"checkbox frame modified: {self.scrollable_checkbox_frame.get_checked_items()}")

    def create_main_frame(self):
        self.login_frame.destroy()
        self.main_frame()

        # create scrollable checkbox frame to show meals
        self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=self, width=200, height=300, command=self.checkbox_frame_event,
                                                                 item_list=[f"meal {i}" for i in range(3)])
        self.scrollable_checkbox_frame.grid(
            row=0, column=0, padx=15, pady=15, sticky="ns")
        self.scrollable_checkbox_frame.add_item("new item")

        # button to add meals
        # self.button_add_meal = customtkinter.CTkButton(
        #     master=self.main_frame, text="Add a Meal", command=self.meal_add, width=200, height=20)
        # self.button_add_meal.pack(padx=20, pady=10)
        # self.button_add_meal.place(x=100, y=350)

        # get the details entered by user

        # create meal with details
        createMeal("fried pickes", "pickles and fries",
                   10000, 3, 78, "today", "today")

    def meal_add(self):
        print("yes")


if __name__ == "__main__":
    app = App()
    app.mainloop()
