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
        'SELECT username, password FROM user WHERE username=?', [username])
    db_res = c.fetchone()
    if db_res is None:
        return False
    _, db_hashed_password = db_res
    if bcrypt.checkpw(password.encode('utf-8'), db_hashed_password):
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
            encoded_password = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
            print(hashed_password)
            c.execute('INSERT INTO user VALUES (?, ?, ?)',
                      [None, username, hashed_password])
            conn.commit()
            tkinter.messagebox.showinfo('Success', 'Account has been created')
    elif username == '' or password == '':
        tkinter.messagebox.showerror(
            'Error', 'Please enter username and password')

    conn.close()
