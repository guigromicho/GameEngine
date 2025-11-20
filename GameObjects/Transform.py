from GameEngine.GameObjects.GameObjects import GameObject

class Transform(GameObject):
    def __init__(self, scene, pos, size):
        super().__init__(scene, pos, size,False)