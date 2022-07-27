import tkinter as tk


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

    def create_ingredient(self, x, y, color):
        """Create a token at the given coordinate in the given color"""
        self.create_oval(
            x - 25,
            y - 25,
            x + 25,
            y + 25,
            outline=color,
            fill=color,
            tags=("token",),
        )

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
        self.canvas.create_rectangle(x1, y1, x2, y2)




class InventorySlot:
    pass


class CraftingSlot:
    pass


class Ingredients:
    pass

