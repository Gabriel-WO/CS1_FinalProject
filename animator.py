# New Animation Manager
__author__ = 'Gabriel'
__version__ = '5.22.2025'

import pygame
import json
import os

# Parent animator class
class Animator:
    def __init__(self, config_path=None, config_dict=None):
        self.animations = {}
        self.sprite_sheets = {}
        self.current_animation = None
        self.current_direction = None
        self.current_frame = 0
        self.frame_timer = 0
        self.animation_complete = False

        # Load
        if config_path and os.path.exists(config_path):
            self.load_config_from_file(config_path)
        if config_dict:
            self.load_config_from_dict(config_dict)

        # Fallback default animation if no config is loaded
        if not self.animations:
            print("WARNING: No animations loaded. Using default.")
            self.animations = {
                    'explorer_idle': {
                        'sprite_sheet': 'assets/images/sprites/explorer/explorer_sprite_sheet.png',
                        'frame_count': 1,
                        'frame_width': 59,
                        'frame_height': 59,
                        'fps': 1,
                        'loop': True,
                        'row': 4
                    },
                    'explorer_walk': {
                        'sprite_sheet': 'assets/images/sprites/explorer/explorer_sprite_sheet.png',
                        'frame_count': 3,
                        'frame_width': 59,
                        'frame_height': 59,
                        'fps': 3,
                        'loop': True,
                        'directions': {
                            'down': {'row': 0},
                            'up': {'row': 1},
                            'left': {'row': 2},
                            'right': {'row': 3}
                        }
                    }
                }

    # Load animations from json file
    def load_config_from_file(self, config_path):
        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
                #print(f'Loaded config from {config_path}')
                #print(f'Config keys: {config.keys()}')
                self.load_config_from_dict(config)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f'Error loading config file: {e}')
            # If file can't be loaded, use default
            self.animations = {
                'explorer_idle': {
                    'sprite_sheet': 'assets/images/sprites/explorer/explorer_sprite_sheet.png',
                    'frame_count': 1,
                    'frame_width': 59,
                    'frame_height': 59,
                    'fps': 1,
                    'loop': True,
                    'row': 4
                }
            }

    # Load animations from dictionary
    def load_config_from_dict(self, config):
        if isinstance(config, dict):
            if 'combat_classes' in config:
                for class_type, animations in config.items():
                    for character_type, char_animations in animations.items():
                        for anim_name, anim_config in char_animations.items():
                            animation_key = f'{character_type}_{anim_name}'
                            self.animations[animation_key] = anim_config
            elif 'explorer_class' in config:
                explorer_config = config['explorer_class'].get('explorer', {})
                for anim_name, anim_config in explorer_config.items():
                    anim_key = f'explorer_{anim_name}'
                    self.animations[anim_key] = anim_config
            # Fallback to default if no explorer animations found
            if not any(key.startswith('explorer_') for key in self.animations):
                print("No explorer animations found. Using default.")
                self.animations['explorer_idle'] = {
                    'sprite_sheet': 'assets/images/sprites/explorer/explorer_sprite_sheet.png',
                    'frame_count': 1,
                    'frame_width': 59,
                    'frame_height': 59,
                    'fps': 1,
                    'loop': True,
                    'row': 4
                }

        '''print('Final processed animations:')
        for key in self.animations.keys():
            print(f' - {key}')'''

    # Load sprite sheet
    def load_sprite_sheet(self, sprite_sheet_path):
        if sprite_sheet_path in self.sprite_sheets:
            return self.sprite_sheets[sprite_sheet_path]

        try:
            sprite_sheet = pygame.image.load(sprite_sheet_path)
            self.sprite_sheets[sprite_sheet_path] = sprite_sheet
            return sprite_sheet
        except pygame.error as e:
            print(f'Error loading spritesheet file {sprite_sheet_path}: {e}')
            placeholder = pygame.Surface((32,32), pygame.SRCALPHA)
            placeholder.fill((255, 0, 255))
            return placeholder

    # Extract frames
    def get_animation_frames(self, animation_key, direction=None):
        if animation_key not in self.animations:
            print(f'Animation key {animation_key} not in animations')
            return pygame.Surface((32,32), pygame.SRCALPHA)

        config = self.animations[animation_key]
        sprite_sheet_path = config.get('sprite_sheet')

        if not sprite_sheet_path:
            print(f'No sprite sheet path for {animation_key}')
            return pygame.Surface((32,32), pygame.SRCALPHA)

        sprite_sheet = self.load_sprite_sheet(sprite_sheet_path)
        frame_width = config.get('frame_width')
        frame_height = config.get('frame_height')
        frame_count = config.get('frame_count', 1)

        # Directional animations
        row = 0
        if direction and 'directions' in config:
            if direction in config['directions']:
                row = config['directions'][direction].get('row', 0)
            else:
                print(f'Direction {direction} not in directions')
                return pygame.Surface((32,32), pygame.SRCALPHA)
        elif 'row' in config:
            row = config['row']

        # Dimensions
        columns = 3

        # Extract frames
        frames = []
        for frame_index in range(frame_count):
            col = frame_index % columns
            current_row = row + (frame_index // columns)
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.fill((0, 0, 0, 0))
            src_x = col * frame_width
            src_y = current_row * frame_height
            frame.blit(sprite_sheet, (0,0), (src_x, src_y, frame_width, frame_height))
            frames.append(frame)

        #print(f"Extracted {len(frames)} frames")
        return frames

    # Updating
    def update(self, animation_key, direction = None, dt=1/60):

        if not animation_key.startswith(('explorer_', 'warrior_', 'mage_', 'priest_')):
            animation_key = f'explorer_{animation_key}'

        # Debugging
        if animation_key not in self.animations:
            print(f'Animation key {animation_key} not in animations')
            animation_key = 'explorer_idle'
        config = self.animations[animation_key]

        # Directional animations
        if direction and 'directions' in config:
            if direction not in config['directions']:
                print(f"ERROR: Direction '{direction}' not found in animation")
                direction = list(config['directions'].keys())[0]

        # Check if animation changed
        animation_changed = (self.current_animation != animation_key or self.current_direction != direction)
        if animation_changed:
            self.current_animation = animation_key
            self.current_direction = direction
            self.current_frame = 0
            self.frame_timer = 0
            self.animation_complete = False

        config = self.animations[animation_key]
        fps = config.get('fps', 3)
        frame_duration = 1.0 / fps
        loop = config.get('loop', True)

        # Get frames
        frames = self.get_animation_frames(animation_key, direction)

        if not frames:
            return pygame.Surface((32,32), pygame.SRCALPHA)

        # Update timer
        self.frame_timer += dt

        # Check if it's time to advance to next frame
        if self.frame_timer >= frame_duration:
            self.frame_timer -= frame_duration
            self.current_frame += 1
            if self.current_frame >= len(frames):
                if loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(frames) - 1
                    self.animation_complete = True

        return frames[self.current_frame]

    # Check for completion
    def is_animation_complete(self):
        return self.animation_complete

# Player-specific animator class
class PlayerAnimator(Animator):
    def __init__(self, character_class, config_path=None):
        super().__init__(config_path)
        self.character_class = character_class
        self.last_animation = None

    # Updating
    def update(self, animation_name, direction = None, dt=1/60):
        animation_key = f'{self.character_class}_{animation_name}'
        if self.last_animation != animation_key:
            self.last_animation = animation_key
        frame = super().update(animation_key, direction, dt=dt)
        return frame

    def is_animation_complete(self):
        return self.animation_complete





