# Party management
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '5.22.2025'

import pygame
import random
from player import Player
from enemy import ENEMY_TYPES, Enemy

# Parent class
class Party:
    def __init__(self):
        self.members = []
        self.max_size = 3

    # Add players
    def add_member(self, member):
        if len(self.members) < self.max_size:
            self.members.append(member)
            return True
        return False

# Player party
class PlayerParty(Party):
    def __init__(self):
        super().__init__()

# Enemy party
class EnemyParty(Party):
    def __init__(self):
        super().__init__()
        self.possible_enemies = ['rat', 'knight']

    # Create random party
    def generate_random_party(self, encounter_type = None):
        # Woods enemies
        if encounter_type == 'woods_enemies':
            enemy_types = ['wolf', 'bandit', 'spider']
        # Mountains enemies
        elif encounter_type == 'mountains_enemies':
            enemy_types = ['troll', 'eagle', 'golem']
        # Dungeon enemies
        elif encounter_type == 'dungeon_enemies':
            enemy_types = ['skeleton', 'ghost', 'zombie']
        # Final boss
        elif encounter_type == 'final_boss':
            enemy_types = ['final_boss']
        else:
            # Default enemies
            enemy_types = ['wolf', 'eagle', 'skeleton']

        # Generate
        num_enemies = random.randint(1, min(3, self.max_size))
        for i in range(num_enemies):
            enemy_type = random.choice(enemy_types)
            enemy = Enemy(f'{enemy_type.capitalize()}', enemy_type)
            self.add_member(enemy)

        return self

    # Final boss
    def generate_final_boss(self, encounter_type = 'final_boss', enemy_type = 'final_boss'):
        enemy = Enemy('Final Boss', enemy_type)
        self.add_member(enemy)
        return self

    # Choose actions
    def choose_actions(self, player_party):
        actions = []
        for enemy in self.members:
            if enemy.stats['hp'] > 0:
                target, action_type = enemy.choose_action(player_party, self)
                if action_type == 'attack':
                    action = {'type': 'attack', 'target': target}
                elif action_type == 'heal':
                    healing_spells = [spell for spell in enemy.magic if spell.type == 'white']
                    if healing_spells and enemy.stats['mp'] >= healing_spells[0].cost:
                        spell = healing_spells[0]
                        action = {'type': 'magic', 'spell': spell, 'target': target}
                    else:
                        action = {'type': 'attack', 'target': target}
                elif action_type == 'magic':
                    black_magic_spells = [spell for spell in enemy.magic if spell.type == 'black']
                    if black_magic_spells and enemy.stats['mp'] >= black_magic_spells[0].cost:
                        spell = random.choice(black_magic_spells)
                        action = {'type': 'magic', 'spell': spell, 'target': target}
                elif action_type == 'defend':
                    action = {'type': 'defend'}
                else:
                    action = {'type': 'attack', 'target': target}
            else:
                enemy.update()

            actions.append((enemy, action))

        return actions