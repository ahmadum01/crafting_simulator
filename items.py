import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from config import (images,
                    win_bg_color,
                    win_width,
                    win_height,
                    COLOR_TEXT,
                    COLOR_FRAME,
                    COLOR_TEXT_STATEMENT,
                    COLOR_TEXT_MAIN_SLOT)
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
        item = self.find_closest(event.x, event.y)[0]
        if not self.gettags(item):
            return
        """Beginning drag of an object"""
        self._drag_data["item"] = item
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
        if self._drag_data["item"] is None:
            return
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        self.move(self._drag_data["item"], delta_x, delta_y)
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y


class InventoryBase:
    """
    elements - Служит как словарь. Примерная структура: {'A1': {'elems': [], 'level': 1, 'rarity': A}, ...}

    action_elements - список содержащий активные элементы в слотах инвентаря, необходим для показа определенного
    количества элементов в инвентаре. 1ый элемент списка находится в 1ом слоте инвентаря и т.д.

    slots - словарь содержащий информацию о слотах, ключами являются номера слотов, а значениями объекты Класса
    "InventorySlot"

    index - необходим для прокрутки инвентаря, взаимодействие происходит в дочернем классе "Inventory"

    list_elements - список содержащий информацию об ингридиентах, копия словаря "elements" см. выше.
    """
    elements = {}
    action_elements = []
    list_elements = []
    slots = None
    index = 0

    @staticmethod
    def init_or_update_data():
        """Вызывается для инициализации/обновления данных"""
        InventoryBase.list_elements = list(InventoryBase.elements.values())
        InventoryBase.action_elements = InventoryBase.list_elements[InventoryBase.index: InventoryBase.index + 6]
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
    def remove_empty_elements(element: 'Ingredient'):
        if not InventoryBase.elements[f'{element.rarity}{element.level}']['elems']:
            InventoryBase.elements.pop(f'{element.rarity}{element.level}')
            if InventoryBase.index - 1 != -1:
                InventoryBase.index -= 1

    @staticmethod
    def remove_ingredient(element: 'Ingredient', canvas: CustomCanvas):
        InventoryBase.elements[f'{element.rarity}{element.level}']['elems'].remove(element)

        InventoryBase.remove_empty_elements(element)

        if len(InventoryBase.list_elements) <= 6:
            InventoryBase.action_elements = InventoryBase.list_elements
        else:
            InventoryBase.action_elements = InventoryBase.list_elements[InventoryBase.index:InventoryBase.index + 6]

        InventoryBase.show_slot_content(canvas)

    @staticmethod
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
        self.canvas.create_rectangle(x1, y1, x2, y2, width=2, outline=COLOR_FRAME)

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
        self.canvas.create_rectangle(x1, y1, x2, y2, width=2, outline=COLOR_FRAME)


class InventorySlot(InventoryBase):
    def __init__(self, canvas: CustomCanvas, x1=55, y1=110, x2=320, y2=190, r=35):
        self.x1 = x1
        self.y1 = y1
        self.canvas = canvas
        self.canvas.create_rectangle(x1, y1, x2, y2, width=2, outline=COLOR_FRAME)
        self.text = self.canvas.create_text(self.x1 + 150, self.y1 + 45, text='', font='Tahoma 14', fill=COLOR_TEXT)
        self.flag = False

    def set_text(self, lvl='', rarity='', amount=''):
        text = ''
        if self.flag:
            text += f'Level: {lvl}\nRarity: {rarity}\nAmount: {amount}'
        self.canvas.itemconfig(self.text, text=text, fill=COLOR_TEXT)


