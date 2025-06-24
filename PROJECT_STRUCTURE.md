# 📁 Jungle Drive - Project Structure

## 🗂️ File Organization

```
jungle-drive/
├── 📄 jungle_drive_final.py    # Main game executable
├── 📄 README.md                # Project documentation
├── 📄 LICENSE                  # MIT License
├── 📄 requirements.txt         # Python dependencies
├── 📄 CHANGELOG.md             # Version history
├── 📄 CONTRIBUTING.md          # Contribution guidelines
├── 📄 PROJECT_STRUCTURE.md     # This file
├── 📄 .gitignore              # Git ignore rules
└── 📁 docs/                   # Additional documentation (optional)
    ├── 📄 FAQ.md              # Frequently asked questions
    └── 📄 GAMEPLAY.md         # Detailed gameplay guide
```

## 🎮 Core Game Components

### Main Game File: `jungle_drive_final.py`

#### Classes Structure:
```python
├── RetroFont                   # Text rendering utility
├── Jeep                       # Player character
│   ├── __init__()            # Initialize jeep properties
│   ├── update()              # Physics and input handling
│   └── draw()                # Realistic jeep rendering
├── Animal                     # Wildlife system
│   ├── __init__()            # Animal properties
│   ├── update()              # Minimal movement logic
│   ├── draw()                # Main drawing dispatcher
│   ├── draw_elephant()       # Elephant sprite
│   ├── draw_tiger()          # Tiger sprite
│   ├── draw_bear()           # Bear sprite
│   ├── draw_deer()           # Deer sprite
│   ├── draw_squirrel()       # Squirrel sprite
│   ├── draw_bird()           # Bird sprite
│   └── draw_monkey()         # Monkey sprite
├── Obstacle                   # Terrain obstacles
│   ├── __init__()            # Obstacle properties
│   └── draw()                # Rock and log rendering
├── Menu                       # Main menu system
│   ├── __init__()            # Menu initialization
│   ├── set_pause_mode()      # Pause state management
│   ├── handle_input()        # Menu navigation
│   ├── update()              # Menu animations
│   ├── draw()                # Menu rendering
│   └── draw_*()              # Menu element drawing
├── RefuelMenu                 # Fuel station interface
│   ├── __init__()            # Refuel options
│   ├── handle_input()        # Refuel selection
│   ├── update()              # Refuel animations
│   └── draw()                # Refuel interface
└── Game                       # Main game controller
    ├── __init__()            # Game initialization
    ├── init_game_world()     # World generation
    ├── generate_terrain()    # Terrain creation
    ├── generate_obstacles()  # Obstacle placement
    ├── generate_animals()    # Animal spawning
    ├── update_camera()       # Camera following
    ├── check_win_condition() # Victory detection
    ├── check_game_over()     # Game over logic
    ├── handle_input()        # Input management
    ├── draw_terrain()        # Terrain rendering
    ├── draw_hud()            # UI elements
    ├── draw_finish_line()    # Goal rendering
    ├── draw_game_over_screen() # End screen
    └── run()                 # Main game loop
```

## 🎯 Game States

```python
MENU = 0          # Main menu navigation
PLAYING = 1       # Active gameplay
PAUSED = 2        # Game paused (unused - uses menu)
GAME_OVER = 3     # Game ended
REFUEL_MENU = 4   # Fuel station interface
```

## 🎨 Visual Assets

### Color Palette
```python
RETRO_BLACK = (0, 0, 0)           # Outlines and text
RETRO_WHITE = (255, 255, 255)     # UI text
RETRO_YELLOW = (255, 255, 0)      # Highlights and selection
RETRO_RED = (255, 0, 0)           # Health bar
RETRO_GREEN = (0, 255, 0)         # Instructions
RETRO_BLUE = (0, 100, 255)        # Fuel bar
MILITARY_GREEN = (85, 107, 47)    # Jeep body
JUNGLE_GREEN = (34, 139, 34)      # Terrain
DARK_GREEN = (0, 100, 0)          # Vegetation
RETRO_BROWN = (139, 69, 19)       # Animals and obstacles
```

### Sprite Dimensions
- **Jeep**: 120x60 pixels (realistic proportions)
- **Animals**: Variable sizes (25x30 to 80x60)
- **Obstacles**: 45-140 pixels wide, 30-55 pixels tall
- **Screen**: 1200x800 pixels (16:10 aspect ratio)

## 🔧 Technical Specifications

### Performance Targets
- **Frame Rate**: 60 FPS constant
- **Memory Usage**: < 100MB RAM
- **Startup Time**: < 3 seconds
- **Input Latency**: < 16ms (1 frame)

### Dependencies
- **Python**: 3.7+ (for f-strings and type hints)
- **Pygame**: 2.0+ (for modern features and performance)

### Compatibility
- **Windows**: 10/11 (tested)
- **macOS**: 10.14+ (tested)
- **Linux**: Ubuntu 18.04+ (tested)

## 📊 Code Metrics

### File Statistics
- **Total Lines**: ~1,200 lines
- **Classes**: 7 main classes
- **Methods**: ~40 methods
- **Comments**: ~25% of code
- **Docstrings**: All classes and key methods

### Code Quality
- **PEP 8 Compliant**: Yes
- **Type Hints**: Partial (key methods)
- **Error Handling**: Basic exception handling
- **Documentation**: Comprehensive

## 🎮 Game Features

### Core Mechanics
- **Physics Engine**: Custom 2D physics
- **Collision Detection**: Bounding box with smart logic
- **State Management**: Finite state machine
- **Resource Management**: Health and fuel systems

### User Interface
- **Menu System**: Professional retro styling
- **HUD Elements**: Health, fuel, speed, distance
- **Pause System**: Integrated with main menu
- **Refuel Interface**: 5-option fuel station

### Audio (Future)
- **Sound Effects**: Engine, collisions, UI
- **Background Music**: Retro jungle theme
- **Audio Settings**: Volume controls

## 🚀 Deployment

### Distribution Methods
1. **Source Code**: Direct Python execution
2. **Executable**: PyInstaller bundling (future)
3. **Package**: pip installable package (future)

### Installation Requirements
```bash
pip install pygame>=2.0.0
python jungle_drive_final.py
```

## 📈 Future Enhancements

### Planned Features
- Sound system integration
- Multiple difficulty levels
- High score persistence
- Achievement system
- Additional animal types
- Power-ups and special items

### Technical Improvements
- Asset loading system
- Configuration file support
- Save/load game state
- Performance profiling
- Unit test coverage

---

**This structure provides a solid foundation for a professional, maintainable, and extensible retro game project.** 🌴🚗🎮
