base_probabilities = dict(
    A={'A': 70, 'B': 15, 'C': 10, 'D': 3, 'E': 2},
    B={'A': 22.5, 'B': 60, 'C': 12.5, 'D': 3, 'E': 2},
    C={'A': 2, 'B': 22.5, 'C': 60, 'D': 12.5, 'E': 3},
    D={'A': 1, 'B': 5, 'C': 24, 'D': 60, 'E': 10},
    E={'A': 0, 'B': 5, 'C': 8, 'D': 17, 'E': 70},
)

rarity_nums = dict(
    A=0,
    B=1,
    C=2,
    D=3,
    E=4,
)

serum_probabilities = dict(
    A=2,
    B=3,
    C=5,
    D=10,
    E=20,
)

serum_weights = {2: 0.5, 3: 0.25, 4: 0.15, 5: 0.1}
rarities = ['A', 'B', 'C', 'D', 'E']
levels = list(range(1, 5))
serum_levels = list(range(1, 6))
