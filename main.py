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

    def create_cell(self, row, column):
        # Create a cell
        cell_sprite = arcade.Sprite('images/tile.png')
        cell_sprite.center_x = (WIDTH + MARGIN) * column + MARGIN + WIDTH // 2
        cell_sprite.center_y = (HEIGHT + MARGIN) * row + MARGIN + HEIGHT // 2
        cell_sprite.color = arcade.color.WHITE
        return cell_sprite

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

        self.grid.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.changed_on_this_drag = []

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, _buttons: int, _modifiers: int):
        """
        Called when user presses a mouse button
        """

        # Change x/y screen coords to grid coords
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))

        # Get the cell that was clicked
        clicked_cell = self.grid[row * COLUMN_COUNT + column]

        # Make sure in grid (can click upper right corner in margin and go to non-existant grid location
        # Also make sure that the box hasn't already been changed during this drag
        if row < ROW_COUNT and column < COLUMN_COUNT and clicked_cell not in self.changed_on_this_drag:
            if _buttons == 1:
                # Flip the color between gray and white
                if clicked_cell.color == arcade.color.WHITE:
                    clicked_cell.color = (50, 50, 50)
            elif _buttons == 4:
                print('Rclick')
                clicked_cell.color = arcade.color.WHITE
                print(clicked_cell.color)

        self.changed_on_this_drag.append(clicked_cell)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    view = GridView()
    window.show_view(view)
    arcade.run()


main()
