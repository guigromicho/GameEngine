import pygame
from GameEngine.Scene.Transição_entre_Scene import Transicao

class Engine:
    def __init__(self, gravaty, back_ground_color=(0,0,0)):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("My Game")
        
        self.back_ground_color = back_ground_color
        self.clock = pygame.time.Clock()
        self.running = True

        self.scenes = {}
        self.current_scene = None
        self.gravaty = gravaty

        self.transitions = {}
        self.current_transition = None

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def set_scene(self, name):
        if name in self.scenes:
            self.current_scene = self.scenes[name]

    def start_transition(self, origem, destino, estilo="fade_in", velocidade=5):
        key = (origem, destino)

        if key not in self.transitions:
            self.transitions[key] = Transicao(
                engine=self,
                cena_destino=destino,
                estilo=estilo,
                velocidade=velocidade
            )

        self.current_transition = self.transitions[key]
        self.current_transition.cena_destino = destino
        self.current_transition.estilo = estilo
        self.current_transition.iniciar()

    def start(self):
        while self.running:
            self.update()

    def update(self):
        dt = self.clock.tick(60) / 1000.0
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

        if self.current_scene and (not self.current_transition or not self.current_transition.ativa):
            self.current_scene.handle_event(events)
            self.current_scene.update(dt, events)

        if self.current_transition and self.current_transition.ativa:
            self.current_transition.update()

        self.draw()

    def draw(self):
        self.screen.fill(self.back_ground_color)

        if self.current_transition and self.current_transition.ativa:
            if self.current_transition.estilo == "fade_in":
                self.current_transition.scene_anterior.draw(self.screen)
            else:
                if self.current_scene:
                    self.current_scene.draw(self.screen)

            self.current_transition.draw(self.screen)

        else:
            if self.current_scene:
                self.current_scene.draw(self.screen)

        pygame.display.flip()
