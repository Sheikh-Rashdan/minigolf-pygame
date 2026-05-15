import pygame
import os
import sys

def get_path(relative_path):
    BASE_PATH = os.path.abspath(os.path.dirname('\\'.join(__file__.split('\\')[:-1])))
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, os.path.join(BASE_PATH, relative_path))
    return os.path.join(BASE_PATH, relative_path)

# dimensions
WIDTH,HEIGHT = 900,650
BG_TILE_SIZE = 50

# colors
BG = '#B5E61D'
TILE = ('#A6D616', '#9ECC15')
TERRAIN = ('#e7f20a', '#416bf2', '#b42ded', '#ed5d2d', '#ed2f72', 'white')

# editor
EDITOR_ITEMS = {
    0: 'player',
    1: 'hole',
    2: 'terrain'
}

# LAYERS
Z = {
    'BG': 0,
    'MAIN': 1,
    'FG': 2,
    'UI': 3,
}