"""
Face Fun Game - Interactive face detection game for kids
"""

import pygame
import random
import math
from src.games.base_game import BaseGame

class FaceFunGame(BaseGame):
    def __init__(self, screen, camera_manager):
        super().__init__(screen, camera_manager)
        self.faces = []
        self.particles = []
        self.score = 0
        self.last_face_count = 0
        self.celebration_timer = 0
        self.sparkle_timer = 0
        
        # Face effects
        self.face_effects = []
        
        # Game state
        self.instructions = [
            "🎭 Make faces at the camera!",
            "😊 Smile to create sparkles!",
            "😮 Open your mouth for surprises!",
            "😉 Wink to change colors!"
        ]
        self.current_instruction = 0
        self.instruction_timer = 0
        
    def update(self):
        """Update face fun game"""
        if not self.running:
            return
        
        # Detect faces
        self.faces = self.camera_manager.detect_faces()
        
        # Update instruction rotation
        self.instruction_timer += 1
        if self.instruction_timer > 180:  # Change every 3 seconds at 60 FPS
            self.current_instruction = (self.current_instruction + 1) % len(self.instructions)
            self.instruction_timer = 0
        
        # Face detection effects
        if len(self.faces) > self.last_face_count:
            # New face detected!
            self.celebration_timer = 60
            self.score += 10
            self._create_celebration_particles()
        
        self.last_face_count = len(self.faces)
        
        # Create sparkles around faces
        self.sparkle_timer += 1
        if self.sparkle_timer > 10 and self.faces:  # Every 10 frames
            self._create_face_sparkles()
            self.sparkle_timer = 0
        
        # Update particles
        self.update_particles(self.particles)
        
        # Update face effects
        self._update_face_effects()
        
        # Update celebration timer
        if self.celebration_timer > 0:
            self.celebration_timer -= 1
    
    def draw(self):
        """Draw face fun game"""
        # Background gradient
        self._draw_background()
        
        # Draw camera feed with face overlays
        self.draw_camera_feed()
        self._draw_face_overlays()
        
        # Draw particles
        self.draw_particle_effect(self.particles)
        
        # Draw UI
        self._draw_game_ui()
        
        # Draw base UI
        self.draw_ui()
    
    def _draw_background(self):
        """Draw animated background"""
        # Create rainbow gradient background
        for y in range(self.height):
            hue = (y / self.height + pygame.time.get_ticks() * 0.0001) % 1.0
            color = pygame.Color(0)
            color.hsva = (hue * 360, 30, 90, 100)  # Light pastel colors
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))
    
    def _draw_face_overlays(self):
        """Draw fun overlays on detected faces"""
        for i, face in enumerate(self.faces):
            # Calculate face position in camera rect
            face_x = self.camera_rect.x + (face['x'] * self.camera_rect.width) // 640
            face_y = self.camera_rect.y + (face['y'] * self.camera_rect.height) // 480
            face_w = (face['width'] * self.camera_rect.width) // 640
            face_h = (face['height'] * self.camera_rect.height) // 480
            
            # Draw face border with pulsing effect
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.01 + i)) * 5
            border_color = self.colors['yellow']
            
            if self.celebration_timer > 0:
                # Rainbow border during celebration
                hue = (pygame.time.get_ticks() * 0.01 + i) % 1.0
                border_color = pygame.Color(0)
                border_color.hsva = (hue * 360, 100, 100, 100)
            
            # Draw pulsing border
            border_rect = pygame.Rect(face_x - pulse, face_y - pulse, 
                                    face_w + 2*pulse, face_h + 2*pulse)
            pygame.draw.rect(self.screen, border_color, border_rect, 3)
            
            # Draw fun accessories
            self._draw_face_accessories(face_x, face_y, face_w, face_h, i)
    
    def _draw_face_accessories(self, x, y, w, h, face_index):
        """Draw fun accessories on faces"""
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Rotating crown
        crown_angle = pygame.time.get_ticks() * 0.005 + face_index
        crown_points = []
        crown_radius = w // 3
        
        for i in range(8):
            angle = crown_angle + i * math.pi / 4
            point_x = center_x + math.cos(angle) * crown_radius
            point_y = y - 20 + math.sin(angle) * 10
            crown_points.append((point_x, point_y))
        
        # Draw crown
        if len(crown_points) >= 3:
            pygame.draw.polygon(self.screen, self.colors['yellow'], crown_points[:4])
            
        # Draw floating hearts
        for i in range(3):
            heart_angle = pygame.time.get_ticks() * 0.01 + i * 2
            heart_x = center_x + math.cos(heart_angle) * (w // 2 + 30)
            heart_y = center_y + math.sin(heart_angle) * (h // 2 + 20)
            self._draw_heart(heart_x, heart_y, 8)
    
    def _draw_heart(self, x, y, size):
        """Draw a heart shape"""
        heart_color = self.colors['pink']
        
        # Simple heart using circles and triangle
        pygame.draw.circle(self.screen, heart_color, (int(x - size//2), int(y)), size//2)
        pygame.draw.circle(self.screen, heart_color, (int(x + size//2), int(y)), size//2)
        
        triangle_points = [
            (x - size, y),
            (x + size, y),
            (x, y + size)
        ]
        pygame.draw.polygon(self.screen, heart_color, triangle_points)
    
    def _draw_game_ui(self):
        """Draw game-specific UI"""
        # Title
        title = "🎭 Face Fun Game!"
        self.draw_text_with_shadow(title, self.title_font, self.colors['white'], 
                                 self.colors['black'], (self.width//2 - 150, 10))
        
        # Score
        score_text = f"Fun Points: {self.score} ⭐"
        score_surface = self.text_font.render(score_text, True, self.colors['white'])
        self.screen.blit(score_surface, (self.width - 250, 10))
        
        # Current instruction
        instruction = self.instructions[self.current_instruction]
        instruction_surface = self.text_font.render(instruction, True, self.colors['black'])
        
        # Instruction background
        instruction_rect = instruction_surface.get_rect()
        instruction_rect.center = (self.width//2, self.height - 150)
        instruction_bg = instruction_rect.inflate(20, 10)
        
        pygame.draw.rect(self.screen, self.colors['white'], instruction_bg, border_radius=10)
        pygame.draw.rect(self.screen, self.colors['black'], instruction_bg, 2, border_radius=10)
        
        self.screen.blit(instruction_surface, instruction_rect)
        
        # Face count
        face_count_text = f"Faces detected: {len(self.faces)}"
        face_count_surface = self.small_font.render(face_count_text, True, self.colors['black'])
        self.screen.blit(face_count_surface, (self.camera_rect.x, self.camera_rect.bottom + 10))
        
        # Celebration message
        if self.celebration_timer > 0:
            celebration_text = "🎉 Great job! Keep making faces! 🎉"
            celebration_surface = self.title_font.render(celebration_text, True, self.colors['yellow'])
            celebration_rect = celebration_surface.get_rect(center=(self.width//2, self.height//2))
            
            # Pulsing effect
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.02)) * 10
            celebration_rect.inflate_ip(pulse, pulse)
            
            self.screen.blit(celebration_surface, celebration_rect)
    
    def _create_celebration_particles(self):
        """Create celebration particle effects"""
        for _ in range(20):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height // 2)
            color = random.choice([self.colors['yellow'], self.colors['pink'], 
                                 self.colors['orange'], self.colors['purple']])
            
            particle = self.create_particle(x, y, color, size=random.randint(3, 8))
            self.particles.append(particle)
    
    def _create_face_sparkles(self):
        """Create sparkle effects around faces"""
        for face in self.faces:
            # Calculate face position in camera rect
            face_x = self.camera_rect.x + (face['x'] * self.camera_rect.width) // 640
            face_y = self.camera_rect.y + (face['y'] * self.camera_rect.height) // 480
            face_w = (face['width'] * self.camera_rect.width) // 640
            face_h = (face['height'] * self.camera_rect.height) // 480
            
            # Create sparkles around face
            for _ in range(3):
                sparkle_x = face_x + random.randint(-face_w//2, face_w + face_w//2)
                sparkle_y = face_y + random.randint(-face_h//2, face_h + face_h//2)
                
                sparkle_color = random.choice([self.colors['white'], self.colors['yellow'], 
                                             self.colors['pink']])
                
                particle = self.create_particle(sparkle_x, sparkle_y, sparkle_color, 
                                              size=2, velocity=(0, -1))
                self.particles.append(particle)
    
    def _update_face_effects(self):
        """Update face-based effects"""
        # This could be expanded to include more sophisticated face analysis
        # For now, we just track basic face presence
        pass
