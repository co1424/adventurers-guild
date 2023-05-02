import arcade

class Entity(arcade.Sprite):
    def __init__(self, name_folder, name_file):
            super().__init__()
            img = f":resources:images/tiles/torch1.png"
            self.player_list = arcade.SpriteList()
            self.player_sprite = arcade.Sprite(img)
            

            #self.set_hit_box(self.texture.hit_box_points)
    #self.player_list = arcade.SpriteList()  
    
    def add(self):
        self.player_list.append(self.player_sprite)
        pass

    def Move(self, objects_touching_sprite):
        pass

    def Attack(self):
        pass

    def Check_Collisions(self, sprite_list):
        entities_touching_object = arcade.check_for_collision_with_list(self.__sprite, sprite_list)
        self.Move(entities_touching_object)
        pass
