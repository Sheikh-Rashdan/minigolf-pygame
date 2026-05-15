from scripts.settings import *
from math import cos

def get_text_surf(text, depth, font):
    text_surfs = (font.render(text, True, 'white'), font.render(text, True, 'gray85'))
    surf = pygame.Surface((text_surfs[0].get_width(),text_surfs[0].get_height()+depth), pygame.SRCALPHA)
    for y in range(1,depth+1):
        surf.blit(text_surfs[1], (0,y))
    surf.blit(text_surfs[0], (0,0))
    return surf


class Button(pygame.sprite.Sprite):
    def __init__(self, groups, pos, size, text = 'Button', font = None, command = None, ratio = 5/6, strength = 0.1, depth = 2, y_offset = 2, place = 'topleft', parent = None):
        super().__init__(groups)

        # general values
        self.parent = parent
        self.size = pygame.Vector2(size)
        self.hovering = False
        self.z = Z['UI']

        # press values
        self.pressed = False
        self.command = command
        self.strength = strength
        self.ratio = ratio
        self.y = 0

        # surf
        font = font if font else pygame.Font(pygame.font.get_default_font())
        self.text = text
        self.text_surf = get_text_surf(text, depth, font)
        self.text_size = pygame.Vector2(self.text_surf.get_size())
        self.y_offset = y_offset

        # main
        self.update_surf()
        self.rect = self.image.get_frect()
        setattr(self.rect, place, pos)

        # controls
        self.old_mouse_pressed = pygame.mouse.get_pressed()

    def update_surf(self):

        surf = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.rect(surf, 'gray75', ((0,self.y),self.size))
        pygame.draw.rect(surf, 'gray55', ((0,self.y+self.size.y*self.ratio),self.size))

        surf.blit(self.text_surf, ((self.size.x-self.text_size.x)/2,(self.size.y*self.ratio-self.text_size.y)/2+self.y+self.y_offset))

        self.image = surf

    def input(self):

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        self.hovering = self.rect.collidepoint(mouse_pos)

        if self.hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        if not self.old_mouse_pressed[0] and mouse_pressed[0] and self.hovering:
            self.y = self.size.y*self.strength
            self.update_surf()
            self.pressed = True
            self.parent.parent.assets['sounds']['click'].play()
        elif self.pressed and self.old_mouse_pressed[0] and not mouse_pressed[0]:
            self.y = 0
            self.pressed = False
            if self.command:
                self.command()
            self.update_surf()

        self.old_mouse_pressed = mouse_pressed

    def update(self, _):

        self.input()

class Text(pygame.sprite.Sprite):
    def __init__(self, groups, pos, text = 'Text', depth = 2, font = None, place = 'topleft', wave = None):
        super().__init__(groups)

        # values
        font = font if font else pygame.Font(pygame.font.get_default_font())
        self.wave = wave
        self.wave_angle = 0
        self.z = Z['UI']

        # reset
        self.place, self.pos = place, pos

        self.image = get_text_surf(text, depth, font)
        self.rect = self.image.get_frect()
        setattr(self.rect, self.place, self.pos)

    def reset_pos(self):

        setattr(self.rect, self.place, self.pos)
        self.wave_angle = 0

    def update(self, dt):

        if self.wave and dt < 10:
            self.wave_angle += self.wave
            self.rect.y += 0.02 * cos(self.wave_angle*0.01) * dt