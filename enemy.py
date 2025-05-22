# Enemies
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '5.22.2025'

import pygame
import random
from enum import Enum
from magic import Magic

# Black magic
fire = Magic('Fire', 5, 7, 'black')
thunder = Magic('Thunder', 5, 7, 'black')
blizzard = Magic('Blizzard', 5, 7, 'black')

# White magic
cure = Magic('Cure', 5, 5, 'white')
cura = Magic('Cura', 10, 10, 'white')
curaga = Magic('Curaga', 20, 20, 'white')

ENEMY_TYPES = {
    'wolf': {
        'max_hp': 20,
        'hp': 20,
        'max_mp': 10,
        'mp': 10,
        'physical_damage': 12,
        'magical_damage': 7,
        'size': 200,
        'defense': 7,
        'spirit': 5,
        'luck': 3,
        'magic': [fire, cure],
        'image_path': 'assets/images/sprites/enemies/wolf.png'
    },
    'bandit': {
        'max_hp': 20,
        'hp': 20,
        'max_mp': 10,
        'mp': 10,
        'physical_damage': 15,
        'magical_damage': 5,
        'size': 200,
        'defense': 10,
        'spirit': 3,
        'luck': 3,
        'magic': [blizzard],
        'image_path': 'assets/images/sprites/enemies/bandit.png'
    },
    'spider': {
        'max_hp': 20,
        'hp': 20,
        'max_mp': 20,
        'mp': 20,
        'physical_damage': 7,
        'magical_damage': 13,
        'size': 200,
        'defense': 8,
        'spirit': 12,
        'luck': 3,
        'magic': [thunder, cura],
        'image_path': 'assets/images/sprites/enemies/spider.png'
    },
    'troll': {
        'max_hp': 30,
        'hp': 30,
        'max_mp': 7,
        'mp': 7,
        'physical_damage': 15,
        'magical_damage': 3,
        'size': 200,
        'defense': 15,
        'spirit': 5,
        'luck': 3,
        'magic': [fire, thunder],
        'image_path': 'assets/images/sprites/enemies/troll.png'
    },
    'eagle': {
        'max_hp': 15,
        'hp': 15,
        'max_mp': 20,
        'mp': 20,
        'physical_damage': 5,
        'magical_damage': 15,
        'size': 200,
        'defense': 7,
        'spirit': 12,
        'luck': 3,
        'magic': [fire, thunder, cure],
        'image_path': 'assets/images/sprites/enemies/eagle.png'
    },
    'golem': {
        'max_hp': 40,
        'hp': 40,
        'max_mp': 5,
        'mp': 5,
        'physical_damage': 20,
        'magical_damage': 3,
        'size': 600,
        'defense': 20,
        'spirit': 2,
        'luck': 3,
        'magic': [fire, cura],
        'image_path': 'assets/images/sprites/enemies/golem.png'
    },
    'skeleton': {
        'max_hp': 20,
        'hp': 20,
        'max_mp': 20,
        'mp': 20,
        'physical_damage': 10,
        'magical_damage': 10,
        'size': 200,
        'defense': 10,
        'spirit': 10,
        'luck': 3,
        'magic': [blizzard],
        'image_path': 'assets/images/sprites/enemies/skeleton.png'
    },
    'ghost': {
        'max_hp': 15,
        'hp': 15,
        'max_mp': 30,
        'mp': 30,
        'physical_damage': 5,
        'magical_damage': 15,
        'size': 200,
        'defense': 7,
        'spirit': 15,
        'luck': 3,
        'magic': [fire, thunder, blizzard, cura],
        'image_path': 'assets/images/sprites/enemies/ghost.png'
    },
    'zombie': {
        'max_hp': 25,
        'hp': 25,
        'max_mp': 20,
        'mp': 20,
        'physical_damage': 7,
        'magical_damage': 13,
        'size': 200,
        'defense': 10,
        'spirit': 10,
        'luck': 3,
        'magic': [thunder, blizzard, cure],
        'image_path': 'assets/images/sprites/enemies/zombie.png'
    },
    'final_boss': {
        'max_hp': 300,
        'hp': 300,
        'max_mp': 50,
        'mp': 50,
        'physical_damage': 40,
        'magical_damage': 35,
        'size': 400,
        'defense': 30,
        'spirit': 30,
        'luck': 3,
        'magic': [fire, thunder, blizzard, cure, cura, curaga],
        'image_path': 'assets/images/sprites/enemies/final_boss.png'
    }
}


