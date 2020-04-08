


class EventHandler():

    __singleton = None

    class __EventHandlerObject():
        def __init__(self):
            self.handlers = []

        def dispatch(self, event):
            for event_type, handler in self.handlers:
                if event.type == event_type:
                    handler(event)

        def register(self, event_type, handler):
            self.handlers.append((event_type, handler))

        def deregister(self, handler):
            remove_list = []
            for handle in self.handlers:
                if handle[1] == handler:
                    remove_list.append(handle)
            for handle in remove_list:
                self.handlers.remove(handle)
        
        def clear(self):
            self.handlers.clear()

        def __repr__(self):
            return "Event Handler Object:"
    
    # Singleton
    def __init__(self):
        if EventHandler.__singleton == None:
            EventHandler.__singleton = EventHandler.__EventHandlerObject()
    def __getattr__(self, name):
        return getattr(EventHandler.__singleton, name)    
    def __setattr__(self, name, value):
        setattr(EventHandler.__singleton, name, value)