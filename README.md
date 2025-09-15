# Bomberman Game

A Python implementation of the classic Bomberman game with a modern interface and score tracking system.

## Features

- **Classic Bomberman Gameplay**: Navigate through a maze, plant bombs, and defeat enemies
- **Modern Interface**: Clean menu system with high score tracking
- **JSON Database**: Persistent score storage with player statistics
- **Modular Architecture**: Well-organized code following software engineering best practices
- **Extensible Design**: Easy to add new features and modify game mechanics

## Game Controls

- **Movement**: WASD or Arrow Keys
- **Plant Bomb**: Spacebar
- **Menu Navigation**: Arrow Keys + Enter
- **Back/Quit**: Escape

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Bomberman
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python run_game.py
```

## Project Structure

```
Bomberman/
├── src/
│   ├── game/           # Core game logic
│   │   ├── game_engine.py
│   │   ├── game_map.py
│   │   ├── player.py
│   │   ├── bomb.py
│   │   └── enemy.py
│   ├── ui/             # User interface components
│   │   ├── menu.py
│   │   └── score_display.py
│   ├── database/       # Data persistence
│   │   └── score_manager.py
│   ├── utils/          # Utilities and constants
│   │   └── constants.py
│   └── main.py         # Main application entry point
├── tests/              # Unit tests
├── data/               # JSON database storage
├── assets/             # Game assets (sprites, sounds)
├── requirements.txt
├── setup.py
└── run_game.py
```

## Architecture

The game follows a modular architecture with clear separation of concerns:

- **Game Engine**: Manages the main game loop, events, and state
- **Game Objects**: Player, enemies, bombs, and map with their own logic
- **UI Components**: Menu system and score display
- **Database Layer**: JSON-based score persistence
- **Utils**: Shared constants and utilities

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Adding New Features
1. Create new modules in appropriate directories
2. Follow the existing naming conventions (snake_case)
3. Add unit tests for new functionality
4. Update constants.py for new configuration values

## Game Mechanics

- **Player**: Blue square that can move and plant bombs
- **Enemies**: Red squares that move randomly and can kill the player
- **Bombs**: Explode after 3 seconds, destroying walls and enemies
- **Walls**: Gray (indestructible) and brown (destructible) barriers
- **Scoring**: Points for destroying walls and enemies, bonus for completing levels

## Configuration

Game settings can be modified in `src/utils/constants.py`:
- Screen dimensions
- Game speed
- Bomb timer and explosion radius
- Scoring values
- Map size

## License

This project is open source and available under the MIT License.