import pygame 
pygame.init()

from events import EventHandler
from config import GameConfig
from render import RenderHandler
from scene_handler import SceneHandler

def game():
    
    config = GameConfig()
    event_handler = EventHandler()
    screen = pygame.display.set_mode([config.w, config.h])
    config.screen = screen

    render_handler = RenderHandler()
    scene_handler = SceneHandler()

    config.scene_handler = scene_handler

    last_ticks = pygame.time.get_ticks()
    ticks_since_render = pygame.time.get_ticks()
    while config.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.running = False
            else:
                event_handler.dispatch(event)
        
        current_ticks = pygame.time.get_ticks()
        dt = current_ticks - last_ticks
        # Update
        scene_handler.update(dt)
        # Render
        ticks_since_render += dt
        last_ticks = current_ticks
        if ticks_since_render > config.min_mspf:
            screen.fill((0,0,0))
            render_handler.draw()
            pygame.display.flip()
            ticks_since_render = 0




if __name__ == "__main__":
    game()