import pygame

class GameObject:
    def __init__(self, engine, scene, pos, size, tag, detect_colligions=False):
        self.scene = scene
        self.engine = engine
        self.pos = list(pos)
        self.size = size
        self.tag = tag

        self.detect_collisions_enabled = detect_colligions
        self.rect = pygame.Rect(self.pos, self.size)

    def update(self, dt, events=None):
        # Atualiza o rect baseado na posição
        self.rect.topleft = self.pos

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

        if self.detect_collisions_enabled and self.engine.show_colliders:
            pygame.draw.rect(surface, (0, 255, 0), self.rect, 2)

    def detect_collision(self, other):
        return self.rect.colliderect(other.rect)
