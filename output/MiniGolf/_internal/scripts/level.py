from scripts.settings import *
from scripts.player import *
from scripts.sprites import *
from scripts.groups import *
from scripts.ui import *
import json

class Level:
    def __init__(self, name, parent, path = ('levels',)):

        # values
        self.display = pygame.display.get_surface()
        self.parent = parent
        self.path = join(*path,name)
        self.default_cursor = pygame.cursors.tri_left
        self.playing = True

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.Group()

        # ui
        Button((self.ui_sprites), (WIDTH-10,HEIGHT-10), (80,45), 'BACK', self.parent.assets['fonts']['button_s'], lambda: setattr(self.parent, 'mode', 'menu'), ratio = 5/6, place = 'bottomright', parent = self)
        Button((self.ui_sprites), (WIDTH-100,HEIGHT-10), (80,45), 'RESET', self.parent.assets['fonts']['button_s'], self.load_level, ratio = 5/6, place = 'bottomright', parent = self)

    def load_level(self):

        self.playing = True
        [sprite.kill() for sprite in self.all_sprites if sprite not in self.ui_sprites]

        try:
            with open(get_path(self.path), 'r') as f:
                self.level = json.load(f)

            for pos,size in self.level['terrain']:
                Terrain(pos, size, (self.all_sprites, self.collision_sprites))
            self.hole = Sprite(self.parent.assets['images']['hole'], self.level['hole'], self.all_sprites)
            self.player = Player(self.parent.assets['images']['player'], self.level['player'], self.all_sprites, self)
            flag = Sprite(self.parent.assets['images']['flag'], self.level['hole'], self.all_sprites, Z['FG'])
            flag.rect.midbottom = self.hole.rect.center
        except FileNotFoundError as e:
            print('Missing Files!')
            print(e)

    def manage_ui(self):
        
        if pygame.mouse.get_cursor() != self.default_cursor:
            if not any([sprite.hovering for sprite in self.ui_sprites if hasattr(sprite, 'hovering')]):
                pygame.mouse.set_cursor(self.default_cursor)

        buttons = [button for button in self.ui_sprites if hasattr(button, 'hovering')]
        for button in buttons:
            if pygame.Vector2(self.player.rect.center).distance_to(button.rect.center) >= 100:
                button.update(None)        # buttons dont require dt
                self.display.blit(button.image, button.rect)

    def update(self, dt):

        self.all_sprites.update(dt)
        self.all_sprites.draw()
        self.manage_ui()