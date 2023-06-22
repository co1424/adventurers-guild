import arcade
import math
from constants import SWORD_OFFSET
from entities.entity import Entity

class Sword(Entity):
    def __init__(self, x, y, angle):
        folder = "assets/Sprite/Player"
        prefix = "sword"
        scale = .75
        super().__init__(folder, prefix, scale)
        angle_radians = math.radians(angle + 30)
        self.center_x = x + math.cos(angle_radians) * SWORD_OFFSET
        self.center_y = y + math.sin(angle_radians) * SWORD_OFFSET
        self.angle = angle

    def swing(self, rotation_point, step_in_degrees):

        angle_radians = math.radians(self.angle)
        self.center_x = rotation_point[0] + math.cos(angle_radians) * SWORD_OFFSET
        self.center_y = rotation_point[1] + math.sin(angle_radians) * SWORD_OFFSET
        self.angle += step_in_degrees

        self.position = arcade.rotate_point(
            self.center_x, self.center_y,
            rotation_point[0], rotation_point[1], step_in_degrees)