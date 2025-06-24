#!/usr/bin/env python3
"""
Live test for Menu navigation - run this and use arrow keys
"""

import pygame
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from jungle_drive import Game
    
    print("🎮 Live Menu Test - Use arrow keys to test navigation")
    print("Press ESC to exit test")
    
    # Initialize pygame
    pygame.init()
    
    # Create game instance
    game = Game()
    
    # Test loop
    running = True
    frame_count = 0
    
    while running and frame_count < 600:  # Run for 10 seconds max
        frame_count += 1
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    print(f"UP pressed - Current selection: {game.menu.selected_option}")
                elif event.key == pygame.K_DOWN:
                    print(f"DOWN pressed - Current selection: {game.menu.selected_option}")
                elif event.key == pygame.K_RETURN:
                    print(f"ENTER pressed on option: {game.menu.selected_option}")
        
        # Handle input using game's method
        if not game.handle_input():
            running = False
        
        # Update menu
        game.menu.update()
        
        # Draw
        game.screen.fill((0, 0, 0))
        game.menu.draw(game.screen)
        
        # Show current selection in window title
        pygame.display.set_caption(f"Menu Test - Selected: {game.menu.selected_option} - {game.menu.options[game.menu.selected_option]['text']}")
        
        pygame.display.flip()
        game.clock.tick(60)
    
    print("✅ Live menu test completed!")
    pygame.quit()
    
except Exception as e:
    print(f"❌ Error during test: {e}")
    import traceback
    traceback.print_exc()
    pygame.quit()
