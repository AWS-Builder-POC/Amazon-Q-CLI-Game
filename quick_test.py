#!/usr/bin/env python3
"""
Quick test to verify the game runs without errors
"""

import pygame
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from jungle_drive import Game
    
    print("🎮 Starting Jungle Drive test...")
    
    # Initialize pygame
    pygame.init()
    
    # Create game instance
    game = Game()
    print("✓ Game created successfully")
    
    # Test basic game loop for a few frames
    for i in range(10):
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        
        # Test menu update
        game.menu.update()
        
        # Test menu drawing
        game.menu.draw(game.screen)
        
        # Update display
        pygame.display.flip()
        game.clock.tick(60)
    
    print("✓ Game loop test completed successfully")
    print("✅ Game is working properly!")
    
    pygame.quit()
    
except Exception as e:
    print(f"❌ Error during test: {e}")
    import traceback
    traceback.print_exc()
    pygame.quit()
