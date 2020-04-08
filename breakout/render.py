from config import GameConfig

class Renderer():
    def __call__(self):
        raise NotImplementedError()

class RenderHandler():

    __singleton = None

    class __RenderHandlerObject():
        def __init__(self):
            self.config = GameConfig()
            self.handlers = {}
        
        def draw(self):
            if self.config.game_state not in self.handlers:
                raise Exception("No Renderer Registered For Game State %s"%(self.config.game_state))
            self.handlers[self.config.game_state]()

        def register(self, game_state, handler):
            if game_state in self.handlers:
                raise Exception("Multiple Render Handlers for Game State %s Not Allowed"%game_state)
            self.handlers[game_state] = handler

        def deregister(self, game_state):
            if game_state in self.handlers:
                del self.handlers[game_state]

        def clear(self):
            self.handlers.clear()

        def __repr__(self):
            return "Render Handler Object"
    
    # Singleton
    def __init__(self):
        if RenderHandler.__singleton == None:
            RenderHandler.__singleton = RenderHandler.__RenderHandlerObject()
    def __getattr__(self, name):
        return getattr(RenderHandler.__singleton, name)    
    def __setattr__(self, name, value):
        setattr(RenderHandler.__singleton, name, value)