from entities.entity import Entity
import arcade

class Enemy(Entity):
    def __init__(self, folder, file_prefix, scale):

        # Setup parent class
        super().__init__(folder, file_prefix, scale)

        self.should_update_walk = 0
        self.health = 1
        self.hit_timer = 0

    # For enemy i-Frames
    def start_hit_timer(self):
        self.hit_timer = .5

    def is_hit(self, delta_time: float = 1 / 60):
        if self.hit_timer <= 0:
            self.color = arcade.color.WHITE
            return True
        
        self.color = arcade.color.GRAY
        if not self.hit_timer <= 0:
            self.hit_timer -= delta_time

        return False

    def change_health(self, value: int):
        self.health += value
        
