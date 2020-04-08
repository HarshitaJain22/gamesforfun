class GameConfig():

    _game_config_singleton = None

    class __GameConfigObject():
        def __init__(self):
            self.game_state = 0
            self.w = 800
            self.h = 600
            self.running = True
            self.screen = None
            self.fps_cap = -1
            self.min_mspf = -1000
            self.scene_handler = None
        def __repr__(self):
            return "Game Config:\n\tState: %s\n\tWidth x Height: %sx%s\n\tRunning: %s"%(self.game_state, self.w, self.h, self.running)
        
    #Singleton
    def __init__(self):
        if GameConfig._game_config_singleton == None:
            GameConfig._game_config_singleton = GameConfig.__GameConfigObject()
    def __getattr__(self, name):
        return getattr(GameConfig._game_config_singleton, name)    
    def __setattr__(self, name, value):
        if(name == "fps"):
            setattr(GameConfig._game_config_singleton, name, value)
            GameConfig._game_config_singleton.min_mspf = 1000/value
        elif name == "game_state":
            GameConfig._game_config_singleton.game_state = value
            if self.scene_handler is not None:
                self.scene_handler.refresh(value)
        else:
            setattr(GameConfig._game_config_singleton, name, value)