# Background management
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '5.22.2025'

import pygame

# Background class
class BackgroundManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.backgrounds = {
            'woods': self.load_background('assets/images/backgrounds/woods.png'),
            'woods_combat': self.load_background('assets/images/backgrounds/woods_combat.png'),
            'mountains': self.load_background('assets/images/backgrounds/mountains.png'),
            'mountains_combat': self.load_background('assets/images/backgrounds/mountains_combat.png'),
            'dungeon': self.load_background('assets/images/backgrounds/dungeon.png'),
            'dungeon_combat': self.load_background('assets/images/backgrounds/dungeon_combat.png'),
        }
        self.current_background = 'woods'
        self.previous_background = None
        self.transition_alpha = 255  # Full opacity
        self.is_transitioning = False
        self.fade_speed = 5  # Lower = slower fade

    def load_background(self, path):
        try:
            # Load and scale the background to fit the window
            image = pygame.image.load(path).convert()
            return pygame.transform.scale(image, (self.screen_width, self.screen_height))
        except pygame.error as e:
            print(f"Couldn't load background {path}: {e}")
            # Create a fallback background if image loading fails
            fallback = pygame.Surface((self.screen_width, self.screen_height))
            if 'boss' in path:
                # Dark red background for boss waves
                fallback.fill((40, 0, 0))
            else:
                # Dark blue background for regular waves
                fallback.fill((0, 0, 40))
            return fallback

    def set_background(self, bg_type):
        if bg_type != self.current_background:
            self.previous_background = self.current_background
            self.current_background = bg_type
            self.transition_alpha = 0  # Start fully transparent
            self.is_transitioning = True

    def update(self):
        if self.is_transitioning:
            self.transition_alpha += self.fade_speed
            if self.transition_alpha >= 255:
                self.transition_alpha = 255
                self.is_transitioning = False
                self.previous_background = None

    def draw(self, screen, width, height):
        if self.is_transitioning and self.previous_background:
            # Draw the previous background fully opaque
            screen.blit(self.backgrounds[self.previous_background], (0, 0))

            # Create a copy of the new background for alpha blending
            temp_surface = self.backgrounds[self.current_background].copy()
            # Create an alpha surface
            alpha_surface = pygame.Surface((width, height))
            alpha_surface.fill((255, 255, 255))
            # Apply alpha to the new background
            temp_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            temp_surface.set_alpha(self.transition_alpha)
            # Draw the new background with transparency
            screen.blit(temp_surface, (0, 0))
        else:
            # No transition, just draw the current background
            screen.blit(self.backgrounds[self.current_background], (0, 0))