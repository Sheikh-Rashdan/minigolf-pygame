from scripts.settings import *
from random import choice
from math import sin, cos, radians


class Sprite(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups, z = Z['MAIN']):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.z = z


class Terrain(Sprite):
    def __init__(self, pos, size, groups):

        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(surf, choice(TERRAIN), ((0,0),size), 0, 3)
        pygame.draw.rect(surf, 'gray12', ((0,0),size), 3, 3)

        super().__init__(surf, pos, groups, Z['FG'])


class Arrow(Sprite):
    def __init__(self, pos, groups, player):

        # values
        self.player = player

        # surf
        self.o_image = pygame.Surface((240,240), pygame.SRCALPHA)
        self.empty_surf = pygame.Surface((1,1), pygame.SRCALPHA)

        # arc
        radius = 100
        arc_length = radians(60//2)
        color = 'black'
        pygame.draw.arc(self.o_image, color, (20,20,200,200), -arc_length, arc_length, 3)
        for n in (-1,1):
            x = 120 - radius * -cos(arc_length*n)
            y = 120 - radius * sin(arc_length*n)
            pygame.draw.line(self.o_image, color, (120,120), (x,y), 2)

        super().__init__(self.o_image.copy(), pos, groups)

    def draw_arrow(self):

        angle = self.player.arrow_direction.angle_to((1,0))
        surf = pygame.transform.rotozoom(self.o_image, angle, self.player.arrow_size/2)
        surf.set_alpha(200)
        self.image = surf

    def update(self, _):

        if self.player.grabbed:
            self.draw_arrow()
            self.rect = self.image.get_rect(center = self.player.rect.center)
        else:
            self.image = self.empty_surf