class CraftingSlot:
    slots = []

    def __init__(self, canvas: CustomCanvas, x, y, r, main=False):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.main = main
        self.shape = self.canvas.create_oval(x - r, y - r, x + r, y + r, width=2, fill='#3914AF', outline=COLOR_FRAME)
        if main:
            self.text = self.canvas.create_text(self.x, self.y + self.r * 1.40, text='',
                                                font='Tahoma 12', justify=tk.CENTER, fill=COLOR_TEXT)
        else:
            self.text = self.canvas.create_text(self.x, self.y + self.r * 1.55, text='', font='Tahoma 10',
                                                fill=COLOR_TEXT)
        if not main:
            self.indicator = Indicator(canvas, self)
        else:
            self.text_message = self.canvas.create_text(self.x, self.y - 15, text='',
                                                        font='Tahoma 16', fill=COLOR_TEXT_MAIN_SLOT, justify=tk.CENTER)
        self.ingredients = []
        self.slots.append(self)

    def set_text(self):
        text = ''
        if self.ingredients:
            if isinstance(self.ingredients[0], Serum):
                text = f'Serum\n'
            elif isinstance(self.ingredients[0], Ingredient):
                text = f'Level: {self.ingredients[0].level}\n' \
                       f'Rarity: {self.ingredients[0].rarity}\n'

            if self.main:
                text += f'x{len(self.ingredients)}'
        self.canvas.itemconfig(self.text, text=text, fill=COLOR_TEXT)

    def text_message_main_slot(self, text=''):
        self.canvas.itemconfig(self.text_message, text=text, fill=COLOR_TEXT)

    # @staticmethod
    # def clear_main_slot():
    #     for element in CraftingSlot.slots[0].ingredients:
    #         element.move_to_slot()

    @staticmethod
    def update_slots_data():
        """Обновляем все индикаторы, тексты и т.д."""
        for slot in CraftingSlot.slots:  #
            if not slot.main:
                slot.indicator.set_state()
                slot.slots[0].text_message_main_slot()
            slot.set_text()


