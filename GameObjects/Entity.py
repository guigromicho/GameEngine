from GameEngine.GameObjects.GameObjects import GameObject
import pygame

class Entity(GameObject):

    def __init__(self, engine,scene, pos, size,tag,detect_colligions=False, affected_by_gravity=False,sprite=None):
        super().__init__(engine,scene,pos, size, tag ,detect_colligions, sprite)
        self.engine = engine
        self.affected_by_gravity = affected_by_gravity
        self.velocity = [0, 0]
        self.gravaty = self.engine.gravaty

    def update(self, dt,events):
        super().update(dt)
        self.handel_events(events)
        self.update_gravity(dt)

    def update_gravity(self, dt):
        if self.affected_by_gravity:
            self.velocity[1] += (self.engine.gravaty * 2) * dt
            self.pos[1] += self.velocity[1] * dt
            self.rect.topleft = self.pos

    def handel_events(self, events):
        for event in events:
            pass