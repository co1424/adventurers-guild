from entities.enemy import Enemy


class Basic_Enemy(Enemy):
    def __init__(self):
        scale = .1
        # Set up parent class
        super().__init__("assets/Sprite/Enemy/Basic", "enemyPlaceholder", scale)

        self.health = 50