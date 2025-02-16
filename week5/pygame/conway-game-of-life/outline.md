# Conway's Game of Life - Code Explanation

This example implements Conway's *Game of Life* using Python and Pygame. Below is an explanation of the main components of the code.

## Constants

```python
CELL_SIZE = 10
GRID_WIDTH = 120  # Width of the grid in cells
GRID_HEIGHT = 80  # Height of the grid in cells
FPS = 2  # Frames per second (0.5 seconds per frame)
```

## Colors

```python
WHITE = (255, 255, 255)
COLOR_1 = (67, 76, 94)  # HEX: 434c5e
COLOR_2 = (46, 52, 64)  # HEX: 2e3440
COLOR_3 = (94, 129, 172)  # HEX: 5e81ac
COLOR_4 = (143, 188, 187)  # HEX: 8fbcbb
```

* `WHITE`: The color used for dead cells.
* `COLOR_1`, `COLOR_2`, `COLOR_3`, `COLOR_4`: Different shades of blue used for live cells based on the number of alive neighbors.

## Functions
`initialize_grid`

```python
def initialize_grid():
    """Initialize the grid with random 0s and 1s."""
    return np.random.choice([0, 1], size=(GRID_HEIGHT, GRID_WIDTH))
```

* Initializes the grid with random `0s` and `1s` using NumPy's `random.choice` method.

`count_alive_neighbors`

```python
def count_alive_neighbors(grid, x, y):
    """Count the number of alive neighbors for a cell at position (x, y)."""
    return np.sum(grid[max(0, y-1):min(GRID_HEIGHT, y+2), max(0, x-1):min(GRID_WIDTH, x+2)]) - grid[y, x]
```

* Counts the number of alive neighbors for a cell at position `(x, y)`.

`update_grid`

```python
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
```

* Updates the grid based on Conway's *Game of Life* rules.

`get_cell_color`

```python
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
```

* Determines the color of a cell based on its state and the number of alive neighbors.

`draw_grid`

```python
def draw_grid(screen, grid):
    """Draw the grid on the screen."""
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            alive_neighbors = count_alive_neighbors(grid, x, y)
            color = get_cell_color(grid[y, x], alive_neighbors)
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
```

* Draws the grid on the screen.

`handle_events`

```python
def handle_events():
    """Handle Pygame events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True
```

* Handles Pygame events, such as quitting the game.

`main`

```python
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
```

* The `main` function initializes Pygame, sets up the display window, and runs the main game loop.
* The game loop handles events, updates the game state, and renders the grid on the screen.
* The game continues running until a quit event is detected.
* The screen is updated at a fixed frame rate defined by the FPS constant.
