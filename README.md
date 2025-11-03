# Simple Pacman Game

A basic Pacman-style game built with Python and Pygame that runs on Mac desktop.

## Features

- Classic Pacman gameplay with maze navigation
- Player-controlled Pacman character with mouth animation
- Four colorful ghosts with simple AI
- **Power Pellets** - Large yellow pellets that make ghosts vulnerable
- **Ghost Eating** - Eat vulnerable ghosts for bonus points during power mode
- Dot collection scoring system
- Lives system (3 lives)
- Win/lose conditions
- Keyboard controls (WASD or Arrow Keys)
- Power pellet timer with visual indicators

## Requirements

- Python 3.6 or higher
- Pygame 2.0.0 or higher
- macOS (tested on macOS)

## Installation

1. **Clone or download this repository**
   ```bash
   cd /Users/jlacanienta/workspace/acme-pacman-prototype
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install Pygame directly:
   ```bash
   pip install pygame
   ```

3. **Make the game executable (optional)**
   ```bash
   chmod +x pacman.py
   ```

## How to Run

Simply run the Python script:

```bash
python pacman.py
```

Or if you made it executable:

```bash
./pacman.py
```

## How to Play

### Controls
- **Arrow Keys** or **WASD**: Move Pacman around the maze
- **ESC**: Quit the game

### Objective
- Collect all the white dots and yellow power pellets in the maze to win
- Avoid the colored ghosts (red, pink, cyan, orange) when they're not vulnerable
- **Power Pellets**: Eat the large yellow pulsing pellets to make ghosts vulnerable for 5 seconds
- **Ghost Eating**: When ghosts are blue and vulnerable, you can eat them for bonus points!
- You have 3 lives - lose one each time a ghost catches you (when not in power mode)
- Score points by collecting dots (10 points), power pellets (50 points), and eating ghosts (200, 400, 800, 1600 points)

### Game Elements
- **Yellow Circle**: Pacman (you)
- **Colored Circles with Eyes**: Ghosts (avoid when normal, eat when blue!)
- **White Small Dots**: Collectible dots (10 points each)
- **Large Yellow Pulsing Circles**: Power pellets (50 points, makes ghosts vulnerable)
- **Blue Circles with Eyes**: Vulnerable ghosts (can be eaten for bonus points)
- **Blue Squares**: Walls (can't pass through)

### Power Pellet Mechanics
- **Duration**: Power pellets make ghosts vulnerable for 5 seconds
- **Visual Feedback**: Timer bar and countdown displayed on screen
- **Ghost Behavior**: Vulnerable ghosts turn blue and move slower
- **Scoring Bonus**: Eating ghosts gives increasing points (200→400→800→1600)
- **Flashing Warning**: Ghosts flash white when power effect is about to end
- **Respawn**: Eaten ghosts respawn as eyes and return to the ghost house

## Game Features

- **Pacman Movement**: Smooth movement with directional mouth animation
- **Ghost AI**: Ghosts move randomly and change direction when hitting walls
- **Power Pellet System**: Four power pellets positioned strategically in maze corners
- **Vulnerable Ghosts**: Ghosts turn blue and move slower when power pellet is active
- **Ghost Eating**: Eat vulnerable ghosts for exponentially increasing bonus points
- **Visual Feedback**: Power timer bar, countdown, and ghost flashing warnings
- **Collision Detection**: Accurate collision with walls, dots, power pellets, and ghosts
- **Scoring System**: Points for dots (10), power pellets (50), and ghosts (200-1600)
- **Lives System**: Start with 3 lives, lose one per ghost collision (when not powered)
- **Win/Lose Conditions**: Win by collecting all items, lose when lives reach zero

## Technical Details

- **Window Size**: 800x600 pixels
- **Frame Rate**: 60 FPS
- **Maze Size**: 40x27 grid cells
- **Programming Language**: Python 3
- **Graphics Library**: Pygame

## Troubleshooting

### "No module named 'pygame'"
Install Pygame using pip:
```bash
pip install pygame
```

### Permission denied when running
Make the file executable:
```bash
chmod +x pacman.py
```

### Game runs slowly
- Close other applications to free up system resources
- The game is designed to run at 60 FPS on modern Macs

### Game window doesn't appear
- Make sure you have a graphical environment (not running in terminal-only mode)
- Try running from Terminal.app rather than other terminal applications

## Customization

You can easily modify the game by editing `pacman.py`:

- **Change colors**: Modify the color constants at the top of the file
- **Adjust speed**: Change `PACMAN_SPEED` or ghost speed values
- **Modify maze**: Edit the `self.maze` array in the Game class
- **Add sounds**: Pygame supports sound - add `pygame.mixer` calls
- **Change window size**: Modify `WINDOW_WIDTH` and `WINDOW_HEIGHT`

## License

This is a simple educational project. Feel free to modify and distribute as needed.

## Credits

Created as a simple demonstration of game development with Python and Pygame.