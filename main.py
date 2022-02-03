from math import sqrt
from telnetlib import SE
from typing import Set
import pygame
import os
import random

class Settings:
    # Window settings
    window_height = 750
    window_width = 1000
    window_fps = 60
    window_caption = ""

    # Base paths
    path_working_directory = os.path.dirname(os.path.abspath(__file__))
    path_images = os.path.join(path_working_directory, 'images')

    @staticmethod
    def _get_images_from_folder(path):
        return sorted([os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])

    # Animation settings
    fighter_scale = 3
    animation_speed = 100 # in ms
    animation_textures = {
        'hit': _get_images_from_folder(os.path.join(path_images, 'animation1')),
        'uppercut': _get_images_from_folder(os.path.join(path_images, 'animation2')),
        'high_kick': _get_images_from_folder(os.path.join(path_images, 'animation3')),
        'uppercut2': _get_images_from_folder(os.path.join(path_images, 'animation4'))
    }

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(os.path.join(Settings.path_images, 'background.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (
            Settings.window_width,
            Settings.window_height
        ))

    def draw(self):
        # Blit background image at coords 0/0 (top-left)
        game.screen.blit(self.image, (0, 0))

class Timer:
    def __init__(self, duration, with_start = True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False

class Fighter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(os.path.join(Settings.path_images, 'idle.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rescale_fighter()

        self.animation_timer = Timer(Settings.animation_speed)
        self.animation_index = 0
        self.animation = None
    
    def rescale_fighter(self):
        self.image = pygame.transform.scale(self.image, (
            int(self.rect.width * Settings.fighter_scale),
            int(self.rect.height * Settings.fighter_scale)
        ))
        self.rect = self.image.get_rect()
    
    def is_animation_done(self):
        if self.animation is None:
            return True
        return self.animation_index >= len(Settings.animation_textures[self.animation]) - 1
    
    def play_animation(self, animation):
        if not self.is_animation_done(): return
        self.animation = animation
        self.animation_index = 0
    
    def update(self):
        if self.animation_timer.is_next_stop_reached() and self.animation is not None:
            center = self.rect.center
            self.animation_index += 1

            if self.animation_index >= len(Settings.animation_textures[self.animation]):
                self.animation_index = 0
            
            self.image = pygame.image.load(Settings.animation_textures[self.animation][self.animation_index]).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.rescale_fighter()
        
        if self.is_animation_done():
            self.animation = None
            self.image = pygame.image.load(os.path.join(Settings.path_images, 'idle.png')).convert_alpha()
            self.rect = self.image.get_rect()
            self.rescale_fighter()

    def draw(self):
        game.screen.blit(self.image, self.rect)

class Game:
    def __init__(self):
        super().__init__()

        # PyGame Init
        os.environ['SDL_VIDEO_WINDOW_CENTERED'] = '1'
        pygame.init()
        pygame.display.set_caption(Settings.window_caption)


        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        self.running = False

        # Sprites
        self.background = Background()
        self.fighter = Fighter()

    def start(self):
        self.running = True

        while self.running:
            self.clock.tick(Settings.window_fps)

            self.watch_events()

            self.update()
            self.draw()

        pygame.quit()
    
    def watch_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.fighter.play_animation('hit')
                if event.key == pygame.K_UP:
                    self.fighter.play_animation('uppercut')
                if event.key == pygame.K_LEFT:
                    self.fighter.play_animation('high_kick')
                if event.key == pygame.K_RIGHT:
                    self.fighter.play_animation('uppercut2')

    def update(self):
        self.background.update()
        self.fighter.update()

    def draw(self):
        self.background.draw()
        self.fighter.draw()
        
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.start()
