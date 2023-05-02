import tkinter
import customtkinter
from PIL import ImageTk, Image
import sqlite3
import bcrypt
from database import *
from main import *

MAIN_APP = None


def handle_login(username: str, password: str) -> None:
    if login(username, password):
        tkinter.messagebox.showinfo('Success', 'Login Success')
        # open new window here
        MAIN_APP = MainApp()

    else:
        tkinter.messagebox.showinfo(
            'Error', 'Username and Password are not valid')


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("720x480")
app.title('Login')

create_user_table()

l_username = customtkinter.CTkLabel(master=app)
l_username.place(x=50, y=45)

frame = customtkinter.CTkFrame(master=app, width=320, height=360)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

l_password = customtkinter.CTkLabel(
    master=frame, text="Log into your account", font=('Century Gothic', 20))
l_password.place(x=50, y=45)

entry_username = customtkinter.CTkEntry(
    master=frame, width=120, placeholder_text="username")
entry_username.place(x=50, y=110)

entry_password = customtkinter.CTkEntry(
    master=frame, width=120, placeholder_text="password", show="*")
entry_password.place(x=50, y=165)

button_login = customtkinter.CTkButton(master=frame, command=lambda: handle_login(
    entry_username.get(), entry_password.get()), width=220, text='Login', corner_radius=6)
button_login.place(x=50, y=240)

button_signup = customtkinter.CTkButton(master=frame, command=lambda: signup(entry_username.get(
), entry_password.get()), width=220, text='Sign Up', corner_radius=6, fg_color=("black", "gray"))
button_signup.place(x=50, y=280)

app.mainloop()
