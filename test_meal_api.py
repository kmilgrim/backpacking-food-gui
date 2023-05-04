import tkinter
import customtkinter
from PIL import ImageTk, Image
import sqlite3
import bcrypt
from database import *
from meal_add_window import *
from meal_api import *


createMeal("fried pickes", "pickles and fries",
           10000, 3, 78, "today", "today")
