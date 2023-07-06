"""
Name Menu
"""
import arcade
import arcade.gui
import random

#from views import PauseView
from views.view_game import GameView
#from view_game_over import GameOverView
from views.view import View
from constants import *

from views.file import file

player_name = ""

class NameView(View):
    def __init__(self):
        super().__init__()

        # A Vertical BoxGroup to align Buttons
        self.v_box = None
        self.time_elapsed = 0.0

        self.subheader_color = (255,255,255)
        self.light_on = True

        self.slide_from_distance1 = 300
        self.slide_from_distance2 = 400
        self.slide_from_distance3 = 950

        self.text_wobble = 0
        self.wobble_forward = True

        self.text_grow = 0
        self.grow_forward = True

        self.text_glitch_grow = 0
        self.glitch_grow_forward = True


    def setup(self):
        super().setup()

        self.save = file.read_from_file("save.json")

        self.ui_manager = arcade.gui.UIManager()

        self.setup_buttons()

        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box
            )
        )

    def on_show_view(self):
        arcade.set_background_color((38,38,38))

    def setup_buttons(self):
        global player_name
        self.v_box = arcade.gui.UIBoxLayout()

        bg_tex = arcade.load_texture(":resources:gui_basic_assets/window/grey_panel.png")

        custom_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": (134,9,195),
            "bg_color": arcade.color.BLACK,
            # used if button is pressed
            "bg_color_pressed": arcade.color.BLACK,
            "border_color_pressed": arcade.color.WHITE,  # also used when hovered
            "font_color_pressed": arcade.color.WHITE,
            "font_name": "Consolas"
            
        }
        
        play_button = arcade.gui.UIFlatButton(text="Step Into", width=200, style=custom_style)
    
        input_text = arcade.gui.UIInputText(x=340, y=200, width=200, height=25, text="Enter Name Here", font_name=custom_style["font_name"][0], font_size=15, text_color=arcade.color.WHITE)

        self.v_box.add(input_text)
        self.v_box.add(play_button.with_space_around(top= 20,bottom= 20))


        @play_button.event("on_click")
        def on_click_play(event):
            global player_name
            player_name = input_text.text
            print(player_name)

            self.window.views["game"] = GameView()
            self.window.views["game"].player_name = player_name
            self.window.show_view(self.window.views["game"])

        
    def on_draw(self):
        arcade.start_render()
        self.ui_manager.draw()

        arcade.gui.UIInputText