class SerumSlot:
    slots = []

    def __init__(self, canvas: CustomCanvas, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.r = CraftingSlot.slots[1].r
        self.canvas = canvas
        self.serums = []
        self.shape = self.canvas.create_rectangle(x1, y1, x2, y2, width=2, outline=COLOR_FRAME)
        text_message = f'Serum\nAmount: {Serum.counter}'
        self.text = self.canvas.create_text(self.x1 + 140, self.y1 + 50, text=text_message, font='Tahoma 14',
                                            fill=COLOR_TEXT)
        self.image = ImageTk.PhotoImage(Image.open(images['empty_serum']).resize((self.r * 2 - 50, self.r * 2 - 50)))
        self.empty_serum = self.canvas.create_image(self.x1 + 50, self.y1 + 50, image=self.image, anchor=tk.CENTER)
        SerumSlot.slots.append(self)

    def set_text(self):
        self.canvas.itemconfig(self.text, text=f'Serum\nAmount: {Serum.counter}', fill=COLOR_TEXT)


class Serum:
    counter = 0

    def __init__(self, canvas: CustomCanvas):
        self.canvas = canvas
        self.x = CraftingSlot.slots[0].x
        self.y = CraftingSlot.slots[0].y
        self.r = CraftingSlot.slots[1].r
        self.slot = None
        tag = f"serum{Ingredient.counter}"
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", self.drag_stop)
        self.image = ImageTk.PhotoImage(Image.open(images['serum']).resize((self.r * 2 - 50, self.r * 2 - 50)))
        self.shape = self.canvas.create_image(self.x, self.y, image=self.image, anchor=tk.CENTER, tags=(tag,))
        Serum.counter += 1

    def move_to_slot(self):
        for elem in self.slot.ingredients:
            self.canvas.moveto(elem.shape, SerumSlot.slots[0].x1 + 15, SerumSlot.slots[0].y1 + 15)
            elem.slot = SerumSlot.slots[0]
            SerumSlot.slots[0].serums.append(elem)
        SerumSlot.slots[0].set_text()
        CraftingSlot.slots[0].ingredients.clear()
        CraftingSlot.update_slots_data()

    def drag_stop(self, event):
        if self.slot in SerumSlot.slots:
            pass
        else:
            self.move_to_slot()


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

    def intersects(self, slot: CraftingSlot) -> bool:
        x, y = self.canvas.coords(self.shape)
        return ((slot.x - x) ** 2 + (slot.y - y) ** 2) ** 0.5 <= slot.r + self.r

    def equals(self, other: 'Ingredient') -> bool:
        return other.level == self.level and other.rarity == self.rarity

    def is_slot_suitable(self, slot: CraftingSlot) -> bool:
        return (not slot.ingredients or self.equals(slot.ingredients[0])) and len(slot.ingredients) < 5

    def drag_stop(self, event):
        intersected_slot = None
        for crafting_slot in CraftingSlot.slots:
            if not crafting_slot.main and self.intersects(crafting_slot):
                intersected_slot = crafting_slot

        if intersected_slot is None:  # Если ингредиент не пересекает ниодин слот

            if self.slot is not None:
                self.slot.ingredients.remove(self)
                InventoryBase.edit_amount(canvas=self.canvas, elem=self, option=True)
                self.slot = None
                self.move_to_slot()
            else:
                self.slot = None
                self.move_to_slot(clear_main_slot=False)

            InventoryBase.check_in_action_elements(elem=self)
            CraftingSlot.slots[0].text_message_main_slot()

        elif self.is_slot_suitable(intersected_slot):  # Если ингредиент пересекает слот и этот слот подходит
            if self.slot is not None:
                self.slot.ingredients.remove(self)
            else:
                InventoryBase.edit_amount(canvas=self.canvas, elem=self)
            if self not in intersected_slot.ingredients:
                intersected_slot.ingredients.append(self)
                self.slot = intersected_slot
            self.move_to_slot()

        CraftingSlot.update_slots_data()  # Обновляем все индикаторы, тексты и т.д.

        self.canvas.drag_stop(event)

    def move_to_slot(self, clear_main_slot=True):
        if clear_main_slot:
            for elem in CraftingSlot.slots[0].ingredients:
                if isinstance(elem, Serum):
                    elem.move_to_slot()
                else:
                    InventoryBase.check_in_action_elements(elem)
                    InventoryBase.edit_amount(elem.canvas, elem, option=True)
                    elem.canvas.moveto(elem.shape, elem.x, elem.y)
                    CraftingSlot.update_slots_data()
            CraftingSlot.slots[0].ingredients.clear()
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
        self.shape = self.canvas.create_rectangle(x, y, x + w, y + h, fill=self.default_color, tags=(tag,),
                                                  outline=COLOR_FRAME)
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
        self.shape = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill='white', outline=COLOR_FRAME)
        self.inner_shape = self.canvas.create_rectangle(self.x1 + 1, self.y1 + 1, self.x1, self.y1, fill='green',
                                                        outline=COLOR_FRAME)
        Indicator.indicators.append(self)

    def set_state(self):
        self.state = len(self.slot.ingredients)
        self.canvas.coords(self.inner_shape, self.x1 + 1, self.y1 + 1, self.x1 + (self.w / 5) * self.state, self.y2)


