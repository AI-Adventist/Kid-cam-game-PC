#!/usr/bin/env python3
"""
Kid Cam Game PC - Main Application
A fun camera-based game for kids!
"""

import pygame
import sys
import cv2
from src.game_manager import GameManager
from src.ui.main_menu import MainMenu
from src.utils.camera import CameraManager

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 30

class KidCamGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Kid Cam Game PC 🎮📷")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize game components
        self.camera_manager = CameraManager()
        self.game_manager = GameManager(self.screen, self.camera_manager)
        self.main_menu = MainMenu(self.screen)
        
        # Game state
        self.current_state = "menu"  # menu, playing, paused
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_state == "playing":
                        self.current_state = "menu"
                        self.game_manager.stop_current_game()
                    else:
                        self.running = False
                elif event.key == pygame.K_SPACE:
                    if self.current_state == "playing":
                        self.game_manager.toggle_pause()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_state == "menu":
                    selected_game = self.main_menu.handle_click(event.pos)
                    if selected_game:
                        self.current_state = "playing"
                        self.game_manager.start_game(selected_game)
    
    def update(self):
        """Update game state"""
        if self.current_state == "playing":
            self.game_manager.update()
        elif self.current_state == "menu":
            self.main_menu.update()
    
    def draw(self):
        """Draw everything to screen"""
        self.screen.fill((50, 150, 200))  # Sky blue background
        
        if self.current_state == "menu":
            self.main_menu.draw()
        elif self.current_state == "playing":
            self.game_manager.draw()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        print("🎮 Starting Kid Cam Game PC!")
        print("📷 Initializing camera...")
        
        if not self.camera_manager.initialize():
            print("❌ Could not initialize camera. Please check your camera connection.")
            return
        
        print("✅ Camera ready!")
        print("🎉 Game starting! Have fun!")
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        # Cleanup
        self.camera_manager.cleanup()
        pygame.quit()
        print("👋 Thanks for playing Kid Cam Game PC!")

def main():
    """Entry point"""
    try:
        game = KidCamGame()
        game.run()
    except Exception as e:
        print(f"❌ Error starting game: {e}")
        print("Please make sure you have a camera connected and try again.")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
