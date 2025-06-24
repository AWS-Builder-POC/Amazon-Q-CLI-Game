#!/usr/bin/env python3
"""
Test script for Menu functionality in Jungle Drive game
"""

import pygame
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from jungle_drive import Menu, Game
    
    print("🎮 Testing Menu functionality...")
    
    # Initialize pygame
    pygame.init()
    
    # Test Menu creation
    menu = Menu()
    print("✓ Menu created successfully")
    
    # Test menu options
    print(f"✓ Menu has {len(menu.options)} options:")
    for i, option in enumerate(menu.options):
        print(f"  {i}: {option['text']}")
    
    # Test pause mode
    menu.set_pause_mode(True)
    print("✓ Pause mode set")
    print(f"  First option now: {menu.options[0]['text']}")
    print(f"  Second option now: {menu.options[1]['text']}")
    
    # Test normal mode
    menu.set_pause_mode(False)
    print("✓ Normal mode restored")
    print(f"  First option now: {menu.options[0]['text']}")
    print(f"  Second option now: {menu.options[1]['text']}")
    
    # Test Game creation
    game = Game()
    print("✓ Game created successfully")
    
    print("\n✅ All menu tests passed!")
    
    pygame.quit()
    
except Exception as e:
    print(f"❌ Error during test: {e}")
    import traceback
    traceback.print_exc()
    pygame.quit()
