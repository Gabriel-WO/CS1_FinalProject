# Player
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '5.22.2025'

import pygame
import random
from enum import Enum
from magic import Magic
from animator import PlayerAnimator

# Black magic
fire = Magic('Fire', 5, 7, 'black')
thunder = Magic('Thunder', 5, 7, 'black')
blizzard = Magic('Blizzard', 5, 7, 'black')

# White magic
cure = Magic('Cure', 5, 5, 'white')
cura = Magic('Cura', 10, 10, 'white')
curaga = Magic('Curaga', 20, 20, 'white')


PLAYER_TYPES = {
    'warrior': {
        'max_hp': 200,
        'hp': 200,
        'max_mp': 30,
        'mp': 30,
        'physical_damage': 10,
        'magical_damage': 2,
        'size': 20,
        'defense': 20,
        'spirit': 10,
        'luck': 3,
        'magic': [fire, cure],
    },
    'priest': {
        'max_hp': 100,
        'hp': 100,
        'max_mp': 80,
        'mp': 80,
        'physical_damage': 5,
        'magical_damage': 10,
        'size': 20,
        'defense': 10,
        'spirit': 20,
        'luck': 3,
        'magic': [cure, cura, curaga],
    },
    'mage': {
        'max_hp': 150,
        'hp': 150,
        'max_mp': 80,
        'mp': 80,
        'physical_damage': 5,
        'magical_damage': 20,
        'size': 20,
        'defense': 15,
        'spirit': 15,
        'luck': 3,
        'magic': [fire, thunder, blizzard],
    }
}

# Player types
class PlayerTypes(Enum):
    WARRIOR = 0
    PRIEST = 1
    MAGE = 2

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, name, player_type):
        pygame.sprite.Sprite.__init__(self)

        # Animation
        self.animator = PlayerAnimator(player_type, config_path = 'assets/animations.json')

        # Info
        self.type = player_type
        self.name = name

        # Stats
        self.stats = {
            'max_hp': PLAYER_TYPES[player_type]['max_hp'],
            'hp': PLAYER_TYPES[player_type]['hp'],
            'max_mp': PLAYER_TYPES[player_type]['max_mp'],
            'mp': PLAYER_TYPES[player_type]['mp'],
            'physical_damage': PLAYER_TYPES[player_type]['physical_damage'],
            'magical_damage': PLAYER_TYPES[player_type]['magical_damage'],
            'defense': PLAYER_TYPES[player_type]['defense'],
            'spirit': PLAYER_TYPES[player_type]['spirit'],
            'luck': PLAYER_TYPES[player_type]['luck']
        }

        # Magic
        self.magic = PLAYER_TYPES[player_type]['magic']

        # Size
        self.size = PLAYER_TYPES[player_type]['size']

        # Combat
        self.defending = False

        # Initial image
        self.image = self.animator.update('idle')
        self.rect = self.image.get_rect()

    # Positioning
    def set_position(self, x, y, width, height):
        self.position = (x, y, width, height)
        self.rect.x = x
        self.rect.y = y

    def get_position(self):
        if hasattr(self, 'position'):
            return self.position
        return (0, 0, 0 ,0)

    # Update everything
    def update(self):
        pass

    # Receive magical damage
    def take_magical_damage(self, damage):
        damage = max(1, damage - self.stats['spirit'] // 4)
        self.stats['hp'] -= damage
        return damage

    # Receive physical damage
    def take_physical_damage(self, damage):
        # Reduce damage if defending
        if self.defending:
            damage = max(1, damage // 2)
            self.defending = False
        else:
            damage = max(1, damage - self.stats['defense'] // 4)
        self.stats['hp'] -= damage

        return damage

    # Heal
    def heal(self, amount):
        self.stats['hp'] = min(self.stats['hp'] + amount, self.stats['max_hp'])

    # Use mp
    def reduce_mp(self, cost):
        self.stats['mp'] -= cost

    # Attack
    def attack(self):
        damage = random.randrange(
            self.stats['physical_damage'] - 5,
            self.stats['physical_damage'] + 5)
        return damage

    # Cast spell
    def cast(self, spell):
        damage = random.randrange(
            self.stats['magical_damage'] * spell.base_damage - 5,
            self.stats['magical_damage'] * spell.base_damage + 5)
        return damage

    # Defend
    def defend(self):
        self.defending = True

    # Check if alive
    def is_alive(self):
        return self.stats['hp'] > 0









