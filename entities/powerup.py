from entities.entity import Entity

class Powerup(Entity):
    """Powerup Sprite"""
    def __init__(self):
        folder = "Sprite/Player"
        file_prefix = "powerup"

        # Set up parent class
        scale = .1

        super().__init__(folder, file_prefix, scale)

        
    

