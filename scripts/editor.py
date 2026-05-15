from scripts.settings import *
from scripts.sprites import *
from scripts.groups import *
from scripts.ui import *
from scripts.support import *
from os.path import exists, join
import json


class Editor:
    def __init__(self, parent):

        # values
        self.display = pygame.display.get_surface()
        self.parent = parent
        self.default_cursor = pygame.cursors.tri_left
        self._level_name = None
        self.editor_help = False

        # groups
        self.all_sprites = AllSprites()
        self.terrain_sprites = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.Group()
        
        # ui
        Text((self.all_sprites,self.ui_sprites), (15,HEIGHT-15), 'Press "H" for Help.', font = self.parent.assets['fonts']['button_s'], place = 'bottomleft', wave = 0.5)
        Button((self.all_sprites, self.ui_sprites), (WIDTH-10,HEIGHT-10), (80,45), 'BACK', self.parent.assets['fonts']['button_s'], lambda: setattr(self.parent, 'mode', 'menu'), ratio = 5/6, place = 'bottomright', parent = self)
        Button((self.all_sprites, self.ui_sprites), (WIDTH-100,HEIGHT-10), (80,45), 'RESET', self.parent.assets['fonts']['button_s'], self.reset, ratio = 5/6, place = 'bottomright', parent = self)
        Button((self.all_sprites, self.ui_sprites), (WIDTH-190,HEIGHT-10), (80,45), 'SAVE', self.parent.assets['fonts']['button_s'], lambda: save_custom_level(self), ratio = 5/6, place = 'bottomright', parent = self)
        self.editor_help_surf = self.parent.assets['images']['editor_help']

        # control
        self.selected = 0
        self.terrain_size = [50,50]
        self.terrain = []

    def input(self, dt):

        # get input
        self.mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        mouse_pressed = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        recent_keys = pygame.key.get_just_pressed()
        self.over_ui = any([sprite.hovering for sprite in self.ui_sprites if hasattr(sprite, 'hovering')])

        # how to play check
        if recent_keys[pygame.K_h]:
            self.editor_help = not self.editor_help

        # change selection
        if recent_keys[pygame.K_RIGHT]:
            self.selected += 1
        elif recent_keys[pygame.K_LEFT]:
            self.selected -= 1
        if not -1<self.selected<len(EDITOR_ITEMS):
            if self.selected == -1: self.selected = len(EDITOR_ITEMS)-1
            else: self.selected = 0

        # change terrain size
        if EDITOR_ITEMS[self.selected] == 'terrain' and not keys[pygame.K_LCTRL]:
            shift_multiplier = (0.1 if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else 0.5)
            self.terrain_size[0] += (int(keys[pygame.K_d]) - int(keys[pygame.K_a])) * dt * shift_multiplier
            self.terrain_size[1] += (int(keys[pygame.K_w]) - int(keys[pygame.K_s])) * dt * shift_multiplier
            self.terrain_size[0] = min(max(15, self.terrain_size[0]),WIDTH+100)
            self.terrain_size[1] = min(max(15, self.terrain_size[1]),HEIGHT+100)

        if not self.editor_help:
            # place
            if not self.over_ui:
                if mouse_pressed[0]:
                    if (name:=EDITOR_ITEMS[self.selected]) in ('player', 'hole'):
                        if hasattr(self, f'{name}_sprite'):
                            self.all_sprites.remove(getattr(self, f'{name}_sprite'))
                        surf = self.parent.assets['images'][name]
                        setattr(self, f'{name}_pos', self.mouse_pos - pygame.Vector2(surf.get_size())/2)
                        setattr(self, f'{name}_sprite', Sprite(surf, getattr(self, f'{name}_pos'), self.all_sprites))
                    elif not self.old_pressed[0]:
                        int_terrain_size = [int(x) for x in self.terrain_size]
                        pos = tuple(self.mouse_pos - pygame.Vector2(int_terrain_size)/2)
                        self.terrain.append((pos,tuple(int_terrain_size)))
                        Terrain(pos, int_terrain_size, (self.all_sprites, self.terrain_sprites))
                    
                # remove
                if EDITOR_ITEMS[self.selected] == 'terrain' and mouse_pressed[2]:
                    for sprite in self.terrain_sprites:
                        rect = (sprite.rect.topleft, sprite.rect.size) 
                        if sprite.rect.collidepoint(self.mouse_pos) and rect in self.terrain:
                            sprite.kill()
                            self.terrain.remove(rect)

        if keys[pygame.K_LCTRL] and recent_keys[pygame.K_s]:
            save_custom_level(self)

        self.old_pressed = mouse_pressed

    def preview(self):

        if not self.over_ui:
            if EDITOR_ITEMS[self.selected] in ('player', 'hole'):
                preview_surf = self.parent.assets['images'][EDITOR_ITEMS[self.selected]].copy()
            else:
                preview_surf = pygame.Surface(self.terrain_size, pygame.SRCALPHA)
                pygame.draw.rect(preview_surf, 'white', ((0,0),self.terrain_size), 0, 3)
                pygame.draw.rect(preview_surf, 'gray12', ((0,0),self.terrain_size), 3, 3)

            preview_surf.set_alpha(175)
            self.display.blit(preview_surf, self.mouse_pos-pygame.Vector2(preview_surf.get_size())/2)

    def reset(self):
        
        self.selected = 0
        self.terrain_size = [50,50]
        if hasattr(self, 'player_pos'): del self.player_pos
        if hasattr(self, 'hole_pos'): del self.hole_pos
        for sprite in self.all_sprites:
            if sprite not in self.ui_sprites:
                sprite.kill()
        self.terrain.clear()

    @property
    def level_name(self):
        return self._level_name

    @level_name.setter
    def level_name(self, level_name):

        self._level_name = level_name
        level = {'player': tuple(self.player_pos), 'hole': tuple(self.hole_pos), 'terrain': self.terrain}
        with open(get_path(join('levels','custom',self.level_name)), 'w') as f:
            json.dump(level, f)

        self.parent.mode = 'menu'
        self.reset()

    def check_level_criteria(self):

        return hasattr(self, 'player_pos') and hasattr(self, 'hole_pos')

    def update(self, dt):

        self.input(dt)
        self.all_sprites.draw()
        if self.editor_help: self.display.blit(self.editor_help_surf, (100,100))
        self.all_sprites.update(dt)
        self.preview()
        if pygame.mouse.get_cursor() != self.default_cursor:
            if not any([sprite.hovering for sprite in self.ui_sprites if hasattr(sprite, 'hovering')]):
                pygame.mouse.set_cursor(self.default_cursor)