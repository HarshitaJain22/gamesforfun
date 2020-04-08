from render import RenderHandler

class Scene():
    def __init__(self, game_state):
        self.render_handler = RenderHandler()
        self.render_handler.register(game_state, self.get_renderer())
    def update(self):
        raise NotImplementedError()
    def get_renderer(self):
        if self.renderer == None:
            raise NotImplementedError()
        return self.renderer
    def refresh(self):
        raise NotImplementedError()