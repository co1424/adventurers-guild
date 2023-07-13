import arcade
import arcade.gui
from views.view import View

class WinView(View):
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
        arcade.set_background_color((53, 126, 199))

    def setup_buttons(self):
        self.v_box = arcade.gui.UIBoxLayout()

        
        play_button = arcade.gui.UIFlatButton(text="Restart", width=200)

        @play_button.event("on_click")
        def on_click_play(event):
            from views.view_main_menu import MainMenuView
            self.window.views["main_menu"] = MainMenuView()
            self.window.show_view(self.window.views["main_menu"])
            
            

        self.v_box.add(play_button.with_space_around(bottom=20))
        

        
        quit_button = arcade.gui.UIFlatButton(text="Stop", width=200)

        @quit_button.event("on_click")
        def on_click_quit(event):
            arcade.exit()

        self.v_box.add(quit_button)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            "You Win!",
            self.window.width / 2,
            self.window.height - 130,
            arcade.color.WHITE,
            font_size=100,
            anchor_x="center",
            anchor_y="center",
        )

        arcade.draw_text(
            "",
            self.window.width / 5,
            self.window.height - 250,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="left",
            anchor_y="center",
        )

        self.ui_manager.draw()
    pass 