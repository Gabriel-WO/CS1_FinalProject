# Sound and music
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '5.22.2025'

import pygame

# Sound effects
SOUND_EFFECTS = {
    'attack': 'assets/sounds/effects/attack.wav',
    'fire': 'assets/sounds/effects/fire.wav',
    'blizzard': 'assets/sounds/effects/blizzard.wav',
    'thunder': 'assets/sounds/effects/thunder.wav',
    'heal': 'assets/sounds/effects/heal.wav',
}

# Music
MUSIC = {
    'woods': 'assets/sounds/music/woods.mp3',
    'mountains': 'assets/sounds/music/mountains.mp3',
    'dungeon': 'assets/sounds/music/dungeon.mp3',
    'battle_woods': 'assets/sounds/music/battle_woods.mp3',
    'battle_mountains': 'assets/sounds/music/battle_mountains.mp3',
    'battle_dungeon': 'assets/sounds/music/battle_dungeon.mp3',
    'battle_boss': 'assets/sounds/music/battle_boss.mp3',
    'victory': 'assets/sounds/music/victory.mp3',
    'game_over': 'assets/sounds/music/game_over.mp3',
}

# Sound manager
class SoundManager:
    def __init__(self):
        # Volume
        self.volume = 0.7

        # Cache
        self.sound_cache = {}

    # Set volume
    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sound_cache.values():
            sound.set_volume(self.volume)

    # Load sounds
    def load_sound(self, name, path):
        try:
            if name not in self.sound_cache:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.volume)
                self.sound_cache[name] = sound
            return self.sound_cache[name]
        except pygame.error as e:
            print(f'Could not load sound {name} from {path}: {e}')
            return None

    # Play sounds
    def play_sound(self, name):
        try:
            if name in self.sound_cache:
                self.sound_cache[name].play()
            elif name in SOUND_EFFECTS:
                sound = self.load_sound(name, SOUND_EFFECTS[name])
                if sound:
                    sound.play()
                    print(f'Sound {name} played')
            else:
                print(f'Sound {name} not found')
            self.is_sound_on = True
        except pygame.error as e:
            print(f"Couldn't play sound: {e}")


# Music manager
class MusicManager:
    def __init__(self):
        # Volume
        self.volume = 0.5
        self.set_volume(self.volume)

        # Flag
        self.is_music_on = False

    # Set volume
    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)

    # Play song
    def play_song(self, path):
        try:
            if self.is_music_on:
                self.stop_music()
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)
            self.is_music_on = True
        except pygame.error as e:
            print(f"Couldn't play song: {e}")

    # Stop song
    def stop_music(self):
        pygame.mixer.music.stop()
        self.is_music_on = False






