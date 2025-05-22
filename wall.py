# Walls
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '5.22.2025'

import pygame

# Wall class
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = pygame.Rect(x, y, width, height)
        self.type = 'generic'

        # For collisions
        self.blocking = True

    # Check if wall blocking movement
    def is_blocking(self):
        return self.blocking