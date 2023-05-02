import tkinter
import customtkinter
from PIL import ImageTk, Image
import sqlite3
import bcrypt
from database import *
from meal_add_window import *

MAIN_APP = None


class App(customtkinter.CTk):
    def handle_login(self, username: str, password: str) -> None:
        if login(username, password):
            tkinter.messagebox.showinfo('Success', 'Login Success')
            # open new window here
            # MAIN_APP = MealAddWindow()
            self.login_frame.destroy()
            self.main_frame()

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


if __name__ == "__main__":
    app = App()
    app.mainloop()
