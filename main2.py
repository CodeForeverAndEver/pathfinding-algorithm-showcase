import arcade
from BetterButton import BetterButton

# Cell dimensions
CELL_WIDTH = 30
CELL_HEIGHT = 30
CELL_MARGIN = 5

# Columsn and rows
COLUMN_COUNT = 40
ROW_COUNT = 30

# Margins
GUI_WIDTH = 400
GRID_MARGIN = 50

# Predefined colors
WHITE = arcade.csscolor.WHITE
GRAY = (50, 50, 50, 255)
GREEN = [num for num in arcade.csscolor.MEDIUM_AQUAMARINE] + [255]
PURPLE = [num for num in arcade.csscolor.MEDIUM_ORCHID] + [255]
TRANSPARENT = (0, 0, 0, 0)

# BG Color
BG_COLOR = arcade.csscolor.MEDIUM_SPRING_GREEN # (171, 52, 235) # 252, 83, 71, 255

# Screen dimensions
SCREEN_WIDTH = (CELL_WIDTH + CELL_MARGIN) * COLUMN_COUNT + CELL_MARGIN + GUI_WIDTH + GRID_MARGIN
SCREEN_HEIGHT = (CELL_HEIGHT + CELL_MARGIN) * ROW_COUNT + CELL_MARGIN + GRID_MARGIN * 2

class Cell(arcade.Sprite):
    """
    Class for cells
    """

    def __init__(self, path, x, y, color):
        super().__init__(path)

        # Set coordinates to be whatever passed
        self.center_x = x
        self.center_y = y
        # Color
        self.color = color
        # Variable to store location of cell before it was dragged
        self.start_location_before_drag = None
        self.is_dragging = False

    def get_center(self):
        # Return center of grid

        return [self.center_x, self.center_y]



