import arcade

# Set how many rows and columns we will have
COLUMN_COUNT, ROW_COUNT = [50, 30]
# Set the width and height of each cell
WIDTH, HEIGHT = [30, 30]
# Set the distance between each cell
MARGIN = 5

# Math to figure out the screen dimensions
SCREEN_WIDTH = COLUMN_COUNT * (WIDTH + MARGIN) + MARGIN
SCREEN_HEIGHT = ROW_COUNT * (HEIGHT + MARGIN) + MARGIN
SCREEN_TITLE = "Path Finding Algorithms"


class MainView(arcade.View):
    """
    Main Window To Display The Algorithms
    """

    def __init__(self):
        """
        Set up class
        """
        super().__init__()

        # Create 1D array
        self.grid = arcade.SpriteList()
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # Append a cell
                tile_sprite = arcade.Sprite('images/tile.png')
                tile_sprite.center_x = (WIDTH + MARGIN) * column + MARGIN + WIDTH // 2
                tile_sprite.center_y = (HEIGHT + MARGIN) * row + MARGIN + HEIGHT // 2
                tile_sprite.color = arcade.color.WHITE
                self.grid.append(tile_sprite)

    def on_show(self):
        """
        Setup screen
        """

        arcade.set_background_color((200, 200, 200))

    def on_draw(self):
        """
        Render the screen
        """

        arcade.start_render()

        self.grid.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """
        Called when user presses a mouse button
        """

        # Change x/y screen coords to grid coords
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # Make sure in grid (can click upper right corner in margin and go to non-existant grid location
        if row < ROW_COUNT and column < COLUMN_COUNT:
            # Flip the color between green and white
            if self.grid[row * COLUMN_COUNT + column].color == arcade.color.WHITE:
                self.grid[row * COLUMN_COUNT + column].color = arcade.color.GREEN
            else:
                self.grid[row * COLUMN_COUNT + column].color = arcade.color.WHITE


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    view = MainView()
    window.show_view(view)
    arcade.run()


main()