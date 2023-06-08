from entities.enemy import Enemy


class Ranged_Enemy(Enemy):
    def __init__(self):
        scale = 1
        # Set up parent class
        super().__init__(":resources:images/space_shooter/playerShip2_orange.png", "enemy_basic", scale)

        self.health = 50