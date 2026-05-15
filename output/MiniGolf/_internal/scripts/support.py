from scripts.settings import *
from os import walk
from os.path import join
import customtkinter as ctk
from threading import Thread

class Timer:
    def __init__(self, duration, func = None, autostart = False, loop = False):

        self.duration = duration
        self.func = func
        self.loop = loop

        self.active = False
        self.start_time = 0

        if autostart:
            self.activate()

    def activate(self):
        
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):

        self.active = False
        self.start_time = 0
        if self.loop:
            self.activate()

    def update(self):

        if self.active:
            if pygame.time.get_ticks() >= self.start_time + self.duration:
                self.deactivate()
                if self.func:
                    self.func()


# load single image
def load_image(*path, alpha = True):

    path = join(*path)
    image = pygame.image.load(get_path(path))
    if alpha: image = image.convert_alpha()
    else: image = image.convert()

    return image


def load_sound(*path, volume = 1):

    path = join(*path)
    sound = pygame.mixer.Sound(get_path(path))
    sound.set_volume(volume)
    return sound

def load_sounds(*path):

    path = join(*path)
    sounds = []
    for file_name in list(walk(get_path(path)))[0][-1]:
        full_path = join(path, file_name)
        sounds.append(load_sound(full_path))
    return sounds


def multifunc(*args):
    for func in args:
        func()


def get_file(parent):

    window = ctk.CTk()
    window.title('Save Custom Level')
    window.geometry('300x300')
    window.resizable(False,False)

    def choose_file(file):
        file_name_var.set(file)
        window.destroy()

    files = list(walk(get_path(join('levels','custom'))))[0][-1]

    file_name_var = ctk.StringVar()
    file_name_dropdown = ctk.CTkScrollableFrame(window)
    file_name_dropdown.pack(expand = True, fill = 'both', padx = 25, pady = 25)

    def add_button(file):
        ctk.CTkButton(file_name_dropdown, text = file[:-5], height = 40, command = lambda: choose_file(file)).pack(fill = 'x', padx = 5, pady = 5)

    for file in files:
        add_button(file)

    window.mainloop()

    file_name = file_name_var.get()
    parent.load_custom_level(file_name)

def save_file(parent):
    
    window = ctk.CTk()
    window.title('Save Custom Level')
    window.geometry('300x150')
    window.resizable(False,False)

    def confirm_name():
        global confirmed
        confirmed = True
        window.destroy()

    file_name_var = ctk.StringVar()
    file_name_entry = ctk.CTkEntry(window, placeholder_text = 'Name', textvariable = file_name_var, font = ('Verdana', 28))
    file_name_entry.pack(fill = 'x', padx = 25, expand = True, pady = (25,8))

    global confirmed
    confirmed = False
    confirm_button = ctk.CTkButton(window, text = 'Confirm', command = confirm_name, height = 35)
    confirm_button.pack(fill = 'x', pady = (0,25), padx = 25)

    window.mainloop()

    if confirmed and (file_name:=file_name_var.get()):
        file_name += '.json'
        setattr(parent, 'level_name', file_name)

def open_custom_level(parent):
    Thread(target = get_file, args = (parent,), daemon = True).run()

def save_custom_level(parent):
    if parent.check_level_criteria():
        Thread(target = save_file, args = (parent,), daemon = True).run()