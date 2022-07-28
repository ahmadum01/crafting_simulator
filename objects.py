from items import Ingredient, CraftingSlot
from GUI import canvas


INGREDIENTS = []
CRAFTING_SLOTS = []
left_slot = CraftingSlot(
    canvas,
    x=500,
    y=500,
    r=80
)
CRAFTING_SLOTS.extend(
    [left_slot]
)
