import tkinter as tk
from items import (
    CustomCanvas,
    Inventory,
    Laboratory,
    Ingredient,
    InventorySlot,
    InventoryBase,
    Button)

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
button = Button(canvas, x=win_width - 150, y=win_height - 100, w=100, h=40, text="Craft", action=lambda: print('Hello'))

ingredient = Ingredient(
    canvas=canvas,
    level=2,
    rarity='E'
)

ingredient4 = Ingredient(
    canvas=canvas,
    level=2,
    rarity='E'
)

ingredient2 = Ingredient(
    canvas=canvas,
    level=4,
    rarity='E'
)

ingredient3 = Ingredient(
    canvas=canvas,
    level=1,
    rarity='E'
)

ingredient0 = Ingredient(
    canvas=canvas,
    level=3,
    rarity='E'
)

ingredient05 = Ingredient(
    canvas=canvas,
    level=3,
    rarity='A'
)

ingredient075 = Ingredient(
    canvas=canvas,
    level=3,
    rarity='B'
)
ingredient079 = Ingredient(
    canvas=canvas,
    level=3,
    rarity='C'
)
# after created ingredients
InventoryBase.slots = {i//100: InventorySlot(canvas=canvas, y1=i, y2=i+90) for i in range(130, 700, 100)}
InventoryBase.init_data().active_data(canvas=canvas)
# ---------------------------


button_up = tk.Button(root, width=30, height=1, text="Up", command=inventory.up)
button_up.pack()
button_down = tk.Button(root, width=30, text="Down", command=inventory.down)
button_down.pack()
canvas.create_window((53, 100), anchor=tk.NW, window=button_up)
canvas.create_window((53, 720), anchor=tk.NW, window=button_down)


