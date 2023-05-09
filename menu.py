import arcade
import arcade.gui
"""
class Menus():

    def start_menu(self):
        #get the GUI manager set up
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.AMAZON)
                
        self.v_box = arcade.gui.UIBoxLayout()

        #Create title
        menu_title = arcade.gui.UITextArea(text="A Title",
                                        width=100,
                                        height=40,
                                        font_size=24)
        self.v_box.add(menu_title.with_space_around(bottom=20))

        # Create the buttons
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        tutorial_button = arcade.gui.UIFlatButton(text="Tutorial", width=200)
        self.v_box.add(tutorial_button.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton(text="Quit Game", width=200)
        self.v_box.add(quit_button.with_space_around(bottom=20))

        start_button.on_click = self.on_click_start
        tutorial_button.on_click = self.on_click_tutorial
        quit_button.on_click = self.on_click_quit

        # Hold the v_box that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
"""

class MainView(arcade.View):
    """This is the class where your normal game would go."""

    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()

        #Create title
        menu_title = arcade.gui.UITextArea(text="A Title",
                                        width=100,
                                        height=40,
                                        font_size=24)
        self.v_box.add(menu_title.with_space_around(bottom=20))

        # Create buttons
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        switch_menu_button = arcade.gui.UIFlatButton(text="Tutorial", width=200)
        self.v_box.add(switch_menu_button.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton(text="Quit Game", width=200)
        self.v_box.add(quit_button.with_space_around(bottom=20))

        # Initialise the buttons with an on_click event.
        @start_button.event("on_click")
        def on_click_start_button(event):
            menu_view = GameView(self)
            self.window.show_view(menu_view)

        @switch_menu_button.event("on_click")
        def on_click_switch_button(event):
            # Passing the main view into menu view as an argument.
            menu_view = MenuView(self)
            self.window.show_view(menu_view)

        @quit_button.event("on_click")
        def on_click_quit_button(event):
            arcade.exit()

        # Hold the v_box that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Enable the UIManager when the view is showm.
        self.manager.enable()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Draw the manager.
        self.manager.draw()


class MenuView(arcade.View):
    """Main menu view class."""

    def __init__(self, main_view):
        super().__init__()

        self.manager = arcade.gui.UIManager()

        self.main_view = main_view
        self.v_box = arcade.gui.UIBoxLayout()

        #Create title
        menu_title = arcade.gui.UITextArea(text="A Tutorial",
                                        width=100,
                                        height=40,
                                        font_size=16)
        self.v_box.add(menu_title.with_space_around(bottom=20))

        back_button = arcade.gui.UIFlatButton(text="Go Back", width=200)
        self.v_box.add(back_button.with_space_around(bottom=20))

        # Initialise the button with an on_click event.
        @back_button.event("on_click")
        def on_click_back_button(event):
            # Passing the main view into menu view as an argument.
            main_view = MainView()
            self.window.show_view(main_view)

        # Use the anchor to position the button on the screen.
        # Hold the v_box that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_show_view(self):
        """ This is run once when we switch to this view """

        # Makes the background darker
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.DARK_BLUE_GRAY])

        self.manager.enable()

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.clear()
        self.manager.draw()


class GameView(arcade.View):
    """game view class."""

    def __init__(self, main_view):
        super().__init__()

        self.manager = arcade.gui.UIManager()

        self.main_view = main_view
        self.v_box = arcade.gui.UIBoxLayout()

        back_button = arcade.gui.UIFlatButton(text="Pause", width=200)
        self.v_box.add(back_button.with_space_around(bottom=20))

        # Initialise the button with an on_click event.
        @back_button.event("on_click")
        def on_click_back_button(event):
            # Passing the main view into menu view as an argument.
            main_view = MainView()
            self.window.show_view(main_view)

        # Use the anchor to position the button on the screen.
        # Hold the v_box that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_show_view(self):
        """ This is run once when we switch to this view """

        # Makes the background darker
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.DARK_BLUE_GRAY])

        self.manager.enable()

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.clear()
        self.manager.draw()