# Enemy types
class EnemyTypes(Enum):
    WOLF = 'wolf'
    BANDIT = 'bandit'
    SPIDER = 'spider'
    TROLL = 'troll'
    EAGLE = 'eagle'
    GOLEM = 'golem'
    SKELETON = 'skeleton'
    GHOST = 'ghost'
    ZOMBIE = 'zombie'

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, enemy_type):
        pygame.sprite.Sprite.__init__(self)

        # Info
        self.type = enemy_type
        self.name = name

        # Stats
        self.stats = {
            'max_hp': ENEMY_TYPES[enemy_type]['max_hp'],
            'hp': ENEMY_TYPES[enemy_type]['hp'],
            'max_mp': ENEMY_TYPES[enemy_type]['max_mp'],
            'mp': ENEMY_TYPES[enemy_type]['mp'],
            'physical_damage': ENEMY_TYPES[enemy_type]['physical_damage'],
            'magical_damage': ENEMY_TYPES[enemy_type]['magical_damage'],
            'defense': ENEMY_TYPES[enemy_type]['defense'],
            'spirit': ENEMY_TYPES[enemy_type]['spirit'],
            'luck': ENEMY_TYPES[enemy_type]['luck']
        }

        # Size
        self.size = ENEMY_TYPES[enemy_type]['size']

        # Magic
        self.magic = ENEMY_TYPES[enemy_type]['magic']

        # Initial image
        self.image = self.load_image(f'assets/images//sprites/enemies/{self.type}.png')
        self.rect = self.image.get_rect()

    # Image loading
    def load_image(self, path):
        try:
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, (self.size, self.size))
        except pygame.error as e:
            print(f'Could not load image: {path}:{e}')
            placeholder = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            placeholder.fill((255, 0, 255))
            return placeholder

    # Update if dead
    def update(self):
        if not self.is_alive():
            self.kill()

    # Choose action
    def choose_action(self, player_party, enemy_party):

        # Healing spells
        healing_spells = [spell for spell in self.magic if spell.type == 'white']
        black_magic_spells = [spell for spell in self.magic if spell.type == 'black']

        # Prioritize healing itself
        if self.stats['hp'] <= 0.3 * self.stats['max_hp']:
            if healing_spells and self.stats['mp'] >= healing_spells[0].cost:
                return self, 'heal'

        # Check if allies need healing
        for ally in enemy_party.members:
            if ally.stats['hp'] <= 0.3 * ally.stats['max_hp']:
                if healing_spells and self.stats['mp'] >= healing_spells[0].cost:
                    return ally, 'heal'

        # If mp is too low to heal, defend
        if self.stats['hp'] <= 0.3 * self.stats['max_hp'] and self.stats['mp'] < 10:
            target = random.choice(player_party.members)
            action = 'defend'
            return target, action

        # Check for vulnerable player
        for player in player_party.members:
            if player.stats['hp'] <= 0.3 * player.stats['max_hp']:
                target = player
                if self.stats['magical_damage'] > self.stats['physical_damage']:
                    if black_magic_spells and self.stats['mp'] >= black_magic_spells[0].cost:
                        spell = random.choice(black_magic_spells)
                        action = {'type': 'magic', 'spell': spell, 'target': target}
                    else:
                        action = {'type': 'attack', 'target': target}
                else:
                    action = {'type': 'attack', 'target': target}
                return target, action

        # Default to attack
        target = random.choice(player_party.members)
        action = 'attack'
        return target, action

    # Take physical damage
    def take_physical_damage(self, damage):
        damage = max(1, damage - self.stats['defense'] // 4)
        self.stats['hp'] -= damage
        return damage

    # Take magical damage
    def take_magical_damage(self, damage):
        damage = max(1, damage - self.stats['spirit'] // 4)
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

    # Check if dead
    def is_alive(self):
        return self.stats['hp'] > 0






