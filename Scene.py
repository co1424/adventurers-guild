import arcade

class Scene:
    def __init__(self, output_service):
        self.__output_service = output_service
        self.entity_list = []

    def draw_scene(self):
        