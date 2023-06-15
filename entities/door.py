from entities.entity import Entity


class Door(Entity):
    def __init__(self):
        scale = 1
        # Set up parent class
        super().__init__("assets/Sprite", "door", scale)
