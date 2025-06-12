"""
Color Hunt Game - Interactive color detection game for kids
"""

import pygame
import random
import math
from src.games.base_game import BaseGame

class ColorHuntGame(BaseGame):
    def __init__(self, screen, camera_manager):
        super().__init__(screen, camera_manager)
        self.target_color = None
        self.detected_color = None
        self.score = 0
        self.particles = []
        self.success_timer = 0
        self.color_change_timer = 0
        
        # Color definitions with fun names
        self.color_targets = {
            'red': {'name': '🔴 Red Fire', 'color': self.colors['red'], 'effect': 'fire'},
            'blue': {'name': '🔵 Blue Ocean', 'color': self.colors['blue'], 'effect': 'water'},
            'green': {'name': '🟢 Green Nature', 'color': self.colors['green'], 'effect': 'leaves'},
            'yellow': {'name': '🟡 Yellow Sun', 'color': self.colors['yellow'], 'effect': 'sparkle'},
            'purple': {'name': '🟣 Purple Magic', 'color': self.colors['purple'], 'effect': 'magic'}
        }
        
        # Start with first color
        self._set_new_target_color()
        
        # Game state
        self.consecutive_detections = 0
        self.detection_threshold = 30  # Frames needed for success
        
    def _set_new_target_color(self):
        """Set a new target color to find"""
        self.target_color = random.choice(list(self.color_targets.keys()))
        self.consecutive_detections = 0
        self.color_change_timer = 0
        print(f"🎯 New target: {self.color_targets[self.target_color]['name']}")
    
    def update(self):
        """Update color hunt game"""
        if not self.running:
            return
        
        # Detect dominant color in camera
        self.detected_color = self.camera_manager.detect_dominant_color()
        
        # Check if detected color matches target
        if self.detected_color == self.target_color:
            self.consecutive_detections += 1
            
            # Success if detected for enough frames
            if self.consecutive_detections >= self.detection_threshold:
                self._color_found_success()
        else:
            self.consecutive_detections = max(0, self.consecutive_detections - 2)
        
        # Auto-change color after time limit
        self.color_change_timer += 1
        if self.color_change_timer > 600:  # 10 seconds at 60 FPS
            self._set_new_target_color()
        
        # Update particles
        self.update_particles(self.particles)
        
        # Create ambient particles based on detected color
        if self.detected_color and random.random() < 0.3:
            self._create_color_particles()
        
        # Update success timer
        if self.success_timer > 0:
            self.success_timer -= 1
    
    def draw(self):
        """Draw color hunt game"""
        # Background based on target color
        self._draw_themed_background()
        
        # Draw camera feed
        self.draw_camera_feed()
        
        # Draw color detection area
        self._draw_detection_area()
        
        # Draw particles
        self.draw_particle_effect(self.particles)
        
        # Draw UI
        self._draw_game_ui()
        
        # Draw base UI
        self.draw_ui()
    
    def _draw_themed_background(self):
        """Draw background themed to target color"""
        target_info = self.color_targets[self.target_color]
        base_color = target_info['color']
        
        # Create gradient background
        for y in range(self.height):
            ratio = y / self.height
            # Fade from light version of color to darker
            r = int(base_color[0] * (0.3 + 0.4 * (1 - ratio)))
            g = int(base_color[1] * (0.3 + 0.4 * (1 - ratio)))
            b = int(base_color[2] * (0.3 + 0.4 * (1 - ratio)))
            
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y))
    
    def _draw_detection_area(self):
        """Draw the color detection area overlay"""
        # Detection area in center of camera
        detection_rect = pygame.Rect(
            self.camera_rect.centerx - 50,
            self.camera_rect.centery - 50,
            100, 100
        )
        
        # Draw detection area border
        border_color = self.colors['white']
        if self.detected_color == self.target_color:
            # Green border when correct color detected
            border_color = self.colors['green']
            # Pulsing effect
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.02)) * 5
            detection_rect.inflate_ip(pulse, pulse)
        
        pygame.draw.rect(self.screen, border_color, detection_rect, 3)
        
        # Draw progress bar for detection
        if self.consecutive_detections > 0:
            progress = self.consecutive_detections / self.detection_threshold
            progress_width = int(detection_rect.width * progress)
            progress_rect = pygame.Rect(detection_rect.x, detection_rect.bottom + 5,
                                      progress_width, 10)
            pygame.draw.rect(self.screen, self.colors['green'], progress_rect)
            
            # Progress bar border
            progress_border = pygame.Rect(detection_rect.x, detection_rect.bottom + 5,
                                        detection_rect.width, 10)
            pygame.draw.rect(self.screen, self.colors['white'], progress_border, 2)
        
        # Show detected color
        if self.detected_color:
            color_info = self.color_targets.get(self.detected_color)
            if color_info:
                detected_text = f"Found: {color_info['name']}"
                text_surface = self.small_font.render(detected_text, True, self.colors['white'])
                text_rect = text_surface.get_rect(center=(detection_rect.centerx, 
                                                        detection_rect.bottom + 25))
                
                # Text background
                bg_rect = text_rect.inflate(10, 5)
                pygame.draw.rect(self.screen, self.colors['black'], bg_rect, border_radius=5)
                
                self.screen.blit(text_surface, text_rect)
    
    def _draw_game_ui(self):
        """Draw game-specific UI"""
        # Title
        title = "🌈 Color Hunt Game!"
        self.draw_text_with_shadow(title, self.title_font, self.colors['white'], 
                                 self.colors['black'], (self.width//2 - 150, 10))
        
        # Score
        score_text = f"Colors Found: {self.score} 🎨"
        score_surface = self.text_font.render(score_text, True, self.colors['white'])
        self.screen.blit(score_surface, (self.width - 250, 10))
        
        # Target color display
        target_info = self.color_targets[self.target_color]
        target_text = f"Find: {target_info['name']}"
        
        # Large target color display
        target_rect = pygame.Rect(self.width - 300, 100, 200, 80)
        pygame.draw.rect(self.screen, target_info['color'], target_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.colors['white'], target_rect, 3, border_radius=10)
        
        # Target text
        text_surface = self.text_font.render(target_text, True, self.colors['white'])
        text_rect = text_surface.get_rect(center=target_rect.center)
        
        # Text shadow for visibility
        shadow_surface = self.text_font.render(target_text, True, self.colors['black'])
        shadow_rect = text_rect.move(2, 2)
        
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(text_surface, text_rect)
        
        # Instructions
        instructions = [
            "🎯 Point the camera at the target color!",
            "📱 Hold steady in the detection area",
            "⏱️ Colors change automatically"
        ]
        
        instruction_y = self.height - 200
        for instruction in instructions:
            text_surface = self.small_font.render(instruction, True, self.colors['white'])
            text_rect = text_surface.get_rect(center=(self.width//2, instruction_y))
            
            # Background for readability
            bg_rect = text_rect.inflate(10, 5)
            pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect, border_radius=5)
            
            self.screen.blit(text_surface, text_rect)
            instruction_y += 25
        
        # Success message
        if self.success_timer > 0:
            success_text = f"🎉 Great job! You found {target_info['name']}! 🎉"
            success_surface = self.title_font.render(success_text, True, self.colors['yellow'])
            success_rect = success_surface.get_rect(center=(self.width//2, self.height//2))
            
            # Pulsing effect
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.03)) * 10
            success_rect.inflate_ip(pulse, pulse)
            
            # Background
            bg_rect = success_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, self.colors['black'], bg_rect, border_radius=10)
            
            self.screen.blit(success_surface, success_rect)
        
        # Time remaining indicator
        time_remaining = max(0, 600 - self.color_change_timer) / 600
        time_bar_width = 200
        time_bar_rect = pygame.Rect(self.width//2 - time_bar_width//2, 60, 
                                  int(time_bar_width * time_remaining), 10)
        
        pygame.draw.rect(self.screen, self.colors['yellow'], time_bar_rect)
        
        time_border = pygame.Rect(self.width//2 - time_bar_width//2, 60, time_bar_width, 10)
        pygame.draw.rect(self.screen, self.colors['white'], time_border, 2)
    
    def _color_found_success(self):
        """Handle successful color detection"""
        self.score += 1
        self.success_timer = 120  # 2 seconds
        
        # Create celebration particles
        self._create_success_particles()
        
        # Set new target color
        self._set_new_target_color()
    
    def _create_color_particles(self):
        """Create particles based on detected color"""
        if not self.detected_color:
            return
        
        color_info = self.color_targets.get(self.detected_color)
        if not color_info:
            return
        
        # Create particles around detection area
        center_x = self.camera_rect.centerx
        center_y = self.camera_rect.centery
        
        for _ in range(2):
            x = center_x + random.randint(-60, 60)
            y = center_y + random.randint(-60, 60)
            
            particle = self.create_particle(x, y, color_info['color'], 
                                          size=random.randint(2, 5))
            self.particles.append(particle)
    
    def _create_success_particles(self):
        """Create celebration particles when color is found"""
        target_info = self.color_targets[self.target_color]
        
        # Burst of particles from center
        center_x = self.width // 2
        center_y = self.height // 2
        
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            x = center_x + random.randint(-50, 50)
            y = center_y + random.randint(-50, 50)
            
            particle = self.create_particle(x, y, target_info['color'], 
                                          size=random.randint(3, 8),
                                          velocity=(vx, vy))
            self.particles.append(particle)
