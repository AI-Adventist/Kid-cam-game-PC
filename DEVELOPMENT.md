# Kid Cam Game PC - Development Guide

## Project Structure

```
Kid-cam-game-PC/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup configuration
├── install.py             # Installation helper script
├── test_game.py           # Test suite
├── README.md              # User documentation
├── LICENSE                # MIT License
├── .gitignore            # Git ignore rules
├── DEVELOPMENT.md         # This file
└── src/                   # Source code
    ├── __init__.py
    ├── game_manager.py    # Manages game states and transitions
    ├── games/             # Individual game implementations
    │   ├── __init__.py
    │   ├── base_game.py   # Base class for all games
    │   ├── face_fun.py    # Face detection game
    │   ├── color_hunt.py  # Color detection game
    │   └── motion_magic.py # Hand/motion detection game
    ├── ui/                # User interface components
    │   ├── __init__.py
    │   └── main_menu.py   # Main menu interface
    ├── utils/             # Utility modules
    │   ├── __init__.py
    │   └── camera.py      # Camera management and CV processing
    └── effects/           # Visual effects (future expansion)
        └── __init__.py
```

## Architecture Overview

### Core Components

1. **Main Application (`main.py`)**
   - Entry point and main game loop
   - Handles pygame initialization and cleanup
   - Manages overall application state

2. **Game Manager (`src/game_manager.py`)**
   - Coordinates between different game modes
   - Handles game state transitions
   - Manages pause/resume functionality

3. **Camera Manager (`src/utils/camera.py`)**
   - Interfaces with OpenCV for camera input
   - Provides computer vision processing (face detection, hand tracking, color detection)
   - Uses MediaPipe for advanced CV features

4. **UI System (`src/ui/`)**
   - Main menu with animated, kid-friendly interface
   - Extensible for additional UI components

5. **Game Modules (`src/games/`)**
   - Base game class with common functionality
   - Individual game implementations
   - Particle systems and visual effects

### Game Modes

#### 1. Face Fun (`face_fun.py`)
- **Technology**: MediaPipe Face Detection
- **Features**: 
  - Real-time face detection and tracking
  - Fun visual overlays (crowns, hearts, sparkles)
  - Celebration effects when faces are detected
  - Score system based on face interactions

#### 2. Color Hunt (`color_hunt.py`)
- **Technology**: OpenCV color detection in HSV space
- **Features**:
  - Detects dominant colors in camera feed
  - Target color challenges with themed backgrounds
  - Progress tracking for color detection
  - Particle effects based on detected colors

#### 3. Motion Magic (`motion_magic.py`)
- **Technology**: MediaPipe Hand Tracking
- **Features**:
  - Real-time hand detection and tracking
  - Magic wand effects following hand movements
  - Falling star catching game
  - Magical particle trails and effects

## Technical Details

### Dependencies

- **pygame**: Game framework and graphics
- **opencv-python**: Computer vision and camera input
- **mediapipe**: Advanced CV features (face/hand detection)
- **numpy**: Numerical computations
- **Pillow**: Image processing support

### Performance Considerations

- Target framerate: 30 FPS
- Camera resolution: 640x480 for optimal performance
- Particle systems limited to prevent performance issues
- MediaPipe models optimized for real-time processing

### Safety and Privacy

- All processing happens locally
- No data is transmitted or stored
- Camera access only during active gameplay
- Easy exit mechanisms (ESC key)

## Development Guidelines

### Adding New Games

1. Create new game class inheriting from `BaseGame`
2. Implement required methods: `update()`, `draw()`
3. Add game to `GameManager.games` dictionary
4. Add menu button in `MainMenu`

Example:
```python
from src.games.base_game import BaseGame

class NewGame(BaseGame):
    def __init__(self, screen, camera_manager):
        super().__init__(screen, camera_manager)
        # Initialize game-specific variables
    
    def update(self):
        if not self.running:
            return
        # Game logic here
    
    def draw(self):
        # Drawing code here
        self.draw_camera_feed()
        self.draw_ui()
```

### Code Style

- Follow PEP 8 Python style guidelines
- Use descriptive variable names
- Add docstrings to classes and methods
- Keep methods focused and small
- Use type hints where appropriate

### Testing

Run the test suite before making changes:
```bash
python test_game.py
```

### Common Issues and Solutions

1. **Camera not detected**
   - Check camera permissions
   - Ensure no other applications are using the camera
   - Try different camera indices (0, 1, 2...)

2. **Performance issues**
   - Reduce particle count
   - Lower camera resolution
   - Optimize drawing operations

3. **MediaPipe errors**
   - Ensure proper lighting for face/hand detection
   - Check MediaPipe model files are accessible

## Future Enhancements

### Planned Features

1. **Sound System**
   - Background music
   - Sound effects for interactions
   - Volume controls

2. **Additional Games**
   - Object detection games
   - Gesture recognition challenges
   - Multiplayer modes

3. **Customization**
   - Theme selection
   - Difficulty levels
   - Accessibility options

4. **Data Features**
   - High score tracking
   - Achievement system
   - Progress statistics

### Technical Improvements

1. **Performance**
   - Multi-threading for CV processing
   - GPU acceleration where available
   - Optimized rendering pipeline

2. **Robustness**
   - Better error handling
   - Automatic camera recovery
   - Graceful degradation

3. **Extensibility**
   - Plugin system for games
   - Configuration files
   - Modular effects system

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## Building and Distribution

### Creating Executable

Use PyInstaller to create standalone executable:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

### Package Installation

Install in development mode:
```bash
pip install -e .
```

Create distribution packages:
```bash
python setup.py sdist bdist_wheel
```

## Troubleshooting

### Common Development Issues

1. **Import errors**: Ensure all dependencies are installed
2. **Camera permissions**: Check system camera permissions
3. **Performance**: Monitor CPU usage and optimize accordingly
4. **Cross-platform**: Test on different operating systems

### Debug Mode

Add debug prints and visual indicators:
```python
DEBUG = True

if DEBUG:
    print(f"FPS: {clock.get_fps():.1f}")
    pygame.draw.circle(screen, (255, 0, 0), hand_pos, 5)  # Debug marker
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Happy coding! 🎮📷✨
