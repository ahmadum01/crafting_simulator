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

    def __hash__(self):
        return hash(self.properties)


class Serum:
    def __init__(self, level):
        if level not in configs.serum_levels:
            raise ValueError(f'level have to be in {configs.levels}')
        self.level = level

    def __eq__(self, other):
        return self.level == other.level

    def __hash__(self):
        return hash(str(self.level))

    def __repr__(self):
        return f'Serum(level={self.level})'


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


@dataclass
class CraftingResult:
    message: str
    type: str
    res: list


class Craft:
    slots = []
    daily_recipe = None
    serum_crafting_recipe = None

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
    def count_serum_win_chance():
        win_probability = 0
        for slot in Craft.slots:
            if slot[0].level == configs.levels[-1]:
                win_probability += configs.serum_probabilities[slot[0].rarity] * len(slot)
        return win_probability

    @staticmethod
    def count_fail_chance() -> int:
        if Craft.slots_is_not_empty():
            if Craft.is_serum_crafts():
                return max(100 - Craft.count_serum_win_chance(), 0)
            else:
                senior_ingredient = Craft.get_senior_ingredient()
                common_level_difference = 0
                for i, slot in enumerate(Craft.slots):
                    common_level_difference += senior_ingredient.level - slot[0].level
                fail_probability = common_level_difference * 25 - Craft.count_ingredients(senior_ingredient) * 3
                return max(fail_probability, 0)
        return 100

    @staticmethod
    def count_probability_for_mix(senior_ingredient: Ingredient) -> dict:
        base_probability = configs.base_probabilities[senior_ingredient.rarity]
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
                    result_probability[key] = result_probability[key] + move_probability / rarity_num
                if rarity_num != 0:
                    result_probability[senior_ingredient.rarity] -= move_probability

        return result_probability

    @staticmethod
    def is_craft_possible() -> bool:
        return Craft.slots_is_not_empty() and Craft.count_fail_chance() < 100

    @staticmethod
    def is_fail(fail_chance: int) -> bool:
        return choices([True, False], [fail_chance, 100 - fail_chance], k=1)[0]

    @staticmethod
    def generate_new_ingredient(probability: dict, level: int) -> Ingredient:
        rarities, probabilities = zip(*probability.items())
        new_ingredient_rarity = choices(rarities, probabilities, k=1)[0]
        return Ingredient(rarity=new_ingredient_rarity, level=level)

    @staticmethod
    def generate_serum(win_chance) -> Serum:
        rest_of_probability = win_chance - 100

        if not Craft.is_fail(100 - rest_of_probability * configs.serum_weights[5]):
            return Serum(level=5)
        if not Craft.is_fail(100 - rest_of_probability * configs.serum_weights[4]):
            return Serum(level=4)
        if not Craft.is_fail(100 - rest_of_probability * configs.serum_weights[3]):
            return Serum(level=3)
        if not Craft.is_fail(100 - rest_of_probability * configs.serum_weights[2]):
            return Serum(level=2)
        return Serum(level=1)

    @staticmethod
    def is_serum_crafts():
        for slot in Craft.slots:
            for ingredient in slot.ingredients:
                if ingredient.level == configs.levels[-1]:
                    return True
        return False

    @staticmethod
    def craft() -> CraftingResult:
        if not Craft.slots_is_not_empty():
            return CraftingResult(message='There are empty slots',
                                  type='message', res=[])

        if not Craft.is_craft_possible():
            return CraftingResult(message='Fail chance is 100 percents',
                                  type='message', res=[])

        if Craft.is_serum_crafts():
            # Serum recipe temporary disabled

            # if Craft.is_recipe_match(serum=True):
            #     return CraftingResult(message='Serum crafted success',
            #                           type='Serum',
            #                           res=[Serum() for _ in range(3)])

            serum_win_chance = Craft.count_serum_win_chance()
            if serum_win_chance > 100:
                return CraftingResult(message='Serum crafted success',
                                      type='Serum', res=[Craft.generate_serum(serum_win_chance)])
            if Craft.is_fail(Craft.count_fail_chance()):
                return CraftingResult(message='Fail',
                                      type='message', res=[])
            return CraftingResult(message='Serum crafted success',
                                  type='Serum',
                                  res=[Serum(level=1)])

        senior_ingredient = Craft.get_senior_ingredient()

        if Craft.is_recipe_match():
            return CraftingResult(message='Ingredient crafted success',
                                  type='Ingredient',
                                  res=[Ingredient(rarity='E', level=senior_ingredient.level + 1) for _ in range(5)])

        if Craft.is_fail(Craft.count_fail_chance()):
            return CraftingResult(message='Fail',
                                  type='message', res=[])

        mix_probability = Craft.count_probability_for_mix(senior_ingredient)

        return CraftingResult(message='Ingredient crafted success',
                              type='Ingredient',
                              res=[Craft.generate_new_ingredient(mix_probability, senior_ingredient.level + 1)])

    @staticmethod
    def is_recipe_match(serum: bool = False):
        color_statement = Craft.check_recipe_matching(serum)
        return all(
            (color_statement.slot1 == Colors.GREEN,
             color_statement.slot2 == Colors.GREEN,
             color_statement.slot3 == Colors.GREEN)
        )

    @staticmethod
    def generate_rand_ingredient(number: int, max_level=len(configs.levels), exact_level=None) -> list[Ingredient]:
        rarity = choice(configs.rarities)
        if exact_level:
            level = exact_level
        else:
            level = choice(configs.levels[: max_level])
        return [Ingredient(rarity, level) for _ in range(number)]

    @staticmethod
    def generate_rand_recipe(serum: bool = False) -> list[Slot]:
        if serum:
            while True:
                slots = []
                for _ in range(3):
                    number = randrange(1, 5)
                    slots.append(
                        Slot(
                            *Craft.generate_rand_ingredient(number, max_level=len(configs.levels))
                        )
                    )
                for slot in slots:
                    if slot[0].level == configs.levels[-1]:
                        return slots
        else:
            slots = []
            level = choice(configs.levels[:len(configs.levels) - 1])
            for _ in range(3):
                number = randrange(1, 5)
                slots.append(
                    Slot(
                        *Craft.generate_rand_ingredient(number, exact_level=level)
                    )
                )
            return slots

    @staticmethod
    def set_daily_recipe(*slots):
        Craft.daily_recipe = slots

    @staticmethod
    def set_serum_crafting_recipe(*slots):
        Craft.serum_crafting_recipe = slots

    @staticmethod
    def check_recipe_matching(serum: bool = False) -> ColorStatement:
        recipe_slots = Craft.serum_crafting_recipe if serum else Craft.daily_recipe
        slot_colors = dict(slot1=Colors.GREEN, slot2=Colors.GREEN, slot3=Colors.GREEN)
        for i, key in enumerate(slot_colors):
            slot = Craft.slots[i]
            if slot == recipe_slots[i]:
                slot_colors[key] = Colors.GREEN
            elif slot[0].properties == recipe_slots[i][0].properties:
                if len(slot) < len(recipe_slots[i]):
                    slot_colors[key] = Colors.VIOLET
                else:
                    slot_colors[key] = Colors.BLUE
            else:
                for recipe_slot in recipe_slots:
                    if slot[0].properties == recipe_slot[0].properties:
                        slot_colors[key] = Colors.YELLOW
                        break
                else:
                    slot_colors[key] = Colors.RED

        return ColorStatement(slot1=slot_colors['slot1'], slot2=slot_colors['slot2'], slot3=slot_colors['slot3'])


if __name__ == '__main__':
    from collections import Counter

    left_slot = Slot(*[Ingredient('E', 4) for _ in range(5)])
    bottom_slot = Slot(*[Ingredient('E', 4) for _ in range(5)])
    right_slot = Slot(*[Ingredient('E', 4) for _ in range(5)])

    Craft.init_slots(left_slot, bottom_slot, right_slot)




    # left_slot_d = Slot(*[Ingredient('B', 1) for _ in range(2)])
    # bottom_slot_d = Slot(*[Ingredient('A', 2) for _ in range(3)])
    # right_slot_d = Slot(*[Ingredient('C', 2) for _ in range(3)])

    # Craft.set_serum_crafting_recipe()
    #

    # Craft.set_daily_recipe(left_slot_d, bottom_slot_d, right_slot_d)
    # Craft.set_serum_crafting_recipe(left_slot_d, bottom_slot_d, right_slot_d)
    print(Craft.slots)
    print(Counter([Craft.craft().res[0] for _ in range(100_000)]))
    #
    # print('Рецепт:', Craft.daily_recipe)
    # print('Мой крафтинг: ', Craft.slots)
    # print(Craft.check_recipe_matching(serum=True))

