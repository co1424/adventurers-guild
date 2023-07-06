"""
Main Menu
"""
import arcade
import arcade.gui
import random

#from views import PauseView
from views.view_game import GameView
from views.view_name import NameView
#from view_game_over import GameOverView
from views.view import View

from views.file import file



class MainMenuView(View):
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
        self.v_box = arcade.gui.UIBoxLayout()
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

        @play_button.event("on_click")
        def on_click_play(event):
            self.window.views["name"] = NameView()
                    #self.window.views["game_over"] = GameOverView()
                    #self.window.views["pause"] = PauseView()
            self.window.show_view(self.window.views["name"])

        self.v_box.add(play_button.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton(text="Stop", width=200, style=custom_style)

        @quit_button.event("on_click")
        def on_click_quit(event):
            arcade.exit()

        self.v_box.add(quit_button)

    def animate_text_wobble(self):
        if (self.wobble_forward == True):
            self.text_wobble += 0.1
            if (self.text_wobble >= 8):
                self.wobble_forward = False
        else:
            self.text_wobble -= 0.1
            if (self.text_wobble <= -4):
                self.wobble_forward = True
                

    def animate_text_grow(self):
        if (self.grow_forward == True):
            self.text_grow += 0.5
            if (self.text_grow >= 4):
                self.grow_forward = False
        else:
            self.text_grow -= 0.25
            if (self.text_grow <= -4):
                self.grow_forward = True

    def animate_text_glitch_visible(self):
        flicker_chance_on = 0.99  # Adjust this value to control the chance of the light staying on
        flicker_chance_off = 0.9  # Adjust this value to control the chance of the light staying off
        
        if self.light_on:
            self.subheader_color = (255, 255, 255)  # Light is on (white color)
            if random.random() > flicker_chance_on:
                self.light_on = False
        else:
            self.subheader_color = (38, 38, 38)  # Light is off (black color)
            if random.random() > flicker_chance_off:
                self.light_on = True

    def animate_text_glitch_size(self):
        if (self.glitch_grow_forward == True):
            self.text_glitch_grow += 0.1
            if (self.text_glitch_grow >= 1):
                self.glitch_grow_forward = False
        else:
            self.text_glitch_grow -= 0.1
            if (self.text_glitch_grow <= -1):
                self.glitch_grow_forward = True
                        
    
    def animate_slide_in(self):
        if (self.slide_from_distance1 >= 0):
            self.slide_from_distance1 -= 10

        if (self.slide_from_distance2 >= 0):
            self.slide_from_distance2 -= 10
        
        if (self.slide_from_distance3 >= 0):
            self.slide_from_distance3 -= 14
        
        


    def on_update(self, delta_time):
        self.animate_text_wobble()
        self.animate_text_grow()
        self.animate_slide_in()
        self.animate_text_glitch_visible()
        self.animate_text_glitch_size()        
        
        self.time_elapsed += delta_time


    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            "Code Catacombs",
            self.window.width / 2,
            self.window.height - 125 + self.slide_from_distance1,
            (255,255,255),
            font_size=72,
            anchor_x="center",
            anchor_y="center",
            font_name="Consolas"

        )

        arcade.draw_text(
            "Code Catacombs",
            (self.window.width / 2) + 1,
            self.window.height - 127 + self.slide_from_distance1,
            (134,9,195),
            font_size=72,
            anchor_x="center",
            anchor_y="center",
            font_name="Consolas"
        )

        arcade.draw_text(
            "The Debugging Dungeon",
            self.window.width / 2,
            self.window.height - 220 + self.text_glitch_grow + self.slide_from_distance1,
            self.subheader_color,
            font_size=30 + self.text_glitch_grow,
            anchor_x="center",
            anchor_y="center",
            font_name="Courier New"
        )


        arcade.draw_text(
            "A game by The Adventurer's Guild",
            self.window.width / 2,
            self.window.height / 2 - 320 - self.slide_from_distance2,
            (255,255,255),
            font_size=15,
            anchor_x="center",
            anchor_y="center",
            font_name="Consolas"
        )

        self.ui_manager.draw()

        arcade.draw_text(
            "Total bugs debugged:",
            self.window.width / 5 - self.slide_from_distance3,
            self.window.height - 400,
            (255,255,255),
            font_size=18,
            anchor_x="center",
            anchor_y="center",
            font_name="Consolas",
            rotation=self.text_wobble
        )

        arcade.draw_text(
            "Total bugs debugged:",
            (self.window.width / 5) + 1 - self.slide_from_distance3,
            self.window.height - 400,
            (134,9,195),
            font_size= 18,
            anchor_x="center",
            anchor_y="center",
            font_name="Consolas",
            rotation=self.text_wobble
        )
        
        arcade.draw_text(
            self.save[0], # Number from storage
            self.window.width / 5 - self.slide_from_distance3,
            self.window.height - 450 + self.text_grow,
            (255,255,255),
            font_size=36 + self.text_grow,
            anchor_x="center",
            anchor_y="center",
            font_name="Consolas"
        )

        #arcade.draw_text(
        #    self.save,
        #    (self.window.width / 5) + 1,
        #    self.window.height - 450,
        #    (255,0,0),
        #    font_size=36 + self.text_grow,
        #    anchor_x="center",
        #    anchor_y="center",
        #    font_name="Consolas"
        #)