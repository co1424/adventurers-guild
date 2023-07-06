from entities.enemy import Enemy


class Basic_Enemy(Enemy):
    def __init__(self, name):
        self.name = name
        scale = 1
        # Set up parent class
        super().__init__("assets/Sprite/Enemy/Basic", "enemy_basic", scale)

        self.health = 3
