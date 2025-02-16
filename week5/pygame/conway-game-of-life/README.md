# Conway's Game of Life

This example implements Conway's *Game of Life* using Pygame. 

The game is a cellular automaton devised by the British mathematician John Horton Conway in 1970. It consists of a grid of cells that can be either alive or dead, and the state of each cell changes based on the states of its neighbors according to specific rules.

## Project Structure

```
conway-game-of-life
├── src
│   ├── game_of_life.py  # Main implementation of the game
│   └── __init__.py      # Marks the src directory as a Python package
├── requirements.txt      # Lists the dependencies required for the project
└── README.md             # Documentation for the project
```

## Requirements

To run this project, you need to have Python and Pygame installed. You can install the required dependencies using the following command:

```
pip install -r requirements.txt
```

or using Conda within an existing environment.

## Running the Game

To start the game, run the following command in your terminal from the root of the project directory:

```
python src/game_of_life.py
```

## Game Rules

1. Any live cell with fewer than two live neighbors dies as if caused by under-population.
2. Any live cell with two or three live neighbors lives on to the next generation.
3. Any live cell with more than three live neighbors dies, as if by over-population.
4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.