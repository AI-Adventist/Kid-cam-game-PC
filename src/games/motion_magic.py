"""
Motion Magic Game - Interactive hand/motion detection game for kids
"""

import pygame
import random
import math
from src.games.base_game import BaseGame

class MotionMagicGame(BaseGame):
    def __init__(self, screen, camera_manager):
        super().__init__(screen, camera_manager)
        self.hands = []
        self.magic_wands = []
        self.falling_stars = []
        self.particles = []
        self.score = 0
        self.magic_trails = []
        
        # Game elements
        self.star_spawn_timer = 0
        self.wand_effects = []
        
        # Magic colors
        self.magic_colors = [
            self.colors['purple'], self.colors['pink'], self.colors['yellow'],
            self.colors['blue'], self.colors['green'], (255, 100, 255)  # Magenta
        ]
        
    def update(self):
        """Update motion magic game"""
        if not self.running:
            return
        
        # Detect hands
        self.hands = self.camera_manager.detect_hands()
        
        # Update magic wands based on hand positions
        self._update_magic_wands()
        
        # Spawn falling stars
        self.star_spawn_timer += 1
        if self.star_spawn_timer > 60:  # Every second
            self._spawn_falling_star()
            self.star_spawn_timer = 0
        
        # Update falling stars
        self._update_falling_stars()
        
        # Update particles and trails
        self.update_particles(self.particles)
        self._update_magic_trails()
        
        # Create magic particles from hands
        if self.hands:
            self._create_hand_particles()
    
    def draw(self):
        """Draw motion magic game"""
        # Magical background
        self._draw_magical_background()
        
        # Draw camera feed
        self.draw_camera_feed()
        
        # Draw hand overlays
        self._draw_hand_overlays()
        
        # Draw magic wands
        self._draw_magic_wands()
        
        # Draw falling stars
        self._draw_falling_stars()
        
        # Draw magic trails
        self._draw_magic_trails()
        
        # Draw particles
        self.draw_particle_effect(self.particles)
        
        # Draw UI
        self._draw_game_ui()
        
        # Draw base UI
        self.draw_ui()
    
    def _draw_magical_background(self):
        """Draw animated magical background"""
        # Dark starry background
        self.screen.fill((20, 20, 40))
        
        # Draw twinkling stars
        for i in range(50):
            star_x = (i * 137) % self.width  # Pseudo-random positions
            star_y = (i * 211) % self.height
            
            # Twinkling effect
            twinkle = abs(math.sin(pygame.time.get_ticks() * 0.01 + i)) * 255
            star_color = (int(twinkle), int(twinkle), 255)
            
            pygame.draw.circle(self.screen, star_color, (star_x, star_y), 2)
        
        # Draw magical aurora effect
        time = pygame.time.get_ticks() * 0.001
        for y in range(0, self.height, 10):
            wave = math.sin(time + y * 0.01) * 30
            alpha = abs(math.sin(time * 0.5 + y * 0.005)) * 50
            
            color = (int(100 + wave), int(50 + alpha), int(150 + wave), int(alpha))
            
            # Create surface with alpha for aurora effect
            aurora_surface = pygame.Surface((self.width, 10), pygame.SRCALPHA)
            aurora_surface.fill(color)
            self.screen.blit(aurora_surface, (0, y))
    
    def _update_magic_wands(self):
        """Update magic wands based on hand positions"""
        # Clear old wands
        self.magic_wands = []
        
        for i, hand in enumerate(self.hands):
            # Convert hand position to screen coordinates
            hand_x = self.camera_rect.x + (hand['center'][0] * self.camera_rect.width) // 640
            hand_y = self.camera_rect.y + (hand['center'][1] * self.camera_rect.height) // 480
            
            # Create magic wand
            wand_color = self.magic_colors[i % len(self.magic_colors)]
            self.magic_wands.append({
                'x': hand_x,
                'y': hand_y,
                'color': wand_color,
                'size': 20 + abs(math.sin(pygame.time.get_ticks() * 0.01 + i)) * 10
            })
            
            # Add to magic trail
            self.magic_trails.append({
                'x': hand_x,
                'y': hand_y,
                'color': wand_color,
                'life': 30,
                'size': 15
            })
    
    def _spawn_falling_star(self):
        """Spawn a new falling star"""
        star = {
            'x': random.randint(0, self.width),
            'y': -20,
            'vx': random.uniform(-2, 2),
            'vy': random.uniform(2, 5),
            'color': random.choice(self.magic_colors),
            'size': random.randint(8, 15),
            'rotation': 0,
            'caught': False
        }
        self.falling_stars.append(star)
    
    def _update_falling_stars(self):
        """Update falling stars and check for catches"""
        for star in self.falling_stars[:]:
            if star['caught']:
                continue
            
            # Move star
            star['x'] += star['vx']
            star['y'] += star['vy']
            star['rotation'] += 0.1
            
            # Check collision with magic wands
            for wand in self.magic_wands:
                distance = math.sqrt((star['x'] - wand['x'])**2 + (star['y'] - wand['y'])**2)
                if distance < wand['size'] + star['size']:
                    # Star caught!
                    star['caught'] = True
                    self.score += 10
                    self._create_star_catch_effect(star['x'], star['y'], star['color'])
                    break
            
            # Remove stars that fall off screen
            if star['y'] > self.height + 50:
                self.falling_stars.remove(star)
        
        # Remove caught stars after effect
        self.falling_stars = [star for star in self.falling_stars if not star['caught']]
    
    def _update_magic_trails(self):
        """Update magic trails behind hands"""
        for trail in self.magic_trails[:]:
            trail['life'] -= 1
            trail['size'] *= 0.95
            
            if trail['life'] <= 0 or trail['size'] < 1:
                self.magic_trails.remove(trail)
    
    def _draw_hand_overlays(self):
        """Draw magical overlays on detected hands"""
        for i, hand in enumerate(self.hands):
            # Convert hand position to screen coordinates
            hand_x = self.camera_rect.x + (hand['center'][0] * self.camera_rect.width) // 640
            hand_y = self.camera_rect.y + (hand['center'][1] * self.camera_rect.height) // 480
            
            # Draw magical aura around hand
            aura_color = self.magic_colors[i % len(self.magic_colors)]
            aura_size = 30 + abs(math.sin(pygame.time.get_ticks() * 0.02 + i)) * 15
            
            # Create aura surface with alpha
            aura_surface = pygame.Surface((aura_size * 2, aura_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(aura_surface, (*aura_color, 100), 
                             (aura_size, aura_size), aura_size)
            
            self.screen.blit(aura_surface, (hand_x - aura_size, hand_y - aura_size))
            
            # Draw hand outline
            pygame.draw.circle(self.screen, self.colors['white'], (hand_x, hand_y), 15, 3)
    
    def _draw_magic_wands(self):
        """Draw magic wands at hand positions"""
        for wand in self.magic_wands:
            # Draw wand glow
            glow_surface = pygame.Surface((wand['size'] * 3, wand['size'] * 3), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*wand['color'], 80), 
                             (wand['size'] * 3 // 2, wand['size'] * 3 // 2), wand['size'])
            
            self.screen.blit(glow_surface, (wand['x'] - wand['size'] * 3 // 2, 
                                          wand['y'] - wand['size'] * 3 // 2))
            
            # Draw wand core
            pygame.draw.circle(self.screen, wand['color'], 
                             (int(wand['x']), int(wand['y'])), int(wand['size'] // 2))
            pygame.draw.circle(self.screen, self.colors['white'], 
                             (int(wand['x']), int(wand['y'])), int(wand['size'] // 2), 2)
    
    def _draw_falling_stars(self):
        """Draw falling stars"""
        for star in self.falling_stars:
            if star['caught']:
                continue
            
            # Draw star shape
            self._draw_star(star['x'], star['y'], star['size'], star['color'], star['rotation'])
    
    def _draw_star(self, x, y, size, color, rotation):
        """Draw a star shape"""
        points = []
        for i in range(10):  # 5-pointed star = 10 points
            angle = rotation + i * math.pi / 5
            if i % 2 == 0:
                # Outer points
                radius = size
            else:
                # Inner points
                radius = size * 0.4
            
            point_x = x + math.cos(angle) * radius
            point_y = y + math.sin(angle) * radius
            points.append((point_x, point_y))
        
        if len(points) >= 3:
            pygame.draw.polygon(self.screen, color, points)
            pygame.draw.polygon(self.screen, self.colors['white'], points, 2)
    
    def _draw_magic_trails(self):
        """Draw magic trails behind hands"""
        for trail in self.magic_trails:
            alpha = int(255 * (trail['life'] / 30))
            trail_color = (*trail['color'], alpha)
            
            trail_surface = pygame.Surface((trail['size'] * 2, trail['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, trail_color, 
                             (int(trail['size']), int(trail['size'])), int(trail['size']))
            
            self.screen.blit(trail_surface, (trail['x'] - trail['size'], trail['y'] - trail['size']))
    
    def _draw_game_ui(self):
        """Draw game-specific UI"""
        # Title
        title = "🎯 Motion Magic Game!"
        self.draw_text_with_shadow(title, self.title_font, self.colors['white'], 
                                 self.colors['black'], (self.width//2 - 150, 10))
        
        # Score
        score_text = f"Stars Caught: {self.score} ⭐"
        score_surface = self.text_font.render(score_text, True, self.colors['white'])
        self.screen.blit(score_surface, (self.width - 250, 10))
        
        # Hand count
        hand_count_text = f"Magic Wands: {len(self.hands)} 🪄"
        hand_surface = self.text_font.render(hand_count_text, True, self.colors['white'])
        self.screen.blit(hand_surface, (self.camera_rect.x, self.camera_rect.bottom + 10))
        
        # Instructions
        instructions = [
            "🪄 Wave your hands to create magic wands!",
            "⭐ Catch falling stars with your wands",
            "✨ Move around to create magical trails"
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
        
        # Active stars count
        active_stars = len([star for star in self.falling_stars if not star['caught']])
        stars_text = f"Active Stars: {active_stars}"
        stars_surface = self.small_font.render(stars_text, True, self.colors['yellow'])
        self.screen.blit(stars_surface, (10, self.height - 100))
    
    def _create_hand_particles(self):
        """Create magical particles from hand positions"""
        for i, hand in enumerate(self.hands):
            if random.random() < 0.5:  # 50% chance each frame
                # Convert hand position to screen coordinates
                hand_x = self.camera_rect.x + (hand['center'][0] * self.camera_rect.width) // 640
                hand_y = self.camera_rect.y + (hand['center'][1] * self.camera_rect.height) // 480
                
                # Create sparkle particle
                color = self.magic_colors[i % len(self.magic_colors)]
                particle = self.create_particle(
                    hand_x + random.randint(-20, 20),
                    hand_y + random.randint(-20, 20),
                    color,
                    size=random.randint(2, 6),
                    velocity=(random.uniform(-2, 2), random.uniform(-3, 1))
                )
                self.particles.append(particle)
    
    def _create_star_catch_effect(self, x, y, color):
        """Create particle effect when star is caught"""
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            particle = self.create_particle(
                x + random.randint(-10, 10),
                y + random.randint(-10, 10),
                color,
                size=random.randint(3, 8),
                velocity=(vx, vy)
            )
            self.particles.append(particle)
