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


class Inventory:
    def __init__(self, canvas: CustomCanvas,  x1, y1, x2, y2):
        self.canvas = canvas
        self.canvas.create_rectangle(x1, y1, x2, y2, width=2)


class Laboratory:
    def __init__(self, canvas: CustomCanvas, x1, y1, x2, y2):
        self.canvas = canvas
        self.canvas.create_rectangle(x1, y1, x2, y2, width=2)


class InventorySlot:
    x1 = 40
    y1 = 110
    x2 = 320
    y2 = 190

    def __init__(self, canvas: CustomCanvas, x1=40, y1=110, x2=320, y2=190):
        self.canvas = canvas
        self.canvas.create_rectangle(x1, y1, x2, y2, width=2)


class CraftingSlot:
    def __init__(self, canvas: CustomCanvas, x, y, r, main=False):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.main = main
        self.canvas.create_oval(x - r, y - r, x + r, y + r, width=2)


class Ingredient:
    def __init__(self, canvas, rarity, level, x, y, w):
        self.canvas = canvas
        self.rarity = rarity
        self.level = level
        self.default_coordinate = {'x': x, 'y': y}
        self.background_image = ImageTk.PhotoImage(Image.open(images[self.rarity.lower()]).resize((w, w)))
        self.shape = self.canvas.create_image(x, y, image=self.background_image, anchor="nw", tags=("token",))

    def drag_stop(self, event):
        pass

    def check_move_to_back(self):
        pass


class Button:
    def __init__(self, canvas: CustomCanvas, x1, y1, x2, y2, action):
        self.action = action
        # self.canvas = canvas

    def run(self):
        self.action()