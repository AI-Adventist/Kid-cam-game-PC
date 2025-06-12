"""
Main Menu UI - Kid-friendly game selection screen
"""

import pygame
import math

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Colors
        self.colors = {
            'background': (135, 206, 235),  # Sky blue
            'title': (255, 255, 255),       # White
            'button_face': (255, 182, 193), # Light pink
            'button_color': (255, 165, 0),  # Orange
            'button_motion': (144, 238, 144), # Light green
            'button_hover': (255, 255, 0),  # Yellow
            'text': (0, 0, 0),              # Black
            'shadow': (100, 100, 100)       # Gray
        }
        
        # Fonts
        try:
            self.title_font = pygame.font.Font(None, 72)
            self.button_font = pygame.font.Font(None, 48)
            self.subtitle_font = pygame.font.Font(None, 36)
        except:
            # Fallback to default font
            self.title_font = pygame.font.Font(None, 72)
            self.button_font = pygame.font.Font(None, 48)
            self.subtitle_font = pygame.font.Font(None, 36)
        
        # Button setup
        self.buttons = self._create_buttons()
        self.hovered_button = None
        
        # Animation
        self.animation_time = 0
        
    def _create_buttons(self):
        """Create game mode buttons"""
        button_width = 250
        button_height = 100
        spacing = 50
        
        # Calculate positions
        total_width = 3 * button_width + 2 * spacing
        start_x = (self.width - total_width) // 2
        button_y = self.height // 2
        
        buttons = [
            {
                'name': 'face_fun',
                'title': '🎭 Face Fun',
                'subtitle': 'Make silly faces!',
                'color': self.colors['button_face'],
                'rect': pygame.Rect(start_x, button_y, button_width, button_height)
            },
            {
                'name': 'color_hunt',
                'title': '🌈 Color Hunt',
                'subtitle': 'Show me colors!',
                'color': self.colors['button_color'],
                'rect': pygame.Rect(start_x + button_width + spacing, button_y, 
                                  button_width, button_height)
            },
            {
                'name': 'motion_magic',
                'title': '🎯 Motion Magic',
                'subtitle': 'Move and dance!',
                'color': self.colors['button_motion'],
                'rect': pygame.Rect(start_x + 2 * (button_width + spacing), button_y, 
                                  button_width, button_height)
            }
        ]
        
        return buttons
    
    def handle_click(self, pos):
        """Handle mouse click on buttons"""
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                return button['name']
        return None
    
    def update(self):
        """Update menu state"""
        self.animation_time += 0.1
        
        # Check for button hover
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_button = None
        
        for button in self.buttons:
            if button['rect'].collidepoint(mouse_pos):
                self.hovered_button = button['name']
                break
    
    def draw(self):
        """Draw the main menu"""
        # Background gradient effect
        for y in range(self.height):
            color_ratio = y / self.height
            r = int(135 + (173 - 135) * color_ratio)  # Sky blue to light blue
            g = int(206 + (216 - 206) * color_ratio)
            b = int(235 + (230 - 235) * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y))
        
        # Draw floating clouds
        self._draw_clouds()
        
        # Title with shadow
        title_text = "Kid Cam Game PC"
        title_shadow = self.title_font.render(title_text, True, self.colors['shadow'])
        title_surface = self.title_font.render(title_text, True, self.colors['title'])
        
        title_x = (self.width - title_surface.get_width()) // 2
        title_y = 80
        
        # Draw shadow offset
        self.screen.blit(title_shadow, (title_x + 3, title_y + 3))
        self.screen.blit(title_surface, (title_x, title_y))
        
        # Subtitle
        subtitle_text = "Choose your adventure! 🎮📷"
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, self.colors['text'])
        subtitle_x = (self.width - subtitle_surface.get_width()) // 2
        self.screen.blit(subtitle_surface, (subtitle_x, title_y + 90))
        
        # Draw buttons
        for button in self.buttons:
            self._draw_button(button)
        
        # Instructions
        instructions = [
            "🎮 Click a game to start playing!",
            "📷 Make sure your camera is connected",
            "⌨️ Press ESC to exit games"
        ]
        
        instruction_y = self.height - 120
        for instruction in instructions:
            text_surface = self.subtitle_font.render(instruction, True, self.colors['text'])
            text_x = (self.width - text_surface.get_width()) // 2
            self.screen.blit(text_surface, (text_x, instruction_y))
            instruction_y += 30
    
    def _draw_button(self, button):
        """Draw a single button with hover effects"""
        rect = button['rect']
        color = button['color']
        
        # Hover effect
        if self.hovered_button == button['name']:
            # Pulsing effect
            pulse = abs(math.sin(self.animation_time * 3)) * 10
            expanded_rect = rect.inflate(pulse, pulse)
            color = self.colors['button_hover']
        else:
            expanded_rect = rect
        
        # Draw button shadow
        shadow_rect = expanded_rect.move(5, 5)
        pygame.draw.rect(self.screen, self.colors['shadow'], shadow_rect, border_radius=15)
        
        # Draw button
        pygame.draw.rect(self.screen, color, expanded_rect, border_radius=15)
        pygame.draw.rect(self.screen, self.colors['text'], expanded_rect, 3, border_radius=15)
        
        # Draw button text
        title_surface = self.button_font.render(button['title'], True, self.colors['text'])
        subtitle_surface = self.subtitle_font.render(button['subtitle'], True, self.colors['text'])
        
        # Center text
        title_x = expanded_rect.centerx - title_surface.get_width() // 2
        title_y = expanded_rect.centery - title_surface.get_height() // 2 - 10
        
        subtitle_x = expanded_rect.centerx - subtitle_surface.get_width() // 2
        subtitle_y = title_y + title_surface.get_height() + 5
        
        self.screen.blit(title_surface, (title_x, title_y))
        self.screen.blit(subtitle_surface, (subtitle_x, subtitle_y))
    
    def _draw_clouds(self):
        """Draw animated clouds in background"""
        cloud_offset = int(self.animation_time * 20) % (self.width + 200)
        
        # Cloud positions
        clouds = [
            (cloud_offset - 200, 150, 80),
            (cloud_offset - 100, 200, 60),
            (cloud_offset + 300, 120, 70),
            (cloud_offset + 600, 180, 90)
        ]
        
        for x, y, size in clouds:
            if x > -size and x < self.width + size:
                self._draw_cloud(x, y, size)
    
    def _draw_cloud(self, x, y, size):
        """Draw a single fluffy cloud"""
        cloud_color = (255, 255, 255, 180)  # Semi-transparent white
        
        # Create cloud surface with alpha
        cloud_surface = pygame.Surface((size * 2, size), pygame.SRCALPHA)
        
        # Draw cloud circles
        pygame.draw.circle(cloud_surface, cloud_color, (size//2, size//2), size//3)
        pygame.draw.circle(cloud_surface, cloud_color, (size, size//2), size//4)
        pygame.draw.circle(cloud_surface, cloud_color, (size//4, size//3), size//5)
        pygame.draw.circle(cloud_surface, cloud_color, (size*3//2, size//3), size//4)
        
        self.screen.blit(cloud_surface, (x, y))
