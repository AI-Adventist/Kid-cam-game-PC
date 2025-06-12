"""
Game Manager - Handles different game modes and transitions
"""

import pygame
from src.games.face_fun import FaceFunGame
from src.games.color_hunt import ColorHuntGame
from src.games.motion_magic import MotionMagicGame

class GameManager:
    def __init__(self, screen, camera_manager):
        self.screen = screen
        self.camera_manager = camera_manager
        self.current_game = None
        self.game_name = None
        self.paused = False
        
        # Initialize games
        self.games = {
            'face_fun': FaceFunGame(screen, camera_manager),
            'color_hunt': ColorHuntGame(screen, camera_manager),
            'motion_magic': MotionMagicGame(screen, camera_manager)
        }
        
        # Fonts for pause screen
        try:
            self.pause_font = pygame.font.Font(None, 72)
            self.instruction_font = pygame.font.Font(None, 36)
        except:
            self.pause_font = pygame.font.Font(None, 72)
            self.instruction_font = pygame.font.Font(None, 36)
    
    def start_game(self, game_name):
        """Start a specific game mode"""
        if game_name in self.games:
            self.current_game = self.games[game_name]
            self.game_name = game_name
            self.paused = False
            self.current_game.start()
            print(f"🎮 Starting {game_name} game!")
    
    def stop_current_game(self):
        """Stop the current game"""
        if self.current_game:
            self.current_game.stop()
            self.current_game = None
            self.game_name = None
            self.paused = False
            print("🛑 Game stopped!")
    
    def toggle_pause(self):
        """Toggle pause state"""
        if self.current_game:
            self.paused = not self.paused
            if self.paused:
                print("⏸️ Game paused")
            else:
                print("▶️ Game resumed")
    
    def update(self):
        """Update current game"""
        if self.current_game and not self.paused:
            # Capture new frame
            if self.camera_manager.capture_frame():
                self.current_game.update()
    
    def draw(self):
        """Draw current game"""
        if self.current_game:
            self.current_game.draw()
            
            # Draw pause overlay if paused
            if self.paused:
                self._draw_pause_overlay()
    
    def _draw_pause_overlay(self):
        """Draw pause screen overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.pause_font.render("PAUSED", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(self.screen.get_width()//2, 
                                                self.screen.get_height()//2 - 50))
        self.screen.blit(pause_text, pause_rect)
        
        # Instructions
        instructions = [
            "Press SPACE to resume",
            "Press ESC to return to menu"
        ]
        
        y_offset = 50
        for instruction in instructions:
            text = self.instruction_font.render(instruction, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen.get_width()//2, 
                                            self.screen.get_height()//2 + y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 40
