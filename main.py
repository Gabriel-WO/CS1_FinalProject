# Final Project Main File
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '5.22.2025'

import pygame
import sys
from magic import Magic
from player import Player, PLAYER_TYPES
from party import PlayerParty, EnemyParty
from explorer import Explorer
from room_factory import RoomFactory
from background import BackgroundManager
from sound import SoundManager, MusicManager, SOUND_EFFECTS, MUSIC

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_COLOR = (200, 200, 200) # light gray
BUTTON_HOVER_COLOR = (150, 150, 150) # dark gray

# Game states
STATE_MENU = 0
STATE_CHARACTER_SELECT = 1
STATE_EXPLORING = 2
STATE_PLAYER_TURN = 3
STATE_ENEMY_TURN = 4
STATE_BATTLE_ANIMATION = 5
STATE_WIN = 6
STATE_GAME_OVER = 7
STATE_FINISHED = 8

# Black magic
fire = Magic('Fire', 5, 7, 'black')
thunder = Magic('Thunder', 5, 7, 'black')
blizzard = Magic('Blizzard', 5, 7, 'black')

# White magic
cure = Magic('Cure', 5, 5, 'white')
cura = Magic('Cura', 10, 10, 'white')
curaga = Magic('Curaga', 20, 20, 'white')

# Game class
class TurnBasedRPG:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Turn Based')
        self.game_state = STATE_MENU

        # Create font objects
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)

        # Managing actions
        self.current_actor_index = 0
        self.selected_actions = []
        self.action_menu_state = 'main'

        # Rooms
        self.rooms = RoomFactory.load_rooms()
        self.current_room = self.rooms['woods']

        # Exploration
        self.player_party = PlayerParty()
        self.explorer = Explorer(self.player_party)
        self.explorer.rect_x = self.current_room.player_start_x
        self.explorer.rect_y = self.current_room.player_start_y

        # Initialize game
        self.background_manager = BackgroundManager(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.sound_manager = SoundManager()
        self.music_manager = MusicManager()
        self.selected_characters = []
        self.reset_game()
        self.clock = pygame.time.Clock()
        self.win_count = 0
        self.is_final_boss = False

    # Reset game
    def reset_game(self):
        # Party creation
        self.selected_characters = []
        self.game_state = STATE_CHARACTER_SELECT
        self.music_manager.stop_music()

        # Managing actions
        self.current_actor_index = 0
        self.selected_actions = []
        self.action_menu_state = 'main'

        # Rooms
        self.rooms = RoomFactory.load_rooms()
        self.current_room = self.rooms['woods']

        # Exploration
        self.player_party = PlayerParty()
        self.explorer = Explorer(self.player_party)
        self.explorer.rect_x = self.current_room.player_start_x
        self.explorer.rect_y = self.current_room.player_start_y

        # Win counter
        self.win_count = 0
        self.is_final_boss = False

    # Exploration handling
    def handle_exploration_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.explorer.change_speed(-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.explorer.change_speed(1, 0)
            elif event.key == pygame.K_UP:
                self.explorer.change_speed(0, -1)
            elif event.key == pygame.K_DOWN:
                self.explorer.change_speed(0, 1)
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                self.explorer.change_speed(0, 0)

    # Draw exploration
    def draw_exploration(self):
        self.screen.blit(self.current_room.background, (0, 0))
        if self.win_count < 10:
            self.draw_text(None, f'Wins: {str(self.win_count).upper()}/10', 25, 25, (255, 255, 255))
        else:
            self.draw_text(None, 'Kill the boss!', 25, 25, (255, 255, 255))

        # Draw explorer
        if self.explorer:
            self.screen.blit(self.explorer.image, (self.explorer.rect_x, self.explorer.rect_y))

    # Player positioning in a row
    def get_player_position(self, index):
        x = SCREEN_WIDTH - 150
        y = 150 + (index * 120)
        return x, y, 80, 100 # x, y, width, height

    # Enemy positioning in a row
    def get_enemy_position(self, index):
        x = 100
        y = 150 + (index * 120)
        return x, y, 80, 100

    # Enemy encounters
    def encounter_enemies(self, encounter_type = None):
        # Generate enemy party
        for room_name, room in self.rooms.items():
            if room == self.current_room:
                if room_name == 'woods':
                    encounter_type = 'woods_enemies'
                elif room_name == 'mountains':
                    encounter_type = 'mountains_enemies'
                elif room_name == 'dungeon':
                    encounter_type = 'dungeon_enemies'
                break

        # Final boss if already in dungeon
        if room_name == 'dungeon' and self.win_count >= 10:
            self.enemy_party = EnemyParty().generate_final_boss()
            self.is_final_boss = True
        # Anything else
        else:
            self.enemy_party = EnemyParty().generate_random_party(encounter_type)
        self.game_state = STATE_PLAYER_TURN

        # Reset player positions for battle
        for i, player in enumerate(self.player_party.members):
            player_x, player_y, width, height = self.get_player_position(i)
            player.set_position(player_x, player_y, width, height)

        # Background
        combat_background = 'woods_combat'
        if not hasattr(self, 'background_manager'):
            self.background_manager = BackgroundManager(SCREEN_WIDTH, SCREEN_HEIGHT)
        for room_name, room in self.rooms.items():
            if room == self.current_room:
                if room_name == 'woods':
                    combat_background = 'woods_combat'
                elif room_name == 'mountains':
                    combat_background = 'mountains_combat'
                elif room_name == 'dungeon':
                    combat_background = 'dungeon_combat'
                break
        self.background_manager.set_background(combat_background)

        # Play music
        if room_name == 'woods':
            self.music_manager.play_song(MUSIC['battle_woods'])
        elif room_name == 'mountains':
            self.music_manager.play_song(MUSIC['battle_mountains'])
        elif room_name == 'dungeon' and self.win_count >= 10:
            self.music_manager.play_song(MUSIC['battle_boss'])
        elif room_name == 'dungeon' and self.win_count < 10:
            self.music_manager.play_song(MUSIC['battle_dungeon'])

    # Win battle
    def win_battle(self):
        if self.is_final_boss:
            self.game_state = STATE_FINISHED
            self.music_manager.play_song(MUSIC['victory'])
        else:
            self.game_state = STATE_WIN
            self.music_manager.play_song(MUSIC['victory'])
            self.win_count += 1

    # Draw text
    def draw_text(self, font, text, x, y, color=None):
        self.screen.blit(self.font.render(text, True, color), (x, y))

    # Draw win state
    def draw_win_state(self):
        self.screen.fill((0, 0, 0))
        '''enemies = self.enemy_party.members
        enemies_defeated = []
        for enemy in enemies:
            name = enemy.name
            enemies_defeated.append(name)
        enemies_defeated_text = ', '.join(enemies_defeated)'''
        self.draw_text(None, 'YOU WIN!', SCREEN_WIDTH // 2 - 50, 100, (255, 255, 255))
        #self.draw_text(None, f'Enemies defeated: {enemies_defeated_text}', 50, SCREEN_HEIGHT - 300, (255, 255, 255))
        self.draw_button('Continue', SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 100, 100, 50, BUTTON_COLOR)

    # Handle win state
    def handle_win_click(self, mouse_pos):
        x = SCREEN_WIDTH // 2 - 50
        y = SCREEN_HEIGHT - 100
        width = 100
        height = 50
        if self.check_button_click(mouse_pos, x, y, width, height):
            self.game_state = STATE_EXPLORING

            # Music
            for room_name, room in self.rooms.items():
                if room == self.current_room:
                    if room_name == 'woods':
                        self.music_manager.play_song(MUSIC['woods'])
                    elif room_name == 'mountains':
                        self.music_manager.play_song(MUSIC['mountains'])
                    elif room_name == 'dungeon':
                        self.music_manager.play_song(MUSIC['dungeon'])
                    break

            self.explorer.change_speed(0, 0)
            self.battle_animation_queue = []

    # Game over
    def lose_battle(self):
        self.game_state = STATE_GAME_OVER
        self.music_manager.play_song(MUSIC['game_over'])

    # Draw game over
    def draw_game_over_state(self):
        self.screen.fill((0, 0, 0))
        self.draw_text(None, 'GAME OVER', SCREEN_WIDTH // 2 - 75, 100, (255, 255, 255))
        self.draw_text(None, 'Press the button to reset the game', SCREEN_WIDTH // 2 - 200, 300, (255, 255, 255))
        self.draw_button('Reset', SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 100, 100, 50, BUTTON_COLOR)

    # Handle game over click
    def handle_game_over_click(self, mouse_pos):
        x = SCREEN_WIDTH // 2 - 50
        y = SCREEN_HEIGHT - 100
        width = 100
        height = 50
        if self.check_button_click(mouse_pos, x, y, width, height):
            self.reset_game()

    # Handle player choices
    def handle_player_turn(self):

        # Check if lost
        if all(player.stats['hp'] <= 0 for player in self.player_party.members) or len(self.player_party.members) == 0:
            self.lose_battle()

        # Check for dead players
        for player in self.player_party.members:
            if player.stats['hp'] <= 0:
                player.kill()
                self.player_party.members.remove(player)

        current_actor = self.player_party.members[self.current_actor_index]

        # Draw character's name
        name_text = self.font.render(f"{current_actor.name}'s turn", True, (255, 255, 255))
        self.screen.blit(name_text, (50, 400))

        # Draw buttons
        if self.action_menu_state == 'main':
            self.draw_main_action_buttons()
        elif self.action_menu_state == 'magic':
            self.draw_magic_buttons(current_actor)
        elif self.action_menu_state == 'target_select':
            self.draw_target_selection()

    # Prepare battle animations
    def prepare_battle_animations(self, actions):
        if not hasattr(self, 'battle_animation_queue'):
            self.battle_animation_queue = []

        self.battle_animation_queue.extend(actions)
        self.current_animation_index = 0
        self.animation_timer = 0
        if self.game_state == STATE_PLAYER_TURN:
            self.game_state = STATE_ENEMY_TURN
        else:
            self.game_state = STATE_BATTLE_ANIMATION

    # Battle animations
    def update_battle_animations(self):
        # Check queue
        if not self.battle_animation_queue:
            self.game_state = STATE_PLAYER_TURN
            self.current_actor_index = 0
            return

        # Get action
        current_action = self.battle_animation_queue[self.current_animation_index]
        actor = current_action['actor']

        # Check if this is a new animation
        is_new_animation = False
        if not hasattr(self, 'last_animation_index') or self.last_animation_index != self.current_animation_index:
            is_new_animation = True
            self.last_animation_index = self.current_animation_index

        # Animate and sound effects
        if hasattr(actor, 'animator'):
            if current_action['type'] == 'attack':
                actor.image = actor.animator.update('attack')
                if is_new_animation:
                    self.sound_manager.play_sound('attack')
            elif current_action['type'] == 'magic':
                actor.image = actor.animator.update('cast')
                if is_new_animation:
                    spell = current_action['spell']
                    if spell.name.lower() == 'fire':
                        self.sound_manager.play_sound('fire')
                    elif spell.name.lower() == 'thunder':
                        self.sound_manager.play_sound('thunder')
                    elif spell.name.lower() == 'blizzard':
                        self.sound_manager.play_sound('blizzard')
                    elif spell.name.lower() == 'cure' or spell.name.lower() == 'cura' or spell.name.lower() == 'curaga':
                        self.sound_manager.play_sound('heal')
            elif current_action['type'] == 'defend':
                actor.image = actor.animator.update('defend')
            else:
                actor.image = actor.animator.update('idle')

        if hasattr(actor, 'animator') and actor.animator.is_animation_complete():
            actor.image = actor.animator.update('idle')
            self.current_animation_index += 1
            if self.current_animation_index >= len(self.battle_animation_queue):
                self.battle_animation_queue = []
                self.game_state = STATE_PLAYER_TURN
                self.current_actor_index = 0
                self.last_animation_index = None
                return

    # Draw main action buttons
    def draw_main_action_buttons(self):
        self.draw_button("Attack", 50, 450, 100, 40)
        self.draw_button("Magic", 160, 450, 100, 40)
        self.draw_button("Defend", 270, 450, 100, 40)

    # Draw magic action buttons
    def draw_magic_buttons(self, actor):
        # Back button
        self.draw_button('Back', 50, 450, 100, 40)

        # Draw button for each spell character has
        y_pos = 450
        for i, spell in enumerate(actor.magic):
            can_cast = actor.stats['mp'] >= spell.cost
            color = BUTTON_COLOR if can_cast else (100, 100, 100)
            self.draw_button(f"{spell.name} ({spell.cost} MP)", 160, y_pos, 200, 40, color)
            y_pos += 45

    # Hitboxes
    def draw_target_hitboxes(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.current_action['type'] == 'attack' or (self.current_action['type'] == 'magic' and self.current_action['spell'].type) == 'black':
            targets = [(i, enemy, self.get_enemy_position(i)) for i, enemy in enumerate(self.enemy_party.members) if enemy.stats['hp'] > 0]
        elif self.current_action['type'] == 'magic' and self.current_action['spell'].type == 'white':
            targets = [(i, ally, self.get_player_position(i)) for i, ally in enumerate(self.player_party.members) if ally.stats['hp'] > 0]
        else:
            targets = []

        # Draw hitboxes
        for i, target, (x, y, width, height) in targets:
            hitbox_x = x - 20
            hitbox_y = y - 20
            hitbox_width = width + 40
            hitbox_height = height + 40

            is_hovering = hitbox_x <= mouse_pos[0] <= hitbox_x + hitbox_width and hitbox_y <= mouse_pos[1] <= hitbox_y + hitbox_height
            hitbox_surface = pygame.Surface((hitbox_width, hitbox_height), pygame.SRCALPHA)
            if is_hovering:
                pygame.draw.rect(hitbox_surface, (255, 255, 0, 80), (0, 0, hitbox_width, hitbox_height))
                pygame.draw.rect(hitbox_surface, (255, 255, 0, 180), (0, 0, hitbox_width, hitbox_height), 3)
            else:
                pygame.draw.rect(hitbox_surface, (200, 200, 200, 30), (0, 0, hitbox_width, hitbox_height))
            self.screen.blit(hitbox_surface, (hitbox_x, hitbox_y))

    # Handle button clicks
    def handle_button_click(self, mouse_pos):
        if self.game_state != STATE_PLAYER_TURN:
            return

        current_actor = self.player_party.members[self.current_actor_index]

        # Main state
        if self.action_menu_state == 'main':
            # Attack button
            if self.check_button_click(mouse_pos, 50, 450, 100, 40):
                self.action_menu_state = 'target_select'
                self.current_action = {'type': 'attack'}

            # Magic button
            elif self.check_button_click(mouse_pos, 160, 450, 100, 40):
                self.action_menu_state = 'magic'

            # Defend button
            elif self.check_button_click(mouse_pos, 270, 450, 100, 40):
                self.register_action({'type': 'defend'})

        # Magic state
        elif self.action_menu_state == 'magic':
            # Back button
            if self.check_button_click(mouse_pos, 50, 450, 100, 40):
                self.action_menu_state = 'main'
                return

            # Check spell buttons
            y_pos = 450
            for i, spell in enumerate(current_actor.magic):
                if self.check_button_click(mouse_pos, 160, y_pos, 200, 40):
                    if current_actor.stats['mp'] >= spell.cost:
                        self.action_menu_state = 'target_select'
                        self.current_action = {'type': 'magic', 'spell': spell}
                    break
                y_pos += 45

        # Targeting state
        elif self.action_menu_state == 'target_select':
            # Back button
            if self.check_button_click(mouse_pos, 50, 520, 100, 40):
                if self.current_action['type'] == 'magic':
                    self.action_menu_state = 'magic'
                else:
                    self.action_menu_state = 'main'
                return

            # Handle targeting
            if self.current_action['type'] == 'attack' or self.current_action['type'] == 'magic' and self.current_action['spell'].type == 'black':
                for i, enemy in enumerate(self.enemy_party.members):
                    if enemy.stats['hp'] <= 0:
                        continue
                    # Find enemy position
                    enemy_x, enemy_y, enemy_width, enemy_height = self.get_enemy_position(i)

                    # Create hitbox
                    hitbox_x = enemy_x - 20
                    hitbox_y = enemy_y - 20
                    hitbox_width = enemy_width + 40
                    hitbox_height = enemy_height + 40

                    if self.check_button_click(mouse_pos, hitbox_x, hitbox_y, hitbox_width, hitbox_height):
                        self.current_action['target'] = enemy
                        self.register_action(self.current_action)
                        return
            elif self.current_action['type'] == 'magic' and self.current_action['spell'].type == 'white':
                for i, ally in enumerate(self.player_party.members):
                    if ally.stats['hp'] <= 0:
                        continue
                    ally_x, ally_y, ally_width, ally_height = self.get_player_position(i)

                    # Create hitbox
                    hitbox_x = ally_x - 20
                    hitbox_y = ally_y - 20
                    hitbox_width = ally_width + 40
                    hitbox_height = ally_height + 40

                    if self.check_button_click(mouse_pos, hitbox_x, hitbox_y, hitbox_width, hitbox_height):
                    #if self.check_button_click(mouse_pos, ally_x, ally_y, ally_width, ally_height):
                        self.current_action['target'] = ally
                        self.register_action(self.current_action)
                        return

    # Draw target selection
    def draw_target_selection(self):
        # Attack
        if self.current_action['type'] == 'attack':
            prompt = 'Select an enemy to attack'

        # Magic
        elif self.current_action['type'] == 'magic':
            spell = self.current_action['spell']

            # Black magic
            if spell.type == 'black':
                prompt = f'Select an enemy for {spell.name}'

            # White magic
            else:
                prompt = f'Select an ally for {spell.name}'

        # Rendering
        prompt_text = self.font.render(prompt, True, (255, 255, 255))
        self.screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, 50))
        self.draw_target_hitboxes()

        # Back button
        self.draw_button('Back', 50, 520, 100, 40)

    # Process actions
    def register_action(self, action):
        current_actor = self.player_party.members[self.current_actor_index]
        self.selected_actions.append((current_actor,action))

        # Move to next character and reset
        self.current_actor_index += 1
        self.action_menu_state = 'main'

        # If action selection is done move to enemy's turn
        if self.current_actor_index >= len(self.player_party.members):
            self.execute_player_actions()
            self.game_state = STATE_ENEMY_TURN
            self.current_actor_index = 0
            self.selected_actions = []

    # Execute commands
    def execute_player_actions(self):
        battle_animations = []
        for actor, action in self.selected_actions:
            animation_data = {
                'actor': actor,
                'type': action['type'],
                'target': action.get('target')
            }

            # Attack
            if action['type'] == 'attack':
                target = action['target']
                damage = actor.attack()
                target.take_physical_damage(damage)
                animation_data['damage'] = damage

            # Cast spell and reduce mp
            elif action['type'] == 'magic':
                spell = action['spell']
                target = action['target']
                actor.reduce_mp(spell.cost)
                if spell.type == 'black':
                    damage = actor.cast(spell)
                    target.take_magical_damage(damage)
                    animation_data['damage'] = damage
                    animation_data['spell'] = spell
                elif spell.type == 'white':
                    damage = actor.cast(spell)
                    target.heal(damage)
                    animation_data['damage'] = damage
                    animation_data['spell'] = spell

            # Defend
            elif action['type'] == 'defend':
                actor.defend()

            battle_animations.append(animation_data)

        self.prepare_battle_animations(battle_animations)

    # Process enemy actions
    def handle_enemy_actions(self, player_party, enemy_party):
        enemy_party.members = [enemy for enemy in enemy_party.members if enemy.stats['hp'] > 0]
        if len(enemy_party.members) == 0:
            self.win_battle()
            return

        enemy_actions = enemy_party.choose_actions(player_party)
        for actor, action in enemy_actions:

            # Attack
            if action['type'] == 'attack':
                target = action['target']
                damage = actor.attack()
                target.take_physical_damage(damage)

            # Casting
            elif action['type'] == 'magic':
                spell = action['spell']
                target = action['target']
                actor.reduce_mp(spell.cost)
                if spell.type == 'black':
                    damage = actor.cast(spell)
                    target.take_magical_damage(damage)
                elif spell.type == 'white':
                    damage = actor.cast(spell)
                    target.heal(damage)

        # Player's turn
        if all(player.stats['hp'] <= 0 for player in self.player_party.members):
            self.lose_battle()
            return

        self.game_state = STATE_BATTLE_ANIMATION
        self.current_actor_index = 0

    # Draw buttons
    def draw_button(self, text, x, y, width, height, color=None):
        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse is over button
        if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR, (x, y, width, height))
        else:
            pygame.draw.rect(self.screen, BUTTON_COLOR, (x, y, width, height))

        # Add text
        text_surf = self.small_font.render(text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surf, text_rect)

    # Check for click
    def check_button_click(self, mouse_pos, x, y, width, height):
        return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

    # Draw battle scene
    def draw_battle_scene(self):

        # Draw background
        if hasattr(self, 'background_manager'):
            self.background_manager.draw(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.background_manager.update()
        else:
            self.screen.fill((50, 50, 100))

        # Draw players
        for i, player in enumerate(self.player_party.members):
            player_x, player_y, width, height = player.get_position()

            # Update player image
            try:
                if self.game_state != STATE_BATTLE_ANIMATION or player not in [action['actor'] for action in self.battle_animation_queue]:
                    player_image = player.animator.update('idle')
                    scaled_image = pygame.transform.scale(player_image, (width, height))
                    self.screen.blit(scaled_image, (player_x, player_y))
                else:
                    original_image = player.image
                    scaled_image = pygame.transform.scale(original_image, (width, height))
                    self.screen.blit(scaled_image, (player_x, player_y))
            except pygame.error as e:
                print(f'Error drawing {player.name}: {e}')
                color = (0, 0, 255) if player.stats['hp'] > 0 else (100, 100, 100)
                pygame.draw.rect(self.screen, color, (player_x, player_y, width, height))

            # Draw player name
            name_text = self.small_font.render(player.name, True, (255, 255, 255))
            self.screen.blit(name_text, (player_x, player_y + height - 12))

            # Draw HP/MP bars
            hp_percent = player.stats['hp'] / player.stats['max_hp']
            mp_percent = player.stats['mp'] / player.stats['max_mp']

            # HP bar (red background, green foreground)
            pygame.draw.rect(self.screen, (255, 0, 0), (player_x, player_y + height + 5, width, 10))
            pygame.draw.rect(self.screen, (0, 255, 0), (player_x, player_y + height + 5, int(width * hp_percent), 10))

            # MP bar (black background, blue foreground)
            pygame.draw.rect(self.screen, (0, 0, 0), (player_x, player_y + height + 20, width, 10))
            pygame.draw.rect(self.screen, (0, 0, 255), (player_x, player_y + height + 20, int(width * mp_percent), 10))

        # Draw enemies
        for i, enemy in enumerate(self.enemy_party.members):
            enemy_x, enemy_y, width, height = self.get_enemy_position(i)

            # Image
            try:
                enemy_image = enemy.image
                scaled_image = pygame.transform.scale(enemy_image, (width, height))
                self.screen.blit(scaled_image, (enemy_x, enemy_y))
            except pygame.error as e:
                print(f'Error drawing {enemy.name}: {e}')
                color = (0, 0, 255) if enemy.stats['hp'] > 0 else (100, 100, 100)
                pygame.draw.rect(self.screen, color, (enemy_x, enemy_y, width, height))

            # Draw enemy name
            name_text = self.small_font.render(enemy.name, True, (255, 255, 255))
            self.screen.blit(name_text, (enemy_x, enemy_y + height - 12))

            # Draw HP bar only if enemy is alive
            if enemy.stats['hp'] > 0:
                hp_percent = enemy.stats['hp'] / enemy.stats['max_hp']
                pygame.draw.rect(self.screen, (255, 0, 0), (enemy_x, enemy_y + height + 5, width, 10))
                pygame.draw.rect(self.screen, (0, 255, 0), (enemy_x, enemy_y + height + 5, int(width * hp_percent), 10))

        # If it's player's turn, draw whose turn it is
        if self.game_state == STATE_PLAYER_TURN and self.current_actor_index < len(self.player_party.members):
            current_actor = self.player_party.members[self.current_actor_index]
            turn_text = self.font.render(f"{current_actor.name}'s Turn", True, (255, 255, 0))
            self.screen.blit(turn_text, (SCREEN_WIDTH // 2 - turn_text.get_width() // 2, 10))

    # Draw character selection
    def draw_character_selection(self):
        # Title
        title_text = self.font.render('Choose your party members', True, (255, 255, 255))
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Character types
        character_types = ['warrior', 'mage', 'priest']
        selected_count = len(self.selected_characters)

        # Show how many have been selected
        count_text = self.small_font.render(f"Selected: {selected_count}/3", True, (255, 255, 255))
        self.screen.blit(count_text, (SCREEN_WIDTH - 150, 20))

        # Draw character options
        for i, char_type in enumerate(character_types):
            x = 150 + (i * 200)
            y = 150
            width = 150
            height = 200

            # Highlight if selected
            is_selected = char_type in self.selected_characters
            color = (100, 200, 100) if is_selected else BUTTON_COLOR

            # Draw character box
            pygame.draw.rect(self.screen, color, (x, y, width, height))

            # Draw character name
            name_text = self.font.render(char_type.capitalize(), True, (0, 0, 0))
            self.screen.blit(name_text, (x + width // 2 - name_text.get_width() // 2, y + 20))

            # Draw character stats
            stats = PLAYER_TYPES[char_type]
            stat_y = y + 60
            for stat_name in ['max_hp', 'max_mp', 'physical_damage', 'magical_damage']:
                if stat_name == 'max_hp':
                    stat_text = self.small_font.render(f'HP: {stats[stat_name]}', True, (0, 0, 0))
                elif stat_name == 'max_mp':
                    stat_text = self.small_font.render(f'MP: {stats[stat_name]}', True, (0, 0, 0))
                elif stat_name == 'physical_damage':
                    stat_text = self.small_font.render(f'Strength: {stats[stat_name]}', True, (0, 0, 0))
                elif stat_name == 'magical_damage':
                    stat_text = self.small_font.render(f'Magic: {stats[stat_name]}', True, (0, 0, 0))
                self.screen.blit(stat_text, (x + 10, stat_y))
                stat_y += 25

        # Draw "Start Game" button if at least one character is selected
        if selected_count > 0:
            self.draw_button("Start Game", SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 100, 150, 50)

    # Handle character selection button clicks
    def handle_character_selection_click(self, mouse_pos):
        character_types = ['warrior', 'mage', 'priest']

        # Check character boxes
        for i, char_type in enumerate(character_types):
            x = 150 + (i * 200)
            y = 150
            width = 150
            height = 200

            if self.check_button_click(mouse_pos, x, y, width, height):
                # Toggle selection
                if char_type in self.selected_characters:
                    self.selected_characters.remove(char_type)
                elif len(self.selected_characters) < 3:
                    self.selected_characters.append(char_type)
                return

        # Check "Start Game" button if at least one character is selected
        if len(self.selected_characters) > 0:
            if self.check_button_click(mouse_pos, SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 100, 150, 50):
                self.create_player_party()
                self.game_state = STATE_EXPLORING
                self.music_manager.play_song(MUSIC['woods'])

    # Create player party
    def create_player_party(self):
        self.player_party = PlayerParty()

        for i, char_type in enumerate(self.selected_characters):
            name = f'{char_type.capitalize()}'
            player = Player(name, char_type)
            self.player_party.add_member(player)

        # Create explorer
        self.explorer = Explorer(self.player_party)
        self.explorer.rect_x = self.current_room.player_start_x
        self.explorer.rect_y = self.current_room.player_start_y
        self.explorer.x = float(self.current_room.player_start_x)
        self.explorer.y = float(self.current_room.player_start_y)

    # Draw everything
    def draw_game(self):
        mouse_pos = pygame.mouse.get_pos()

        # Player turn state during combat
        if self.game_state == STATE_PLAYER_TURN:
            self.handle_player_turn()

            # Hover effects
            if self.action_menu_state == 'main':
                if self.is_button_hovered(mouse_pos, 160, 450, 100, 40):
                    self.draw_magic_preview()
            elif self.action_menu_state == 'magic':
                current_actor = self.player_party.members[self.current_actor_index]
                y_pos = 450
                for spell in current_actor.magic:
                    if self.check_button_click(mouse_pos, 160, y_pos, 200, 40):
                        self.draw_spell_details(spell)
                        y_pos += 45

    # Button hovering
    def is_button_hovered(self, mouse_pos, x, y, width, height):
        return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

    # Magic details preview
    def draw_magic_preview(self):
        current_actor = self.player_party.members[self.current_actor_index]

        # Create preview surface
        preview_surface = pygame.Surface((200, 30 * len(current_actor.magic)))
        preview_surface.set_alpha(200)
        preview_surface.fill((50, 50, 50))
        self.screen.blit(preview_surface, (270, 250))

        # List spells
        for i, spell in enumerate(current_actor.magic):
            spell_text = self.small_font.render(spell.name, True, (255, 255, 255))
            self.screen.blit(spell_text, (280, 460 + i * 30))

    # Drawing spell details
    def draw_spell_details(self, spell):
        details_surface = pygame.Surface((300, 150))
        details_surface.set_alpha(230)
        details_surface.fill((30, 30, 60))
        self.screen.blit(details_surface, (400, 350))

        # Add spell details
        name_text = self.font.render(spell.name, True, (255, 255, 255))
        type_text = self.small_font.render(f"Type: {spell.type}", True, (255, 255, 255))
        power_text = self.small_font.render(f"Power: {spell.power}", True, (255, 255, 255))
        cost_text = self.small_font.render(f"MP Cost: {spell.cost}", True, (255, 255, 255))

        self.screen.blit(name_text, (420, 360))
        self.screen.blit(type_text, (420, 400))
        self.screen.blit(power_text, (420, 430))
        self.screen.blit(cost_text, (420, 460))

    # Draw finished state
    def draw_finished_state(self):
        self.screen.fill((0, 0, 0))
        self.draw_text(None, 'YOU FINISHED!', SCREEN_WIDTH // 2 - 100, 100, (255, 255, 255))
        self.draw_button('Play Again', SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 100, 100, 50, BUTTON_COLOR)

    # Handle finished state clicks
    def handle_finished_state(self, mouse_pos):
        x = SCREEN_WIDTH // 2 - 50
        y = SCREEN_HEIGHT - 100
        width = 100
        height = 50
        if self.check_button_click(mouse_pos, x, y, width, height):
            self.reset_game()

    # Update
    def update(self):
        self.explorer.update()

        # Room transitions
        destination = self.explorer.move(self.current_room)
        if destination:
            # Enemy encounters
            if destination in ['woods_enemies', 'mountains_enemies', 'dungeon_enemies']:
                self.encounter_enemies()
            else:
                if destination in self.rooms:
                    self.current_room = self.rooms[destination]

                    # Positioning
                    self.explorer.x = float(self.current_room.player_start_x)
                    self.explorer.y = float(self.current_room.player_start_y)
                    self.explorer.rect_x = self.current_room.player_start_x
                    self.explorer.rect_y = self.current_room.player_start_y

                    # Music
                    if destination == 'woods':
                        self.music_manager.play_song(MUSIC['woods'])
                    elif destination == 'mountains':
                        self.music_manager.play_song(MUSIC['mountains'])
                    elif destination == 'dungeon':
                        self.music_manager.play_song(MUSIC['dungeon'])
                else:
                    print(f"Warning: Room '{destination}' not found")

    # Main game loop
    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            # Clear screen
            self.screen.fill((0, 0, 0))

            # Game logic
            if self.game_state == STATE_MENU:
                # Draw menu screen
                pass

            elif self.game_state == STATE_CHARACTER_SELECT:
                self.draw_character_selection()

            elif self.game_state == STATE_EXPLORING:
                self.update()
                self.draw_exploration()

            elif self.game_state == STATE_PLAYER_TURN:
                self.draw_battle_scene()
                self.handle_player_turn()

            elif self.game_state == STATE_ENEMY_TURN:
                self.draw_battle_scene()
                self.handle_enemy_actions(self.player_party, self.enemy_party)

            elif self.game_state == STATE_BATTLE_ANIMATION:
                self.draw_battle_scene()
                self.update_battle_animations()

            elif self.game_state == STATE_WIN:
                self.draw_win_state()

            elif self.game_state == STATE_GAME_OVER:
                self.draw_game_over_state()

            elif self.game_state == STATE_FINISHED:
                self.draw_finished_state()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.game_state == STATE_CHARACTER_SELECT:
                        self.handle_character_selection_click(mouse_pos)

                    elif self.game_state == STATE_PLAYER_TURN:
                        self.handle_button_click(mouse_pos)

                    elif self.game_state == STATE_WIN:
                        self.handle_win_click(mouse_pos)

                    elif self.game_state == STATE_GAME_OVER:
                        self.handle_game_over_click(mouse_pos)

                    elif self.game_state == STATE_FINISHED:
                        self.handle_finished_state(mouse_pos)

                elif self.game_state == STATE_EXPLORING:
                    self.handle_exploration_input(event)

            # Update display
            pygame.display.flip()

            # Frame rate
            clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = TurnBasedRPG()
    game.run()


