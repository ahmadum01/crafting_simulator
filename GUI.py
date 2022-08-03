import tkinter as tk
from items import (
    CustomCanvas,
    Inventory,
    Laboratory,
    Ingredient,
    InventorySlot,
    InventoryBase,
    Button,
    CraftingSlot,
    SerumSlot,
    Serum,
    craft,
)
from config import win_width, win_height, win_bg_color
from craft.crafting import Craft

root = tk.Tk()
root.geometry(f'{win_width}x{win_height}')
root.title('dare2defi-MAC-internal')
root['bg'] = win_bg_color

canvas = CustomCanvas(root, win_width, win_height)
canvas.place(x=-1, y=-1)

canvas.create_text(100, 50, text='craft', fill='red', font='Tahoma 30')  # header
canvas.create_text(500, 150, text='Laboratory', fill='red', font='Tahoma 25')  # laboratory header
inventory = Inventory(canvas, 30, 100, 350, 750)
laboratory = Laboratory(canvas, 370, 100, win_width - 30, 750)

button_craft = Button(canvas, x=win_width - 150, y=win_height - 100, w=100, h=40, text="craft",
                      action=lambda: craft(canvas, CraftingSlot.slots))

# Scroll buttons
button_up = Button(canvas, x=325, y=100, w=25, h=50, text="ᐱ", action=inventory.up)
button_down = Button(canvas, x=325, y=win_height - 100, w=25, h=50, text="ᐯ", action=inventory.down)

main_slot = CraftingSlot(
    canvas,
    x=laboratory.x1 + (laboratory.x2 - laboratory.x1) / 2,
    y=laboratory.y1 + (laboratory.y2 - laboratory.y1) / 2 - 100,
    r=100,
    main=True
)

left_slot = CraftingSlot(  # slot №1
    canvas,
    x=main_slot.x - 250,
    y=main_slot.y,
    r=60,
)

bottom_slot = CraftingSlot(  # slot №2
    canvas,
    x=main_slot.x,
    y=main_slot.y + 250,
    r=60,
)

right_slot = CraftingSlot(  # slot №3
    canvas,
    x=main_slot.x + 250,
    y=main_slot.y,
    r=60,
)

serum_slot = SerumSlot(
    canvas,
    x1=win_width - 250,
    y1=100,
    x2=win_width - 30,
    y2=200
)

rand_recipe = Craft.generate_rand_recipe()
print('Daily recipe:', rand_recipe)
Craft.set_daily_recipe(*rand_recipe)  # Set daly recipe

ings = [
    *[('A', 1) for _ in range(10)],
    *[('A', 2) for _ in range(10)],
    *[('A', 3) for _ in range(10)],
    *[('A', 4) for _ in range(10)],
    *[('B', 1) for _ in range(10)],
    *[('B', 2) for _ in range(10)],
    *[('B', 3) for _ in range(10)],
    *[('B', 4) for _ in range(10)],
    *[('C', 1) for _ in range(10)],
    *[('C', 2) for _ in range(10)],
    *[('C', 3) for _ in range(10)],
    *[('C', 4) for _ in range(10)],
    *[('D', 1) for _ in range(10)],
    *[('D', 2) for _ in range(10)],
    *[('D', 3) for _ in range(10)],
    *[('D', 4) for _ in range(10)],
    *[('E', 1) for _ in range(10)],
    *[('E', 2) for _ in range(10)],
    *[('E', 3) for _ in range(10)],
    *[('E', 4) for _ in range(10)],
]

for i, ing in enumerate(ings):
    Ingredient(
        canvas=canvas,
        rarity=ing[0],
        level=ing[1],
    )

# after created ingredients
InventoryBase.slots = {i // 100: InventorySlot(canvas=canvas, y1=i, y2=i + 90) for i in range(130, 700, 100)}
InventoryBase.init_or_update_data().show_slot_content(canvas=canvas)
