from GameEngine.GameObjects.GameObjects import GameObject

class Transform(GameObject):
    def __init__(self, scene, pos, size,sprite=None):
        super().__init__(scene, pos, size,False,sprite)