import arcade
from BetterButton import BetterButton

# How many columns wide, how many rows tall
COLUMN_COUNT = 50
ROW_COUNT = 30

# Cell Size
CELL_WIDTH = 30
CELL_HEIGHT = 30
CELL_MARGIN = 5

# Margin on left of screen
LEFT_MARGIN = 400

# Do math to calculate screen dimensions
SCREEN_WIDTH = LEFT_MARGIN + (CELL_MARGIN + CELL_WIDTH) * COLUMN_COUNT + CELL_MARGIN
SCREEN_HEIGHT = (CELL_MARGIN + CELL_HEIGHT) * ROW_COUNT + CELL_MARGIN

# Screen title
TITLE = "Pathfindind Algorithm Visualizer"

# Colors
BLANK = arcade.color.WHITE
WALL = (50, 50, 50)
START = arcade.csscolor.MEDIUM_AQUAMARINE
END = arcade.csscolor.MEDIUM_ORCHID


class GridView(arcade.View):
    """
    Main class for the grid
    """

    def __init__(self):
        super().__init__()

        self.grid = arcade.SpriteList()
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                x = (CELL_WIDTH + CELL_MARGIN) * column + CELL_MARGIN + LEFT_MARGIN + CELL_WIDTH // 2
                y = (CELL_HEIGHT + CELL_MARGIN) * row + CELL_MARGIN + CELL_HEIGHT // 2
                cell = self.create_cell(x, y)
                self.grid.append(cell)

        self.current_color = WALL

        self.hover_sprite = arcade.Sprite('images/tile.png')
        self.hover_sprite.color = (0, 0, 0, 0)

        self.left_area = arcade.create_rectangle_filled(LEFT_MARGIN // 2, SCREEN_HEIGHT // 2, LEFT_MARGIN,
                                                        SCREEN_HEIGHT, (252, 83, 71, 255))

        self.x, self.y = 0, 0
        self.clear_screen_button = BetterButton(LEFT_MARGIN // 2, SCREEN_HEIGHT - 60, LEFT_MARGIN - 20,
                                                100, 'Clear Screen', self.clear_grid)

    def create_cell(self, x, y):
        cell = arcade.Sprite('images/tile.png')
        cell.center_x = x
        cell.center_y = y
        cell.color = BLANK
        return cell

    def get_column_and_row_from_mouse_coords(self, x, y):
        if x > 400:
            column = (x - 400 + CELL_MARGIN) // (CELL_WIDTH + CELL_MARGIN)
            row = (y + CELL_MARGIN) // (CELL_HEIGHT + CELL_MARGIN)
            return [column, row]

        return [-1, -1]

    def clear_grid(self):
        for cell in self.grid:
            if cell.color != BLANK:
                cell.color = arcade.color.WHITE

    def on_show(self):
        arcade.set_background_color((0, 0, 0))

    def on_draw(self):
        arcade.start_render()

        self.left_area.draw()
        self.grid.draw()
        self.hover_sprite.draw()
        self.clear_screen_button.draw()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # Assign x and y variables
        self.x, self.y, = x, y

        column, row = self.get_column_and_row_from_mouse_coords(x, y)

        if 0 <= column < COLUMN_COUNT and 0 <= row < ROW_COUNT:
            self.hover_sprite = arcade.Sprite('images/tile.png')

            x = (CELL_WIDTH + CELL_MARGIN) * column + CELL_MARGIN + LEFT_MARGIN + CELL_WIDTH // 2
            y = (CELL_HEIGHT + CELL_MARGIN) * row + CELL_MARGIN + CELL_HEIGHT // 2
            self.hover_sprite.center_x = x
            self.hover_sprite.center_y = y
            self.hover_sprite.color = self.current_color

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, button: int, _modifiers: int):
        # Assign x and y variables
        self.x, self.y, = x, y

        column, row = self.get_column_and_row_from_mouse_coords(x, y)
        current_cell = self.grid[row * COLUMN_COUNT + column]

        self.hover_sprite = arcade.Sprite('images/tile.png')

        if 0 <= column < COLUMN_COUNT and 0 <= row < ROW_COUNT:
            if button == 1:
                current_cell.color = WALL
            elif button == 4:
                current_cell.color = BLANK

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Assign x and y variables
        self.x, self.y, = x, y

        column, row = self.get_column_and_row_from_mouse_coords(x, y)
        current_cell = self.grid[row * COLUMN_COUNT + column]

        if 0 <= column < COLUMN_COUNT and 0 <= row < ROW_COUNT:
            if button == 1:
                current_cell.color = WALL
            elif button == 4:
                current_cell.color = BLANK

        # Button checks
        self.clear_screen_button.check_mouse_press(self.x, self.y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        # Assign x and y variables
        self.x, self.y, = x, y
        # Button checks
        self.clear_screen_button.check_mouse_release(self.x, self.y)

    def on_update(self, delta_time: float):
        # Button checks
        self.clear_screen_button.check_mouse_hover(self.x, self.y)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    grid = GridView()
    window.show_view(grid)
    arcade.run()


main()
