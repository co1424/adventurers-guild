"""
Game View
"""
import math
import os
import random

import arcade

from constants import *
from entities.player import Player
from entities.enemy import Enemy
from entities.bullet import Bullet
from entities.ranged_enemy import Ranged_Enemy
from entities.basic_enemy import Basic_Enemy
from entities.boss import Boss
from entities.minion import Minion
from entities.key import Key
from entities.door import Door
from views.view import View
from entities.sword import Sword
from entities.health_boost import Health_Boost
from views.file import file

from views.view_game_over import GameOverView
from views.win_menu import WinView

from arcade.pymunk_physics_engine import PymunkPhysicsEngine



class GameView(View):


    def __init__(self):
        """
        Initializer for the game
        """
        super().__init__()

        # SET STARTING MAP:
        self.map_name = "map5.tmj"
        
        self.player_sprite = None
        self.game_over = False
        self.keys_pressed = set()
        self.player_sword_activated = False

        # Set player progress trackers
        self.door_open = False
        self.key_collected = False
        self.found_locked_door = False
        self.health_boost_collected = False

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
        self.bullet_list = arcade.SpriteList()
        self.enemy_timer = 0

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

        # random element
        self.rand = random.Random()


    def populate_sprites(self):
        """
        This method should be called when you load a new map.
        It initializes the enemies, keys, doors, and pickups from the tilemap
        """

        # -- Enemies
        if LAYER_NAME_ENEMIES in self.tile_map.object_lists:
            enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]
            self.scene.add_sprite_list(LAYER_NAME_ENEMIES)
            
            for my_object in enemies_layer:
                cartesian = self.tile_map.get_cartesian(
                    my_object.shape[0], my_object.shape[1]
                )

                # Check the name from the tilemap with the
                enemy_name = my_object.name
                if enemy_name not in self.enemy_kill_dict:
                    # Add the new enemy to the our dictionary
                    self.enemy_kill_dict[enemy_name] = False # This means not killed

                if not self.enemy_kill_dict[enemy_name]:
                    #  The enemy is not killed. Add them to the map!
                    enemy_type = my_object.properties["type"]

                    # Determine enemy type
                    if enemy_type == "basic":
                        enemy = Basic_Enemy(enemy_name)
                    elif enemy_type == "ranged":
                        enemy = Ranged_Enemy(enemy_name)
                    elif enemy_type == "boss":
                        enemy = Boss(enemy_name)

                    # Determine enemy position (x and y)   
                    enemy.center_x = math.floor(
                        cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                    )
                    enemy.center_y = math.floor(
                        (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                    )
                    # Add it to the enemy sprite list!
                    self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)               
                
        # -- Keys
        if LAYER_NAME_KEYS in self.tile_map.object_lists and self.key_collected == False:
            keys_layer = self.tile_map.object_lists[LAYER_NAME_KEYS]

            for my_object in keys_layer:
                cartesian = self.tile_map.get_cartesian(
                    my_object.shape[0], my_object.shape[1]
                )

                key = Key()
                key.center_x = math.floor(
                    cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                )
                key.center_y = math.floor(
                    (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                )

                self.scene.add_sprite(LAYER_NAME_KEYS, key)

        # -- Doors
        if LAYER_NAME_DOORS in self.tile_map.object_lists and self.door_open == False:
            doors_layer = self.tile_map.object_lists[LAYER_NAME_DOORS]

            for my_object in doors_layer:
                cartesian = self.tile_map.get_cartesian(
                    my_object.shape[0], my_object.shape[1]
                )

                door = Door()
                door.center_x = math.floor(
                    cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                )
                door.center_y = math.floor(
                    (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                )

                self.scene.add_sprite(LAYER_NAME_DOORS, door)

        # -- Health Boost
        if LAYER_NAME_HEALTH_BOOST in self.tile_map.object_lists and self.health_boost_collected == False:
            health_boost_layer = self.tile_map.object_lists[LAYER_NAME_HEALTH_BOOST]
            
            for my_object in health_boost_layer:
                cartesian = self.tile_map.get_cartesian(
                    my_object.shape[0], my_object.shape[1]
                )

                health_boost = Health_Boost()
                health_boost.center_x = math.floor(
                    cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                )
                health_boost.center_y = math.floor(
                    (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                )
               
                self.scene.add_sprite(LAYER_NAME_HEALTH_BOOST, health_boost)


    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        super().setup()

        self.save = file.read_from_file("save.json")

        self.enemy_kill_dict = {} # This dictionary keeps track of all enemies and whether or not they are killed

        # Layer Specific Options for the Tilemap
        layer_options = {
            LAYER_NAME_WALLS: {
                "use_spatial_hash": True,
            }, 
        }
        
        # Makes sure game over exists
        if "game_over" not in self.window.views:
            file.save_to_file(self.save)
            self.window.views["game_over"] = GameOverView()

        # Load in TileMap
        self.tile_map = arcade.load_tilemap(rf"views/maps-data/{self.map_name}", TILE_SCALING, layer_options)

        # Initiate New Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Keep track of the score
        self.score = 0
        
        # Set up the player at these coordinates. The unit of measurement is in tiles (Each map total width of 38, height of 25)
        self.player_sprite = Player()
        self.player_sprite.center_x = (
            (SCREEN_TILE_WIDTH / 2) * self.tile_map.tiled_map.tile_size[0] # Middle of the screen (X)
        )
        self.player_sprite.center_y = (
            3 * self.tile_map.tiled_map.tile_size[1] # Bottom of the screen (Y)
        )
        # Adds the player to the scene
        self.player_sprite.angle = 0
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)
        
        # Calculate the right edge of the my_map in pixels
        self.end_of_map = self.tile_map.tiled_map.map_size.width * GRID_PIXEL_SIZE
        
        self.populate_sprites() # Spawns enemies, keys, doors, pickups
        

        # Triggers for the game
        self.door_open = False
        self.key_collected = False
        self.found_locked_door = False
        self.health_boost_collected = False


        self.setup_physics_engine()


    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        arcade.start_render()

        # Activate the game camera
        #self.camera.use()

        # Draw our Scene
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        # self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            40,
            8,
            (255,255,255),
            18,
            font_name="consolas"
        )

        # Draw our health on the screen, scrolling it with the viewport
        health_text = f"Health: {self.player_sprite.get_health()}"
        arcade.draw_text(
            health_text,
            250,
            8,
            (255,255,255),
            18,
            font_name="consolas"
        )


        if (self.found_locked_door == True and self.player_sprite.check_key() == False and self.door_open == False):
            locked_text = "The door is locked."
            arcade.draw_text(
                locked_text,
                900,
                8,
                (255,255,255),
                18,
                font_name="consolas"
            )

        # Notify the player when they have the key
        key_text = "You found a key!"
        if (self.player_sprite.check_key() == True):
            arcade.draw_text(
                key_text,
                900,
                8,
                (255,255,255),
                18,
                font_name="consolas"
            )


        self.bullet_list.draw()

        # Draw hit boxes.
        # for wall in self.wall_list:
        #     wall.draw_hit_box(arcade.color.BLACK, 3)
        # 
        # self.player_sprite.draw_hit_box(arcade.color.RED, 3)

    def detect_map_change(self):
        # Current Map: Map1
        if (self.map_name == "map1.tmj"):
            if (self.player_sprite.center_y < 1): # Bottom Door
                self.change_map("map4.tmj")
            if (self.player_sprite.center_x > SCREEN_WIDTH - 1): # Right Door
                self.change_map("map2.tmj")

        # Current Map: Map2
        if (self.map_name == "map2.tmj"):
            if (self.player_sprite.center_x < 1): # Left Door
                self.change_map("map1.tmj")

        # Current Map: Map3
        if (self.map_name == "map3.tmj"):
            if (self.player_sprite.center_y < 1): # Bottom Door
                self.change_map("map6.tmj")

        # Current Map: Map4
        if (self.map_name == "map4.tmj"):
            if (self.player_sprite.center_x > SCREEN_WIDTH - 1): # Right Door
                self.change_map("map5.tmj")
            if (self.player_sprite.center_y > SCREEN_HEIGHT - 1): # Top Door
                self.change_map("map1.tmj")

        # Current Map: Map5
        if (self.map_name == "map5.tmj"):
            if (self.player_sprite.center_x < 1): # Left Door
                self.change_map("map4.tmj")
            if (self.player_sprite.center_x > SCREEN_WIDTH - 1): # Right Door
                self.change_map("map6.tmj")

        # Current Map: Map6
        if (self.map_name == "map6.tmj"):
            if (self.player_sprite.center_x < 1): # Left Door
                self.change_map("map5.tmj")
            if (self.player_sprite.center_y > SCREEN_HEIGHT - 1): # Top Door
                self.change_map("map3.tmj")


    def change_map(self, map_name: str):
        """
        Updates the map to the given map name, and changes the player position

        PARAMETERS
        map_name (string): Fills in the file path as such: rf"views/maps-data/{map_name}"
        """       
        self.player_sword_activated = False
        self.enemy_list = []
        
        while len(self.bullet_list) > 0: # Remove all bullets
            self.bullet_list.pop()
    
        self.map_name = map_name

        # Layer Specific Options for the Tilemap
        layer_options = {
            LAYER_NAME_WALLS: {
                "use_spatial_hash": True,
            }, 
        }
            
        # Load in TileMap
        self.tile_map = arcade.load_tilemap(rf"views/maps-data/{map_name}", TILE_SCALING, layer_options)

        # Initiate New Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the player at these coordinates. The unit of measurement is in tiles (Each map total width of 38, height of 25)
        #self.player_sprite = Player()
        
        # Check Player X position
        if (self.player_sprite.center_x < SCREEN_WIDTH - ((2 / 3) * SCREEN_WIDTH)): # If player enters door on the left wall,
            self.player_sprite.center_x = ((SCREEN_TILE_WIDTH - 3) * self.tile_map.tiled_map.tile_size[0]) # move them to the right
        elif (self.player_sprite.center_x > SCREEN_WIDTH - ((1 / 3) * SCREEN_WIDTH)): # If player enters door on the right wall,
            self.player_sprite.center_x = (3 * self.tile_map.tiled_map.tile_size[0]) # move them to the left
        # Else the player must have entered a door on the top or bottom, so keep the x value

        # Check Player Y position
        if (self.player_sprite.center_y < SCREEN_HEIGHT - ((2 / 3) * SCREEN_HEIGHT)): # If player enters door on the top wall,
            self.player_sprite.center_y = ((SCREEN_TILE_HEIGHT - 3) * self.tile_map.tiled_map.tile_size[0]) # move them to the bottom
        elif (self.player_sprite.center_y > SCREEN_HEIGHT - ((1 / 3) * SCREEN_HEIGHT)):  # If player enters door on bottom wall,
            self.player_sprite.center_y = (1 * self.tile_map.tiled_map.tile_size[1]) # move them to the top
        # Else the player must have entered a door on the left or right, so keep the y value
        self.player_sprite.angle = 0
        
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        self.populate_sprites() # Spawns enemies, keys, doors, pickups
        
        self.setup_physics_engine() # gets things set up for physics
        
    
    def setup_physics_engine(self):
        # needed for each map of the level
        self.physics_engine = arcade.PymunkPhysicsEngine()

        def enemy_player_handler(player, enemy, arbiter, space, data):
            # Damages the player, bounces back the enemy, sets i-Frames,
            # and starts game over if player is dead
            dx = self.player_sprite.center_x - enemy.center_x
            dy = self.player_sprite.center_y - enemy.center_y
            angle = math.atan2(dy, dx)
            # Calculate the velocity components based on the angle

            velocity_x = BASIC_ENEMY_SPEED * math.cos(angle) * 20
            velocity_y = BASIC_ENEMY_SPEED * math.sin(angle) * 20
            # Update the enemy's position
            force = (-velocity_x, -velocity_y)
            self.physics_engine.apply_force(enemy, force)

            if not self.player_sprite.is_Invulnerable():
                self.player_sprite.change_health(-1)

            self.player_sprite.set_invulnerable_seconds(.2)

            if self.player_sprite.health <= 0:
                # initiates game over
                file.save_to_file(self.save)
                arcade.play_sound(self.game_over)
                self.window.show_view(self.window.views["game_over"])



        def key_player_handler(player, key, arbiter, space, data):
            # registers the key as being picked up by the player
            self.key_collected = True
            self.physics_engine.remove_sprite(key)
            self.scene.get_sprite_list(LAYER_NAME_KEYS).remove(key)
            self.player_sprite.collect_key()


        def health_boost_player_handler(player, health_boost, arbiter, space, data):
            # Adds health to the player when touched by the player
            self.health_boost_collected = True
            self.physics_engine.remove_sprite(health_boost)
            self.scene.get_sprite_list(LAYER_NAME_HEALTH_BOOST).remove(health_boost)
            self.player_sprite.reset_health()

        
        def door_player_handler(player, door, arbiter, space, data):
            # Removes the door if touched by the player while having the key
            if (self.player_sprite.check_key() == True):
                self.door_open = True #ensures the door doesn't respawn
                self.physics_engine.remove_sprite(door)
                self.scene.get_sprite_list(LAYER_NAME_DOORS).remove(door)
                self.player_sprite.use_key()
            else:
                self.found_locked_door = True      


        
        def bullet_handler(player, bullet, arbiter, space, data):
            # Deletes the bullet, damages the player, and ends the game if it kills the player
            self.bullet_list.remove(bullet)
            self.physics_engine.remove_sprite(bullet)

            if not self.player_sprite.is_Invulnerable():
                self.player_sprite.change_health(-1)

            self.player_sprite.set_invulnerable_seconds(.2)

            if self.player_sprite.health <= 0:
                file.save_to_file(self.save)
                arcade.play_sound(self.game_over)
                self.window.show_view(self.window.views["game_over"])



        def bullet_wall_handler(wall, bullet, arbiter, space, data):
            # Deletes the bullet if it hits a wall
            self.bullet_list.remove(bullet)
            self.physics_engine.remove_sprite(bullet)
        
        def bullet_enemy_handler(enemy, bullet, arbiter, space, data):
            # deletes the bullet if it hits anything besides a ranged enemy
            if not isinstance(enemy, Ranged_Enemy):
                self.bullet_list.remove(bullet)
                self.physics_engine.remove_sprite(bullet)

        # Adds all the defined handlers to the physics engine
        self.physics_engine.add_collision_handler("player", "enemy", post_handler=enemy_player_handler)
        self.physics_engine.add_collision_handler("player", "key", post_handler=key_player_handler)
        self.physics_engine.add_collision_handler("player", "health_boost", post_handler=health_boost_player_handler)
        self.physics_engine.add_collision_handler("player", "door", post_handler=door_player_handler)
        self.physics_engine.add_collision_handler("player", "bullet", post_handler=bullet_handler)
        self.physics_engine.add_collision_handler("wall", "bullet", post_handler=bullet_wall_handler)
        self.physics_engine.add_collision_handler("enemy", "bullet", post_handler=bullet_enemy_handler)

        # Adds the player to the physics engine
        self.physics_engine.add_sprite(
            self.player_sprite,
            friction=0.6,
            moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
            damping=0.01,
            collision_type="player",
            max_velocity=400
        )

        # adds all walls in the tile map to the physics engine
        self.physics_engine.add_sprite_list(
            self.scene.get_sprite_list(LAYER_NAME_WALLS),
            friction=0.6,
            collision_type="wall",
            body_type=PymunkPhysicsEngine.STATIC
        )

        # Checks if there's a door in the tilemap and that it hasn't already been opened
        if LAYER_NAME_DOORS in self.tile_map.object_lists and self.door_open == False:
            self.physics_engine.add_sprite_list(
                self.scene.get_sprite_list(LAYER_NAME_DOORS),
                friction=0.6,
                collision_type="door",
                body_type=PymunkPhysicsEngine.STATIC
            )

        # Adds every enemy in the tile map by type
        if LAYER_NAME_ENEMIES in self.tile_map.object_lists:
            for enemy in self.scene.get_sprite_list(LAYER_NAME_ENEMIES):
                if isinstance(enemy, Basic_Enemy):       

                    self.physics_engine.add_sprite(
                        enemy,
                        friction=0.6,
                        moment_of_intertia=PymunkPhysicsEngine.MOMENT_INF,
                        damping=0.01,
                        collision_type="enemy",
                        #max_velocity=200
                    )
                
                if isinstance(enemy, Ranged_Enemy):   
                    self.physics_engine.add_sprite(
                        enemy,
                        friction=0.6,
                        body_type=PymunkPhysicsEngine.STATIC,
                        damping=0.01,
                        collision_type="enemy",
                        #max_velocity=200
                )
                    
                if isinstance(enemy, Boss):
                    self.physics_engine.add_sprite(
                        enemy,
                        friction=0.6,
                        moment_of_intertia=PymunkPhysicsEngine.MOMENT_INF,
                        damping=0.01,
                        collision_type="boss",
                        mass=50,
                    )

        # Checks if there's a key and that it already hasn't been collected
        if LAYER_NAME_KEYS in self.tile_map.object_lists and self.key_collected == False:       
            for key in self.scene.get_sprite_list(LAYER_NAME_KEYS):
                self.physics_engine.add_sprite(
                    key,
                    friction=0.6,
                    moment_of_intertia=PymunkPhysicsEngine.MOMENT_INF,
                    damping=0.01,
                    collision_type="key",
                    #max_velocity=200
            )
        # Checks if there's a health boost on the screen
        if LAYER_NAME_HEALTH_BOOST in self.tile_map.object_lists and self.health_boost_collected == False:       
            for health_boost in self.scene.get_sprite_list(LAYER_NAME_HEALTH_BOOST):
                self.physics_engine.add_sprite(
                    health_boost,
                    friction=0.6,
                    moment_of_intertia=PymunkPhysicsEngine.MOMENT_INF,
                    damping=0.01,
                    collision_type="health_boost",
                    #max_velocity=200
            )

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

        # Activates a sword swing if it hasn't been started already
        if key == arcade.key.SPACE:
            if not self.player_sword_activated:
                # see sword.py for more info on this call
                sword = Sword(
                    self.player_sprite.center_x,
                    self.player_sprite.center_y,
                    self.player_sprite.angle
                    )
                self.scene.add_sprite(LAYER_NAME_SWORD, sword)
                self.player_sprite.start_swing_animation()
                self.player_sword_activated = True


    
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
        # Grabs the mouse position to calculate player rotation
        self.mouse_pos = x, y

    
    def on_update(self, delta_time):
        # DO NOT TOUCH! NEEDED FOR COLLISION CHECKS AND ROTATION HERE
        self.physics_engine.step()

        # Apply acceleration based on the keys pressed
        if self.up_pressed and not self.down_pressed:
            force = (0, ACCELERATION_RATE)
            self.physics_engine.apply_force(self.player_sprite, force)
        elif self.down_pressed and not self.up_pressed:
            force = (0, -ACCELERATION_RATE)
            self.physics_engine.apply_force(self.player_sprite, force)
        if self.left_pressed and not self.right_pressed:
            force = (-ACCELERATION_RATE, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
        elif self.right_pressed and not self.left_pressed:
            force = (ACCELERATION_RATE, 0)
            self.physics_engine.apply_force(self.player_sprite, force)

        dx = self.player_sprite.center_x - self.mouse_pos[0]
        dy = self.player_sprite.center_y - self.mouse_pos[1]
        angle = math.atan2(dy, dx)
        self.player_sprite.angle = math.degrees(angle)

        angle = math.atan2(dy, dx) + 1.5708  # Calculate the angle between the two sprites
        self.player_sprite.angle = math.degrees(angle)  # Convert the angle to degrees
        
        # used for all enemy checks later
        enemy_list = self.scene.get_sprite_list(LAYER_NAME_ENEMIES)

        if self.player_sword_activated:
            swords = self.scene.get_sprite_list(LAYER_NAME_SWORD)
            for sword in swords: # Strange, but needed since it crashes if you try and access the only sword in the list
                for enemy in arcade.check_for_collision_with_list(sword, enemy_list):
                    # Checks for collisions with the sword with all enemies every frame the sword is active
                    if enemy.is_hit():
                        
                        dx = self.player_sprite.center_x - enemy.center_x
                        dy = self.player_sprite.center_y - enemy.center_y
                        angle = math.atan2(dy, dx)
                        enemy.angle = math.degrees(angle)
                        # Calculate the velocity components based on the angle

                        velocity_x = BASIC_ENEMY_SPEED * math.cos(angle) * 20
                        velocity_y = BASIC_ENEMY_SPEED * math.sin(angle) * 20

                        force = (-velocity_x, -velocity_y)
                        # Applies knockback movement to the enemy hit
                        self.physics_engine.apply_force(enemy, force)
                        enemy.change_health(-1)
                        enemy.start_hit_timer()

                        arcade.play_sound(self.hit_sound)
                        self.score += 5


            # if the sword is done swinging
            unfinished = self.player_sprite.update_animation(sword)

            if not unfinished: 
                self.scene.remove_sprite_list_by_name(LAYER_NAME_SWORD)
                # Stops checking if enemies are touching the sword
                self.player_sword_activated = False
                        

        for enemy in enemy_list:
            # Update the enemy's position to follow the player
            dx = self.player_sprite.center_x - enemy.center_x
            dy = self.player_sprite.center_y - enemy.center_y
            angle = math.atan2(dy, dx)
            enemy.angle = math.degrees(angle)
            # Calculate the velocity components based on the angle

            if isinstance(enemy, Basic_Enemy) or isinstance(enemy, Minion):
                
                # Calculate the velocity components based on the angle

                velocity_x = BASIC_ENEMY_SPEED * math.cos(angle)
                velocity_y = BASIC_ENEMY_SPEED * math.sin(angle)
                # Update the enemy's position
                force = (velocity_x, velocity_y)
                self.physics_engine.apply_force(enemy, force)

                # Update the rotation of the enemy sprite to face the player sprite
                angle = math.atan2(dy, dx) - 1.5708  # Calculate the angle between the two sprites
                enemy.angle = math.degrees(angle)  # Convert the angle to degrees

            if isinstance(enemy, Ranged_Enemy):
                
                # Update the rotation of the enemy sprite to face the player sprite
                angle = math.atan2(dy, dx) - 1.5708  # Calculate the angle between the two sprites
                enemy.angle = math.degrees(angle)  # Convert the angle to degrees

                
                # Increase the enemy's timer
                self.enemy_timer += delta_time

                # Check if the enemy can attack. If so, shoot a bullet from the
                # enemy towards the player
                if self.enemy_timer >= ENEMY_ATTACK_COOLDOWN:
                    self.enemy_timer = 0

                    # Create the bullet
                    bullet = Bullet()

                    # Set the bullet's position
                    bullet.position = enemy.position

                    # Set the bullet's angle to face the player
                    diff_x = self.player_sprite.center_x - enemy.center_x
                    diff_y = self.player_sprite.center_y - enemy.center_y
                    angle = math.atan2(diff_y, diff_x)
                    angle_deg = math.degrees(angle) - 90
                    if angle_deg < 0:
                        angle_deg += 360
                    bullet.angle = angle_deg

                    # Give the bullet a velocity towards the player
                    x = math.cos(angle) * BULLET_SPEED
                    y = math.sin(angle) * BULLET_SPEED

                    # Add the bullet to the bullet list
                    self.bullet_list.append(bullet)
                    self.physics_engine.add_sprite(
                        bullet,
                        friction=0.6,
                        moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
                        collision_type="bullet"
                    )

                    # Sets speed of the bullet
                    self.physics_engine.set_velocity(bullet, (x, y))

            if isinstance(enemy, Boss):
                enemy.angle -= 90 # Adjustment for Sprite orientation
                dir_x, dir_y = enemy.get_direction() # See boss.py for more about this function
                if enemy.should_spawn_minions(): # Checks if the minion timer is up 
                    minions_to_spawn = self.rand.randint(3, 6)
                    # Spawns a random amount of minions
                    for _ in range(minions_to_spawn):
                        minion = Minion()
                        minion.center_x = enemy.center_x + self.rand.randint(-10, 10)
                        minion.center_y = enemy.center_y + self.rand.randint(-10, 10)

                        # Adds each minion to the scene
                        self.scene.add_sprite(LAYER_NAME_ENEMIES, minion)
                        # Adds each minion to the physics engine
                        self.physics_engine.add_sprite(
                            minion,
                            friction=0.6,
                            moment_of_intertia=PymunkPhysicsEngine.MOMENT_INF,
                            damping=0.01,
                            collision_type="enemy",
                        )

                dir_x *= BOSS_SPEED
                dir_y *= BOSS_SPEED

                # Applies movement to the boss
                self.physics_engine.apply_force(enemy, (dir_x, dir_y))






            # returns true or false, but meant to decrease invincibility counter.
            enemy.is_hit()

            # decides what to do with a dead enemy
            if enemy.health <= 0:
                self.save += 1

                """
                each isinstance is for a certain enemy type, and performs different
                actions accordingly
                """
                if isinstance(enemy, Basic_Enemy):
                    self.score += 50
                    self.enemy_kill_dict[enemy.name] = True # Mark as dead, so it doesn't respawn.
                    enemy_list.remove(enemy)
                    self.physics_engine.remove_sprite(enemy)

                elif isinstance(enemy, Minion):
                    self.score += 10
                    enemy_list.remove(enemy)
                    self.physics_engine.remove_sprite(enemy)
                
                elif isinstance(enemy, Ranged_Enemy):
                    self.score += 100
                    self.enemy_kill_dict[enemy.name] = True
                    enemy_list.remove(enemy)
                    self.physics_engine.remove_sprite(enemy)

                elif isinstance(enemy, Boss):
                    self.score += 500
                    self.enemy_kill_dict[enemy.name] = True
                    enemy_list.remove(enemy)
                    self.physics_engine.remove_sprite(enemy)

                    file.save_to_file(self.save)
                    self.window.views["win_screen"] = WinView()
                    self.window.show_view(self.window.views["win_screen"])


        self.detect_map_change()