from entities.entity import Entity

class Enemy(Entity):
    def __init__(self, folder, file_prefix, scale):

        # Setup parent class
        super().__init__(folder, file_prefix, scale)

        self.should_update_walk = 0
        self.health = 1
        self.hit_timer = 0
    """
    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Walking animation
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1
    """
    def start_hit_timer(self):
        self.hit_timer = 1

    def is_hit(self, delta_time: float = 1 / 60):
        if self.hit_timer <= 0:
            return True
        
        if not self.hit_timer <= 0:
            self.hit_timer -= delta_time

        return False

    def change_health(self, value: int):
        self.health += value
        
