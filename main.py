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

        self.shape_list = None

        # Create 2D array
        self.grid = []
        for row in range(ROW_COUNT):
            # Add empty array to hold each cell in this cell
            self.grid.append([])
            for column in range(COLUMN_COUNT):
                # Append a cell for each column
                self.grid[row].append(0)
        self.recreate_grid()

    def on_show(self):
        """
        Setup screen
        """

        arcade.set_background_color((200, 200, 200))

    def recreate_grid(self):
        self.shape_list = arcade.ShapeElementList()
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                if self.grid[row][column] == 0:
                    color = arcade.color.WHITE
                else:
                    color = arcade.color.GREEN

                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + WIDTH // 2

                current_rect = arcade.create_rectangle_filled(x, y, WIDTH, HEIGHT, color)
                self.shape_list.append(current_rect)

    def on_draw(self):
        """
        Render the screen
        """

        arcade.start_render()

        self.shape_list.draw()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    view = MainView()
    window.show_view(view)
    arcade.run()

main()
