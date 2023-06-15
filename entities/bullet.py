from entities.entity import Entity
import arcade
from constants import *

class Bullet(arcade.Sprite):
    def __init__(self) -> None:
        super().__init__(
            filename= ":resources:images/space_shooter/laserBlue01.png",
            scale=SPRITE_SCALING_BULLET,
        )

    def on_update(self, delta_time: float = 1 / 60) -> None:
        """Updates the bullet's position."""
        self.position = (
            self.center_x + self.change_x * delta_time,
            self.center_y + self.change_y * delta_time,
        )