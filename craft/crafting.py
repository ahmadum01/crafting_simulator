from craft import configs
from random import choices, randrange, choice
from enum import Enum
from dataclasses import dataclass


class Colors(Enum):
    RED = 'red'
    YELLOW = 'yellow'
    VIOLET = 'violet'
    BLUE = 'blue'
    GREEN = 'green'


@dataclass
class ColorStatement:
    slot1: Colors
    slot2: Colors
    slot3: Colors


class Ingredient:
    def __init__(self, rarity, level):
        if rarity not in configs.rarities:
            raise ValueError(f'rarity have to be in {configs.rarities}')
        if level not in configs.levels:
            raise ValueError(f'level have to be in {configs.levels}')
        self.rarity = rarity
        self.level = level
        self.properties = (self.level, self.rarity)

    def __repr__(self):
        return f'{self.rarity}-{self.level}'

    def __eq__(self, other):
        return self.rarity == other.rarity and self.level == other.level


class Slot:
    def __init__(self, *args):
        self.ingredients = args

    def __getitem__(self, index):
        return self.ingredients[index]

    def __len__(self):
        return len(self.ingredients)

    def __repr__(self):
        return f'Slot({self.ingredients[0]} x {len(self)})'

    def __eq__(self, other):
        return self.ingredients[0] == other.ingredients[0] and len(self.ingredients) == len(other.ingredients)

class Craft:
    slots = []
    daily_recipe = None

    @staticmethod
    def init_slots(*slots):
        Craft.slots = slots

    @staticmethod
    def get_senior_ingredient() -> Ingredient:
        return max(Craft.slots, key=lambda x: x[0].properties)[0]

    @staticmethod
    def slots_is_not_empty():
        for slot in Craft.slots:
            if len(slot) == 0:
                return False
        return True

    @staticmethod
    def count_ingredients(ingredient: Ingredient) -> int:
        """ Counts ingredients in all slots """
        count = 0
        for slot in Craft.slots:
            count += slot.ingredients.count(ingredient)
        return count

    @staticmethod
    def count_fail_chance() -> int:
        if Craft.slots_is_not_empty():
            senior_ingredient = Craft.get_senior_ingredient()
            common_level_difference = 0
            for i, slot in enumerate(Craft.slots):
                common_level_difference += senior_ingredient.level - slot[0].level
            fail_probability = common_level_difference * 25 - Craft.count_ingredients(senior_ingredient) * 3
            return max(fail_probability, 0)
        return 100

    @staticmethod
    def count_probability_for_mix(base_probability: dict, senior_ingredient: Ingredient) -> dict:
        result_probability = base_probability.copy()
        if Craft.slots[0] == Craft.slots[1] == Craft.slots[2] and len(Craft.slots[0]) == 1:
            return base_probability

        move_probability = (Craft.count_ingredients(senior_ingredient) - 1) * 6.6  # TODO: Change coefficient
        rarity_num = configs.rarity_nums[senior_ingredient.rarity]
        for i, key in enumerate(result_probability):
            if i == rarity_num:
                break
            temp = base_probability[key] * move_probability / 100
            result_probability[key] = base_probability[key] - temp
            result_probability[senior_ingredient.rarity] += temp

        for slot in Craft.slots:
            if slot[0] != senior_ingredient:
                level_diff = senior_ingredient.level - slot[0].level
                rarity_diff = configs.rarity_nums[senior_ingredient.rarity] - configs.rarity_nums[slot[0].rarity]
                move_probability = max([15 * (3 * level_diff + rarity_diff) - 2 * (len(slot) - 1), 0])
                move_probability = result_probability[senior_ingredient.rarity] * move_probability / 100
                for i, key in enumerate(result_probability):
                    if i == rarity_num:
                        break
                    result_probability[key] = result_probability[key] + move_probability / 2
                result_probability[senior_ingredient.rarity] -= move_probability

        return result_probability

    @staticmethod
    def is_craft_possible() -> bool:
        return Craft.count_fail_chance() < 100

    @staticmethod
    def is_fail(fail_chance: int) -> bool:
        return choices([True, False], [fail_chance, 100 - fail_chance], k=1)[0]

    @staticmethod
    def generate_new_ingredient(probability: dict, level: int) -> Ingredient:
        rarities, probabilities = zip(*probability.items())
        new_ingredient_rarity = choices(rarities, probabilities, k=1)[0]
        return Ingredient(rarity=new_ingredient_rarity, level=level)

    @staticmethod
    def craft() -> Ingredient | str:
        if not Craft.slots_is_not_empty():
            return 'There are empty slots'

        if not Craft.is_craft_possible():
            return 'Fail chance is 100 percents'

        fail_chance = Craft.count_fail_chance()

        if Craft.is_fail(fail_chance):
            return 'Fail'

        senior_ingredient = Craft.get_senior_ingredient()
        base_probability = configs.base_probabilities[senior_ingredient.rarity]
        mix_probability = Craft.count_probability_for_mix(base_probability, senior_ingredient)
        return Craft.generate_new_ingredient(mix_probability, senior_ingredient.level + 1)

    @staticmethod
    def generate_rand_ingredient(number: int) -> list[Ingredient]:
        rarity = choice(configs.rarities)
        level = choice(configs.levels)
        return [Ingredient(rarity, level) for _ in range(number)]

    @staticmethod
    def generate_rand_recipe() -> list[Slot]:
        slots = []
        for _ in range(3):
            number = randrange(1, 5)
            slots.append(Slot(*Craft.generate_rand_ingredient(number)))
        return slots

    @staticmethod
    def set_daily_recipe(*slots):
        Craft.daily_recipe = slots

    @staticmethod
    def check_recipe_matching() -> ColorStatement:
        slot_colors = dict(slot1=Colors.GREEN, slot2=Colors.GREEN, slot3=Colors.GREEN)
        for i, key in enumerate(slot_colors):
            slot = Craft.slots[i]
            if slot == Craft.daily_recipe[i]:
                slot_colors[key] = Colors.GREEN
            elif slot[0].properties == Craft.daily_recipe[i][0].properties:
                if len(slot) < len(Craft.daily_recipe[0]):
                    slot_colors[key] = Colors.VIOLET
                else:
                    slot_colors[key] = Colors.BLUE
            else:
                for recipe_slot in Craft.daily_recipe:
                    if slot[0].properties == recipe_slot[0].properties:
                        slot_colors[key] = Colors.YELLOW
                        break
                else:
                    slot_colors[key] = Colors.RED

        return ColorStatement(slot1=slot_colors['slot1'], slot2=slot_colors['slot2'], slot3=slot_colors['slot3'])


if __name__ == '__main__':
    left_slot = Slot(*[Ingredient('B', 1) for _ in range(1)])
    bottom_slot = Slot(*[Ingredient('B', 1) for _ in range(2)])
    right_slot = Slot(*[Ingredient('C', 2) for _ in range(3)])

    left_slot_d = Slot(*[Ingredient('B', 1) for _ in range(2)])
    bottom_slot_d = Slot(*[Ingredient('A', 2) for _ in range(3)])
    right_slot_d = Slot(*[Ingredient('C', 2) for _ in range(3)])

    Craft.init_slots(left_slot, bottom_slot, right_slot)
    # temp = Craft.generate_rand_recipe()
    Craft.set_daily_recipe(left_slot_d, bottom_slot_d, right_slot_d)

    print('Рецепт:', Craft.daily_recipe)
    print('Мой крафтинг: ', Craft.slots)
    print(Craft.check_recipe_matching())

