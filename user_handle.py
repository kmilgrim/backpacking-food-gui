import tkinter
import customtkinter
import bcrypt
import sqlite3
from database import *


def login(username: str, password: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    if username == '':
        return False
    if password == '':
        return False

    c.execute(
        'SELECT id, password FROM user WHERE username=?', [username])
    db_res = c.fetchone()
    if db_res is None:
        return False
    user_id, db_hashed_password = db_res
    if bcrypt.checkpw(password.encode('utf-8'), db_hashed_password):
        # Update global state
        GlobalState.get_instance().set_current_user_id(user_id)
        return True
    return False


def signup(username, password):
    conn = sqlite3.connect("backpacking_food.db")
    c = conn.cursor()

    if username != '' and password != '':
        c.execute('SELECT username FROM user WHERE username=?', [username])
        if c.fetchone() is not None:
            tkinter.messagebox.showerror('Error', 'Username already exists.')
        else:
            # Check password length
            if len(password) < 8:
                tkinter.messagebox.showerror(
                    'Error', 'Password must be at least 8 characters long.')
            else:
                # Check password complexity
                has_upper = False
                has_lower = False
                has_digit = False
                has_special = False
                for char in password:
                    if char.isupper():
                        has_upper = True
                    elif char.islower():
                        has_lower = True
                    elif char.isdigit():
                        has_digit = True
                    else:
                        has_special = True

                if not (has_upper and has_lower and has_digit and has_special):
                    tkinter.messagebox.showerror(
                        'Error', 'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.')
                else:
                    encoded_password = password.encode('utf-8')
                    hashed_password = bcrypt.hashpw(
                        encoded_password, bcrypt.gensalt())
                    print(hashed_password)
                    c.execute('INSERT INTO user VALUES (?, ?, ?)',
                              [None, username, hashed_password])
                    conn.commit()
                    tkinter.messagebox.showinfo(
                        'Success', 'Account has been created')
    elif username == '' or password == '':
        tkinter.messagebox.showerror(
            'Error', 'Please enter username and password')

    conn.close()
