from entities.enemy import Enemy
import random

choices = (-1, 0, 1)

class Boss(Enemy):


    def __init__(self, name):
        self.name = name
        folder = "assets/Sprite/Enemy/Boss"
        img_name = "moth_boss"
        scale = 3

        super().__init__(folder, img_name, scale)

        self.health = 20
        self.direction_x = 0
        self.direction_y = 0
        self.direction_timer = 0.0
        self.minion_spawn_timer = 0.0
        self.rand = random.Random()

    def get_direction(self):
        self.tick_direction_timer()
        return (self.direction_x, self.direction_y)
    
    def tick_direction_timer(self, delta_time = 1 / 60):
        self.direction_timer -= delta_time
        if self.direction_timer <= 0:
            self.change_direction()
            self.start_direction_timer()

    def start_direction_timer(self):
        self.direction_timer = 2.0

    def change_direction(self):
        self.direction_x = self.rand.choice(choices)
        self.direction_y = self.rand.choice(choices)

    def start_minion_spawn_timer(self):
        self.minion_spawn_timer = 5.0

    def tick_minion_spawn_timer(self, delta_time = 1 / 60):
        self.minion_spawn_timer -= delta_time
        if self.minion_spawn_timer <= 0:
            self.start_minion_spawn_timer()
            return True
        else:
            return False
        
    def should_spawn_minions(self):
        return self.tick_minion_spawn_timer()
            
