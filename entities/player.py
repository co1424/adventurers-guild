from constants import LEFT_FACING, RIGHT_FACING
from entities.entity import Entity
import arcade


class Player(Entity):
    """Player Sprite"""

    def __init__(self):

        folder = "assets/Sprite/Player"
        file_prefix = "player"

        # Set up parent class

        self.health = 10
        scale = 1

        super().__init__(folder, file_prefix, scale)

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.invulnerable = False
    
    def change_health(self, value):
        '''
        Used to modify the player's health by the given value.
        
        PARAMETERS:

        value = the given amount to add to player health. Positive values add health, negative values subtract health.
        '''
        self.health += value

    
    def get_health(self):
        return self.health
    

    def set_invulnerable_seconds(self, seconds):
        '''
        Sets the amount of time (seconds) for the player to be invulnerable
        
        PARAMETERS:

        seconds = time to be invulnerable
        '''
        self.invulnerable = True
        arcade.unschedule(self.disable_invulnerability)  # Cancel any previous invulnerability timer to make sure the timer resets
        arcade.schedule(self.disable_invulnerability, seconds)

    
    def disable_invulnerability(self, _):
        self.invulnerable = False


    def is_Invulnerable(self):
        return self.invulnerable


    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Climbing animation
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return

        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.facing_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.facing_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.facing_direction]