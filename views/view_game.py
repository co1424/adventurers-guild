"""
Game View
"""
import math
import os

import arcade

from constants import *
from entities.player import Player
from entities.enemy import Enemy
from entities.basic_enemy import Basic_Enemy
from views.view import View

from views.view_game_over import GameOverView


# Speed limit
MAX_SPEED = 8.0

# How fast we accelerate
ACCELERATION_RATE = 0.6

# How fast to slow down after we let off the key
FRICTION = 0.35

class GameView(View):

    # SET STARTING MAP:
    map_name = "map2.tmj"

    def __init__(self):
        """
        Initializer for the game
        """
        super().__init__()

        self.player_sprite = None
        self.game_over = False
        self.keys_pressed = set()

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.shoot_pressed = False

        self.mouse_pos = 0, 0

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our 'physics' engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        self.end_of_map = 0

        # Keep track of the score
        self.score = 0

        # Shooting mechanics
        self.can_shoot = False
        self.shoot_timer = 0

        # The selected player
        self.selected_player = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.shoot_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        super().setup()

        # Track the current state of what key is pressed
       #self.left_pressed = False
        #self.right_pressed = False
        #self.up_pressed = False
        #self.down_pressed = False
        #self.shoot_pressed = False
        #self.jump_needs_reset = False

        # Setup the Cameras
        #self.camera = arcade.Camera(self.window.width, self.window.height)
        #self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        # Layer Specific Options for the Tilemap
        layer_options = {
            LAYER_NAME_WALLS: {
                "use_spatial_hash": True,
            }, 
        }
            
        #    LAYER_NAME_MOVING_PLATFORMS: {
        #        "use_spatial_hash": True,
        #    },
        #    LAYER_NAME_LADDERS: {
        #        "use_spatial_hash": True,
        #    },
        #    LAYER_NAME_COINS: {
        #        "use_spatial_hash": True,
        #    },
            
        if "game_over" not in self.window.views:
            self.window.views["game_over"] = GameOverView()

        # Load in TileMap
        self.tile_map = arcade.load_tilemap(f"views/maps-data/{self.map_name}", TILE_SCALING, layer_options)

        # Initiate New Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Keep track of the score
        self.score = 0

        # Load your sprites and set up the game
        # Sprite lists
        #self.player_list = arcade.SpriteList()

        # Set up the player
        #self.player_sprite = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png")
        #self.player_sprite.center_x = 1216 - self.player_sprite.width // 2
        #self.player_sprite.center_y = 800 - self.player_sprite.height // 2
        #self.player_list.append(self.player_sprite)
        """
        # Shooting mechanics
        self.can_shoot = True
        self.shoot_timer = 0
        """
        
        # Set up the player at these coordinates. The unit of measurement is in tiles (Each map total width of 38, height of 25)
        self.player_sprite = Player()
        self.player_sprite.center_x = (
            (SCREEN_TILE_WIDTH / 2) * self.tile_map.tiled_map.tile_size[0] # Middle of the screen (X)
        )
        self.player_sprite.center_y = (
            3 * self.tile_map.tiled_map.tile_size[1] # Bottom of the screen (Y)
        )
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)
        
        # Calculate the right edge of the my_map in pixels
        self.end_of_map = self.tile_map.tiled_map.map_size.width * GRID_PIXEL_SIZE
        
        # -- Enemies
        enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]

        for my_object in enemies_layer:
            cartesian = self.tile_map.get_cartesian(
                my_object.shape[0], my_object.shape[1]
            )
            enemy_type = my_object.properties["type"]

            if enemy_type == "basic":
                enemy = Basic_Enemy()
            enemy.center_x = math.floor(
                cartesian[0] * TILE_SCALING * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
            )
            """if "boundary_left" in my_object.properties:
                enemy.boundary_left = my_object.properties["boundary_left"]
            if "boundary_right" in my_object.properties:
                enemy.boundary_right = my_object.properties["boundary_right"]"""
            if "change_x" in my_object.properties:
                enemy.change_x = my_object.properties["change_x"]
            self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)
        """
        # Add bullet spritelist to Scene
        self.scene.add_sprite_list(LAYER_NAME_BULLETS)

        # --- Other stuff
        # Set the background color
        if self.tile_map.tiled_map.background_color:
            arcade.set_background_color(self.tile_map.tiled_map.background_color)
        """
    
        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            gravity_constant=GRAVITY,
            walls=self.scene.get_sprite_list(LAYER_NAME_WALLS)
        )



    """
    def on_show_view(self):
        arcade.set_background_color(self.tile_map.background_color)
    """

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        arcade.start_render()

        # Activate the game camera
        #self.camera.use()

        # Draw our Scene
        self.scene.draw()

        self.player_sprite.draw()

        # Activate the GUI camera before drawing GUI elements
        #self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.BLACK,
            18,
        )

        # Draw hit boxes.
        # for wall in self.wall_list:
        #     wall.draw_hit_box(arcade.color.BLACK, 3)
        # 
        #     self.player_sprite.draw_hit_box(arcade.color.RED, 3)

    def detect_map_change(self):
        if (self.map_name == "map2.tmj"):
            if (self.player_sprite.center_x < 1):
                self.change_map("map4.tmj")
        if (self.map_name == "map4.tmj"):
            if (self.player_sprite.center_x > 37):
                self.change_map("map2.tmj")


    def change_map(self, map_name: str):
        """
        Updates the map to the given map name, and changes the player position

        PARAMETERS
        map_name (string): Fills in the file path as such: rf"views/maps-data/{map_name}"
        """
        # SET NEW MAP:
        map_name = rf"views/maps-data/{map_name}"

        # Layer Specific Options for the Tilemap
        layer_options = {
            LAYER_NAME_WALLS: {
                "use_spatial_hash": True,
            }, 
        }
            
        # Load in TileMap
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initiate New Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the player at these coordinates. The unit of measurement is in tiles (Each map total width of 38, height of 25)
        self.player_sprite = Player()

        # Check Player X position
        if (self.player_sprite.center_x < SCREEN_TILE_WIDTH - ((2 / 3) * SCREEN_TILE_WIDTH)): # If player enters door on the left wall,
            self.player_sprite.center_x = ((SCREEN_TILE_WIDTH - 3) * self.tile_map.tiled_map.tile_size[0]) # move them to the right
        elif (self.player_sprite.center_x > SCREEN_TILE_WIDTH - ((1 / 3) * SCREEN_TILE_WIDTH)): # If player enters door on the right wall,
            self.player_sprite.center_x = (3 * self.tile_map.tiled_map.tile_size[0]) # move them to the left
        # Else the player must have entered a door on the top or bottom, so keep the x value

        # Check Player Y position
        if (self.player_sprite.center_y < SCREEN_TILE_HEIGHT - ((2 / 3) * SCREEN_TILE_HEIGHT)): # If player enters door on the top wall,
            self.player_sprite.center_y = (3 * self.tile_map.tiled_map.tile_size[1]) # move them to the bottom
        elif (self.player_sprite.center_y > SCREEN_TILE_HEIGHT - ((1 / 3) * SCREEN_TILE_HEIGHT)):  # If player enters door on bottom wall,
            self.player_sprite.center_y = ((SCREEN_TILE_HEIGHT - 3) * self.tile_map.tiled_map.tile_size[1]) # move them to the top
        # Else the player must have entered a door on the left or right, so keep the y value

        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

    """
    def process_keychange(self):
        
        #Called when we change a key up/down or we move on/off a ladder.
        
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0
    """

    def on_key_press(self, key, modifiers):
        #Called whenever a key is pressed.

        if key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True


    
    def on_key_release(self, key, modifiers):
        #Called when the user releases a key.

        if key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False
    
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_pos = x, y


    """
    def center_camera_to_player(self, speed=0.2):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered, speed)
    """
    
    def on_update(self, delta_time):

        # Add some friction
        if self.player_sprite.change_x > FRICTION:
            self.player_sprite.change_x -= FRICTION
        elif self.player_sprite.change_x < -FRICTION:
            self.player_sprite.change_x += FRICTION
        else:
            self.player_sprite.change_x = 0
        if self.player_sprite.change_y > FRICTION:
            self.player_sprite.change_y -= FRICTION
        elif self.player_sprite.change_y < -FRICTION:
            self.player_sprite.change_y += FRICTION
        else:
            self.player_sprite.change_y = 0
        # Apply acceleration based on the keys pressed
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y += ACCELERATION_RATE
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y += -ACCELERATION_RATE
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x += -ACCELERATION_RATE
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x += ACCELERATION_RATE
        if self.player_sprite.change_x > MAX_SPEED:
            self.player_sprite.change_x = MAX_SPEED
        elif self.player_sprite.change_x < -MAX_SPEED:
            self.player_sprite.change_x = -MAX_SPEED
        if self.player_sprite.change_y > MAX_SPEED:
            self.player_sprite.change_y = MAX_SPEED
        elif self.player_sprite.change_y < -MAX_SPEED:
            self.player_sprite.change_y = -MAX_SPEED
        #self.player_sprite.update()

        dx = self.player_sprite.center_x - self.mouse_pos[0]
        dy = self.player_sprite.center_y - self.mouse_pos[1]
        angle = math.atan2(dy, dx)
        self.player_sprite.angle = math.degrees(angle)

        angle = math.atan2(dy, dx) + 1.5708  # Calculate the angle between the two sprites
        self.player_sprite.angle = math.degrees(angle)  # Convert the angle to degrees

        self.detect_map_change()         
        #Movement and game logic

        # Move the player with the physics engine
        self.physics_engine.update()
        """
        # Update animations
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        if self.can_shoot:
            if self.shoot_pressed:
                arcade.play_sound(self.shoot_sound)
                bullet = arcade.Sprite(
                    ":resources:images/space_shooter/laserBlue01.png",
                    SPRITE_SCALING_LASER,
                )

                if self.player_sprite.facing_direction == RIGHT_FACING:
                    bullet.change_x = BULLET_SPEED
                else:
                    bullet.change_x = -BULLET_SPEED

                bullet.center_x = self.player_sprite.center_x
                bullet.center_y = self.player_sprite.center_y

                self.scene.add_sprite(LAYER_NAME_BULLETS, bullet)

                self.can_shoot = False
        else:
            self.shoot_timer += 1
            if self.shoot_timer == SHOOT_SPEED:
                self.can_shoot = True
                self.shoot_timer = 0

        # Update Animations
        self.scene.update_animation(
            delta_time,
            [
                LAYER_NAME_COINS,
                LAYER_NAME_BACKGROUND,
                LAYER_NAME_PLAYER,
                LAYER_NAME_ENEMIES,
            ],
        )
        """
        # Update moving platforms, enemies, and bullets
        self.scene.update(
            [LAYER_NAME_ENEMIES]
        )
        # See if the enemy hit a boundary and needs to reverse direction.
        for enemy in self.scene.get_sprite_list(LAYER_NAME_ENEMIES):
            # Update the enemy's position to follow the player
            dx = self.player_sprite.center_x - enemy.center_x
            dy = self.player_sprite.center_y - enemy.center_y
            angle = math.atan2(dy, dx)
            enemy.angle = math.degrees(angle)
            # Calculate the velocity components based on the angle

            velocity_x = BASIC_ENEMY_SPEED * math.cos(angle)
            velocity_y = BASIC_ENEMY_SPEED * math.sin(angle)
            # Update the enemy's position
            enemy.center_x += velocity_x
            enemy.center_y += velocity_y
            # Update the rotation of the enemy sprite to face the player sprite
            angle = math.atan2(dy, dx) - 1.5708  # Calculate the angle between the two sprites
            enemy.angle = math.degrees(angle)  # Convert the angle to degrees

        """
        # See if the moving wall hit a boundary and needs to reverse direction.
        for wall in self.scene.get_sprite_list(LAYER_NAME_MOVING_PLATFORMS):

            if (
                wall.boundary_right
                and wall.right > wall.boundary_right
                and wall.change_x > 0
            ):
                wall.change_x *= -1
            if (
                wall.boundary_left
                and wall.left < wall.boundary_left
                and wall.change_x < 0
            ):
                wall.change_x *= -1
            if wall.boundary_top and wall.top > wall.boundary_top and wall.change_y > 0:
                wall.change_y *= -1
            if (
                wall.boundary_bottom
                and wall.bottom < wall.boundary_bottom
                and wall.change_y < 0
            ):
                wall.change_y *= -1

        """
        player_collision_list = arcade.check_for_collision_with_lists(
            self.player_sprite,
            [
                #self.scene.get_sprite_list(LAYER_NAME_COINS),
                self.scene.get_sprite_list(LAYER_NAME_ENEMIES),
            ],
        )
        """
        for bullet in self.scene.get_sprite_list(LAYER_NAME_BULLETS):
            hit_list = arcade.check_for_collision_with_lists(
                bullet,
                [
                    self.scene.get_sprite_list(LAYER_NAME_ENEMIES),
                    self.scene.get_sprite_list(LAYER_NAME_PLATFORMS),
                    self.scene.get_sprite_list(LAYER_NAME_MOVING_PLATFORMS),
                ],
            )

            if hit_list:
                bullet.remove_from_sprite_lists()

                for collision in hit_list:
                    if (
                        self.scene.get_sprite_list(LAYER_NAME_ENEMIES)
                        in collision.sprite_lists
                    ):
                        # The collision was with an enemy
                        collision.health -= BULLET_DAMAGE

                        if collision.health <= 0:
                            collision.remove_from_sprite_lists()
                            self.score += 100

                        # Hit sound
                        arcade.play_sound(self.hit_sound)

                return

            if (bullet.right < 0) or (
                bullet.left
                > (self.tile_map.width * self.tile_map.tile_width) * TILE_SCALING
            ):
                bullet.remove_from_sprite_lists()
        """
        # Loop through each coin we hit (if any) and remove it
        for collision in player_collision_list:

            if self.scene.get_sprite_list(LAYER_NAME_ENEMIES) in collision.sprite_lists:
                #game over and restart
                GameView.setup(self)
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
                self.right_pressed = False
                self.left_pressed = False
                self.down_pressed = False
                self.up_pressed = False
                self.player_sprite.update()    
                arcade.play_sound(self.game_over)
                self.window.show_view(self.window.views["game_over"])
                return
            """
            else:
                # Figure out how many points this coin is worth
                if "Points" not in collision.properties:
                    print("Warning, collected a coin without a Points property.")
                else:
                    points = int(collision.properties["Points"])
                    self.score += points

                # Remove the coin
                collision.remove_from_sprite_lists()
                arcade.play_sound(self.collect_coin_sound)
            """

        # Position the camera
        # self.center_camera_to_player()
