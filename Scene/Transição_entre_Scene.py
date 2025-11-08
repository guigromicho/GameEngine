import pygame

class Transicao:
    def __init__(self, engine, cena_destino, estilo="fade_in", velocidade=5):
        self.engine = engine
        self.cena_destino = cena_destino
        self.estilo = estilo
        self.velocidade = velocidade

        self.alpha = 0
        self.ativa = False

        self.screen_w, self.screen_h = self.engine.screen.get_size()

        self.fade_surface = pygame.Surface((self.screen_w, self.screen_h))
        self.fade_surface.fill((0, 0, 0))

        self.scene_anterior = None

    def iniciar(self):
        self.ativa = True
        self.scene_anterior = self.engine.current_scene

        if self.estilo == "fade_in":
            self.alpha = 0

        elif self.estilo == "fade_out":
            self.alpha = 255

        elif self.estilo == "right_to_left":
            self.slide_x = self.w

        elif self.estilo == "left_to_right":
            self.slide_x = 0

    def update(self):

        if not self.ativa:
            return

        if self.estilo == "fade_in":

            self.alpha += self.velocidade

            if self.alpha >= 255:
                self.alpha = 255
                self.engine.set_scene(self.cena_destino)
                self.estilo = "fade_out"

        elif self.estilo == "fade_out":
            self.alpha -= self.velocidade
            if self.alpha <= 0:
                self.alpha = 0
                self.ativa = False
        
        elif self.estilo == "right_to_left":

            self.slide_x -= self.velocidade
            if self.slide_x <= 0:
                self.slide_x = 0
                self.engine.set_scene(self.cena_destino)

                self.estilo = "fade_out"
                self.alpha = 255
        
        elif self.estilo == "left_to_right":
            self.slide_x += self.velocidade
            if self.slide_x >= self.w:
                self.slide_x = self.w
                self.engine.set_scene(self.scene_destino)

                self.estilo = "fade_out"
                self.alpha = 0


    def draw(self, surface):
        if not self.ativa:
            return

        if self.estilo == "left_to_right" or self.estilo == "right_to_left":
            print("entrou")
            pygame.draw.rect(surface, (0, 0, 0),(self.slide_x, 0, self.w, self.h))
            return

        self.fade_surface.set_alpha(self.alpha)
        surface.blit(self.fade_surface, (0, 0))
