# Columns - Sega Mega Drive (1990) Recreation

Python recreation of the classic Columns puzzle game using Pygame, featuring gameplay mechanics, scoring system, and visual effects.

## Game Overview

Columns is a tile-matching puzzle game where players manipulate falling columns of three colored jewels to create matches of three or more consecutive jewels horizontally, vertically, or diagonally.

## Features

### Core Gameplay
- **6x13 Game Board**: Classic Columns grid dimensions
- **7 Jewel Types**: Pink (X), Purple (Y), Blue (Z), Green (W), Yellow (T), Orange (V), Red (S)
- **Falling Mechanics**: Continuous jewel columns descending with gravity physics
- **Match-3+ Logic**: Matches detected in all directions (horizontal, vertical, diagonal)
- **Cascading Matches**: Jewels fall after matches clear, enabling chain reactions

### Controls
- **Arrow Left/Right**: Shift falling column horizontally
- **Arrow Down**: Accelerate column descent
- **Spacebar**: Rotate jewels within the column

### Visual Features
- **Next Piece Preview**: Shows upcoming 3-jewel column
- **Flashing Animations**: 
  - White flash when jewels are matched
  - Border flash when column lands
- **Color-Coded Jewels**: Vibrant distinct colors for each jewel type
- **Grid System**: Clear visual separation between cells
- **Resizable Window**: Dynamic scaling (800x800 default)

### Scoring System
- **Pink (X)**: 100 points
- **Purple (Y)**: 150 points  
- **Blue (Z)**: 125 points
- **Green (W)**: 75 points
- **Yellow (T)**: 200 points
- **Orange (V)**: 500 points (highest value)
- **Red (S)**: 250 points

### Persistence
- **High Score Tracking**: Automatically saves and displays high score
- **File-Based Storage**: Persistent across game sessions

## Technical Implementation

### Architecture
```
Columns-Game/
├── columns_game.py        # Main game loop and UI rendering
├── game_state_model.py    # Game logic and state management
└── highscore.txt          # Persistent high score storage
```

### Object-Oriented Design
- **ColumnsGame Class**: Handles rendering, event processing, and game loop
- **GameState Class**: Manages board state, match detection, and game logic
- **FallingGems Class**: Represents individual falling columns


#### Match Detection
- **Horizontal Matching**: Row-by-row scan for consecutive jewels
- **Vertical Matching**: Column-by-column scan from bottom to top
- **Diagonal Matching**: Complex algorithm checking all diagonal lines

#### Gravity System
- Jewels automatically fall when space exists below
- Cascading effect after matches are cleared
- Collision detection prevents overlap

#### Faller State Machine
- **FALLER_FALLING**: Column actively descending
- **FALLER_STOPPED**: Column landed but not frozen
- **FILLED_POSITION**: Jewel locked in place
- **MATCHED_POSITION**: Jewel ready to be cleared


## Technical Stack

- **Language**: Python 3.x
- **Game Framework**: Pygame
- **Graphics**: 2D sprite-based rendering
- **Rendering**: 10 FPS tick rate for smooth gameplay

## Performance Optimizations

- Board state representation using 2D arrays
- Separate content and state tracking for each position
- Tick-based timing system (10 FPS) for consistent gameplay
- Event-driven input handling

## Code Highlights

### Dynamic Rendering
- Fractional coordinate system for responsive scaling
- Buffer zones for UI elements
- Real-time color mapping for jewel types

### State Management
- State tracking for every board position
- Separation of concerns (content vs. state)
- Event propagation through game state updates


## Future Enhancements

- Multiple difficulty levels (faster descent rates)
- Sound effects and background music
- Combo multipliers for chain reactions
- Online leaderboard integration
- Power-ups and special jewels
- Level progression system
- Pause/resume functionality

## Learning Outcomes
Things I've learned:
- Game loop architecture and timing
- Event-driven programming
- Complex state machine implementation
- Efficient collision detection
- Pattern matching algorithms
- File-based data persistence
- Object-oriented game design
- 2D graphics rendering

## Credits

Based on the original Columns game developed by Jay Geertsen and published by Sega for the Sega Mega Drive (Genesis) in 1990.
