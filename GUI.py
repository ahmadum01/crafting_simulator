import tkinter as tk
from items import (
    CustomCanvas,
    Inventory,
    Laboratory,
    Ingredient,
    InventorySlot,
    InventoryBase,
    Button,
    CraftingSlot
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




button_up = tk.Button(root, width=30, height=1, text="Up", command=inventory.up)
button_up.pack()
button_down = tk.Button(root, width=30, text="Down", command=inventory.down)
button_down.pack()
canvas.create_window((53, 100), anchor=tk.NW, window=button_up)
canvas.create_window((53, 720), anchor=tk.NW, window=button_down)

button = Button(canvas, x=win_width - 150, y=win_height - 100, w=100, h=40, text="Craft", action=lambda : print('Hello'))
# button2 = Button(canvas, x=win_width - 400, y=win_height - 100, w=100, h=40, text="Craft", action=lambda : print('left button'))
InventorySlot(canvas)

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

right_slot = CraftingSlot(
    canvas,
    x=main_slot.x + 250,
    y=main_slot.y,
    r=60,
)

bottom_slot = CraftingSlot(
    canvas,
    x=main_slot.x,
    y=main_slot.y + 250,
    r=60,
)

ings = [
    ('A', 1), ('A', 1),
    ('A', 3), ('C', 3),
    ('B', 2), ('B', 4),
    ('E', 1), ('D', 1),

]

for i, ing in enumerate(ings):
    Ingredient(
        canvas=canvas,
        level=ing[1],
        rarity=ing[0],
    )
    
# after created ingredients
InventoryBase.slots = {i//100: InventorySlot(canvas=canvas, y1=i, y2=i+90) for i in range(130, 700, 100)}
InventoryBase.init_data().active_data(canvas=canvas)

def test():
    print('\n' * 10 + '-' * 20)
    for slot in CraftingSlot.slots:
        if not slot.main:
            print(slot.ingredients)
    print('-' * 20)


button.action = test
