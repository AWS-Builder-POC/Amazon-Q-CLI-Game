#!/usr/bin/env python3
"""
Test script for Animal methods in Jungle Drive game
"""

try:
    import pygame
    pygame.init()
    
    from jungle_drive import Animal
    
    # Test creating each animal type
    animal_types = ["elephant", "tiger", "deer", "bear", "squirrel", "bird", "monkey"]
    
    print("Testing Animal class methods:")
    
    for animal_type in animal_types:
        try:
            animal = Animal(100, 100, animal_type)
            print(f"✓ {animal_type.capitalize()} created successfully")
            
            # Test if the draw method exists
            method_name = f"draw_{animal_type}"
            if hasattr(animal, method_name):
                print(f"✓ {method_name} method exists")
            else:
                print(f"❌ {method_name} method missing")
                
        except Exception as e:
            print(f"❌ Error creating {animal_type}: {e}")
    
    print("\n🎮 Animal tests completed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
