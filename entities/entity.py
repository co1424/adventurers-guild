import arcade

from constants import CHARACTER_SCALING, RIGHT_FACING


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class Entity(arcade.Sprite):
    def __init__(self, folder, file_prefix, scale=1):
        super().__init__()

        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0
        self.scale = scale

        self.animations = {} # arbitrary code

        self.idle_texture_pair = load_texture_pair(f"{folder}/{file_prefix}_idle.png")
        # self.jump_texture_pair = load_texture_pair(f"{folder}/{file_prefix}_jump.png")
        # self.fall_texture_pair = load_texture_pair(f"{folder}/{file_prefix}_fall.png")

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        # self.set_hit_box(self.texture.hit_box_points)