class Statement:
    statement_root = None
    flag = True
    statement_list = []

    @staticmethod
    def statement(root: tk.Tk):
        if Statement.statement_root is None:
            Statement.statement_root = scrolledtext.ScrolledText(root, width=70, height=38, font='Tahoma 10')
            Statement.statement_root['state'] = 'disabled'
            Statement.statement_root.pack()

        if not Statement.flag:
            Statement.statement_root.place(x=-752, y=-99)
            Statement.statement_root.destroy()
            Statement.statement_root = None
            Statement.flag = True

        else:
            Statement.statement_root.place(x=670, y=99)
            Statement.flag = False

            for elems_list in Statement.statement_list[::-1]:
                frame = tk.Frame(Statement.statement_root)
                for j, elem_list in enumerate(elems_list[:-1]):
                    label_text = tk.Label(frame, text=elem_list[0], fg=COLOR_TEXT_STATEMENT)
                    label = tk.Label(frame, image=elem_list[1], width=30, borderwidth=25, bg=elem_list[2])
                    label.grid(row=0, column=j, padx=20, pady=10)
                    label_text.grid(row=1, column=j, padx=20, pady=5)

                label_text = tk.Label(frame, text='--->', fg=COLOR_TEXT_STATEMENT)
                label_text.grid(row=0, column=j + 1, padx=20, pady=10)

                try:
                    label_text = tk.Label(frame, text=elems_list[-1][0], fg=COLOR_TEXT_STATEMENT)
                    label = tk.Label(frame, image=elems_list[-1][1], width=45, borderwidth=25, bg='white')
                    label.grid(row=0, column=j + 2, padx=20, pady=10)
                    label_text.grid(row=1, column=j + 2, padx=20, pady=10)
                except IndexError:
                    label_text = tk.Label(frame, text='FAIL', bg='red', width=12, fg=COLOR_TEXT_STATEMENT)
                    label_text.grid(row=0, column=j + 2, padx=20, pady=10)

                Statement.statement_root.window_create(tk.END, window=frame)

    @staticmethod
    def create_statement(crafted_element):
        statements = Statement.statement_list
        slots = CraftingSlot.slots

        statements.append([])
        for slot in slots[1:]:
            statements[-1].append(
                [f'{slot.ingredients[0].rarity}{slot.ingredients[0].level}x{len(slot.ingredients)}',
                 slot.ingredients[0].image]
            )
        colors = crafting.Craft.check_recipe_matching()
        Statement.statement_list[-1][0].append(colors.slot1.value)
        Statement.statement_list[-1][1].append(colors.slot2.value)
        Statement.statement_list[-1][2].append(colors.slot3.value)
        if crafted_element.type == 'Ingredient':
            statements[-1].append(
                [f'{crafted_element.res[0].rarity}{crafted_element.res[0].level}x{len(crafted_element.res)}',
                 slots[0].ingredients[0].image])
        elif crafted_element.type == 'Serum':
            statements[-1].append(
                [f'Serum x{len(crafted_element.res)}', slots[0].ingredients[0].image]
            )
        else:
            statements[-1].append(
                ['Fail']
            )


def craft(canvas: CustomCanvas, slots):
    crafting.Craft.init_slots(
        crafting.Slot(*[crafting.Ingredient(rarity=ing.rarity, level=ing.level) for ing in slots[1].ingredients]),
        crafting.Slot(*[crafting.Ingredient(rarity=ing.rarity, level=ing.level) for ing in slots[2].ingredients]),
        crafting.Slot(*[crafting.Ingredient(rarity=ing.rarity, level=ing.level) for ing in slots[3].ingredients]),
    )
    crafted_element = crafting.Craft.craft()
    if crafted_element.type == 'Ingredient':
        for ingredient in crafted_element.res:
            new_ingredient = Ingredient(canvas, rarity=ingredient.rarity, level=ingredient.level)
            new_ingredient.slot = slots[0]
            new_ingredient.move_to_slot(clear_main_slot=False)
            slots[0].ingredients.append(new_ingredient)
            InventoryBase.edit_amount(canvas, elem=new_ingredient, option=False)
    elif crafted_element.type == 'Serum':
        for _ in crafted_element.res:
            new_serum = Serum(canvas)
            new_serum.slot = slots[0]
            slots[0].ingredients.append(new_serum)
    elif crafted_element.type == 'message':
        if 'empty' in crafted_element.message:
            slots[0].text_message_main_slot(crafted_element.message.replace('are ', 'are\n'))
        else:
            slots[0].text_message_main_slot(crafted_element.message)
    Statement.create_statement(crafted_element)
    for slot in slots:
        if not slot.main:
            for ingredient in slot.ingredients:
                canvas.delete(ingredient.shape)
                InventoryBase.remove_ingredient(ingredient, canvas)
            slot.ingredients.clear()
            slot.indicator.set_state()
        slot.set_text()

    InventoryBase.init_or_update_data()
    InventoryBase.show_slot_content(canvas=canvas)

