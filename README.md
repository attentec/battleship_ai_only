# Battleship
![Alt text](/screenshot.png?raw=true "Screenshot")

This is a game of Battleship where two AIs play against each other.

## Installation
- Install python3 and add it to your PATH.
- Install the requirements
  - `python3 -m pip install -r requirements.txt`

## Usage
Execute `main.py` and pass two AIs to start the game\
`python3 main.py --ai1 random_ai.py --ai2 random_ai.py`

The default speed is 10 but can be changed by providing a number to `--fps`\
`python3 main.py --ai1 random_ai.py --ai2 random_ai.py --fps 30`

## Writing your own AI
- Make a copy of `random_ai.py` and give it a good name.
- Open the file and read the documentation.
- Improve your AI by implementing smarter logic.
- Test it against the random AI
  - `python3 main.py --ai1 random_ai.py --ai2 <your ai>`
- ???
- Profit

The AI must implement the functions `get_move` and `place_ship`.

## Rules
The game is lost if any of the following happens
- All of your ships sunk
- You shot outside of the board
- You shot twice on the same coordinate
- You took more than 3 seconds to determine your next move
- Your implementation crashed
- You tried to place a invalid ship

## Controls
- **Esc** — Quit the game
- **Space** — Play again
