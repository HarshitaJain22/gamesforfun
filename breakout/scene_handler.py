from config import GameConfig
from render import RenderHandler
from scenes.loading import LoadingScene

class SceneHandler():

    __singleton = None

    class __SceneHandlerObject():
        def __init__(self):
            self.config = GameConfig()
            self.render_handler = RenderHandler()
            self.scenes = {}
        
        def update(self, dt):
            if self.config.game_state not in self.scenes:
                raise Exception("No Scene Registered For Game State %s"%(self.config.game_state))
            self.scenes[self.config.game_state].update(dt)

        def register(self, game_state, scene):
            if game_state in self.scenes:
                raise Exception("Multiple Scene Handlers for Game State %s Not Allowed"%game_state)
            self.scenes[game_state] = scene

        def deregister(self, game_state):
            if game_state in self.scenes:
                del self.scenes[game_state]
        def refresh(self, game_state):
            if game_state in self.scenes:
                self.scenes[game_state].refresh()
        def clear(self):
            self.scenes.clear()

        def __repr__(self):
            return "Scene Handler Object"
    
    # Singleton
    def __init__(self):
        if SceneHandler.__singleton == None:
            SceneHandler.__singleton = SceneHandler.__SceneHandlerObject()
            SceneHandler.__singleton.register(0, LoadingScene(SceneHandler.__singleton))
    def __getattr__(self, name):
        return getattr(SceneHandler.__singleton, name)    
    def __setattr__(self, name, value):
        setattr(SceneHandler.__singleton, name, value)