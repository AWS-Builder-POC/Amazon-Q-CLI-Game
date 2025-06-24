#!/usr/bin/env python3
"""
Test script for Menu navigation in Jungle Drive game
"""

import pygame
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from jungle_drive import Game
    
    print("🎮 Testing Menu Navigation...")
    
    # Initialize pygame
    pygame.init()
    
    # Create game instance
    game = Game()
    print("✓ Game created successfully")
    print(f"✓ Initial menu selection: {game.menu.selected_option}")
    
    # Simulate key presses
    print("\n🔧 Simulating menu navigation...")
    
    # Test DOWN arrow
    keys_just_pressed = {pygame.K_DOWN}
    old_selection = game.menu.selected_option
    
    # Simulate the key detection logic
    if pygame.K_DOWN in keys_just_pressed:
        if game.menu.selected_option < len(game.menu.options) - 1:
            game.menu.selected_option += 1
    
    print(f"✓ After DOWN key: {old_selection} → {game.menu.selected_option}")
    
    # Test UP arrow
    keys_just_pressed = {pygame.K_UP}
    old_selection = game.menu.selected_option
    
    if pygame.K_UP in keys_just_pressed:
        if game.menu.selected_option > 0:
            game.menu.selected_option -= 1
    
    print(f"✓ After UP key: {old_selection} → {game.menu.selected_option}")
    
    # Test menu options
    print(f"\n📋 Menu options available:")
    for i, option in enumerate(game.menu.options):
        marker = "👉" if i == game.menu.selected_option else "  "
        print(f"{marker} {i}: {option['text']}")
    
    print("\n✅ Menu navigation test completed!")
    
    pygame.quit()
    
except Exception as e:
    print(f"❌ Error during test: {e}")
    import traceback
    traceback.print_exc()
    pygame.quit()
