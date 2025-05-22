# Room factory
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '5.22.2025'

import pygame
from wall import Wall
from room import Room

class RoomFactory:
    # Room configurations
    _room_configs = {
        'woods': {
            'background': 'assets/images/backgrounds/woods.png',
            'walls': [
                {'type': 'boundary', 'x': 0, 'y': 0, 'width': 800, 'height': 5},
                {'type': 'boundary', 'x': 0, 'y': 595, 'width': 350, 'height': 5},
                {'type': 'boundary', 'x': 450, 'y': 595, 'width': 350, 'height': 5},
                {'type': 'boundary', 'x': 0, 'y': 0, 'width': 5, 'height': 600},
                {'type': 'boundary', 'x': 795, 'y': 0, 'width': 5, 'height': 600},
                {'type': 'tree', 'x': 100, 'y': 200, 'width': 50, 'height': 50},
            ],
            'doors': [
                {'x': 350, 'y': 600, 'width': 100, 'height': 5, 'destination': 'mountains'}
            ],
            'player_start': {'x': 200, 'y': 200}
        },
        'mountains': {
            'background': 'assets/images/backgrounds/mountains.png',
            'walls': [
                {'type': 'boundary', 'x': 0, 'y': 0, 'width': 350, 'height': 5},
                {'type': 'boundary', 'x': 450, 'y': 0, 'width': 350, 'height': 5},
                {'type': 'boundary', 'x': 0, 'y': 595, 'width': 350, 'height': 5},
                {'type': 'boundary', 'x': 450, 'y': 590, 'width': 350, 'height': 5},
                {'type': 'boundary', 'x': 0, 'y': 0, 'width': 5, 'height': 600},
                {'type': 'boundary', 'x': 795, 'y': 0, 'width': 5, 'height': 250},
                {'type': 'boundary', 'x': 795, 'y': 350, 'width': 5, 'height': 250},
            ],
            'doors': [
                {'x': 350, 'y': 0, 'width': 100, 'height': 5, 'destination': 'woods'},
                {'x': 800, 'y': 250, 'width': 5, 'height': 100, 'destination': 'dungeon'}
            ],
            'player_start': {'x': 400, 'y': 50}
        },
        'dungeon': {
            'background': 'assets/images/backgrounds/dungeon.png',
            'walls': [
                {'type': 'boundary', 'x': 0, 'y': 0, 'width': 800, 'height': 5},
                {'type': 'boundary', 'x': 0, 'y': 595, 'width': 800, 'height': 5},
                {'type': 'boundary', 'x': 0, 'y': 0, 'width': 5, 'height': 250},
                {'type': 'boundary', 'x': 0, 'y': 350, 'width': 5, 'height': 250},
                {'type': 'boundary', 'x': 795, 'y': 0, 'width': 5, 'height': 600},
            ],
            'doors': [
                {'x': 0, 'y': 250, 'width': 5, 'height': 100, 'destination': 'mountains'},
            ],
            'player_start': {'x': 50, 'y': 250}
        }
    }

    @classmethod
    def create_room(cls, room_type):
        room_config = cls._room_configs[room_type]
        if not room_config:
            raise ValueError(f'Unknown room type: {room_type}')

        # Create rooms
        room = Room(room_config['background'])

        # Create walls
        for wall_config in room_config.get('walls', []):
            room.add_wall(
                wall_config['x'],
                wall_config['y'],
                wall_config['width'],
                wall_config['height'],
                color = (0, 0, 0, 0),
                wall_type = wall_config['type']
            )

        # Create doors
        for door_config in room_config.get('doors', []):
            room.add_door(
                door_config['x'],
                door_config['y'],
                door_config['width'],
                door_config['height'],
                door_config['destination']
            )

        return room

    # Load rooms
    @classmethod
    def load_rooms(cls):
        rooms = {}
        for room_type in cls._room_configs:
            rooms[room_type] = cls.create_room(room_type)
        return rooms
