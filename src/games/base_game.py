"""
Base Game Class - Common functionality for all games
"""

import pygame
import numpy as np

class BaseGame:
    def __init__(self, screen, camera_manager):
        self.screen = screen
        self.camera_manager = camera_manager
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.running = False
        
        # Common colors
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'purple': (128, 0, 128),
            'orange': (255, 165, 0),
            'pink': (255, 192, 203)
        }
        
        # Common fonts
        try:
            self.title_font = pygame.font.Font(None, 48)
            self.text_font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
        except:
            self.title_font = pygame.font.Font(None, 48)
            self.text_font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
        
        # Camera display area
        self.camera_rect = pygame.Rect(50, 50, 320, 240)
        
    def start(self):
        """Start the game"""
        self.running = True
        print(f"🎮 {self.__class__.__name__} started!")
    
    def stop(self):
        """Stop the game"""
        self.running = False
        print(f"🛑 {self.__class__.__name__} stopped!")
    
    def update(self):
        """Update game state - to be overridden by subclasses"""
        pass
    
    def draw(self):
        """Draw game - to be overridden by subclasses"""
        # Draw camera feed
        self.draw_camera_feed()
        
        # Draw UI elements
        self.draw_ui()
    
    def draw_camera_feed(self):
        """Draw the camera feed in a designated area"""
        frame = self.camera_manager.get_frame_for_display()
        if frame is not None:
            # Convert numpy array to pygame surface
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            
            # Scale to fit camera rect
            scaled_frame = pygame.transform.scale(frame_surface, 
                                                (self.camera_rect.width, self.camera_rect.height))
            
            # Draw frame with border
            pygame.draw.rect(self.screen, self.colors['white'], 
                           self.camera_rect.inflate(10, 10))
            pygame.draw.rect(self.screen, self.colors['black'], 
                           self.camera_rect.inflate(10, 10), 3)
            
            self.screen.blit(scaled_frame, self.camera_rect)
    
    def draw_ui(self):
        """Draw common UI elements"""
        # Instructions
        instructions = [
            "Press ESC to return to menu",
            "Press SPACE to pause"
        ]
        
        y_pos = self.height - 60
        for instruction in instructions:
            text = self.small_font.render(instruction, True, self.colors['black'])
            self.screen.blit(text, (10, y_pos))
            y_pos += 25
    
    def draw_text_with_shadow(self, text, font, color, shadow_color, pos, shadow_offset=(2, 2)):
        """Draw text with shadow effect"""
        shadow_surface = font.render(text, True, shadow_color)
        text_surface = font.render(text, True, color)
        
        shadow_pos = (pos[0] + shadow_offset[0], pos[1] + shadow_offset[1])
        
        self.screen.blit(shadow_surface, shadow_pos)
        self.screen.blit(text_surface, pos)
    
    def draw_particle_effect(self, particles):
        """Draw particle effects"""
        for particle in particles:
            if particle['life'] > 0:
                alpha = int(255 * (particle['life'] / particle['max_life']))
                color = (*particle['color'][:3], alpha)
                
                # Create surface with alpha
                particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), 
                                                pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, color, 
                                 (particle['size'], particle['size']), particle['size'])
                
                self.screen.blit(particle_surface, 
                               (particle['x'] - particle['size'], particle['y'] - particle['size']))
    
    def update_particles(self, particles):
        """Update particle system"""
        for particle in particles[:]:  # Copy list to avoid modification during iteration
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # Gravity
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                particles.remove(particle)
    
    def create_particle(self, x, y, color, size=3, velocity=(0, -2)):
        """Create a single particle"""
        return {
            'x': x,
            'y': y,
            'vx': velocity[0] + (np.random.random() - 0.5) * 4,
            'vy': velocity[1] + (np.random.random() - 0.5) * 2,
            'color': color,
            'size': size,
            'life': 60,
            'max_life': 60
        }
