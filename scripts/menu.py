from scripts.settings import *
from scripts.ui import *
from scripts.sprites import Sprite
from scripts.player import *
from scripts.support import *

class Menu:
    def __init__(self, parent):

        # values
        self.parent = parent
        self.display = pygame.display.get_surface()
        self.default_cursor = pygame.cursors.tri_left

        # fonts
        self.title_font = self.parent.assets['fonts']['title']
        self.credits_font = self.parent.assets['fonts']['button_s']
        self.button_font = self.parent.assets['fonts']['button_l']

        # groups
        self.all_sprites = pygame.sprite.Group()

        # title
        title_position = pygame.Vector2(WIDTH/2-42,80)
        title_offset = (85,100)
        mini_title = Text(self.all_sprites, title_position, 'mini', 12, self.title_font, 'center', 1)
        golf_title = Text(self.all_sprites, title_position+title_offset, 'golf', 12, self.title_font, 'center', 1)

        # credits
        Text(self.all_sprites, (15,HEIGHT-15), 'Made by Rashdan', 2, self.credits_font, 'bottomleft')

        # bg
        hole = Sprite(self.parent.assets['images']['hole'], (713,113), self.all_sprites)
        player = Sprite(self.parent.assets['images']['player'], (163,213), self.all_sprites)
        flag = Sprite(self.parent.assets['images']['flag'], pygame.Vector2(hole.rect.center) - (30,50), self.all_sprites)

        # buttons
        Button(self.all_sprites, (WIDTH/2,330), (300,75), 'Play', self.button_font, lambda: setattr(self.parent, 'mode', 'levels'), depth = 4, place = 'center', parent = self)
        Button(self.all_sprites, (WIDTH/2,415), (300,75), 'Custom', self.button_font, lambda: open_custom_level(self.parent), depth = 4, place = 'center', parent = self)
        Button(self.all_sprites, (WIDTH/2,500), (300,75), 'Editor', self.button_font, lambda: setattr(self.parent, 'mode', 'editor'), depth = 4, place = 'center', parent = self)
        Button(self.all_sprites, (WIDTH/2,585), (300,75), 'Exit', self.button_font, lambda: setattr(self.parent, 'running', False), depth = 4, place = 'center', parent = self)

    def update(self, dt):

        self.all_sprites.draw(self.display)
        self.all_sprites.update(dt)
        if pygame.mouse.get_cursor() != self.default_cursor:
            if not any([sprite.hovering for sprite in self.all_sprites if hasattr(sprite, 'hovering')]):
                pygame.mouse.set_cursor(self.default_cursor)