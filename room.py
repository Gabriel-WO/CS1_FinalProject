# Rooms
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '5.22.2025'

import pygame
from wall import Wall

# Room class
class Room:
    def __init__(self, background_path):
        # Background
        try:
            self.background = pygame.image.load(background_path).convert_alpha()
        except pygame.error as e:
            print(f'Error loading background {background_path}: {e}')
            # Fallback
            self.background = pygame.Surface((800,600))
            self.background.fill((100,100,100))

        # Walls
        self.walls = pygame.sprite.Group()

        # Doors (for transitioning between rooms)
        self.doors = []

        # Player initial location
        self.player_start_x = 100
        self.player_start_y = 100

    # Adding walls
    def add_wall(self, x, y, width, height, color=(0,0,0,0), wall_type = 'generic'):
        wall = Wall(x, y, width, height, color)
        wall.type = wall_type
        self.walls.add(wall)
        return wall

    # Adding doors
    def add_door(self, x, y, width, height, destination):
        door = {
            'rect': pygame.Rect(x, y, width, height),
            'destination': destination
        }
        self.doors.append(door)
        return door

    # Return walls
    def get_walls(self):
        return self.walls

    # Return doors
    def get_doors(self):
        return self.doors
