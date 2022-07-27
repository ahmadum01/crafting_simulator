import tkinter as tk
from items import CustomCanvas, Inventory, Laboratory, Ingredient
from config import win_width, win_height, win_bg_color

root = tk.Tk()
root.geometry(f'{win_width}x{win_height}')
root.title('dare2defi-MAC-internal')
root['bg'] = win_bg_color

canvas = CustomCanvas(root, win_width, win_height,)
canvas.place(x=0, y=0)


canvas.create_text(100, 50, text='Craft', fill='red', font='Tahoma 25')  # header
inventory = Inventory(canvas, 30, 100, 350, 750)
laboratory = Laboratory(canvas, 370, 100, win_width - 30, 750)
ingredient = Ingredient(
    canvas=canvas,
    x=40,
    y=110,
    w=50,
    level=4,
    rarity='E'
)

