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
    Indicator
)


from config import win_width, win_height, win_bg_color

root = tk.Tk()
root.geometry(f'{win_width}x{win_height}')
root.title('dare2defi-MAC-internal')
root['bg'] = win_bg_color

canvas = CustomCanvas(root, win_width, win_height)
canvas.place(x=-1, y=-1)


canvas.create_text(100, 50, text='Craft', fill='red', font='Tahoma 30')  # header
canvas.create_text(500, 150, text='Laboratory', fill='red', font='Tahoma 25')  # laboratory header
inventory = Inventory(canvas, 30, 100, 350, 750)
laboratory = Laboratory(canvas, 370, 100, win_width - 30, 750)


button = Button(canvas, x=win_width - 150, y=win_height - 100, w=100, h=40, text="Craft", action=lambda : print('Hello'))
button_up = Button(canvas, x=325, y=100, w=25, h=50, text="ᐱ", action=inventory.up)
button_down = Button(canvas, x=325, y=win_height - 100, w=25, h=50, text="ᐯ", action=inventory.down)


main_slot = CraftingSlot(
    canvas,
    x=laboratory.x1 + (laboratory.x2 - laboratory.x1) / 2,
    y=laboratory.y1 + (laboratory.y2 - laboratory.y1) / 2 - 60,
    r=100,
    main=True
)

left_slot = CraftingSlot(
    canvas,
    x=main_slot.x - 250,
    y=main_slot.y,
    r=60,
)
left_indicator = Indicator(
    canvas,
    slot=left_slot,
)

right_slot = CraftingSlot(
    canvas,
    x=main_slot.x + 250,
    y=main_slot.y,
    r=60,
)
right_indicator = Indicator(
    canvas,
    slot=right_slot,
)

bottom_slot = CraftingSlot(
    canvas,
    x=main_slot.x,
    y=main_slot.y + 250,
    r=60,
)

bottom_indicator = Indicator(
    canvas,
    slot=bottom_slot,
)

ings = [
    ('A', 1), ('A', 1),
    ('A', 1), ('A', 1),
    ('A', 1), ('A', 1),
    ('A', 3), ('C', 3),
    ('B', 2), ('B', 4),
    ('E', 1), ('D', 1),
    ('D', 3), ('C', 3),
    ('A', 2), ('B', 5),
    ('E', 4), ('D', 2),

]

for i, ing in enumerate(ings):
    Ingredient(
        canvas=canvas,
        level=ing[1],
        rarity=ing[0],
    )
    
# after created ingredients
InventoryBase.slots = {i//100: InventorySlot(canvas=canvas, y1=i, y2=i+90) for i in range(130, 700, 100)}
InventoryBase.init_data().show_slot_content(canvas=canvas)

def test():
    print('\n' * 10 + '-' * 20)
    for slot in CraftingSlot.slots:
        if not slot.main:
            print(slot.ingredients)
    print('-' * 20)


button.action = test