class Grid(arcade.View):
    """
    Class for Grid
    """

    def __init__(self):
        super().__init__()

        # 2d grid object
        self.grid = self.create_grid()
        self.starting_cell = Cell('images/tile.png', self.grid[25][4].center_x, self.grid[25][4].center_y, GREEN)
        self.ending_cell = Cell('images/tile.png', self.grid[25][9].center_x, self.grid[25][9].center_y, PURPLE)
        self.placement_tip = Cell('images/tile.png', 0, 0, GRAY)
        self.placement_tip_color = GRAY

        # Gui BG rectangle
        self.gui_bg = arcade.create_rectangle_filled(GUI_WIDTH // 2, SCREEN_HEIGHT // 2, GUI_WIDTH, 
        SCREEN_HEIGHT, BG_COLOR)

        # Gui buttons
        self.clear_screen_button = BetterButton(GUI_WIDTH // 2, SCREEN_HEIGHT - GRID_MARGIN - 50, GUI_WIDTH - 20,
                                                100, 'Clear Screen', self.clear_grid)

        self.button_hover_x = 0
        self.button_hover_y = 0

        # Margin rectangles
        self.padding_top = arcade.create_rectangle_filled(SCREEN_WIDTH // 2 + GUI_WIDTH // 2, 
        SCREEN_HEIGHT - GRID_MARGIN // 2, SCREEN_WIDTH - GUI_WIDTH, GRID_MARGIN, BG_COLOR)
        self.padding_bottom = arcade.create_rectangle_filled(SCREEN_WIDTH // 2 + GUI_WIDTH // 2, 
        GRID_MARGIN // 2, SCREEN_WIDTH - GUI_WIDTH, GRID_MARGIN,BG_COLOR)
        self.padding_right = arcade.create_rectangle_filled(SCREEN_WIDTH - GRID_MARGIN // 2, 
        SCREEN_HEIGHT // 2, GRID_MARGIN, SCREEN_HEIGHT, BG_COLOR)

    def create_grid(self):
        # Create the grid

        grid = []
        for row in range(ROW_COUNT):
            grid.append(arcade.SpriteList())
            for column in range(COLUMN_COUNT):
                x = (CELL_WIDTH + CELL_MARGIN) * column + GUI_WIDTH + CELL_MARGIN + CELL_WIDTH // 2
                y = (CELL_HEIGHT + CELL_MARGIN) * row + CELL_MARGIN + GRID_MARGIN + CELL_HEIGHT // 2
                cell = Cell('images/tile.png', x, y, WHITE)
                grid[row].append(cell)
        return grid

    def draw_grid(self):
        # Draw the grid

        for row in self.grid:
            row.draw()

    def clear_grid(self):
        # Clear the grid
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                cell = self.get_cell_from_column_and_row(column, row)
                if cell.color != WHITE:
                    cell.color = WHITE


    def get_column_and_row_from_mouse_coords(self, x, y):
        # Get column and row of the cell the mouse is over

        column = (x - GUI_WIDTH) // (CELL_WIDTH + CELL_MARGIN)
        row = (y - GRID_MARGIN) // (CELL_HEIGHT + CELL_MARGIN)
        return [column, row]

    def get_cell_from_column_and_row(self, column, row):
        # Return whatever cell is at the specified column and row

        if 0 <= column < COLUMN_COUNT and 0 <= row < ROW_COUNT:
            return self.grid[row][column]

    def get_position_of_cell_from_column_and_row(self, column, row):
        # Find the position of any given cell based on the column and row

        x = (CELL_WIDTH + CELL_MARGIN) * column + GUI_WIDTH + CELL_MARGIN + CELL_WIDTH // 2
        y = (CELL_HEIGHT + CELL_MARGIN) * row + CELL_MARGIN + GRID_MARGIN + CELL_HEIGHT // 2
        return [x, y]
    
    def get_cell_from_x_and_y(self, x, y):
        # Get the cell the mouse is over

        column, row = self.get_column_and_row_from_mouse_coords(x, y)
        cell = self.get_cell_from_column_and_row(column, row)
        return cell

    def place_placement_tip(self, x, y):
        # Place the placement tip in the correct location

        column, row = self.get_column_and_row_from_mouse_coords(x, y)
        if 0 <= column < COLUMN_COUNT and 0 <= row < ROW_COUNT:
            self.placement_tip.center_x, self.placement_tip.center_y = self.get_position_of_cell_from_column_and_row(column, row)
            self.placement_tip.color = self.placement_tip_color
    
    def drag_and_drop(self, cell, x, y):
        # Drag and drop a cell
        column, row = self.get_column_and_row_from_mouse_coords(x, y)
        
        if 0 <= column < COLUMN_COUNT and 0 <= row < ROW_COUNT:
            cell.center_x, cell.center_y = self.get_position_of_cell_from_column_and_row(column, row)

    def draw_wall(self, x, y):
        # Draw a wall

        column, row = self.get_column_and_row_from_mouse_coords(x, y)
        
        if 0 <= column < COLUMN_COUNT and 0 <= row < ROW_COUNT:
            cell = self.get_cell_from_x_and_y(x, y)

            cell_center = cell.get_center()
            starting_cell_center = self.starting_cell.get_center()
            ending_cell_center = self.ending_cell.get_center()

            if not cell_center == starting_cell_center and not cell_center == ending_cell_center:
                cell.color = GRAY

    def erase_wall(self, x, y):
        # Erase a wall

        column, row = self.get_column_and_row_from_mouse_coords(x, y)
        
        if 0 <= column < COLUMN_COUNT and 0 <= row < ROW_COUNT:
            cell = self.get_cell_from_x_and_y(x, y)
            cell.color = WHITE

    def check_button_hovers(self, x, y):
        self.clear_screen_button.check_mouse_hover(x, y)

    def check_button_presses(self, x, y):
        self.clear_screen_button.check_mouse_press(x, y)

    def check_button_release(self, x, y):
        self.clear_screen_button.check_mouse_release(x, y)

    def on_show(self):
        # Called on show

        arcade.set_background_color(arcade.csscolor.BLACK)

    def on_draw(self):
        arcade.start_render()

        # Draw margins
        self.gui_bg.draw()
        self.padding_top.draw()
        self.padding_bottom.draw()
        self.padding_right.draw()
        # Draw grid and placement tip
        self.draw_grid()
        self.placement_tip.draw()
        # Draw either the starting cell or ending cell on top based on whichever should be on top
        if self.starting_cell.is_dragging:
            self.ending_cell.draw()
            self.starting_cell.draw()
        else:
            self.starting_cell.draw()
            self.ending_cell.draw()
        # Draw buttons
        self.clear_screen_button.draw()
    

    def on_mouse_motion(self, x, y, dx, dy):
        # Place the placement tip in the updated location whenever the mouse moves
        self.button_hover_x, self.button_hover_y = x, y

        self.place_placement_tip(x, y)
    
    def on_mouse_press(self, x, y, button, modifiers):
        # Called whenever the mouse is pressed

        # Make sure that when we press the mouse the placement tip is transparent
        self.placement_tip.color = TRANSPARENT

        # Get the being clicked (if any)
        cell = self.get_cell_from_x_and_y(x, y)
        
        # Get the centers of each cell
        if cell != None:
            cell_center = cell.get_center()
            starting_cell_center = self.starting_cell.get_center()
            ending_cell_center = self.ending_cell.get_center()

        # As long as we aren't dragging anything; draw or erase the walls
        if not self.starting_cell.is_dragging and not self.ending_cell.is_dragging:
            if button == 1:
                self.draw_wall(x, y)
            elif button == 4:
                self.erase_wall(x, y)

        if cell != None:
            # If we click on the starting or ending cell, then we are about to drag it, also log the location of the starting
            # and ending cells before they are moved
            if cell_center == starting_cell_center:
                self.starting_cell.is_dragging = True
                self.starting_cell.start_location_before_drag = self.starting_cell.get_center()
            elif cell_center == ending_cell_center:
                self.ending_cell.is_dragging = True
                self.ending_cell.start_location_before_drag = self.ending_cell.get_center()

        # Check for button presses
        self.clear_screen_button.check_mouse_press(x, y)

    def on_mouse_drag(self, x, y, dx, dy, button, _modifiers):
        # Called whenever the mouse is being dragged

        self.button_hover_x, self.button_hover_y = x, y

        # Draw the walls as long as we aren't dragging anything, otherwise drag the cells
        if not self.starting_cell.is_dragging and not self.ending_cell.is_dragging:
            if button == 1:
                self.draw_wall(x, y)
            else:
                self.erase_wall(x, y)
        elif self.starting_cell.is_dragging:
            self.drag_and_drop(self.starting_cell, x, y)
        elif self.ending_cell.is_dragging:
            self.drag_and_drop(self.ending_cell, x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        # Called whenever the mouse is realesed

        # Make the placement tip `untransparent`
        self.placement_tip_color = GRAY
        # Replace the placement tip
        self.place_placement_tip(x, y)

        # Get the cell that the mouse was released over
        cell = self.get_cell_from_x_and_y(x, y)
        if cell != None:
            cell_color = [num for num in cell.color] + [255]
            gray_list = [num for num in GRAY]

            # If we were dragging anything, stop dragging and make sure that we can drop the cell at that location
            if self.starting_cell.is_dragging :
                self.starting_cell.is_dragging = False
                if cell_color == gray_list or cell.get_center() == self.ending_cell.get_center():
                    self.starting_cell.center_x, self.starting_cell.center_y = self.starting_cell.start_location_before_drag
            elif self.ending_cell.is_dragging:
                self.ending_cell.is_dragging = False
                if cell_color == gray_list or cell.get_center() == self.starting_cell.get_center():
                    self.ending_cell.center_x, self.ending_cell.center_y = self.ending_cell.start_location_before_drag

        # Check for button presses
        self.clear_screen_button.check_mouse_release(x, y)

    def on_update(self, delta_time):
        self.clear_screen_button.check_mouse_hover(self.button_hover_x, self.button_hover_y)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, 'Pathfinding Algorithm Visualizer')
    grid = Grid()
    window.show_view(grid)
    arcade.run()

main()
