from scripts.settings import *
from scripts.support import *
from scripts.sprites import Arrow
from random import choice, randint
from math import dist

class Player(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups, parent):
        super().__init__(groups)
        self.parent = parent

        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.z = Z['FG']

        # movement
        self.direction = pygame.Vector2()
        self.speed = 0

        # control
        self.grabbed = None
        self.old_mouse_pressed = pygame.mouse.get_pressed()
        self.arrow_direction = pygame.Vector2()
        self.arrow_size = 0
        self.arrow = Arrow(self.rect.center, self.parent.all_sprites, self)

        # timers
        self.timers = {'hole': Timer(700)}

    def input(self):

        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

        if not self.grabbed:
            if not self.direction:
                if mouse_pressed[0] and not self.old_mouse_pressed[0] and self.rect.collidepoint(mouse_pos):
                    self.grabbed = pygame.Vector2(mouse_pos)
                    self.parent.parent.assets['sounds']['charge'].play()
        else:
            direction = (self.grabbed - pygame.Vector2(mouse_pos))
            direction = direction.normalize() if direction else direction
            magnitude = self.grabbed.distance_to(mouse_pos)/100
            magnitude = min(magnitude, 2)
            if magnitude and not mouse_pressed[0] and self.old_mouse_pressed[0]:
                self.direction = direction
                spray = int(magnitude * 2.5)
                self.direction.rotate_ip(randint(-spray,spray))
                self.speed = magnitude
                self.grabbed = None
                self.parent.parent.assets['sounds']['swing'].play()
            else:
                self.arrow_direction = direction
                self.arrow_size = max(0.5, magnitude)

        self.old_mouse_pressed = mouse_pressed

    def move(self, dt):
        
        if self.speed:
            self.rect.x += self.direction.x * self.speed * dt
            self.collide('x')
            self.rect.y += self.direction.y * self.speed * dt
            self.collide('y')

            # friction
            self.speed -= self.speed/400

        if round(self.speed,2) <= 0 and self.parent.playing:
            self.speed = 0
            if self.direction:
                self.parent.parent.assets['sounds']['stop'].play()
            self.direction = pygame.Vector2()

    def collide(self, axis):

        collided = False

        # boundary
        if axis == 'x':
            if self.rect.right > WIDTH or self.rect.left < 0:
                if self.direction.x >  0: self.rect.right = WIDTH
                elif self.direction.x < 0: self.rect.left = 0
                self.direction.x *= -1
                collided = True
        else:
            if self.rect.bottom > HEIGHT or self.rect.top < 0:
                if self.direction.y > 0: self.rect.bottom = HEIGHT
                elif self.direction.y < 0: self.rect.top = 0
                self.direction.y *= -1
                collided = True


        # terrain
        for sprite in self.parent.collision_sprites:
            if self.rect.colliderect(sprite.rect):
                if axis == 'x':
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                        self.direction.x *= -1
                    elif self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1
                else:
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1
                    elif self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y *= -1
                collided = True
                break

        # colliding with hole
        if self.speed <= 1.5 and (distance:=dist(self.rect.center, self.parent.hole.rect.center))<15:
            if distance > 0.01:
                hole_direction = pygame.Vector2(self.parent.hole.rect.center) - pygame.Vector2(self.rect.center)
                self.direction = self.direction+hole_direction
                self.direction = self.direction.normalize() if self.direction else self.direction
            else:
                self.speed = 0
                self.direction = pygame.Vector2()
            if self.parent.playing:
                self.image = pygame.transform.scale_by(self.image, 0.75)
                self.rect = self.image.get_frect(center = self.rect.center)
                self.speed = 0.1 if self.speed < 0.1 else self.speed
                self.parent.playing = False
                self.parent.parent.assets['sounds']['hole'].play()
                self.timers['hole'].activate()

        # impact causes reduction in speed
        if collided:
            self.speed *= 3/4
            choice(self.parent.parent.assets['sounds']['collision']).play()

    def update_timers(self):

        for timer in self.timers.values():
            timer.update()

    def update(self, dt):

        self.update_timers()
        if self.parent.playing:
            self.input()
        else:
            if not self.timers['hole'].active:
                self.speed = 0
                self.parent.parent.next_level()
        self.move(dt)