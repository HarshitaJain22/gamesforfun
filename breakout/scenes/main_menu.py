from scene import Scene
from render import Renderer
from config import GameConfig
from events import EventHandler

from scenes.game import GameScene

import fonts

import pygame

class MainMenuScene(Scene):

    def __init__(self):
        self.config = GameConfig()
        self.renderer = MainMenuScene.MainMenuRenderer(self.config)
        self.event_handler = EventHandler()
        super(MainMenuScene, self).__init__(1)
    
    def refresh(self):
        self.time_since_update = 0
        self.selection = 0
        self.event_handler.clear()
        self.event_handler.register(pygame.KEYDOWN, self.handle_change_selection)

    def handle_change_selection(self, event):
        if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
            self.selection = (self.selection + 1) % 2
            self.renderer.set_selection(self.selection)
        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.selection % 2 == 1:
                self.config.running = False
            else:
                self.config.game_state = 2
    
    class MainMenuRenderer(Renderer):
        def __init__(self, config):
            self.screen = config.screen
            self.MainMenu_text = fonts.ariel150.render("Breakout!", True, (255,255,255))
            MainMenu_rect = self.MainMenu_text.get_rect()
            self.MainMenu_x = config.w/2 - MainMenu_rect.width / 2
            self.MainMenu_y = 20
            
            self.PlayGame_text = fonts.ariel120.render("Play", True, (255,255,0))
            PlayGame_rect = self.PlayGame_text.get_rect()
            self.PlayGame_x = config.w/2 - PlayGame_rect.width / 2
            self.PlayGame_y = 200
            
            self.Quit_text = fonts.ariel120.render("Quit", True, (255,0,0))
            Quit_rect = self.Quit_text.get_rect()
            self.Quit_x = config.w/2 - Quit_rect.width / 2
            self.Quit_y = 400

            self.SelectionRect = (self.PlayGame_x - 40, 200, 20, self.PlayGame_text.get_rect().height)
            self.SelectionRect2 = (self.PlayGame_x + self.PlayGame_text.get_rect().width + 40, 200, 20, self.PlayGame_text.get_rect().height)
        
        def set_selection(self, selection):
            if selection == 0:
                self.SelectionRect = (self.PlayGame_x - 40, 200, 20, self.PlayGame_text.get_rect().height)
                self.SelectionRect2 = (self.PlayGame_x + self.PlayGame_text.get_rect().width + 40, 200, 20, self.PlayGame_text.get_rect().height)
            else:
                self.SelectionRect = (self.Quit_x - 40, 400, 20, self.Quit_text.get_rect().height)
                self.SelectionRect2 = (self.Quit_x + self.Quit_text.get_rect().width + 40, 400, 20, self.Quit_text.get_rect().height)
            
        def __call__(self):
            self.screen.blit(self.MainMenu_text, (self.MainMenu_x, self.MainMenu_y))
            self.screen.blit(self.PlayGame_text, (self.PlayGame_x, self.PlayGame_y))
            self.screen.blit(self.Quit_text, (self.Quit_x, self.Quit_y))
            pygame.draw.rect(self.screen, (100, 255, 100), self.SelectionRect)
            pygame.draw.rect(self.screen, (100, 255, 100), self.SelectionRect2)

    def update(self, dt):
        pass