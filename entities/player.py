from constants import LEFT_FACING, RIGHT_FACING, SWING_SPEED, SWING_FRAME_COUNT, KEY_SPACE
from entities.entity import Entity
from entities.sword import Sword


class Player(Entity):
    """Player Sprite"""

    def __init__(self):

        folder = "Sprite/Player"
        file_prefix = "character"

        # Set up parent class
        scale = .1

        super().__init__(folder, file_prefix, scale)

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        
        # Track swinging animation state
        self.is_swinging = False
        self.swing_direction = RIGHT_FACING
        self.swing_progress = 0

    def start_swing_animation(self):
        if not self.is_swinging:
            self.is_swinging = True
            self.swing_progress = 0

    def update_animation(self, sword: Sword, delta_time: float = 1 / 60):

        """
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
        """
        
        # Swing animation
        if self.is_swinging:
            self.swing_progress += delta_time * SWING_SPEED

            if self.swing_progress < 0.5:
                self.swing_direction = RIGHT_FACING
            else:
                self.swing_direction = LEFT_FACING

            if self.swing_progress > 1:
                self.is_swinging == False
            
            sword.swing((self.center_x, self.center_y), SWING_SPEED)
            #swing_frame = int(self.swing_progress * SWING_FRAME_COUNT) % SWING_FRAME_COUNT
            #self.weapon_texture = self.swing_textures[swing_frame][self.swing_direction]
            return self.swing_progress
        """
        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.facing_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.facing_direction]
            return
        """

        """
        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
        """