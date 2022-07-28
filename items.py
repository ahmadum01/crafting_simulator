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
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
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


class Ingredient(InventoryBase):
    counter = [0]

    def __init__(self, canvas: CustomCanvas, rarity, level, x=-100, y=-100, r=35):
        self.x = x
        self.y = y
        self.r = r
        self.canvas = canvas
        self.rarity = rarity
        self.level = level
        self.slot = None
        self.background_image = ImageTk.PhotoImage(Image.open(images[self.rarity.lower()]).resize((r * 2, r * 2)))
        tag = f"token{self.counter[0]}"
        self.shape = self.canvas.create_image(x, y, image=self.background_image, anchor=tk.CENTER, tags=(tag, ), )
        self.canvas.bind_ingredient(tag)
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", self.drag_stop, "+")
        self.counter[0] += 1
        if f'{level}{rarity}' not in InventoryBase.elements:
            InventoryBase.elements[f'{level}{rarity}'] = {'elems': [], 'rarity': rarity, 'amount': 0, 'level': level}
        InventoryBase.elements[f'{level}{rarity}']['amount'] += 1
        InventoryBase.elements[f'{level}{rarity}']['elems'].append(self)

    def check_move_to_back(self):
        self.canvas.moveto(self.shape, self.x, self.y)

    def intersects(self, slot):
        x, y = self.canvas.coords(self.shape)
        return ((slot.x - x) ** 2 + (slot.y - y) ** 2) ** 0.5 <= slot.r + self.r

    def equals(self, other):
        return other.level == self.level and other.rarity == self.rarity

    def drag_stop(self, event):

        for crafting_slot in CraftingSlot.slots:
            if crafting_slot.main:
                continue
            if self.intersects(crafting_slot) and \
                    (not crafting_slot.ingredients or self.equals(crafting_slot.ingredients[0])) and \
                    len(crafting_slot.ingredients) < 5:
                self.slot = crafting_slot
                if self not in crafting_slot.ingredients:
                    crafting_slot.ingredients.append(self)
                self.move_to_slot()
            else:
                self.slot = None  # Надо сюда передавать слот инвентаря
                try:
                    crafting_slot.ingredients.remove(self)
                except ValueError:
                    pass
                # self.move_to_slot()

        for indicator in Indicator.indicators:
            indicator.set_state()
        self.canvas.drag_stop(event)




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
        self.canvas.create_text(x + w / 2, y + h / 2, text=text, fill='white', font='Tahoma 17', tags=(tag,))
        self.canvas.tag_bind(tag, "<ButtonPress-1>", self.button_pressed)
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", self.button_released)
        self.counter[0] += 1

    def button_pressed(self, event):
        self.canvas.itemconfig(self.shape, fill=self.pressed_color)
        self.action()

    def button_released(self, event):
        self.canvas.itemconfig(self.shape, fill=self.default_color)


class Indicator:
    indicators = []

    """Индикатор заполненности слота крафтинга"""
    def __init__(self, canvas: CustomCanvas, slot):
        self.canvas = canvas
        self.state = 0
        self.slot: CraftingSlot = slot
        self.w = 100
        self.h = 20
        self.padding = 30
        self.x1 = slot.x - self.w/2
        self.y1 = slot.y + slot.r + self.padding
        self.x2 = slot.x + self.w / 2
        self.y2 = slot.y + self.slot.r + self.padding + self.h
        self.shape = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill='white')
        self.inner_shape = self.canvas.create_rectangle(self.x1 + 1, self.y1 + 1, self.x1, self.y1, fill='green', outline='')
        self.indicators.append(self)

    def set_state(self):
        self.state = len(self.slot.ingredients)
        self.canvas.coords(self.inner_shape, self.x1 + 1, self.y1 + 1, self.x1 + (self.w / 5) * self.state, self.y2)



# def craft():