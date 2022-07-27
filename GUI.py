import tkinter as tk
from items import CustomCanvas, Inventory
from config import win_width, win_height, win_bg_color
root = tk.Tk()
root.geometry(f'{win_width}x{win_height}')
root['bg'] = win_bg_color
canvas = CustomCanvas(root, win_width, win_height,)

canvas.place(x=0, y=0)


canvas.create_text(100, 50, text='Craft', fill='red', font='Tahoma 25')
inventory = Inventory(canvas, 30, 100, 350, 750)
canvas.create_ingredient(50, 50, 'red')