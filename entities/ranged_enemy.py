from entities.enemy import Enemy


class Ranged_Enemy(Enemy):
    def __init__(self):
        scale = .1
        # Set up parent class
        super().__init__("assets/Sprite/Enemy/Ranged", "temp_wasp", scale)

        self.health = 50