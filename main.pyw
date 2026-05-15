from scripts.settings import *
from scripts.level import *
from scripts.editor import *
from scripts.menu import *
from scripts.support import *
from os import walk

class Game:
    def __init__(self):

        # setup
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('MiniGolf')
        self.running = True

        self.load_game()
        pygame.display.set_icon(self.assets['images']['icon'])

        self.menu = Menu(self)
        self.editor = Editor(self)

        self.levels = [Level(level_name, self) for level_name in list(walk(get_path('levels')))[0][-1]]
        self.custom_level = None
        self._mode = 'menu'
        self.current_level = 0

        self.assets['sounds']['music'].play(-1)

    @property
    def mode(self):
        return self._mode
    
    @mode.setter
    def mode(self, new_mode):
        self._mode = new_mode
        match new_mode:
            case 'levels':  self.levels[self.current_level].load_level()
            case 'custom': self.custom_level.load_level()

    def load_game(self):

        # tile
        tile_surf = pygame.Surface((50,50), pygame.SRCALPHA)
        pygame.draw.rect(tile_surf, TILE[0], (0,0,50,50), 0, 15)
        pygame.draw.rect(tile_surf, TILE[1], (8,8,34,34), 0, 10)

        # bg
        bg_surf = pygame.Surface((WIDTH,HEIGHT))
        bg_surf.fill(BG)
        for row in range(0,WIDTH//BG_TILE_SIZE):
            for col in range(0,HEIGHT//BG_TILE_SIZE):
                if row%2==col%2:
                    bg_surf.blit(tile_surf, (row*BG_TILE_SIZE,col*BG_TILE_SIZE))

        # shadow
        shadow_surf = pygame.Surface((20,8), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, 'black', (0,0,20,8))
        shadow_surf.set_alpha(100)

        # player
        player_surf = pygame.Surface((20,20), pygame.SRCALPHA)
        pygame.draw.circle(player_surf, 'gray12', (10,10), 10)
        pygame.draw.circle(player_surf, 'white', (10,10), 7)
        player_surf.blit(shadow_surf, (0,12))

        # hole
        hole_rim_surf = pygame.Surface((24,24), pygame.SRCALPHA)
        pygame.draw.ellipse(hole_rim_surf, 'black', (0,0,24,20))
        hole_rim_surf.set_alpha(100)
        hole_surf = pygame.Surface((24,24), pygame.SRCALPHA)
        hole_surf.blit(hole_rim_surf, (0,0))
        pygame.draw.ellipse(hole_surf, 'black', (0,4,24,20))

        # flag
        flag_surf = pygame.Surface((60,50), pygame.SRCALPHA)
        icon_surf = pygame.Surface((32,32), pygame.SRCALPHA)
        for surf in (icon_surf, flag_surf):
            pygame.draw.polygon(surf, '#fa2125', ((30,0), (0,12), (30,24)))
            pygame.draw.line(surf, 'black', (30,0), (30,42), 3)

        # load game assets
        self.assets = {
            'images': {
                'bg': bg_surf,
                'player': player_surf,
                'hole': hole_surf,
                'flag': flag_surf,
                'icon': icon_surf,
                'editor_help': load_image('assets', 'editor_help.png', alpha = False)
            },
            'sounds': {
                'collision': load_sounds('assets','sounds','collision'),
                'swing': load_sound('assets','sounds','swing.wav'),
                'charge': load_sound('assets','sounds','charge.wav'),
                'stop': load_sound('assets','sounds','stop.wav'),
                'hole': load_sound('assets','sounds','hole.wav'),
                'click': load_sound('assets','sounds','click.wav'),
                'music': load_sound('assets','sounds','music.mp3', volume = 0.1),
            },
            'fonts': {
                'button_s': pygame.font.Font(get_path(join('assets','fonts','ToonAround.ttf')), 32),
                'button_l': pygame.font.Font(get_path(join('assets','fonts','ToonAround.ttf')), 48),
                'title': pygame.font.Font(get_path(join('assets','fonts','ToonAround.ttf')), 120),
            },
        }

    def next_level(self):

        if self.mode == 'levels' and not self.current_level+1 >= len(self.levels):
            self.current_level += 1
            self.mode = 'levels'
        else:
            self.current_level = 0
            self.mode = 'menu'

    def load_custom_level(self, file_name):

        if file_name:
            self.custom_level = Level(file_name, self, ('levels','custom'))
            self.mode = 'custom'

    def run(self):

        # game loop
        while self.running:
            dt = self.clock.tick()              # delta time
            for event in pygame.event.get():        # event loop
                if event.type == pygame.QUIT:           # exit event
                    self.running = False

            # draw bg
            self.display.blit(self.assets['images']['bg'], (0,0))

            # update level
            match self.mode:
                case 'menu': self.menu.update(dt)
                case 'levels': self.levels[self.current_level].update(dt)
                case 'editor': self.editor.update(dt)
                case 'custom': self.custom_level.update(dt)

            # flip to display
            pygame.display.flip()

        pygame.quit()

    
if __name__ == '__main__':
    Game().run()