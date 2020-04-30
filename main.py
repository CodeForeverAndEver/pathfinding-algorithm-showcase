import arcade

# Set how many rows and columns we will have
COLUMN_COUNT, ROW_COUNT = [50, 30]
# Set the width and height of each cell
WIDTH, HEIGHT = [30, 30]
# Set the distance between each cell
MARGIN = 5
# Set the margin for the buttons
BUTTON_MARGIN = 400
# Math to figure out the screen dimensions
SCREEN_WIDTH = BUTTON_MARGIN + COLUMN_COUNT * (WIDTH + MARGIN) + MARGIN
SCREEN_HEIGHT = ROW_COUNT * (HEIGHT + MARGIN) + MARGIN
SCREEN_TITLE = "Path Finding Algorithms"


class BetterButton(arcade.TextButton):
    def __init__(self, text, center_y):
        super().__init__(BUTTON_MARGIN // 2, center_y, BUTTON_MARGIN - 20, 100,
                        font_face='fonts/Ubuntu/Ubuntu-Regular', text=text,
                        font_color=arcade.color.BLACK, face_color=(0, 0, 0, 0),
                        highlight_color=(0, 0, 0, 0), shadow_color=(0, 0, 0, 0))

        self.mouse_pressed = False

    def check_mouse_hover(self, x, y):
        if x > self.center_x + self.width / 2:
            self.face_color = (0, 0, 0, 0)
            return
        if x < self.center_x - self.width / 2:
            self.face_color = (0, 0, 0, 0)
            return
        if y > self.center_y + self.height / 2:
            self.face_color = (0, 0, 0, 0)
            return
        if y < self.center_y - self.height / 2:
            self.face_color = (0, 0, 0, 0)
            return
        if not self.mouse_pressed:
            self.on_hover()

    def on_hover(self):
        self.face_color = (0, 0, 0, 50)

    def on_press(self):
        self.mouse_pressed = True
        self.face_color = (0, 0, 0, 100)

    def check_mouse_release(self, x, y):
        if x > self.center_x + self.width / 2:
            return
        if x < self.center_x - self.width / 2:
            return
        if y > self.center_y + self.height / 2:
            self.face_color = (0, 0, 0, 0)
            return
        if y < self.center_y - self.height / 2:
            self.face_color = (0, 0, 0, 0)
            return
        self.mouse_pressed = False
        self.on_release()

    def on_release(self):
        GRID.clear_grid()


class GridView(arcade.View):
    """
    Main Window To Display The Algorithms
    """

    def __init__(self):
        """
        Set up class
        """
        super().__init__()

        # Variable that stores all boxes that were clicked within a the current "period of drag"
        # makes sure that boxes don't blink white and gray super fast bu checking to make sure
        # that they haven't already been changed during the current drag
        self.changed_on_this_drag = []

        # Create 1D array
        self.grid = arcade.SpriteList()
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # Append a cell
                self.grid.append(self.create_cell(row, column))

        # Create button margin area
        color = (252, 83, 71, 255)
        self.button_margin_area = arcade.create_rectangle_filled(BUTTON_MARGIN // 2, SCREEN_HEIGHT // 2,
                                                                 BUTTON_MARGIN, SCREEN_HEIGHT, color)

        # Current mouse positions
        self.x, self.y = 0, 0

        # Buttons
        self.clear_button = BetterButton('Clear', SCREEN_HEIGHT - 60)
        self.place_start_button = BetterButton('Place Starting Square', SCREEN_HEIGHT - 170)

    def create_cell(self, row, column):
        # Create a cell
        cell_sprite = arcade.Sprite('images/tile.png')
        cell_sprite.center_x = BUTTON_MARGIN + (WIDTH + MARGIN) * column + MARGIN + WIDTH // 2
        cell_sprite.center_y = (HEIGHT + MARGIN) * row + MARGIN + HEIGHT // 2
        cell_sprite.color = arcade.color.WHITE
        return cell_sprite

    def switch_color(self, row, column, clicked_cell, button):
        # Make sure in grid (can click upper right corner in margin and go to non-existant grid location
        # Also make sure that the box hasn't already been changed during this drag
        if 0 <= row < ROW_COUNT and 0 <= column < COLUMN_COUNT and clicked_cell not in self.changed_on_this_drag:
            # If it was a left click
            if button == 1:
                # Flip the color between gray and white
                if clicked_cell.color == arcade.color.WHITE:
                    clicked_cell.color = (50, 50, 50)
            elif button == 4:
                if clicked_cell.color == (50, 50, 50):
                    clicked_cell.color = arcade.color.WHITE

    def get_column_and_row(self, x, y):
        column = int((x - BUTTON_MARGIN) // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))

        return column, row

    def clear_grid(self):
        for cell in self.grid:
            if cell.color == (50, 50, 50):
                cell.color = arcade.color.WHITE

    def on_show(self):
        """
        Setup screen
        """

        arcade.set_background_color((0, 0, 0))

    def on_draw(self):
        """
        Render the screen
        """

        arcade.start_render()

        self.button_margin_area.draw()
        self.clear_button.draw()
        self.place_start_button.draw()

        self.grid.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.x, self.y = x, y

        self.changed_on_this_drag = []

        # Change x/y screen coords to grid coords
        column, row = self.get_column_and_row(x, y)

        # Get the cell that was clicked
        clicked_cell = self.grid[row * COLUMN_COUNT + column]

        # Switch the color
        self.switch_color(row, column, clicked_cell, button)

        self.clear_button.check_mouse_press(self.x, self.y)
        self.place_start_button.check_mouse_press(self.x, self.y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        self.clear_button.check_mouse_release(x, y)
        self.place_start_button.check_mouse_release(x, y)

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, _buttons: int, _modifiers: int):
        """
        Called when user presses a mouse button
        """

        self.x, self.y = x, y

        # Change x/y screen coords to grid coords
        column, row = self.get_column_and_row(x, y)

        # Get the cell that was clicked
        clicked_cell = self.grid[row * COLUMN_COUNT + column]

        # Switch the color
        self.switch_color(row, column, clicked_cell, _buttons)

        self.changed_on_this_drag.append(clicked_cell)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.x, self.y = x, y

    def on_update(self, delta_time: float):
        self.clear_button.check_mouse_hover(self.x, self.y)
        self.place_start_button.check_mouse_hover(self.x, self.y)


# Define Window
WINDOW = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

# Define Grid
GRID = GridView()


def main():
    WINDOW.show_view(GRID)
    arcade.run()


main()
