# Explorer class
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '5.22.2025'

import pygame
import random
from animator import Animator

# Explorer class
class Explorer(pygame.sprite.Sprite):
    def __init__(self, player_party):
        pygame.sprite.Sprite.__init__(self)

        # Party
        self.player_party = player_party

        # Animation
        self.animator = Animator(config_path='assets/animations.json')

        # Spawning
        self.image = self.animator.update('explorer_idle')
        initial_x = 400
        initial_y = 300
        self.rect = self.image.get_rect(x=initial_x, y=initial_y)

        # Position tracking
        self.x = float(initial_x)
        self.y = float(initial_y)
        self.rect_x = initial_x
        self.rect_y = initial_y

        # Movement
        self.speed = 3
        self.change_x = 0
        self.change_y = 0
        self.is_moving = False
        self.current_direction = 'down'

        # Encounters
        self.encounter_chance = 0.005
        self.steps_since_last_encounter = 0

    # Direction and sprite updating
    def change_speed(self, x, y):

        # Diagonal movement
        if x != 0 and y != 0:
            x *= 0.7071
            y *= 0.7071

        self.change_x = x * self.speed
        self.change_y = y * self.speed
        self.is_moving = x != 0 or y != 0

        # Update image
        if x < 0:
            self.current_direction = 'left'
        elif x > 0:
            self.current_direction = 'right'
        elif y < 0:
            self.current_direction = 'up'
        elif y > 0:
            self.current_direction = 'down'

        if self.is_moving:
            self.image = self.animator.update('explorer_walk', self.current_direction)
        else:
            self.image = self.animator.update('explorer_idle')

    # Movement and collision
    def move(self, current_room):
        if self.change_x != 0 or self.change_y != 0:
            # Store old x/y
            old_x = self.x
            old_y = self.y

            # Update
            self.x += self.change_x
            self.y += self.change_y
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
            self.rect_x = self.rect.x
            self.rect_y = self.rect.y

            # Collision detection
            collided = pygame.sprite.spritecollide(self, current_room.walls, False)
            if collided:
                self.x = old_x
                self.y = old_y
                self.rect.x = int(self.x)
                self.rect.y = int(self.y)
                self.rect_x = self.rect.x
                self.rect_y = self.rect.y
                self.change_x = 0
                self.change_y = 0

            # Room transitions
            for door in current_room.doors:
                if self.rect.colliderect(door['rect']):
                    return door['destination']

            # Encounters
            if self.change_x != 0 or self.change_y != 0:
                self.steps_since_last_encounter += 1

                # Random encounter
                if random.random() < self.encounter_chance:
                    return self.trigger_encounter()

        return None

    # Trigger encounters
    def trigger_encounter(self):
        self.steps_since_last_encounter = 0

        encounter_types = [
            'woods_enemies',
            'mountains_enemies',
            'dungeon_enemies',
        ]

        return random.choice(encounter_types)

    # Updating
    def update(self):
        if self.change_x != 0 or self.change_y != 0:
            if self.change_x < 0:
                self.current_direction = 'left'
            elif self.change_x > 0:
                self.current_direction = 'right'
            elif self.change_y < 0:
                self.current_direction = 'up'
            elif self.change_y > 0:
                self.current_direction = 'down'
            self.image = self.animator.update('explorer_walk', self.current_direction)
        else:
            self.image = self.animator.update('explorer_idle')

    # Check for movement
    def is_moving(self):
        return self.change_x != 0 or self.change_y != 0
