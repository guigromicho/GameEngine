import pygame

class Scene:
    def __init__(self, engine):
        self.engine = engine
        self.objects = []
        self.buttons = []

    def add_object(self, obj):
        self.objects.append(obj)

    def update(self, dt,events):
        for obj in self.objects:
            obj.update(dt, events)
            for other in self.objects:
                if obj is not other and other.detect_collisions_enabled:
                    obj.detect_collision(other)

        for button in self.buttons:
            button.update()

    def draw(self, surface):
        for obj in self.objects:
            obj.draw(surface)
        for button in self.buttons:
            button.draw(surface)

    def handle_event(self, events):
        for event in events:
            for obj in self.objects:
                if hasattr(obj, "handle_event"):
                    obj.handle_event(event)

            for button in self.buttons:
                button.handle_event([event])

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.engine.current_scene == self.engine.scenes.get("game"):
                    self.pause_game()
        
    
    
    def quit_game(self):
        self.engine.running = False

    def back_to_menu(self):
        self.engine.start_transition("game", "menu")

    def play_game(self):
        self.engine.start_transition("menu", "game")

    def options_menu(self):
        self.engine.start_transition("options","menu")
    
    def pause_game(self):
        self.engine.start_transition("game","pause")
