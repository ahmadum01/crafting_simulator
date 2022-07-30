import tkinter as tk
from PIL import Image, ImageTk
from config import images, win_bg_color
import craft.crafting as crafting


class CustomCanvas(tk.Canvas):
    def __init__(self, parent, w, h, bg=win_bg_color):
        super().__init__(parent, width=w, height=h, bg=bg)
        self.w = w
        self.h = h
        self.bg = bg
        self._drag_data = {"x": 0, "y": 0, "item": None}

    def bind_ingredient(self, tag_name, ):
        self.tag_bind(tag_name, "<ButtonPress-1>", self.drag_start)
        self.tag_bind(tag_name, "<ButtonRelease-1>", self.drag_stop)
        self.tag_bind(tag_name, "<B1-Motion>", self.drag)

    def drag_start(self, event):
        """Beginning drag of an object"""
        self._drag_data["item"] = self.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self.lift(self._drag_data["item"])

    def drag_stop(self, event):
        """End drag of an object"""
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def drag(self, event):
        """Handle dragging of an object"""
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        self.move(self._drag_data["item"], delta_x, delta_y)
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y


class InventoryBase:
    """
    elements - при создании ингредиентов служит как словарь, а при инициализации данных преобразуется в список и в
    дальнейшем служит как список ингредиентов. Примерная структура: [{'elems': [], 'level': 1, 'rarity': A}, {}, {}]

    action_elements - список содержащий активные элементы в слотах инвентаря, необходим для показа определенного
    количества элементов в инвентаре. 1ый элемент списка находится в 1ом слоте инвентаря и т.д.

    slots - словарь содержащий информацию о слотах, ключами являются номера слотов, а значениями объекты Класса
    "InventorySlot"

    index - необходим для прокрутки инвентаря, взаимодействие происходит в дочернем классе "Inventory"

    dict_elements - словарь содержащий информацию об ингридиентах, копия словаря "elements" см. выше.
    """
    elements = {}
    action_elements = []
    list_elements = []
    slots = None
    index = 0

    @staticmethod
    def init_data():
        """Вызывается один раз при запуске, необходим для первоначальной инициализации данных"""
        InventoryBase.list_elements = list(InventoryBase.elements.values())
        InventoryBase.action_elements = InventoryBase.list_elements[:6]
        return InventoryBase

    @staticmethod
    def show_slot_content(canvas: CustomCanvas, active=True):
        """Для показа/скрытия ингредиентов в инвентаре
        Параметр "active" служит для контролирования показа/скрытия ингредиентов инвентаря
        Для того чтобы, скрыть действенные элементы из инвентаря необходимо передать параметр active=False
        """
        if len(InventoryBase.list_elements) < 6:
            for key in range(6, len(InventoryBase.list_elements), -1):
                InventoryBase.slots[key].flag = False
        for slot, elems in zip(InventoryBase.slots.values(), InventoryBase.action_elements):
            for elem in elems['elems']:
                if elem.slot is None:
                    if active:
                        slot.flag = True
                        elem.x = slot.x1 + 10
                        elem.y = slot.y1 + 10
                    else:
                        elem.x = -100
                        elem.y = -100
                    canvas.moveto(elem.shape, elem.x, elem.y)
            if slot.flag:
                slot.set_text(elems['level'], elems['rarity'], elems['amount'])
        for slot in InventoryBase.slots.values():
            if not slot.flag:
                slot.set_text()

    @staticmethod
    def remove_empty_elements():
        for element in InventoryBase.list_elements:
            if not element['elems']:
                InventoryBase.list_elements.remove(element)

    @staticmethod
    def remove_ingredient(element: 'Ingredient', canvas: CustomCanvas):
        InventoryBase.elements[f'{element.rarity}{element.level}']['elems'].remove(element)

        InventoryBase.remove_empty_elements()

        if len(InventoryBase.list_elements) <= 6:
            InventoryBase.action_elements = InventoryBase.list_elements
        else:
            if InventoryBase.index - 1 != -1:
                InventoryBase.index -= 1

            InventoryBase.action_elements = InventoryBase.list_elements[InventoryBase.index:InventoryBase.index + 6]

        InventoryBase.show_slot_content(canvas)

    @staticmethod
    # TODO: works crookedly, in development
    def edit_amount(canvas: CustomCanvas, elem: 'Ingredient', option=False):
        if option:
            InventoryBase.elements[f'{elem.rarity}{elem.level}']['amount'] += 1
        else:
            InventoryBase.elements[f'{elem.rarity}{elem.level}']['amount'] -= 1

        InventoryBase.show_slot_content(canvas=canvas)

    @staticmethod
    def check_in_action_elements(elem: 'Ingredient'):
        l = [f'{elem["rarity"]}{elem["level"]}' for elem in InventoryBase.action_elements]
        if f'{elem.rarity}{elem.level}' not in l:
            elem.x = -100
            elem.y = -100


