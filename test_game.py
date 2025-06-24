#!/usr/bin/env python3
"""
Test script for Jungle Drive game
"""

try:
    import pygame
    print("✓ Pygame imported successfully")
    
    # Test basic game initialization
    from jungle_drive import Game
    print("✓ Game class imported successfully")
    
    # Test game creation (without running)
    game = Game()
    print("✓ Game object created successfully")
    
    print("\n🎮 Game is ready to run!")
    print("Run: python jungle_drive.py")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install pygame: pip install pygame")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Check the game code for issues")
