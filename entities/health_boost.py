from entities.entity import Entity


class Health_Boost(Entity):
    def __init__(self):
        scale = 1.5
        # Set up parent class
        super().__init__("assets/Sprite", "health_boost", scale)
