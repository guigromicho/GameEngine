from GameEngine.GameObjects.GameObjects import GameObject
import pygame
import math

class Light(GameObject):
    def __init__(self, engine, scene, pos, size,tag, raio_mais_pequeno=20,
                piscar=False, intensity=1.0, color=(255, 255, 200)):
        super().__init__(engine, scene, pos, size,tag)

        self.intensity_base = intensity
        self.intensity = intensity
        self.color = color
        self.size = size

        self.surface = pygame.Surface(size, pygame.SRCALPHA)

        self.piscar = piscar
        self.piscar_speed = 3.0
        self.time = 0.0

        self.raio_mais_pequeno = raio_mais_pequeno

        self.update_light_surface()

    def update(self, dt, events=None):
        if self.piscar:
            self.time += dt * self.piscar_speed
            # piscar suave
            self.intensity = self.intensity_base * (0.5 + 0.5 * math.sin(self.time))
            self.update_light_surface()

    def update_light_surface(self):
        self.surface.fill((0, 0, 0, 0))

        radius = self.raio_mais_pequeno
        center = (self.size[0] // 2, self.size[1] // 2)

        for r in range(radius, 0, -1):
            alpha = int((self.intensity * 255) * (1 - (r / radius))**2)
            pygame.draw.circle(self.surface, (*self.color, alpha), center, r)

    def draw(self, surface):
        surface.blit(self.surface, self.pos)
