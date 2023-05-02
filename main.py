import tkinter
import customtkinter
from PIL import ImageTk, Image
import sqlite3
import bcrypt
from database import *


class MainApp(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="new window")
        self.label.pack(padx=20, pady=20)
