# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple Pacman game prototype built with Python 3 and Pygame for macOS. The game is contained in a single Python file (`pacman.py`) and implements classic Pacman gameplay including power pellets, ghost AI, scoring, and lives system.

## Running the Game

**Standard execution:**
```bash
python pacman.py
```

**Using the launcher script:**
```bash
./run_game.sh
```

**Note:** The `run_game.sh` script expects a virtual environment at `./.venv/bin/python`. If running without venv, use `python pacman.py` directly.

## Dependencies

Install dependencies with:
```bash
pip install -r requirements.txt
```

Or install Pygame directly:
```bash
pip install pygame
```

## Architecture

### Single-File Structure

The entire game is implemented in `pacman.py` with the following class hierarchy:

**Main Classes:**
- `Game` - Main game loop and state management (initialization at line 203)
- `Pacman` - Player character with movement and collision detection (line 40)
- `Ghost` - Enemy AI with vulnerability and respawn mechanics (line 112)

### Key Game Systems

**Maze System:**
- Grid-based maze defined as 2D array in `Game.__init__` (line 215)
- Values: `1` = wall, `0` = empty, `2` = dot, `3` = power pellet
- Maze dimensions: 40x27 grid cells, each cell is 20x20 pixels

**Power Pellet System:**
- Duration: 300 frames (5 seconds at 60 FPS) - configurable via `POWER_PELLET_DURATION` (line 38)
- Timer managed in `Game.update()` (line 280)
- Ghosts check timer in `Ghost.update()` (line 125) to determine vulnerability state
- Exponential scoring: 200 → 400 → 800 → 1600 points per ghost eaten

**Ghost AI:**
- Random direction changes in `Ghost.update()` (line 152)
- Wall collision triggers immediate direction change (line 174)
- Speed reduction to 50% when vulnerable (line 158)
- Respawn system: 180-frame timer (3 seconds) before returning to ghost house (line 141-148)

**Collision Detection:**
- Pacman-to-wall: Grid-based check in `Pacman.check_wall_collision()` (line 82)
- Pacman-to-ghost: Distance-based collision in `Game.update()` (line 306)
- Collision threshold: `PACMAN_SIZE + GHOST_SIZE - 10` pixels

**Scoring System:**
- Regular dots: 10 points (line 293)
- Power pellets: 50 points (line 296)
- Ghost eating: Base 200 points, doubles per ghost (line 299, 313)

### Constants and Configuration

Key constants defined at top of file (lines 14-38):
- `WINDOW_WIDTH`, `WINDOW_HEIGHT`: 800x600 pixels
- `FPS`: 60 frames per second
- `PACMAN_SPEED`: 3 pixels per frame
- `POWER_PELLET_DURATION`: 300 frames (5 seconds)
- Color definitions for all game elements

### Game Loop Structure

The main game loop in `Game.run()` (line 456) follows standard pattern:
1. `handle_events()` - Process keyboard input
2. `update()` - Update game state (physics, collisions, scoring)
3. `draw()` - Render all game elements
4. `clock.tick(FPS)` - Maintain 60 FPS

## Development Notes

**Modifying the maze:**
Edit the 2D array in `Game.__init__` starting at line 215. Use `1` for walls, `0` for empty space, `2` for dots, and `3` for power pellets.

**Adjusting game balance:**
- Ghost speed: Modify `self.speed` in `Ghost.__init__` (line 119)
- Power pellet duration: Change `POWER_PELLET_DURATION` constant (line 38)
- Pacman speed: Change `PACMAN_SPEED` constant (line 37)

**Controls:**
Keyboard handling in `Game.handle_events()` (line 260). Supports both WASD and arrow keys.

**No Testing Framework:**
This project has no automated tests. Manual testing via `python pacman.py` is required.
