import pygame

class Entity:
    def __init__(self, engine, scene, pos, size, tag,
                detect_collisions=True, affected_by_gravity=True):

        self.engine = engine
        self.scene = scene

        self.pos = list(pos)
        self.size = size
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])

        self.velocity = [0, 0]
        self.tag = tag

        self.detect_collisions_enabled = detect_collisions
        self.affected_by_gravity = affected_by_gravity

    def update(self, dt, events):
        if self.affected_by_gravity:
            self.velocity[1] += 2000 * dt

        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt

        self.rect.topleft = self.pos

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 255), self.rect)

    def detect_collision(self, other):
        pass
