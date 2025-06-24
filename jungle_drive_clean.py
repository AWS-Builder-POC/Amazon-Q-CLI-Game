#!/usr/bin/env python3
"""
Jungle Drive - Retro Military Offroad Adventure Game

A classic retro-style jungle driving game where you navigate a military jeep
through challenging terrain to reach the finish line on top of a mountain.

Features:
- Realistic military jeep with detailed side-view graphics
- 7 different jungle animals (Elephant, Tiger, Bear, Deer, Squirrel, Birds, Monkey)
- Smart collision system with fuel management
- Professional pause/resume functionality
- Fuel refueling system with 5 options
- Retro pixel art styling with authentic 80s/90s aesthetics

Controls:
- Arrow Keys: Navigate menus, control jeep
- P Key: Pause/Resume game
- Enter: Select menu options
- ESC: Return to main menu

Author: Game Development Team
Version: 1.0
License: MIT
"""

import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors (Retro Palette)
RETRO_BLACK = (0, 0, 0)
RETRO_WHITE = (255, 255, 255)
RETRO_RED = (255, 0, 0)
RETRO_GREEN = (0, 255, 0)
RETRO_BLUE = (0, 100, 255)
RETRO_YELLOW = (255, 255, 0)
RETRO_BROWN = (139, 69, 19)
MILITARY_GREEN = (85, 107, 47)
JUNGLE_GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)

# Game States
MENU = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3
REFUEL_MENU = 4
class RetroFont:
    """Utility class for rendering retro-style text"""
    
    @staticmethod
    def render_retro_text(screen, text, x, y, size, color, bold=False):
        """Render text with retro styling"""
        try:
            font = pygame.font.Font(None, size)
            if bold:
                font.set_bold(True)
            
            # Create text surface
            text_surface = font.render(text, True, color)
            
            # Add retro outline effect
            if size > 30:
                outline_surface = font.render(text, True, RETRO_BLACK)
                for dx in [-2, -1, 0, 1, 2]:
                    for dy in [-2, -1, 0, 1, 2]:
                        if dx != 0 or dy != 0:
                            screen.blit(outline_surface, (x + dx, y + dy))
            
            screen.blit(text_surface, (x, y))
        except Exception as e:
            print(f"Font rendering error: {e}")


class Jeep:
    """Military jeep player character with realistic physics and graphics"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 120
        self.height = 60
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_speed = 6
        self.acceleration = 0.4
        self.jump_power = 15
        self.gravity = 0.8
        self.friction = 0.85
        self.health = 100
        self.fuel = 100
        self.on_ground = True
        self.facing_right = True
        self.engine_sound_timer = 0