class Inventory(InventoryBase):
    def __init__(self, canvas: CustomCanvas, x1=30, y1=100, x2=350, y2=750):
        self.canvas = canvas
        self.canvas.create_rectangle(x1, y1, x2, y2, width=2)

    def up(self):
        if InventoryBase.index - 1 != -1:
            InventoryBase.index -= 1
            InventoryBase.show_slot_content(canvas=self.canvas, active=False)
            InventoryBase.action_elements = InventoryBase.list_elements[Inventory.index: Inventory.index + 6]
            InventoryBase.show_slot_content(canvas=self.canvas)

    def down(self):
        if InventoryBase.index + 6 < len(InventoryBase.list_elements):
            InventoryBase.index += 1
            InventoryBase.show_slot_content(canvas=self.canvas, active=False)
            InventoryBase.action_elements = InventoryBase.list_elements[Inventory.index: Inventory.index + 6]
            InventoryBase.show_slot_content(canvas=self.canvas)


class Laboratory:
    def __init__(self, canvas: CustomCanvas, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.canvas = canvas
        self.canvas.create_rectangle(x1, y1, x2, y2, width=2)


class InventorySlot(InventoryBase):
    def __init__(self, canvas: CustomCanvas, x1=55, y1=110, x2=320, y2=190, r=35):
        self.x1 = x1
        self.y1 = y1
        self.canvas = canvas
        self.canvas.create_rectangle(x1, y1, x2, y2, width=2)
        self.text = self.canvas.create_text(self.x1 + 150, self.y1 + 45, text='', font='Tahoma 14')
        self.flag = False

    def set_text(self, lvl='', rarity='', amount=''):
        text = ''
        if self.flag:
            text += f'Level: {lvl}\nRarity: {rarity}\nAmount: {amount}'
        self.canvas.itemconfig(self.text, text=text)


class CraftingSlot:
    slots = []

    def __init__(self, canvas: CustomCanvas, x, y, r, main=False):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.main = main
        self.shape = self.canvas.create_oval(x - r, y - r, x + r, y + r, width=2, fill='#3914AF')
        self.text = self.canvas.create_text(self.x, self.y + self.r * 1.55, text='', font='Tahoma 10')
        if not main:
            self.indicator = Indicator(canvas, self)
        self.ingredients = []
        self.slots.append(self)

    def set_text(self):
        text = ''
        if self.ingredients:
            text = f'Level: {self.ingredients[0].level}\n' \
                   f'Rarity: {self.ingredients[0].rarity}\n'
        self.canvas.itemconfig(self.text, text=text)


class SerumSlot:
    def __init__(self, canvas: CustomCanvas, x1, y1, x2, y2):
        self.canvas = canvas
        self.shape = self.canvas.create_rectangle(x1, y1, x2, y2, width=2)


class Ingredient(InventoryBase):
    counter = 0

    def __init__(self, canvas: CustomCanvas, rarity, level, x=-100, y=-100, r=35):
        self.x = x + r
        self.y = y + r
        self.r = r
        self.canvas = canvas
        self.rarity = rarity
        self.level = level
        self.slot = None
        self.image = ImageTk.PhotoImage(Image.open(images[self.rarity.lower()]).resize((r * 2, r * 2)))
        tag = f"token{Ingredient.counter}"
        self.shape = self.canvas.create_image(x, y, image=self.image, anchor=tk.CENTER, tags=(tag,), )
        self.canvas.bind_ingredient(tag)
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", self.drag_stop, "+")
        Ingredient.counter += 1
        if f'{rarity}{level}' not in InventoryBase.elements:
            InventoryBase.elements[f'{rarity}{level}'] = {'elems': [], 'rarity': rarity, 'amount': 0, 'level': level}
        InventoryBase.elements[f'{rarity}{level}']['amount'] += 1
        InventoryBase.elements[f'{rarity}{level}']['elems'].append(self)

    def check_move_to_back(self):
        self.canvas.moveto(self.shape, self.x, self.y)

    def intersects(self, slot):
        x, y = self.canvas.coords(self.shape)
        return ((slot.x - x) ** 2 + (slot.y - y) ** 2) ** 0.5 <= slot.r + self.r

    def equals(self, other):
        return other.level == self.level and other.rarity == self.rarity

    def drag_stop(self, event):
        for crafting_slot in CraftingSlot.slots:
            # if :
            #     continue
            if not crafting_slot.main and self.intersects(crafting_slot) and \
                    (not crafting_slot.ingredients or self.equals(crafting_slot.ingredients[0])) and \
                    len(crafting_slot.ingredients) < 5:
                self.slot = crafting_slot
                if self not in crafting_slot.ingredients:
                    crafting_slot.ingredients.append(self)
                    InventoryBase.edit_amount(canvas=self.canvas, elem=self)
                self.move_to_slot()
                crafting_slot.set_text()
                crafting_slot.indicator.set_state()
                break
            else:
                self.slot = None
                try:
                    crafting_slot.ingredients.remove(self)
                    InventoryBase.check_in_action_elements(elem=self)
                    InventoryBase.edit_amount(canvas=self.canvas, elem=self, option=True)
                except ValueError:
                    pass
            crafting_slot.set_text()
            if not crafting_slot.main:
                crafting_slot.indicator.set_state()
        else:
            self.move_to_slot()

        self.canvas.drag_stop(event)

    def move_to_slot(self):
        if self.slot is None:
            self.canvas.moveto(self.shape, self.x, self.y)
        else:
            self.canvas.moveto(self.shape, self.slot.x - self.r, self.slot.y - self.r)

    def __repr__(self):
        return f'Ing({self.rarity}{self.level})'


class Button:
    counter = 0

    def __init__(self, canvas: CustomCanvas, x, y, w, h, text, action):
        self.canvas = canvas
        self.action = action
        self.default_color = '#7785a4'
        self.pressed_color = '#49536c'
        tag = f'button{Button.counter}'
        self.shape = self.canvas.create_rectangle(x, y, x + w, y + h, fill=self.default_color, tags=(tag,))
        self.canvas.create_text(x + w / 2, y + h / 2, text=text, fill='white', font='Tahoma 17', tags=(tag,))
        self.canvas.tag_bind(tag, "<ButtonPress-1>", self.button_pressed)
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", self.button_released)
        Button.counter += 1

    def button_pressed(self, event):
        self.canvas.itemconfig(self.shape, fill=self.pressed_color)
        self.action()

    def button_released(self, event):
        self.canvas.itemconfig(self.shape, fill=self.default_color)


class Indicator:
    """Индикатор заполненности слота крафтинга"""
    indicators = []

    def __init__(self, canvas: CustomCanvas, slot):
        self.canvas = canvas
        self.state = 0
        self.slot: CraftingSlot = slot
        self.w = 100
        self.h = 20
        self.padding = 50
        self.x1 = slot.x - self.w / 2
        self.y1 = slot.y + slot.r + self.padding
        self.x2 = slot.x + self.w / 2
        self.y2 = slot.y + self.slot.r + self.padding + self.h
        self.shape = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill='white')
        self.inner_shape = self.canvas.create_rectangle(self.x1 + 1, self.y1 + 1, self.x1, self.y1, fill='green',
                                                        outline='')
        Indicator.indicators.append(self)

    def set_state(self):
        self.state = len(self.slot.ingredients)
        self.canvas.coords(self.inner_shape, self.x1 + 1, self.y1 + 1, self.x1 + (self.w / 5) * self.state, self.y2)


