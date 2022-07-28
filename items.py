import tkinter as tk
from PIL import Image, ImageTk
from config import images


class CustomCanvas(tk.Canvas):
    def __init__(self, parent, w, h, bg='white'):
        super().__init__(parent, width=w, height=h, bg=bg)
        self.w = w
        self.h = h
        self.bg = bg


        # this data is used to keep track of an
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.tag_bind("token", "<ButtonPress-1>", self.drag_start)
        self.tag_bind("token", "<ButtonRelease-1>", self.drag_stop)
        self.tag_bind("token", "<B1-Motion>", self.drag)


    def drag_start(self, event):
        """Beginning drag of an object"""
        # record the item and its location
        self._drag_data["item"] = self.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def drag_stop(self, event):
        """End drag of an object"""
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def drag(self, event):
        """Handle dragging of an object"""
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y


class InventoryBase:
    elements = {}
    action_elements = {}
    slots = None
    index = 1

    @staticmethod
    def init_data():
        data_list = list(InventoryBase.elements.values())

        for elem in InventoryBase.elements:
            InventoryBase.action_elements[elem] = InventoryBase.elements[elem]
            if len(InventoryBase.action_elements) == 6:
                break
        return InventoryBase

    @staticmethod
    def active_data(canvas: CustomCanvas):
        for slot, elems in zip(InventoryBase.slots.values(), InventoryBase.action_elements.values()):
            for elem in elems['elems']:
                elem.x = slot.x1 + 10
                elem.y = slot.y1 + 10
                canvas.moveto(elem.shape, elem.x, elem.y)

            slot.create_text(elems['level'], elems['rarity'], elems['amount'])


class Inventory(InventoryBase):
    def __init__(self, canvas: CustomCanvas,  x1=30, y1=100, x2=350, y2=750):
        self.canvas = canvas
        self.canvas.create_rectangle(x1, y1, x2, y2, width=2)

    def up(self):
        for elem in InventoryBase.elements:
            if elem not in InventoryBase.action_elements:
                InventoryBase.action_elements[elem] = InventoryBase.elements[elem]
                break

        for elems in list(InventoryBase.action_elements.values()):
            for elem in elems['elems']:
                self.canvas.moveto(elem.shape, elem.x, elem.y)
            break

        for elem in InventoryBase.action_elements:
            InventoryBase.action_elements.pop(elem)
            break

        # TODO: popitem() delete last item

    def down(self):
        for elem in InventoryBase.elements:
            if elem not in InventoryBase.action_elements:
                InventoryBase.action_elements[elem] = InventoryBase.elements[elem]
                break

        for elems in InventoryBase.action_elements.values():
            for elem in elems['elems']:
                self.canvas.moveto(elem.shape, elem.x, elem.y)
            break

        for elem in InventoryBase.action_elements:
            InventoryBase.action_elements.pop(elem)
            break


class Laboratory:
    def __init__(self, canvas: CustomCanvas, x1, y1, x2, y2):
        self.canvas = canvas
        self.canvas.create_rectangle(x1, y1, x2, y2, width=2)


class InventorySlot(InventoryBase):
    def __init__(self, canvas: CustomCanvas, x1=55, y1=110, x2=320, y2=190):
        self.x1 = x1
        self.y1 = y1
        self.canvas = canvas
        self.canvas.create_rectangle(x1, y1, x2, y2, width=2)

    def create_text(self, level, rarity, amount):
        self.canvas.create_text(self.x1 + 150, self.y1 + 45,
                                text=f'Level: {level}\nRarity: {rarity}\nAmount: {amount}',
                                font='Tahoma 14')


class CraftingSlot:
    def __init__(self, canvas: CustomCanvas, x, y, r, main=False):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.main = main
        self.canvas.create_oval(x - r, y - r, x + r, y + r, width=2)


class Ingredient(InventoryBase):
    def __init__(self, canvas: CustomCanvas, rarity, level, x=-100, y=-100, w=70):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.rarity = rarity
        self.level = level
        self.default_coordinate = {'x': x, 'y': y}  # TODO: it seems useless
        self.background_image = ImageTk.PhotoImage(Image.open(images[self.rarity.lower()]).resize((w, w)))
        self.shape = self.canvas.create_image(x, y, image=self.background_image, anchor="nw", tags=("token",))
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.drag_stop)
        if f'{level}{rarity}' not in InventoryBase.elements:
            InventoryBase.elements[f'{level}{rarity}'] = {'elems': [], 'rarity': rarity, 'amount': 0, 'level': level}
        InventoryBase.elements[f'{level}{rarity}']['amount'] += 1
        InventoryBase.elements[f'{level}{rarity}']['elems'].append(self)

    def check_move_to_back(self):
        self.canvas.moveto(self.shape, self.x, self.y)

    def drag_stop(self, event):
        self.check_move_to_back()
        self.canvas.drag_stop(event)


class Button:
    def __init__(self, canvas: CustomCanvas, x, y, w, h, text, action):
        self.canvas = canvas
        self.action = action
        self.default_color = '#7785a4'
        self.pressed_color = '#49536c'
        self.shape = self.canvas.create_rectangle(x, y, x + w, y + h, fill=self.default_color, tags=("button",))
        self.canvas.create_text(x + w / 2, y + h / 2, text='Craft', fill='white', font='Tahoma 17', tags=("button",))
        self.canvas.tag_bind("button", "<ButtonPress-1>", self.button_pressed)
        self.canvas.tag_bind("button", "<ButtonRelease-1>", self.button_released)

    def button_pressed(self, event):
        self.canvas.itemconfig(self.shape, fill=self.pressed_color, outline='yellow')
        self.action()

    def button_released(self, event):
        self.canvas.itemconfig(self.shape, fill=self.default_color, outline='yellow')
