from scene import Scene
from render import Renderer
from config import GameConfig
from events import EventHandler

import fonts
import pygame
import math

def floor_tuple(x):
    return tuple(math.floor(i) for i in x)

class GameScene(Scene):

    class GameInfo():
        def __init__(self, config):
            self.config = config
            self.reset()

        def reset(self):
            self.paddle_rect = [self.config.w*0.4, self.config.h-40, self.config.w*0.2, 20]
            self.paddle_color = (255,255,0)
            self.paddle_velocity = 0
            self.paddle_speed = 1
            
            self.acceleration = 1
            self.ball_speed = 1
            self.ball_vector = [0,-1]
            self.ball_radius = 20
            self.ball_color = (255,55,55)
            self.ball_center = [self.config.w//2, self.config.h//2]

    class GameRenderer(Renderer):
        def __init__(self, config, info):
            self.screen = config.screen
            self.info = info
            
        def __call__(self):
            pygame.draw.rect(self.screen, self.info.paddle_color, tuple(self.info.paddle_rect))
            pygame.draw.circle(self.screen, self.info.ball_color, floor_tuple(self.info.ball_center), self.info.ball_radius)
    def __init__(self):
        self.config = GameConfig()
        self.info = GameScene.GameInfo(self.config)
        self.renderer = GameScene.GameRenderer(self.config, self.info)
        self.event_handler = EventHandler()
        super(GameScene, self).__init__(2)
    
    def refresh(self):
        self.info.reset()
        self.event_handler.clear()
        self.event_handler.register(pygame.KEYDOWN, self.handle_keydown)
        self.event_handler.register(pygame.KEYUP, self.handle_keyup)
    
    def handle_keydown(self, event):
        if event.key == pygame.K_LEFT:
            self.info.paddle_velocity = -1*self.info.paddle_speed
        if event.key == pygame.K_RIGHT:
            self.info.paddle_velocity = self.info.paddle_speed

    def handle_keyup(self, event):
        if event.key == pygame.K_LEFT and self.info.paddle_velocity < 0:
            self.info.paddle_velocity = 0
        if event.key == pygame.K_RIGHT and self.info.paddle_velocity > 0:
            self.info.paddle_velocity = 0
    
    def test_collission(self, rect):
        circle_x_min = self.info.ball_center[0] - self.info.ball_radius
        circle_x_max = self.info.ball_center[0] + self.info.ball_radius
        circle_y_min = self.info.ball_center[1] - self.info.ball_radius
        circle_y_max = self.info.ball_center[1] + self.info.ball_radius

        rect_x_min = rect[0]
        rect_x_max = rect[0] + rect[2]
        rect_y_min = rect[1]
        rect_y_max = rect[1] + rect[3]

        rx, ry = 0, 0

        if (circle_y_max >= rect_y_min and circle_y_max <= rect_y_max) or (circle_y_min >= rect_y_min and circle_y_min <= rect_y_max):
            if (circle_x_min <= rect_x_max and circle_x_max > rect_x_max):
                rx = 1
            if (circle_x_max >= rect_x_min and circle_x_min < rect_x_min):
                rx = -1
        if (circle_x_max >= rect_x_min and circle_x_max <= rect_x_max) or (circle_x_min >= rect_x_min and circle_x_min <= rect_x_max):
            if (circle_y_min <= rect_y_max and circle_y_max > rect_y_max):
                ry = 1
            if (circle_y_max >= rect_y_min and circle_y_min < rect_y_min):
                ry = -1
        return rx, ry


    def update(self, dt):
        new_x = self.info.paddle_velocity*dt + self.info.paddle_rect[0]
        if new_x > 0 and new_x + self.info.paddle_rect[2] < self.config.w:
            self.info.paddle_rect[0] = new_x
        
        b_x = (self.info.ball_center[0] + dt*self.info.ball_speed*self.info.ball_vector[0])
        b_y = (self.info.ball_center[1] + dt*self.info.ball_speed*self.info.ball_vector[1])
        player_col = self.test_collission(self.info.paddle_rect)
        
        if b_x < self.info.ball_radius or b_x + self.info.ball_radius > self.config.w:
            self.info.ball_vector[0] *= -1
        elif b_y < self.info.ball_radius:
            self.info.ball_vector[1] *= -1
        elif b_y - self.info.ball_radius > self.config.h:
            self.config.game_state = 1
        elif player_col[0] != 0 or player_col[1] != 0:
            bvx, bvy = self.info.ball_vector
            bvy = -1*abs(bvy)
            bvx += self.info.paddle_velocity*0.1+(self.info.paddle_rect[0]+self.info.paddle_rect[2]/2 - self.info.ball_center[0])*-0.0005
            
            bv_norm = math.sqrt(bvx**2+bvy**2)
            self.info.ball_vector = [(bvx/bv_norm), (bvy/bv_norm)]
        
        b_x = (self.info.ball_center[0] + dt*self.info.ball_speed*self.info.ball_vector[0])
        b_y = (self.info.ball_center[1] + dt*self.info.ball_speed*self.info.ball_vector[1])
        self.info.ball_center = [b_x, b_y]
