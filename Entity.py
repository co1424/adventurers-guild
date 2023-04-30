import arcade

class Entity():

    def __init__(self, sprite='', x=200, y=200, max_acceleration=-1, max_speed=-1):
        self.__sprite = sprite
        self.__x = x
        self.__y = y
        self.__max_acceleration = max_acceleration
        self.__max_speed = max_speed
    
    def Draw(self):
        self.__sprite.draw()
        pass

    def Move(self, objects_touching_sprite):
        pass

    def Attack(self):
        pass

    def Check_Collisions(self, sprite_list):
        entities_touching_object = arcade.check_for_collision_with_list(self.__sprite, sprite_list)
        self.Move(entities_touching_object)
        pass