def craft(canvas: CustomCanvas, slots):
    crafting.Craft.init_slots(
        crafting.Slot(*[crafting.Ingredient(rarity=ing.rarity, level=ing.level) for ing in slots[1].ingredients]),
        crafting.Slot(*[crafting.Ingredient(rarity=ing.rarity, level=ing.level) for ing in slots[2].ingredients]),
        crafting.Slot(*[crafting.Ingredient(rarity=ing.rarity, level=ing.level) for ing in slots[3].ingredients]),
    )
    # if crafting
    print(f'Fail chance: {crafting.Craft.count_fail_chance()}')
    crafted_ingredient = crafting.Craft.craft()
    print(crafted_ingredient)
    if isinstance(crafted_ingredient, crafting.Ingredient):

        new_ingredient = Ingredient(canvas, rarity=crafted_ingredient.rarity, level=crafted_ingredient.level)
        new_ingredient.slot = slots[0]
        new_ingredient.move_to_slot()
        slots[0].ingredients = [new_ingredient]
        slots[0].set_text()
        InventoryBase.edit_amount(canvas, elem=new_ingredient, option=False)
    for slot in slots:
        if slot.main:
            continue
        for ingredient in slot.ingredients:
            canvas.delete(ingredient.shape)
            InventoryBase.remove_ingredient(ingredient, canvas)
        slot.ingredients.clear()
        slot.set_text()
        slot.indicator.set_state()

