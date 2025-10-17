
# 2048 Game (Flask Web App)

## Overview

Classic 2048 puzzle game implemented as a web app using Python (Flask). Play by combining tiles with the same number to reach 2048. Features GUI controls, restart option, live score tracking, and configurable board size.

***

## Installation

1. **Clone the repository**  
   ```
   git clone <your-repository-url>
   cd <your-repository-folder>
   ```

2. **Set up a Python environment (recommended)**  
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**  
   ```
   pip install -r requirements.txt
   ```

***

## Running the Game

1. **Start the Flask server**  
   ```
   python app.py
   ```
   - Or for deployment on Render:
     ```
     gunicorn app:app
     ```

2. **Access the game**  
   Open your web browser and navigate to:
   ```
   http://localhost:5000/
   ```
   or the public URL if deployed.

***

## Gameplay Instructions

- **Board Size**: Default is 4x4 (can be changed via `BOARD_SIZE` environment variable).
- **Starting Tiles**: Board initializes with two tiles, each with value 2 or 4.
- **Controls**: Use your keyboard (Arrow keys) or GUI buttons to slide tiles [Up, Down, Left, Right].
- **Merging**: Tiles of the same number touching each other merge into one (sum of the numbers), increasing the score according to the merged value.
- **New Tiles**: Each valid move spawns a new tile (2 or 4) in a random empty position.
- **Win Condition**: Reach the 2048 tile to win.
- **Lose Condition**: No empty tiles and no possible merges means game over.
- **Restart**: Use the Restart button or command to reset the game.

***

## Implementation Details

- **Language:** Python 3.x  
- **Web Framework:** Flask
- **Frontend:** HTML/CSS/JS (template: `templates/index.html`)
- **Functional Design:**  
  - Game logic (tile movement/merging, random tiles, win/lose detection) as pure functions
  - Score tracking and dynamic updates after each move
  - Modular structure for code reuse and readability
- **Configurable Board Size:**  
  - Set `BOARD_SIZE` environment variable to any integer ≥ 4 (e.g., `export BOARD_SIZE=5`).
- **Live API Endpoints:**  
  - `/state` (GET): Get current board, score, game status  
  - `/move` (POST): Make a move (pass direction in JSON)  
  - `/reset` (POST): Restart game  
- **Session Management:**  
  - Game state held server-side (for multiple users or persistence, use sessions or a database).

***

## Notes

- For production hosting (e.g., Render), set `PORT` and `BOARD_SIZE` as environment variables if required.
- The game GUI updates automatically on any move; if customizing, make sure your front-end reads the API (see `index.html` example).
- Code is modularized; functions are reusable and single-responsibility.

***