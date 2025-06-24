# 🌴 Jungle Drive - Retro Military Offroad Adventure

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

A classic retro-style jungle driving game where you navigate a military jeep through challenging terrain to reach the finish line on top of a mountain. Experience the nostalgia of classic arcade games with modern gameplay mechanics!

![Game Screenshot](screenshots/gameplay.png)

## 🎮 Features

### 🚗 Realistic Military Jeep
- **Detailed side-view graphics** with authentic military styling
- **Realistic physics** including acceleration, jumping, and gravity
- **Military star emblem** and canvas soft top
- **Detailed wheels** with tread patterns and military rims

### 🐾 Wildlife & Environment
- **7 different jungle animals**: Elephant, Tiger, Bear, Deer, Squirrel, Birds, Monkey
- **Static, non-distracting animations** for immersive gameplay
- **Dynamic terrain** with hills, valleys, and mountain climbing
- **Retro pixel art styling** with authentic 80s/90s aesthetics

### ⚡ Smart Gameplay Mechanics
- **Intelligent collision system**: Different effects for top vs side collisions
- **Fuel management**: Strategic gameplay with 2x consumption when landing on obstacles
- **Health system**: Take damage from side collisions only
- **Refueling stations**: 5 different refuel options to continue your journey

### 🎨 Retro Presentation
- **Professional menu system** with sunset backgrounds
- **Pause/resume functionality** with "Resting on Tyres" theme
- **Chunky pixel graphics** with bold outlines
- **Classic arcade color palette**

## 🕹️ Controls

### Menu Navigation
- **↑↓ Arrow Keys**: Navigate menu options
- **ENTER**: Select highlighted option
- **ESC**: Return to main menu (from game)

### Gameplay
- **→ Right Arrow**: Accelerate forward
- **← Left Arrow**: Reverse/brake
- **↑ Up Arrow**: Jump over obstacles
- **↓ Down Arrow**: Fast descent (when airborne)
- **P Key**: Pause game (shows "Resting on Tyres")
- **R Key**: Restart (when game over)

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Pygame 2.0 or higher

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/jungle-drive](https://github.com/AWS-Builder-POC/Amazon-Q-CLI-Game.git
   cd jungle-drive
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**
   ```bash
   python jungle_drive_final.py
   ```

## 📋 Game Mechanics

### Collision System
- **Landing on top of obstacles**: Reduces fuel by 2x (strategic gameplay)
- **Side collisions**: Causes health damage and bounce-back
- **Smart detection**: Y-position comparison determines collision type

### Fuel Management
- **Normal consumption**: 0.04 units when moving, 0.01 when idle
- **Obstacle penalty**: 0.2 units when landing on obstacles
- **Refuel options**: 5 different levels (25%, 50%, 75%, 100%, or continue)

### Health System
- **Starting health**: 100 points
- **Damage source**: Side collisions with obstacles only
- **Game over**: When health reaches 0

## 🎯 Gameplay Tips

### For Beginners
- **Jump early**: Use up arrow to clear obstacles before hitting them
- **Watch your speed**: Slower speeds make obstacle avoidance easier
- **Land on top**: Strategic obstacle landing saves health but costs fuel
- **Conserve fuel**: Don't hold accelerator constantly

### Advanced Strategies
- **Fuel vs Health trade-off**: Sometimes it's better to take side damage than waste fuel
- **Momentum management**: Use terrain slopes to maintain speed efficiently
- **Animal spotting**: Enjoy the wildlife while focusing on the path ahead

## 🏗️ Technical Details

### Architecture
- **Object-oriented design** with separate classes for game components
- **State management** for menu, gameplay, pause, and refuel states
- **Modular rendering** system for clean graphics pipeline
- **Event-driven input** handling for responsive controls

### Performance
- **60 FPS gameplay** for smooth retro gaming experience
- **Efficient collision detection** with bounding box optimization
- **Static background generation** to prevent visual artifacts
- **Memory-efficient sprite rendering**

### Code Structure
```
jungle_drive_final.py       # Main game file
├── RetroFont              # Text rendering utility
├── Jeep                   # Player character class
├── Animal                 # Wildlife system
├── Obstacle               # Terrain obstacles
├── Menu                   # Main menu system
├── RefuelMenu             # Fuel station interface
└── Game                   # Main game controller
```

## 🎨 Art Style

### Retro Aesthetics
- **Chunky pixel art** with thick black outlines
- **Bold, contrasting colors** inspired by 80s arcade games
- **Authentic retro palette** with military and jungle themes
- **Professional presentation** with modern polish

### Visual Elements
- **Military jeep**: Detailed side-view with realistic proportions
- **Jungle animals**: Natural colors with retro styling
- **Terrain**: Varied landscapes from jungle to mountain peak
- **UI elements**: Clean, readable interface with retro flair

## 🔧 Development

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings to classes and methods
- Keep functions focused and modular

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by classic arcade driving games
- Built with Python and Pygame
- Retro art style influenced by 80s/90s arcade aesthetics
- Military jeep design based on classic WWII vehicles


---

**Enjoy your retro jungle adventure!** 🌴🚗🎮

*Made with ❤️ for retro gaming enthusiasts*
