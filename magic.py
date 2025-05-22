# Magic
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '5.22.2025'

import random

# Magic class
class Magic:
    def __init__(self, name, cost, base_damage, type):
        self.name = name
        self.cost = cost
        self.base_damage = base_damage
        self.type = type

    # Deal variable damage
    def deal_damage(self):
        damage = random.randrange(self.base_damage - 5, self.base_damage + 5)
        return damage