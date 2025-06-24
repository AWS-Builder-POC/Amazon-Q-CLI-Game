# Contributing to Jungle Drive

Thank you for your interest in contributing to Jungle Drive! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Pygame 2.0 or higher
- Git for version control

### Setting Up Development Environment

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/jungle-drive.git
   cd jungle-drive
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the game to test**
   ```bash
   python jungle_drive_final.py
   ```

## 🎯 How to Contribute

### Reporting Bugs
- Use the GitHub issue tracker
- Include detailed steps to reproduce
- Provide system information (OS, Python version, Pygame version)
- Include screenshots if applicable

### Suggesting Features
- Open an issue with the "enhancement" label
- Describe the feature and its benefits
- Consider backward compatibility
- Discuss implementation approach

### Code Contributions

#### Branch Naming
- `feature/feature-name` for new features
- `bugfix/bug-description` for bug fixes
- `docs/documentation-update` for documentation

#### Coding Standards
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Add docstrings to classes and methods
- Keep functions focused and modular
- Comment complex logic

#### Example Code Style
```python
class GameComponent:
    """Brief description of the component's purpose"""
    
    def __init__(self, x, y):
        """Initialize component with position"""
        self.x = x
        self.y = y
        self.active = True
    
    def update(self, delta_time):
        """Update component state
        
        Args:
            delta_time (float): Time elapsed since last update
        """
        if not self.active:
            return
        
        # Update logic here
        pass
```

### Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Test your changes thoroughly
   - Ensure the game runs without errors

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**
   - Provide a clear title and description
   - Reference any related issues
   - Include screenshots for visual changes

## 🎮 Game Architecture

### Core Components
- **Game**: Main game controller and state management
- **Jeep**: Player character with physics and rendering
- **Animal**: Wildlife system with various animal types
- **Obstacle**: Terrain obstacles (rocks and logs)
- **Menu**: Main menu system with navigation
- **RefuelMenu**: Fuel station interface

### Key Systems
- **Collision Detection**: Smart system for top vs side collisions
- **Fuel Management**: Strategic resource management
- **State Management**: Menu, playing, paused, refuel states
- **Rendering Pipeline**: Efficient graphics rendering

## 🎨 Art and Design Guidelines

### Visual Style
- Maintain retro pixel art aesthetic
- Use thick black outlines (2-4 pixels)
- Follow the established color palette
- Keep animations minimal and non-distracting

### Color Palette
```python
RETRO_BLACK = (0, 0, 0)
RETRO_WHITE = (255, 255, 255)
RETRO_YELLOW = (255, 255, 0)
MILITARY_GREEN = (85, 107, 47)
JUNGLE_GREEN = (34, 139, 34)
```

## 🧪 Testing

### Manual Testing
- Test all menu navigation
- Verify collision detection works correctly
- Check fuel and health systems
- Test pause/resume functionality
- Ensure refuel system works

### Performance Testing
- Maintain 60 FPS during gameplay
- Check memory usage doesn't grow over time
- Verify smooth scrolling and animations

## 📝 Documentation

### Code Documentation
- Add docstrings to all classes and methods
- Comment complex algorithms
- Update README.md for new features
- Update CHANGELOG.md for releases

### User Documentation
- Update controls section for new features
- Add gameplay tips for new mechanics
- Include screenshots for visual features

## 🏆 Recognition

Contributors will be recognized in:
- README.md acknowledgments section
- CHANGELOG.md for their contributions
- GitHub contributors list

## 📞 Getting Help

- Open an issue for questions
- Join discussions in the repository
- Contact maintainers for major changes

## 📋 Checklist for Contributors

Before submitting a pull request:

- [ ] Code follows PEP 8 style guidelines
- [ ] All functions have docstrings
- [ ] Changes are tested manually
- [ ] No debug print statements left in code
- [ ] README.md updated if needed
- [ ] CHANGELOG.md updated for significant changes
- [ ] Commit messages are clear and descriptive

Thank you for contributing to Jungle Drive! 🌴🚗🎮
