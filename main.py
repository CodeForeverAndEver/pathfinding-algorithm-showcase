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


class StartCell(arcade.Sprite):
    def __init__(self):
        super().__init__('images/tile.png')
        self.color = START
        self.center_x = (CELL_WIDTH + CELL_MARGIN) * 5 + CELL_MARGIN + LEFT_MARGIN + CELL_WIDTH // 2
        self.center_y = (CELL_HEIGHT + CELL_MARGIN) * 20 + CELL_MARGIN + CELL_HEIGHT // 2

        self.is_dragging = False

    def on_update(self):
        pass


class EndCell(arcade.Sprite):
    def __init__(self):
        super().__init__('images/tile.png')
        self.color = END
        self.center_x = (CELL_WIDTH + CELL_MARGIN) * 10 + CELL_MARGIN + LEFT_MARGIN + CELL_WIDTH // 2
        self.center_y = (CELL_HEIGHT + CELL_MARGIN) * 20 + CELL_MARGIN + CELL_HEIGHT // 2

        self.is_dragging = False
    
    def on_update(self):
        pass


class Cell(arcade.Sprite):
    def __init__(self):
        super().__init__('images/tile.png')


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

        self.starting_cell = StartCell()
        self.ending_cell = EndCell()

        self.current_color = WALL

        self.hover_sprite = arcade.Sprite('images/tile.png')
        self.hover_sprite.color = (0, 0, 0, 0)

        self.left_area = arcade.create_rectangle_filled(LEFT_MARGIN // 2, SCREEN_HEIGHT // 2, LEFT_MARGIN,
                                                        SCREEN_HEIGHT, (252, 83, 71, 255))

        self.x, self.y = 0, 0
        self.clear_screen_button = BetterButton(LEFT_MARGIN // 2, SCREEN_HEIGHT - 60, LEFT_MARGIN - 20,
                                                100, 'Clear Screen', self.clear_grid)

    def create_cell(self, x, y):
        cell = Cell()
        cell.center_x = x
        cell.center_y = y
        cell.color = BLANK
        return cell

    def get_column_and_row_from_mouse_coords(self):
        if self.x > 400:
            column = (self.x - 400 + CELL_MARGIN) // (CELL_WIDTH + CELL_MARGIN)
            row = (self.y + CELL_MARGIN) // (CELL_HEIGHT + CELL_MARGIN)
            return [column, row]

        return [-1, -1]

    def clear_grid(self):
        for cell in self.grid:
            if cell.color != BLANK:
                cell.color = arcade.color.WHITE

    def draw_cell(self, button, current_cell):
        # Check if left click
        if button == 1:
            current_cell.color = self.current_color
        # Check if right click
        elif button == 4:
            current_cell.color = BLANK    
    
    def drag_and_drop(self, what_is_being_dragged):
        column, row = self.get_column_and_row_from_mouse_coords()

        x = (CELL_WIDTH + CELL_MARGIN) * column + CELL_MARGIN + LEFT_MARGIN + CELL_WIDTH // 2
        y = (CELL_HEIGHT + CELL_MARGIN) * row + CELL_MARGIN + CELL_HEIGHT // 2

        if what_is_being_dragged == 'starting cell':
            self.starting_cell.center_x = x
            self.starting_cell.center_y = y
        elif what_is_being_dragged == 'ending cell':
            self.ending_cell.center_x = x
            self.ending_cell.center_y = y

    def on_show(self):
        arcade.set_background_color((0, 0, 0))

    def on_draw(self):
        arcade.start_render()

        self.left_area.draw()
        self.grid.draw()
        self.hover_sprite.draw()
        self.starting_cell.draw()
        self.ending_cell.draw()
        self.clear_screen_button.draw()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # Assign x and y variables
        self.x, self.y, = x, y

        column, row = self.get_column_and_row_from_mouse_coords()

        if 0 <= column < COLUMN_COUNT and 0 <= row < ROW_COUNT:
            # Create the sprite to be placed at mouse
            self.hover_sprite = arcade.Sprite('images/tile.png')

            # Calculate x and y coordinates
            x = (CELL_WIDTH + CELL_MARGIN) * column + CELL_MARGIN + LEFT_MARGIN + CELL_WIDTH // 2
            y = (CELL_HEIGHT + CELL_MARGIN) * row + CELL_MARGIN + CELL_HEIGHT // 2

            self.hover_sprite.center_x = x
            self.hover_sprite.center_y = y

            self.hover_sprite.color = self.current_color

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, button: int, _modifiers: int):
        # Assign x and y variables
        self.x, self.y, = x, y

        column, row = self.get_column_and_row_from_mouse_coords()
        
        if 0 <= column < COLUMN_COUNT and 0 <= row < ROW_COUNT:
            current_cell = self.grid[row * COLUMN_COUNT + column]
            self.hover_sprite.color = (0, 0, 0, 0)
            if not self.starting_cell.is_dragging and not self.ending_cell.is_dragging:
                self.draw_cell(button, current_cell)
            elif self.starting_cell.is_dragging:
                self.drag_and_drop('starting cell')
            elif self.ending_cell:
                self.drag_and_drop('ending cell')

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Assign x and y variables
        self.x, self.y, = x, y

        column, row = self.get_column_and_row_from_mouse_coords()

        if 0 <= column < COLUMN_COUNT and 0 <= row < ROW_COUNT:
            current_cell = self.grid[row * COLUMN_COUNT + column]
            if current_cell.center_x == self.starting_cell.center_x and current_cell.center_y == self.starting_cell.center_y:
                self.starting_cell.is_dragging = True
            elif current_cell.center_x == self.ending_cell.center_x and current_cell.center_y == self.ending_cell.center_y:
                self.ending_cell.is_dragging = True
            else:
                self.draw_cell(button, current_cell)

        # Button checks
        self.clear_screen_button.check_mouse_press(self.x, self.y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        # Assign x and y variables
        self.x, self.y, = x, y

        if self.starting_cell.is_dragging:
            self.starting_cell.is_dragging = False
        elif self.ending_cell.is_dragging:
            self.ending_cell.is_dragging = False

        column, row = self.get_column_and_row_from_mouse_coords()

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
