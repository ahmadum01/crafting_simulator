import tkinter as tk
from items import (
    CustomCanvas,
    Inventory,
    Laboratory,
    Ingredient,
    InventorySlot,
    Button,

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
button = Button(canvas, x=win_width - 150, y=win_height - 100, w=100, h=40, text="Craft", action=lambda : print('Hello'))
InventorySlot(canvas)
