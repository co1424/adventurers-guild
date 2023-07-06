from entities.enemy import Enemy

class Minion(Enemy):
    def __init__(self):
        scale = .5
        # Set up parent class
        super().__init__("assets/Sprite/Enemy/Basic", "enemy_basic", scale)

        self.health = 1
