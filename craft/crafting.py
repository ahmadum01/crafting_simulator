from random import choices
from craft.configs import base_probabilities, rarity_nums


class Ingredient:
    def __init__(self, rarity, level):
        self.rarity = rarity
        self.level = level
        self.properties = (self.level, self.rarity)

    def __repr__(self):
        return f'{self.rarity}-{self.level}'

    def __eq__(self, other):
        return self.rarity == other.rarity and self.level == other.level

    # def __hash__(self):
    #     return hash(self.properties)


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

    @staticmethod
    def init_slots(*slots):
        Craft.slots = slots

    @staticmethod
    def get_senior_ingredient() -> Ingredient:
        return max(Craft.slots, key=lambda x: x[0].properties)[0]

    @staticmethod
    def count_ingredients(ingredient: Ingredient) -> int:
        """ Counts ingredients in all slots """
        count = 0
        for slot in Craft.slots:
            count += slot.ingredients.count(ingredient)
        return count

    @staticmethod
    def count_fail_chance() -> int:
        senior_ingredient = Craft.get_senior_ingredient()
        common_level_difference = 0
        for i, slot in enumerate(Craft.slots):
            common_level_difference += senior_ingredient.level - slot[0].level
        fail_probability = common_level_difference * 25 - Craft.count_ingredients(senior_ingredient) * 3
        return max(fail_probability, 0)

    @staticmethod
    def count_probability_for_mix(base_probability: dict, senior_ingredient: Ingredient) -> dict:
        result_probability = base_probability.copy()
        if Craft.slots[0] == Craft.slots[1] == Craft.slots[2] and len(Craft.slots[0]) == 1:
            return base_probability

        move_probability = (Craft.count_ingredients(senior_ingredient) - 1) * 6.6
        rarity_num = rarity_nums[senior_ingredient.rarity]
        for i, key in enumerate(result_probability):
            if i == rarity_num:
                break
            temp = base_probability[key] * move_probability / 100
            result_probability[key] = base_probability[key] - temp
            result_probability[senior_ingredient.rarity] += temp

        for slot in Craft.slots:
            if slot[0] != senior_ingredient:
                level_diff = senior_ingredient.level - slot[0].level
                rarity_diff = rarity_nums[senior_ingredient.rarity] - rarity_nums[slot[0].rarity]
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
    def craft() -> Ingredient | str | None:
        if not Craft.is_craft_possible():
            return 'Impossible'

        fail_chance = Craft.count_fail_chance()

        if Craft.is_fail(fail_chance):
            return None

        senior_ingredient = Craft.get_senior_ingredient()
        base_probability = base_probabilities[senior_ingredient.rarity]
        mix_probability = Craft.count_probability_for_mix(base_probability, senior_ingredient)
        print(mix_probability)
        return Craft.generate_new_ingredient(mix_probability, senior_ingredient.level + 1)


if __name__ == '__main__':

    right_slot = Slot(*[Ingredient('C', 2) for _ in range(3)])
    left_slot = Slot(*[Ingredient('A', 1) for _ in range(1)])
    bottom_slot = Slot(*[Ingredient('B', 1) for _ in range(2)])

    Craft.init_slots(left_slot, right_slot, bottom_slot)
    print(Craft.craft())
    # from collections import Counter
    # c = Counter([craft(right_slot, left_slot, bottom_slot) for _ in range(1000)])
    # print(c)
