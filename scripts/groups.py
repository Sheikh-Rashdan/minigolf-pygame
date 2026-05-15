from scripts.settings import *


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # values
        self.display = pygame.display.get_surface()

    def draw(self):

        for sprite in sorted(self, key = lambda sprite: sprite.z):
            self.display.blit(sprite.image, sprite.rect)