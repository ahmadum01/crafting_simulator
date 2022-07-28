import tkinter as tk
from PIL import Image, ImageTk
from config import images, win_bg_color


# from objects import CRAFTING_SLOTS


class CustomCanvas(tk.Canvas):
    def __init__(self, parent, w, h, bg=win_bg_color):
        super().__init__(parent, width=w, height=h, bg=bg)
        self.w = w
        self.h = h
        self.bg = bg

        # this data is used to keep track of an
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag

    def bind_ingredient(self, tag_name, ):
        self.tag_bind(tag_name, "<ButtonPress-1>", self.drag_start)
        self.tag_bind(tag_name, "<ButtonRelease-1>", self.drag_stop)
        self.tag_bind(tag_name, "<B1-Motion>", self.drag)

    def drag_start(self, event):
        """Beginning drag of an object"""
        # record the item and its location
        self._drag_data["item"] = self.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self.lift(self._drag_data["item"])
        # print('start')

    def drag_stop(self, event):
        """End drag of an object"""
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0
        # print('drop')

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
        # print('drag')


class Inventory:
    def __init__(self, canvas: CustomCanvas, x1, y1, x2, y2):
        self.canvas = canvas
        self.canvas.create_rectangle(x1, y1, x2, y2, width=2)


class Laboratory:
    def __init__(self, canvas: CustomCanvas, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.canvas = canvas
        self.canvas.create_rectangle(x1, y1, x2, y2, width=2)


class InventorySlot:
    def __init__(self, canvas: CustomCanvas, x1=40, y1=110, x2=320, y2=190):
        self.canvas = canvas
        self.canvas.create_rectangle(x1, y1, x2, y2, width=2)


class CraftingSlot:
    slots = []

    def __init__(self, canvas: CustomCanvas, x, y, r, main=False):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.main = main
        self.shape = self.canvas.create_oval(x - r, y - r, x + r, y + r, width=2, fill='#2f185c')
        self.ingredients = []
        self.slots.append(self)


class Ingredient:
    counter = [0]

    def __init__(self, canvas: CustomCanvas, rarity, level, x, y, r):
        self.r = r
        self.canvas = canvas
        self.rarity = rarity
        self.level = level
        self.slot = None
        self.default_coordinate = {'x': x, 'y': y}
        self.background_image = ImageTk.PhotoImage(Image.open(images[self.rarity.lower()]).resize((r * 2, r * 2)))

        tag = f"token{self.counter[0]}"
        self.shape = self.canvas.create_image(x, y, image=self.background_image, anchor=tk.CENTER, tags=(tag, ), )
        self.canvas.bind_ingredient(tag)
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", self.drag_stop, "+")
        self.counter[0] += 1

    def intersects(self, slot):
        x, y = self.canvas.coords(self.shape)
        return ((slot.x - x) ** 2 + (slot.y - y) ** 2) ** 0.5 <= slot.r + self.r

    def equals(self, other):
        return other.level == self.level and other.rarity == self.rarity

    def drag_stop(self, event):
        self.canvas.drag_stop(event)
        for crafting_slot in CraftingSlot.slots:
            if crafting_slot.main:
                continue
            if self.intersects(crafting_slot) and \
                    (not crafting_slot.ingredients or self.equals(crafting_slot.ingredients[0])):
                self.slot = crafting_slot
                if self not in crafting_slot.ingredients:
                    crafting_slot.ingredients.append(self)
                self.move_to_slot()
            else:
                self.slot = None # Надо сюда передавать слот инвентаря
                try:
                    crafting_slot.ingredients.remove(self)
                except ValueError:
                    pass
                # self.move_to_slot()

    def move_to_slot(self):
        self.canvas.moveto(self.shape, self.slot.x - self.r, self.slot.y - self.r)

    def __repr__(self):
        return f'Ing({self.rarity} {self.level})'


class Button:
    counter = [0]

    def __init__(self, canvas: CustomCanvas, x, y, w, h, text, action):
        self.canvas = canvas
        self.action = action
        self.default_color = '#7785a4'
        self.pressed_color = '#49536c'

        tag = f'button{self.counter[0]}'
        self.shape = self.canvas.create_rectangle(x, y, x + w, y + h, fill=self.default_color, tags=(tag,))
        self.canvas.create_text(x + w / 2, y + h / 2, text='Craft', fill='white', font='Tahoma 17', tags=(tag,))
        self.canvas.tag_bind(tag, "<ButtonPress-1>", self.button_pressed)
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", self.button_released)
        self.counter[0] += 1

    def button_pressed(self, event):
        self.canvas.itemconfig(self.shape, fill=self.pressed_color, outline='yellow')
        self.action()

    def button_released(self, event):
        self.canvas.itemconfig(self.shape, fill=self.default_color, outline='yellow')


class Indicator:
    """Индикатор заполненности слота крафтинга"""
    def __init__(self):
        self.state = 0
        self.slot = None