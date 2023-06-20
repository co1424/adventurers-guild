"""
Main Menu
"""
import arcade
import arcade.gui

#from views import PauseView
from views.view_game import GameView
#from view_game_over import GameOverView
from views.view import View


class MainMenuView(View):
    def __init__(self):
        super().__init__()

        # A Vertical BoxGroup to align Buttons
        self.v_box = None

    def setup(self):
        super().setup()
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
            "font_color_pressed": arcade.color.WHITE
        }
        play_button = arcade.gui.UIFlatButton(text="Step Into", width=200, style=custom_style)

        @play_button.event("on_click")
        def on_click_play(event):
            self.window.views["game"] = GameView()
                    #self.window.views["game_over"] = GameOverView()
                    #self.window.views["pause"] = PauseView()
            self.window.show_view(self.window.views["game"])

        self.v_box.add(play_button.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton(text="Stop", width=200, style=custom_style)

        @quit_button.event("on_click")
        def on_click_quit(event):
            arcade.exit()

        self.v_box.add(quit_button)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            "// Title goes here",
            self.window.width / 2,
            self.window.height - 125,
            (134,9,195),
            font_size=44,
            anchor_x="center",
            anchor_y="center",
        )

        self.ui_manager.draw()