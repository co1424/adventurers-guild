from entities.entity import Entity


class Key(Entity):
    def __init__(self):
        scale = 1.5
        # Set up parent class
        super().__init__("assets/Sprite", "enter_key", scale)
