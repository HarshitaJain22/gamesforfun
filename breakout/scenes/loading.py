from scene import Scene
from render import Renderer
from config import GameConfig

from scenes.main_menu import MainMenuScene
from scenes.game import GameScene
import fonts

import pygame

class LoadingScene(Scene):

    def __init__(self, handler):
        self.config = GameConfig()
        self.renderer = LoadingScene.LoadingRenderer(self.config)
        self.loading = False
        self.scene_handler = handler
        super(LoadingScene, self).__init__(0)
    def refresh(self):
        self.renderer = LoadingScene.LoadingRenderer(self.config)
        self.loading = False
    class LoadingRenderer(Renderer):
        def __init__(self, config):
            self.screen = config.screen
            self.loading_text = fonts.ariel30.render("Loading...", True, (255,255,255))
            loading_rect = self.loading_text.get_rect()
            self.loading_x = config.w/2 - loading_rect.width / 2
            self.loading_y = config.h/2 - loading_rect.height / 2
        def __call__(self):
            self.screen.blit(self.loading_text, (self.loading_x, self.loading_y))

    def update(self, dt):
        if(self.loading == False):
            self.loading = True
            return
        self.scene_handler.register(1, MainMenuScene())
        self.scene_handler.register(2, GameScene())
        self.config.game_state = 1