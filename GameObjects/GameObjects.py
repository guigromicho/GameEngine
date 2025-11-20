import pygame

class GameObject:
    def __init__(self,engine,scene, pos, size,tag,detect_colligions=False):
        self.scene = scene
        self.engine = engine
        self.pos = list(pos)
        self.size = size
        self.detect_collisions_enabled = detect_colligions
        self.rect = pygame.Rect(self.pos, self.size)
        self.tag = tag

    def update(self, dt,events=None):
        self.rect.topleft = self.pos
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
    
    def detect_collision(self, other):
        if self.rect.colliderect(other.rect):
            pass
        
