"""
This example implements Conway's Game of Life using Pygame for visualization.
- initialize_grid: Initializes the game grid with random 0s and 1s.
- count_alive_neighbors: Counts the number of alive neighbors for a cell at a given position.
- update_grid: Updates the game grid based on Conway's Game of Life rules.
- get_cell_color: Determines the color of a cell based on its state and number of alive neighbors.
- draw_grid: Draws the grid on the Pygame screen.
- handle_events: Handles Pygame events, such as quitting the game.
- main: The main function to run the game, initializing Pygame, setting up the display, and running the game loop.
Constants:
- CELL_SIZE: The size of each cell in pixels.
- GRID_WIDTH: The width of the grid in cells.
- GRID_HEIGHT: The height of the grid in cells.
- FPS: Frames per second for the game loop.
- WHITE: RGB color for white.
- COLOR_1, COLOR_2, COLOR_3, COLOR_4: RGB colors for different cell states.
"""
import pygame
import numpy as np

# Constants
CELL_SIZE = 10
GRID_WIDTH = 120  # Width of the grid in cells
GRID_HEIGHT = 80  # Height of the grid in cells
FPS = 2  # Frames per second (0.5 seconds per frame)

# Colors
WHITE = (255, 255, 255)
COLOR_1 = (67, 76, 94)  # HEX: 434c5e
COLOR_2 = (46, 52, 64)  # HEX: 2e3440
COLOR_3 = (94, 129, 172)  # HEX: 5e81ac
COLOR_4 = (143, 188, 187)  # HEX: 8fbcbb

def initialize_grid():
    """Initialize the grid with random 0s and 1s."""
    return np.random.choice([0, 1], size=(GRID_HEIGHT, GRID_WIDTH))

def count_alive_neighbors(grid, x, y):
    """Count the number of alive neighbors for a cell at position (x, y)."""
    return np.sum(grid[max(0, y-1):min(GRID_HEIGHT, y+2), max(0, x-1):min(GRID_WIDTH, x+2)]) - grid[y, x]

def update_grid(grid):
    """Update the grid based on Conway's Game of Life rules."""
    new_grid = grid.copy()
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            alive_neighbors = count_alive_neighbors(grid, x, y)
            if grid[y, x] == 1 and (alive_neighbors < 2 or alive_neighbors > 3):
                new_grid[y, x] = 0  # Cell dies
            elif grid[y, x] == 0 and alive_neighbors == 3:
                new_grid[y, x] = 1  # Cell becomes alive
    return new_grid

def get_cell_color(alive, alive_neighbors):
    """Get the color of a cell based on its state and number of alive neighbors."""
    if alive:
        if alive_neighbors < 2:
            return COLOR_1
        elif alive_neighbors == 2:
            return COLOR_2
        elif alive_neighbors == 3:
            return COLOR_3
        else:
            return COLOR_4
    else:
        return WHITE

def draw_grid(screen, grid):
    """Draw the grid on the screen."""
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            alive_neighbors = count_alive_neighbors(grid, x, y)
            color = get_cell_color(grid[y, x], alive_neighbors)
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def handle_events():
    """Handle Pygame events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def main():
    """
    Main function to run the game.
    This function initializes the Pygame library, sets up the display window,
    and runs the main game loop for Conway's Game of Life. It handles events,
    updates the game state, and renders the grid on the screen.
    The game loop continues running until a quit event is detected. The screen
    is updated at a fixed frame rate defined by the FPS constant.
    Functions:
    - initialize_grid: Initializes the game grid.
    - handle_events: Handles user input and events.
    - draw_grid: Renders the game grid on the screen.
    - update_grid: Updates the game grid based on the rules of Conway's Game of Life.
    Pygame functions used:
    - pygame.init: Initializes all imported Pygame modules.
    - pygame.display.set_mode: Sets the display mode.
    - pygame.display.set_caption: Sets the window caption.
    - pygame.display.flip: Updates the full display surface to the screen.
    - pygame.quit: Uninitializes all Pygame modules.
    """
    """Main function to run the game."""
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
    pygame.display.set_caption("Conway's Game of Life")
    clock = pygame.time.Clock()
    
    grid = initialize_grid()
    
    running = True
    while running:
        running = handle_events()
        
        screen.fill(WHITE)
        draw_grid(screen, grid)
        grid = update_grid(grid)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()