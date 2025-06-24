import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Retro Colors
RETRO_GREEN = (0, 100, 0)
RETRO_BROWN = (101, 67, 33)
RETRO_YELLOW = (255, 215, 0)
RETRO_RED = (139, 0, 0)
RETRO_BLUE = (0, 0, 139)
RETRO_WHITE = (255, 248, 220)
RETRO_BLACK = (25, 25, 25)
MILITARY_GREEN = (85, 107, 47)
JUNGLE_GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)

# Game States
MENU = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3
REFUEL_MENU = 4

class RetroFont:
    """Custom retro font rendering"""
    @staticmethod
    def render_retro_text(screen, text, x, y, size=36, color=RETRO_WHITE, shadow=True):
        font = pygame.font.Font(None, size)
        if shadow:
            # Shadow
            shadow_surface = font.render(text, True, RETRO_BLACK)
            screen.blit(shadow_surface, (x + 3, y + 3))
        # Main text
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))
        return text_surface.get_rect(x=x, y=y)

class Jeep:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 120
        self.height = 60
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_speed = 6  # Reduced from 8 to 6 for slower speed
        self.acceleration = 0.4  # Reduced from 0.5 to 0.4
        self.jump_power = 15
        self.gravity = 0.8
        self.friction = 0.85
        self.health = 100
        self.fuel = 100
        self.on_ground = True
        self.facing_right = True
        self.engine_sound_timer = 0
        
    def update(self, keys_pressed, obstacles, terrain_height):
        # Handle horizontal movement
        if keys_pressed[pygame.K_RIGHT]:
            self.velocity_x += self.acceleration
            self.facing_right = True
            self.engine_sound_timer += 1
        elif keys_pressed[pygame.K_LEFT]:
            self.velocity_x -= self.acceleration
            self.facing_right = False
            self.engine_sound_timer += 1
        else:
            # Apply friction when no input
            self.velocity_x *= self.friction
            self.engine_sound_timer = 0
        
        # Limit horizontal speed
        self.velocity_x = max(-self.max_speed, min(self.max_speed, self.velocity_x))
        
        # Handle jumping
        if keys_pressed[pygame.K_UP] and self.on_ground:
            self.velocity_y = -self.jump_power
            self.on_ground = False
        
        # Handle fast descent
        if keys_pressed[pygame.K_DOWN] and not self.on_ground:
            self.velocity_y += self.gravity * 2  # Faster fall
        
        # Apply gravity
        if not self.on_ground:
            self.velocity_y += self.gravity
        
        # Store old position for collision detection
        old_x, old_y = self.x, self.y
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Keep jeep within world bounds
        self.x = max(self.width//2, min(5000 - self.width//2, self.x))
        
        # Terrain collision (with safety checks)
        if 0 <= int(self.x) < len(terrain_height):
            ground_y = terrain_height[int(self.x)]
            
            if self.y + self.height//2 >= ground_y:
                self.y = ground_y - self.height//2
                self.velocity_y = 0
                self.on_ground = True
            else:
                self.on_ground = False
        else:
            # Safety fallback if out of terrain bounds
            ground_y = SCREEN_HEIGHT - 100
            if self.y + self.height//2 >= ground_y:
                self.y = ground_y - self.height//2
                self.velocity_y = 0
                self.on_ground = True
        
        # Check collision with obstacles (modified behavior)
        jeep_rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
        
        for obstacle in obstacles:
            if jeep_rect.colliderect(obstacle.rect):
                # Check if jeep is on top of obstacle (y position comparison)
                if self.y < obstacle.y - obstacle.height//4:  # Jeep is above obstacle
                    # On top of obstacle - reduce fuel 2x instead of health
                    self.fuel -= 0.2  # 2x normal fuel consumption
                    # Small bounce effect
                    if self.velocity_y > 0:
                        self.velocity_y *= -0.3
                else:
                    # Side collision - normal damage and bounce back
                    self.x, self.y = old_x, old_y
                    self.velocity_x *= -0.3
                    self.health -= 8
                break
        
        # Fuel consumption (slower consumption)
        if abs(self.velocity_x) > 0.1:
            self.fuel -= 0.04  # Reduced from 0.08 to 0.04
        else:
            self.fuel -= 0.01  # Reduced from 0.02 to 0.01 (idle consumption)
        
        # Prevent negative values
        self.health = max(0, self.health)
        self.fuel = max(0, self.fuel)
    def draw(self, screen, camera_x):
        # Calculate screen position
        screen_x = self.x - camera_x
        screen_y = self.y
        
        # Realistic military jeep side view (completely redesigned)
        
        # Main chassis (lower body)
        chassis_rect = pygame.Rect(screen_x - 50, screen_y - 10, 100, 25)
        pygame.draw.rect(screen, MILITARY_GREEN, chassis_rect)
        pygame.draw.rect(screen, RETRO_BLACK, chassis_rect, 3)
        
        # Cabin/passenger area (upper body)
        cabin_points = [
            (screen_x - 40, screen_y - 10),  # Back bottom
            (screen_x - 40, screen_y - 35),  # Back top
            (screen_x - 20, screen_y - 40),  # Back roof
            (screen_x + 20, screen_y - 40),  # Front roof
            (screen_x + 35, screen_y - 25),  # Front windshield top
            (screen_x + 35, screen_y - 10),  # Front bottom
        ]
        pygame.draw.polygon(screen, MILITARY_GREEN, cabin_points)
        pygame.draw.polygon(screen, RETRO_BLACK, cabin_points, 3)
        
        # Hood (engine compartment)
        hood_points = [
            (screen_x + 35, screen_y - 25),  # Windshield connection
            (screen_x + 35, screen_y - 10),  # Hood bottom
            (screen_x + 55, screen_y - 10),  # Hood front bottom
            (screen_x + 55, screen_y - 20),  # Hood front top
            (screen_x + 45, screen_y - 25),  # Hood back top
        ]
        pygame.draw.polygon(screen, (70, 90, 40), hood_points)
        pygame.draw.polygon(screen, RETRO_BLACK, hood_points, 3)
        
        # Windshield (angled glass)
        windshield_points = [
            (screen_x - 15, screen_y - 38),
            (screen_x + 25, screen_y - 38),
            (screen_x + 35, screen_y - 25),
            (screen_x - 25, screen_y - 25)
        ]
        pygame.draw.polygon(screen, (120, 180, 255), windshield_points)
        pygame.draw.polygon(screen, RETRO_BLACK, windshield_points, 2)
        
        # Canvas soft top
        canvas_points = [
            (screen_x - 45, screen_y - 35),
            (screen_x - 15, screen_y - 42),
            (screen_x + 15, screen_y - 42),
            (screen_x + 25, screen_y - 38)
        ]
        pygame.draw.polygon(screen, (100, 120, 60), canvas_points)
        pygame.draw.polygon(screen, RETRO_BLACK, canvas_points, 2)
        
        # Wheels (realistic military tires)
        wheel_y = screen_y + 15
        front_wheel_x = screen_x + 30
        rear_wheel_x = screen_x - 30
        
        for wheel_x in [front_wheel_x, rear_wheel_x]:
            # Tire (thick military tread)
            pygame.draw.circle(screen, RETRO_BLACK, (int(wheel_x), int(wheel_y)), 22)
            pygame.draw.circle(screen, (40, 40, 40), (int(wheel_x), int(wheel_y)), 18)
            
            # Rim (military style)
            pygame.draw.circle(screen, (180, 180, 180), (int(wheel_x), int(wheel_y)), 14)
            pygame.draw.circle(screen, RETRO_BLACK, (int(wheel_x), int(wheel_y)), 14, 2)
            
            # Hub cap
            pygame.draw.circle(screen, (120, 120, 120), (int(wheel_x), int(wheel_y)), 8)
            pygame.draw.circle(screen, RETRO_BLACK, (int(wheel_x), int(wheel_y)), 8, 2)
            
            # Spokes
            for i in range(5):
                angle = i * 72
                spoke_x1 = wheel_x + 6 * math.cos(math.radians(angle))
                spoke_y1 = wheel_y + 6 * math.sin(math.radians(angle))
                spoke_x2 = wheel_x + 12 * math.cos(math.radians(angle))
                spoke_y2 = wheel_y + 12 * math.sin(math.radians(angle))
                pygame.draw.line(screen, RETRO_BLACK, (spoke_x1, spoke_y1), (spoke_x2, spoke_y2), 2)
            
            # Tire tread pattern
            for i in range(8):
                angle = i * 45
                tread_x = wheel_x + 20 * math.cos(math.radians(angle))
                tread_y = wheel_y + 20 * math.sin(math.radians(angle))
                pygame.draw.circle(screen, RETRO_BLACK, (int(tread_x), int(tread_y)), 2)
        
        # Headlights (round military style)
        headlight_x = screen_x + 52
        headlight_y = screen_y - 15
        pygame.draw.circle(screen, RETRO_YELLOW, (int(headlight_x), int(headlight_y)), 8)
        pygame.draw.circle(screen, RETRO_WHITE, (int(headlight_x), int(headlight_y)), 6)
        pygame.draw.circle(screen, RETRO_BLACK, (int(headlight_x), int(headlight_y)), 8, 2)
        
        # Military star emblem (on door)
        star_x = screen_x - 10
        star_y = screen_y - 20
        star_points = []
        for i in range(5):
            angle = i * 72 - 90
            outer_x = star_x + 12 * math.cos(math.radians(angle))
            outer_y = star_y + 12 * math.sin(math.radians(angle))
            star_points.append((outer_x, outer_y))
            inner_angle = angle + 36
            inner_x = star_x + 6 * math.cos(math.radians(inner_angle))
            inner_y = star_y + 6 * math.sin(math.radians(inner_angle))
            star_points.append((inner_x, inner_y))
        pygame.draw.polygon(screen, RETRO_WHITE, star_points)
        pygame.draw.polygon(screen, RETRO_BLACK, star_points, 2)
        
        # Door handle
        pygame.draw.rect(screen, (60, 60, 60), (screen_x - 5, screen_y - 15, 3, 8))
        pygame.draw.rect(screen, RETRO_BLACK, (screen_x - 5, screen_y - 15, 3, 8), 1)
        
        # Side mirror
        pygame.draw.rect(screen, RETRO_BLACK, (screen_x + 30, screen_y - 30, 8, 5))
        pygame.draw.rect(screen, (150, 150, 150), (screen_x + 31, screen_y - 29, 6, 3))
        
        # Exhaust pipe
        pygame.draw.rect(screen, (80, 80, 80), (screen_x - 48, screen_y + 8, 8, 4))
        pygame.draw.rect(screen, RETRO_BLACK, (screen_x - 48, screen_y + 8, 8, 4), 1)
        
        # Spare tire (mounted on back)
        spare_x = screen_x - 45
        spare_y = screen_y - 5
        pygame.draw.circle(screen, RETRO_BLACK, (int(spare_x), int(spare_y)), 12)
        pygame.draw.circle(screen, (60, 60, 60), (int(spare_x), int(spare_y)), 10)
        pygame.draw.circle(screen, (120, 120, 120), (int(spare_x), int(spare_y)), 6)
        
        # Roll bar (safety feature)
        pygame.draw.line(screen, (100, 100, 100), (screen_x - 35, screen_y - 35), (screen_x - 35, screen_y - 45), 4)
        pygame.draw.line(screen, (100, 100, 100), (screen_x + 25, screen_y - 35), (screen_x + 25, screen_y - 45), 4)
        pygame.draw.line(screen, (100, 100, 100), (screen_x - 35, screen_y - 45), (screen_x + 25, screen_y - 45), 4)
        
        # Jump indicator (when in air)
        if not self.on_ground:
            pygame.draw.circle(screen, RETRO_YELLOW, 
                             (int(screen_x), int(screen_y - self.height//2 - 25)), 
                             6, 2)

class Animal:
    def __init__(self, x, y, animal_type):
        self.x = x
        self.y = y
        self.type = animal_type
        self.animation_frame = 0
        self.direction = random.choice([-1, 1])
        self.speed = random.uniform(0.3, 1.5)
        
        if animal_type == "elephant":
            self.width, self.height = 80, 60
        elif animal_type == "tiger":
            self.width, self.height = 70, 45
        elif animal_type == "deer":
            self.width, self.height = 50, 50
        elif animal_type == "bear":
            self.width, self.height = 65, 55
        elif animal_type == "squirrel":
            self.width, self.height = 25, 30
        elif animal_type == "bird":
            self.width, self.height = 30, 25
        else:  # monkey
            self.width, self.height = 35, 40
    
    def update(self):
        self.animation_frame += 0.02  # Very slow, subtle animation
        # Minimal movement for realistic feel - NO LOOPS/ROTATION
        if self.type in ["squirrel", "monkey"]:
            # Small animals move very rarely
            if random.randint(0, 1000) == 0:  # Very rare movement
                self.direction *= -1
            self.x += self.direction * self.speed * 0.1  # Very slow movement
        elif self.type == "bird":
            # Birds fly very subtly
            if random.randint(0, 800) == 0:
                self.direction *= -1
            self.x += self.direction * self.speed * 0.1
            # Very minimal vertical movement for birds (no loops)
            self.y += math.sin(self.animation_frame * 0.5) * 0.2  # Reduced amplitude
    
    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        if -200 < screen_x < SCREEN_WIDTH + 200:  # Only draw if on screen
            if self.type == "elephant":
                self.draw_elephant(screen, screen_x)
            elif self.type == "tiger":
                self.draw_tiger(screen, screen_x)
            elif self.type == "deer":
                self.draw_deer(screen, screen_x)
            elif self.type == "bear":
                self.draw_bear(screen, screen_x)
            elif self.type == "squirrel":
                self.draw_squirrel(screen, screen_x)
            elif self.type == "bird":
                self.draw_bird(screen, screen_x)
            else:  # monkey
                self.draw_monkey(screen, screen_x)
    
    def draw_elephant(self, screen, screen_x):
        # Retro elephant with thick outlines
        # Body
        pygame.draw.ellipse(screen, (120, 120, 120), (screen_x - 35, self.y - 25, 70, 50))
        pygame.draw.ellipse(screen, RETRO_BLACK, (screen_x - 35, self.y - 25, 70, 50), 3)
        # Head
        pygame.draw.circle(screen, (120, 120, 120), (int(screen_x - 40), int(self.y - 15)), 22)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x - 40), int(self.y - 15)), 22, 3)
        # Trunk (retro curved)
        trunk_points = [(screen_x - 55, self.y - 10), (screen_x - 70, self.y), (screen_x - 65, self.y + 15)]
        pygame.draw.lines(screen, (120, 120, 120), False, trunk_points, 10)
        pygame.draw.lines(screen, RETRO_BLACK, False, trunk_points, 3)
        # Legs (chunky retro style)
        for leg_x in [screen_x - 25, screen_x - 10, screen_x + 5, screen_x + 20]:
            pygame.draw.rect(screen, (100, 100, 100), (leg_x - 4, self.y + 20, 8, 18))
            pygame.draw.rect(screen, RETRO_BLACK, (leg_x - 4, self.y + 20, 8, 18), 2)
        # Eye (retro style)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x - 45), int(self.y - 20)), 4)
        pygame.draw.circle(screen, RETRO_WHITE, (int(screen_x - 43), int(self.y - 22)), 2)
    
    def draw_monkey(self, screen, screen_x):
        # Retro monkey
        # Body
        pygame.draw.ellipse(screen, RETRO_BROWN, (screen_x - 15, self.y - 18, 30, 35))
        pygame.draw.ellipse(screen, RETRO_BLACK, (screen_x - 15, self.y - 18, 30, 35), 2)
        # Head
        pygame.draw.circle(screen, (160, 100, 50), (int(screen_x), int(self.y - 25)), 15)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x), int(self.y - 25)), 15, 2)
        # Arms (animated)
        arm_offset = math.sin(self.animation_frame) * 6
        pygame.draw.line(screen, RETRO_BROWN, (screen_x - 10, self.y - 12), (screen_x - 18, self.y - 8 + arm_offset), 5)
        pygame.draw.line(screen, RETRO_BROWN, (screen_x + 10, self.y - 12), (screen_x + 18, self.y - 8 - arm_offset), 5)
        # Legs
        pygame.draw.line(screen, RETRO_BROWN, (screen_x - 6, self.y + 12), (screen_x - 10, self.y + 25), 5)
        pygame.draw.line(screen, RETRO_BROWN, (screen_x + 6, self.y + 12), (screen_x + 10, self.y + 25), 5)
        # Face (retro style)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x - 5), int(self.y - 28)), 3)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 5), int(self.y - 28)), 3)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x), int(self.y - 22)), 2)
    
    def draw_tiger(self, screen, screen_x):
        # Retro tiger
        # Body
        pygame.draw.ellipse(screen, (255, 165, 0), (screen_x - 27, self.y - 18, 55, 35))
        pygame.draw.ellipse(screen, RETRO_BLACK, (screen_x - 27, self.y - 18, 55, 35), 3)
        # Head
        pygame.draw.circle(screen, (255, 165, 0), (int(screen_x + 22), int(self.y - 12)), 18)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 22), int(self.y - 12)), 18, 3)
        # Stripes (retro thick)
        for stripe_x in [screen_x - 18, screen_x - 6, screen_x + 6]:
            pygame.draw.line(screen, RETRO_BLACK, (stripe_x, self.y - 15), (stripe_x, self.y + 10), 4)
        # Legs (chunky)
        for leg_x in [screen_x - 18, screen_x - 6, screen_x + 6, screen_x + 18]:
            pygame.draw.rect(screen, (255, 165, 0), (leg_x - 3, self.y + 12, 6, 15))
            pygame.draw.rect(screen, RETRO_BLACK, (leg_x - 3, self.y + 12, 6, 15), 2)
        # Ears (retro triangular)
        pygame.draw.polygon(screen, (255, 165, 0), [(screen_x + 15, self.y - 25), (screen_x + 20, self.y - 30), (screen_x + 25, self.y - 25)])
        pygame.draw.polygon(screen, (255, 165, 0), [(screen_x + 20, self.y - 25), (screen_x + 25, self.y - 30), (screen_x + 30, self.y - 25)])
        # Eyes (retro style)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 18), int(self.y - 15)), 3)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 26), int(self.y - 15)), 3)
        pygame.draw.circle(screen, RETRO_WHITE, (int(screen_x + 19), int(self.y - 16)), 1)
        pygame.draw.circle(screen, RETRO_WHITE, (int(screen_x + 27), int(self.y - 16)), 1)
    
    def draw_bird(self, screen, screen_x):
        # More realistic bird without red trail
        # Body (brown/natural color)
        pygame.draw.ellipse(screen, (139, 69, 19), (screen_x - 12, self.y - 10, 25, 20))
        pygame.draw.ellipse(screen, RETRO_BLACK, (screen_x - 12, self.y - 10, 25, 20), 2)
        # Wing (subtle animation, natural colors)
        wing_flap = math.sin(self.animation_frame * 4) * 6  # Reduced flap intensity
        pygame.draw.ellipse(screen, (101, 67, 33), (screen_x - 8, self.y - 12 + wing_flap, 18, 8))
        pygame.draw.ellipse(screen, RETRO_BLACK, (screen_x - 8, self.y - 12 + wing_flap, 18, 8), 2)
        # Head (natural brown)
        pygame.draw.circle(screen, (160, 82, 45), (int(screen_x + 10), int(self.y - 8)), 8)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 10), int(self.y - 8)), 8, 2)
        # Beak (orange/yellow)
        pygame.draw.polygon(screen, (255, 140, 0), [(screen_x + 16, self.y - 8), (screen_x + 22, self.y - 5), (screen_x + 16, self.y - 2)])
        pygame.draw.polygon(screen, RETRO_BLACK, [(screen_x + 16, self.y - 8), (screen_x + 22, self.y - 5), (screen_x + 16, self.y - 2)], 2)
        # Eye
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 12), int(self.y - 10)), 2)
        pygame.draw.circle(screen, RETRO_WHITE, (int(screen_x + 13), int(self.y - 11)), 1)
    
    def draw_deer(self, screen, screen_x):
        # Retro deer
        # Body
        pygame.draw.ellipse(screen, RETRO_BROWN, (screen_x - 20, self.y - 18, 40, 30))
        pygame.draw.ellipse(screen, RETRO_BLACK, (screen_x - 20, self.y - 18, 40, 30), 3)
        # Head
        pygame.draw.circle(screen, (160, 100, 50), (int(screen_x + 18), int(self.y - 18)), 12)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 18), int(self.y - 18)), 12, 2)
        # Antlers (retro branched)
        pygame.draw.line(screen, (80, 50, 20), (screen_x + 15, self.y - 26), (screen_x + 10, self.y - 35), 4)
        pygame.draw.line(screen, (80, 50, 20), (screen_x + 21, self.y - 26), (screen_x + 26, self.y - 35), 4)
        pygame.draw.line(screen, (80, 50, 20), (screen_x + 12, self.y - 32), (screen_x + 8, self.y - 38), 3)
        pygame.draw.line(screen, (80, 50, 20), (screen_x + 24, self.y - 32), (screen_x + 28, self.y - 38), 3)
        # Legs (retro style)
        for leg_x in [screen_x - 12, screen_x - 4, screen_x + 4, screen_x + 12]:
            pygame.draw.rect(screen, RETRO_BROWN, (leg_x - 2, self.y + 8, 4, 18))
            pygame.draw.rect(screen, RETRO_BLACK, (leg_x - 2, self.y + 8, 4, 18), 1)
        # Eye
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 22), int(self.y - 20)), 3)
        pygame.draw.circle(screen, RETRO_WHITE, (int(screen_x + 23), int(self.y - 21)), 1)
        # Tail (retro white)
        pygame.draw.circle(screen, RETRO_WHITE, (int(screen_x - 20), int(self.y - 8)), 5)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x - 20), int(self.y - 8)), 5, 2)
    
    def draw_bear(self, screen, screen_x):
        # Retro bear
        # Body (chunky and round)
        pygame.draw.ellipse(screen, (101, 67, 33), (screen_x - 32, self.y - 27, 65, 55))
        pygame.draw.ellipse(screen, RETRO_BLACK, (screen_x - 32, self.y - 27, 65, 55), 4)
        # Head
        pygame.draw.circle(screen, (139, 69, 19), (int(screen_x + 25), int(self.y - 20)), 20)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 25), int(self.y - 20)), 20, 4)
        # Ears (round)
        pygame.draw.circle(screen, (139, 69, 19), (int(screen_x + 15), int(self.y - 35)), 8)
        pygame.draw.circle(screen, (139, 69, 19), (int(screen_x + 35), int(self.y - 35)), 8)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 15), int(self.y - 35)), 8, 3)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 35), int(self.y - 35)), 8, 3)
        # Legs (thick)
        for leg_x in [screen_x - 20, screen_x - 5, screen_x + 10, screen_x + 25]:
            pygame.draw.rect(screen, (101, 67, 33), (leg_x - 5, self.y + 20, 10, 22))
            pygame.draw.rect(screen, RETRO_BLACK, (leg_x - 5, self.y + 20, 10, 22), 3)
        # Snout
        pygame.draw.ellipse(screen, (160, 82, 45), (screen_x + 35, self.y - 15, 15, 10))
        pygame.draw.ellipse(screen, RETRO_BLACK, (screen_x + 35, self.y - 15, 15, 10), 2)
        # Eyes
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 20), int(self.y - 25)), 3)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 30), int(self.y - 25)), 3)
        pygame.draw.circle(screen, RETRO_WHITE, (int(screen_x + 21), int(self.y - 26)), 1)
        pygame.draw.circle(screen, RETRO_WHITE, (int(screen_x + 31), int(self.y - 26)), 1)
        # Nose
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 42), int(self.y - 12)), 2)
    
    def draw_squirrel(self, screen, screen_x):
        # Retro squirrel (static tail - no animation loops)
        # Body (small and cute)
        pygame.draw.ellipse(screen, (160, 82, 45), (screen_x - 12, self.y - 15, 25, 30))
        pygame.draw.ellipse(screen, RETRO_BLACK, (screen_x - 12, self.y - 15, 25, 30), 3)
        # Head
        pygame.draw.circle(screen, (160, 82, 45), (int(screen_x + 10), int(self.y - 18)), 10)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 10), int(self.y - 18)), 10, 3)
        # Ears (pointed)
        pygame.draw.polygon(screen, (160, 82, 45), [(screen_x + 5, self.y - 25), (screen_x + 8, self.y - 30), (screen_x + 11, self.y - 25)])
        pygame.draw.polygon(screen, (160, 82, 45), [(screen_x + 9, self.y - 25), (screen_x + 12, self.y - 30), (screen_x + 15, self.y - 25)])
        pygame.draw.polygon(screen, RETRO_BLACK, [(screen_x + 5, self.y - 25), (screen_x + 8, self.y - 30), (screen_x + 11, self.y - 25)], 2)
        pygame.draw.polygon(screen, RETRO_BLACK, [(screen_x + 9, self.y - 25), (screen_x + 12, self.y - 30), (screen_x + 15, self.y - 25)], 2)
        # Tail (static - no animation)
        pygame.draw.ellipse(screen, (139, 69, 19), (screen_x - 25, self.y - 25, 20, 35))
        pygame.draw.ellipse(screen, RETRO_BLACK, (screen_x - 25, self.y - 25, 20, 35), 3)
        # Eyes
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 8), int(self.y - 20)), 2)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 12), int(self.y - 20)), 2)
        pygame.draw.circle(screen, RETRO_WHITE, (int(screen_x + 8), int(self.y - 21)), 1)
        pygame.draw.circle(screen, RETRO_WHITE, (int(screen_x + 12), int(self.y - 21)), 1)
        # Nose
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 15), int(self.y - 16)), 1)
    
    def draw_monkey(self, screen, screen_x):
        # Retro monkey (static - no rotating arms)
        # Body
        pygame.draw.ellipse(screen, RETRO_BROWN, (screen_x - 17, self.y - 20, 35, 40))
        pygame.draw.ellipse(screen, RETRO_BLACK, (screen_x - 17, self.y - 20, 35, 40), 3)
        # Head
        pygame.draw.circle(screen, (160, 100, 50), (int(screen_x), int(self.y - 25)), 15)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x), int(self.y - 25)), 15, 3)
        # Arms (static position - no animation)
        pygame.draw.line(screen, RETRO_BROWN, (screen_x - 12, self.y - 15), (screen_x - 20, self.y - 10), 6)
        pygame.draw.line(screen, RETRO_BROWN, (screen_x + 12, self.y - 15), (screen_x + 20, self.y - 10), 6)
        # Legs (static)
        pygame.draw.line(screen, RETRO_BROWN, (screen_x - 8, self.y + 15), (screen_x - 12, self.y + 28), 6)
        pygame.draw.line(screen, RETRO_BROWN, (screen_x + 8, self.y + 15), (screen_x + 12, self.y + 28), 6)
        # Face (retro style)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x - 6), int(self.y - 28)), 3)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 6), int(self.y - 28)), 3)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x), int(self.y - 22)), 2)
        # Tail (static)
        pygame.draw.line(screen, RETRO_BROWN, (screen_x - 17, self.y), (screen_x - 25, self.y - 8), 5)
    
    def draw_bird(self, screen, screen_x):
        # Realistic bird without animation loops
        # Body (brown/natural color)
        pygame.draw.ellipse(screen, (139, 69, 19), (screen_x - 15, self.y - 12, 30, 25))
        pygame.draw.ellipse(screen, RETRO_BLACK, (screen_x - 15, self.y - 12, 30, 25), 3)
        # Wing (static position - no flapping animation)
        pygame.draw.ellipse(screen, (101, 67, 33), (screen_x - 10, self.y - 15, 22, 10))
        pygame.draw.ellipse(screen, RETRO_BLACK, (screen_x - 10, self.y - 15, 22, 10), 2)
        # Head (natural brown)
        pygame.draw.circle(screen, (160, 82, 45), (int(screen_x + 12), int(self.y - 10)), 10)
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 12), int(self.y - 10)), 10, 3)
        # Beak (orange/yellow)
        pygame.draw.polygon(screen, (255, 140, 0), [(screen_x + 20, self.y - 10), (screen_x + 28, self.y - 7), (screen_x + 20, self.y - 4)])
        pygame.draw.polygon(screen, RETRO_BLACK, [(screen_x + 20, self.y - 10), (screen_x + 28, self.y - 7), (screen_x + 20, self.y - 4)], 2)
        # Eye
        pygame.draw.circle(screen, RETRO_BLACK, (int(screen_x + 15), int(self.y - 12)), 2)
        pygame.draw.circle(screen, RETRO_WHITE, (int(screen_x + 16), int(self.y - 13)), 1)
        # Tail feathers (static)
        pygame.draw.line(screen, (101, 67, 33), (screen_x - 15, self.y - 5), (screen_x - 22, self.y - 8), 3)
        pygame.draw.line(screen, (101, 67, 33), (screen_x - 15, self.y), (screen_x - 22, self.y - 2), 3)

class RefuelMenu:
    def __init__(self):
        self.selected_option = 0
        self.options = [
            {"text": "Emergency Fuel (+25%)", "fuel": 25, "description": "Quick refuel to continue"},
            {"text": "Standard Refuel (+50%)", "fuel": 50, "description": "Half tank refill"},
            {"text": "Premium Fill (+75%)", "fuel": 75, "description": "Three-quarter tank"},
            {"text": "Full Tank (+100%)", "fuel": 100, "description": "Complete fuel refill"},
            {"text": "Continue with Current Fuel", "fuel": 0, "description": "Resume without refueling"}
        ]
        self.title_animation = 0
        
    def update(self):
        self.title_animation += 0.03
        
    def handle_input(self, keys_just_pressed):
        """Handle refuel menu input"""
        if pygame.K_UP in keys_just_pressed and self.selected_option > 0:
            self.selected_option -= 1
            return -1
        elif pygame.K_DOWN in keys_just_pressed and self.selected_option < len(self.options) - 1:
            self.selected_option += 1
            return -1
        elif pygame.K_RETURN in keys_just_pressed:
            return self.selected_option
        return -1
    
    def draw(self, screen, current_fuel=15):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(RETRO_BLACK)
        screen.blit(overlay, (0, 0))
        
        # Refuel panel
        panel_width = 700
        panel_height = 500
        panel = pygame.Rect(SCREEN_WIDTH//2 - panel_width//2, SCREEN_HEIGHT//2 - panel_height//2, panel_width, panel_height)
        pygame.draw.rect(screen, RETRO_BLACK, panel)
        pygame.draw.rect(screen, RETRO_YELLOW, panel, 5)
        
        # Title
        title_y = SCREEN_HEIGHT//2 - 200 + math.sin(self.title_animation) * 5
        RetroFont.render_retro_text(screen, "FUEL STATION", SCREEN_WIDTH//2 - 120, title_y, 48, RETRO_YELLOW, True)
        RetroFont.render_retro_text(screen, "Choose your refuel option:", SCREEN_WIDTH//2 - 180, title_y + 50, 32, RETRO_WHITE, True)
        
        # Fuel gauge visual
        gauge_x = SCREEN_WIDTH//2 - 100
        gauge_y = title_y + 90
        gauge_width = 200
        gauge_height = 20
        
        # Empty gauge
        pygame.draw.rect(screen, RETRO_BLACK, (gauge_x, gauge_y, gauge_width, gauge_height))
        pygame.draw.rect(screen, RETRO_WHITE, (gauge_x, gauge_y, gauge_width, gauge_height), 3)
        
        # Current fuel level
        fuel_fill = (current_fuel / 100) * gauge_width
        fuel_color = RETRO_RED if current_fuel < 25 else RETRO_YELLOW if current_fuel < 50 else RETRO_BLUE
        pygame.draw.rect(screen, fuel_color, (gauge_x + 2, gauge_y + 2, fuel_fill, gauge_height - 4))
        
        RetroFont.render_retro_text(screen, f"Current Fuel: {int(current_fuel)}%", gauge_x, gauge_y + 30, 24, RETRO_WHITE, False)
        
        # Menu options
        start_y = SCREEN_HEIGHT//2 - 80
        for i, option in enumerate(self.options):
            y_pos = start_y + i * 60
            is_selected = i == self.selected_option
            
            # Option background
            if is_selected:
                option_rect = pygame.Rect(SCREEN_WIDTH//2 - 320, y_pos - 8, 640, 50)
                pygame.draw.rect(screen, RETRO_YELLOW, option_rect)
                pygame.draw.rect(screen, RETRO_BLACK, option_rect, 3)
            
            # Selection arrow
            if is_selected:
                arrow_points = [
                    (SCREEN_WIDTH//2 - 300, y_pos + 12),
                    (SCREEN_WIDTH//2 - 280, y_pos + 22),
                    (SCREEN_WIDTH//2 - 300, y_pos + 32)
                ]
                pygame.draw.polygon(screen, RETRO_BLACK if is_selected else RETRO_YELLOW, arrow_points)
            
            # Option text
            color = RETRO_BLACK if is_selected else RETRO_WHITE
            RetroFont.render_retro_text(screen, option["text"], SCREEN_WIDTH//2 - 250, y_pos, 32, color, True)
            
            # Description
            desc_color = (50, 50, 50) if is_selected else (150, 150, 150)
            RetroFont.render_retro_text(screen, option["description"], SCREEN_WIDTH//2 - 250, y_pos + 25, 20, desc_color, False)
        
        # Instructions
        RetroFont.render_retro_text(screen, "↑↓ Navigate    ENTER Select", SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 200, 24, RETRO_GREEN, True)

class Obstacle:
    def __init__(self, x, y, width, height, obstacle_type="rock"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x - width//2, y - height//2, width, height)
        self.type = obstacle_type
    
    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        if -100 < screen_x < SCREEN_WIDTH + 100:  # Only draw if on screen
            if self.type == "rock":
                # Retro stone with chunky pixels
                pygame.draw.ellipse(screen, (120, 120, 120), (screen_x - self.width//2, self.y - self.height//2, self.width, self.height))
                pygame.draw.ellipse(screen, RETRO_BLACK, (screen_x - self.width//2, self.y - self.height//2, self.width, self.height), 4)
                # Add retro highlights and texture
                pygame.draw.ellipse(screen, (160, 160, 160), (screen_x - self.width//3, self.y - self.height//3, self.width//2, self.height//2))
                pygame.draw.ellipse(screen, RETRO_BLACK, (screen_x - self.width//3, self.y - self.height//3, self.width//2, self.height//2), 2)
                # Stone texture dots
                for i in range(3):
                    dot_x = screen_x + random.randint(-self.width//4, self.width//4)
                    dot_y = self.y + random.randint(-self.height//4, self.height//4)
                    pygame.draw.circle(screen, (100, 100, 100), (int(dot_x), int(dot_y)), 3)
            elif self.type == "log":
                # Retro wood log
                log_rect = pygame.Rect(screen_x - self.width//2, self.y - self.height//2, self.width, self.height)
                pygame.draw.rect(screen, RETRO_BROWN, log_rect)
                pygame.draw.rect(screen, RETRO_BLACK, log_rect, 4)
                # Wood grain lines
                for i in range(3):
                    line_y = self.y - self.height//4 + i * (self.height//4)
                    pygame.draw.line(screen, (80, 50, 20), (screen_x - self.width//2 + 5, line_y), (screen_x + self.width//2 - 5, line_y), 2)
                # Log end rings
                for i in range(2):
                    ring_x = screen_x - self.width//2 + 15 + i * (self.width - 30)
                    pygame.draw.circle(screen, (80, 50, 20), (int(ring_x), int(self.y)), 12, 3)
                    pygame.draw.circle(screen, (60, 40, 15), (int(ring_x), int(self.y)), 8, 2)
                    pygame.draw.circle(screen, (40, 25, 10), (int(ring_x), int(self.y)), 4)

class Menu:
    def __init__(self):
        self.selected_option = 0
        self.options = [
            {"text": "Start the Drive", "description": "Begin your jungle adventure"},
            {"text": "Rest on Tyres", "description": "Pause the current game"},
            {"text": "Park Out of Jungle", "description": "Exit the game"}
        ]
        self.title_animation = 0
        self.menu_transition = 0
        self.retro_elements = self.generate_retro_background()
        self.is_paused = False  # Track if coming from pause
        
    def set_pause_mode(self, paused=False):
        """Set menu to pause mode"""
        self.is_paused = paused
        if paused:
            self.options[0] = {"text": "Start the Engine Again", "description": "Resume your jungle adventure"}
            self.options[1] = {"text": "Resting on Tyres", "description": "Currently paused"}
        else:
            self.options[0] = {"text": "Start the Drive", "description": "Begin your jungle adventure"}
            self.options[1] = {"text": "Rest on Tyres", "description": "Pause the current game"}
        
    def generate_retro_background(self):
        """Generate retro-style background elements"""
        elements = []
        # Create retro jungle scene with animals
        # Fixed positions for consistent retro look
        elements.append({"type": "tree", "x": 100, "y": 200, "size": 80})
        elements.append({"type": "tree", "x": 300, "y": 150, "size": 100})
        elements.append({"type": "tree", "x": 900, "y": 180, "size": 90})
        elements.append({"type": "tree", "x": 1100, "y": 160, "size": 85})
        
        # Add retro animal silhouettes in background
        elements.append({"type": "elephant", "x": 150, "y": 300})
        elements.append({"type": "tiger", "x": 800, "y": 320})
        elements.append({"type": "deer", "x": 950, "y": 310})
        elements.append({"type": "bird", "x": 400, "y": 120})
        elements.append({"type": "bird", "x": 600, "y": 140})
        
        return elements
        
    def update(self):
        self.title_animation += 0.05  # Slower, more professional animation
        self.menu_transition += 0.02
        
    def handle_input(self, keys_just_pressed):
        """Handle menu input with proper key detection"""
        if pygame.K_UP in keys_just_pressed and self.selected_option > 0:
            self.selected_option -= 1
            return -1
        elif pygame.K_DOWN in keys_just_pressed and self.selected_option < len(self.options) - 1:
            self.selected_option += 1
            return -1
        elif pygame.K_RETURN in keys_just_pressed:
            # Handle different menu options
            if self.selected_option == 0:  # Start/Resume
                return 0
            elif self.selected_option == 1:  # Rest on Tyres
                if not self.is_paused:  # Only allow if not already paused
                    return 1
                return -1  # Do nothing if already paused
            elif self.selected_option == 2:  # Quit
                return 2
        return -1
    
    def draw(self, screen):
        # Retro sunset/jungle background
        for y in range(0, SCREEN_HEIGHT, 3):
            if y < SCREEN_HEIGHT // 3:
                # Sky - retro orange/yellow sunset
                intensity = int(255 - (y / (SCREEN_HEIGHT // 3)) * 100)
                color = (255, intensity, 100)
            elif y < SCREEN_HEIGHT * 2 // 3:
                # Middle - jungle green
                intensity = int(150 - ((y - SCREEN_HEIGHT // 3) / (SCREEN_HEIGHT // 3)) * 50)
                color = (50, intensity, 50)
            else:
                # Ground - dark green
                color = (30, 80, 30)
            pygame.draw.rect(screen, color, (0, y, SCREEN_WIDTH, 3))
        
        # Draw retro background elements
        for element in self.retro_elements:
            if element["type"] == "tree":
                self.draw_retro_tree(screen, element["x"], element["y"], element["size"])
            elif element["type"] == "elephant":
                self.draw_retro_elephant_silhouette(screen, element["x"], element["y"])
            elif element["type"] == "tiger":
                self.draw_retro_tiger_silhouette(screen, element["x"], element["y"])
            elif element["type"] == "deer":
                self.draw_retro_deer_silhouette(screen, element["x"], element["y"])
            elif element["type"] == "bird":
                self.draw_retro_bird_silhouette(screen, element["x"], element["y"])
        
        # Retro title with chunky pixels
        title_y = 80 + math.sin(self.title_animation) * 8
        
        # Title background (retro style)
        title_bg = pygame.Rect(SCREEN_WIDTH//2 - 350, title_y - 60, 700, 120)
        pygame.draw.rect(screen, RETRO_BLACK, title_bg)
        pygame.draw.rect(screen, RETRO_YELLOW, title_bg, 6)
        
        # Chunky retro title
        RetroFont.render_retro_text(screen, "  JUNGLE DRIVE", SCREEN_WIDTH//2 - 220, title_y - 30, 72, RETRO_YELLOW, True)
        RetroFont.render_retro_text(screen, "    *** MILITARY ADVENTURE ***", SCREEN_WIDTH//2 - 240, title_y + 25, 32, RETRO_WHITE, True)
        
        # Large detailed retro jeep
        jeep_x = SCREEN_WIDTH//2
        jeep_y = 280
        self.draw_detailed_retro_jeep(screen, jeep_x, jeep_y)
        
        # Retro menu box
        menu_bg = pygame.Rect(SCREEN_WIDTH//2 - 300, 400, 600, 280)
        pygame.draw.rect(screen, RETRO_BLACK, menu_bg)
        pygame.draw.rect(screen, RETRO_WHITE, menu_bg, 5)
        
        # Menu title
        RetroFont.render_retro_text(screen, "MISSION CONTROL", SCREEN_WIDTH//2 - 140, 420, 36, RETRO_YELLOW, True)
        
        # Menu options with retro styling
        start_y = 470
        for i, option in enumerate(self.options):
            y_pos = start_y + i * 60
            is_selected = (i == self.selected_option)
            
            # Special handling for paused state - make "Resting on Tyres" non-selectable
            if self.is_paused and i == 1:  # "Resting on Tyres" when paused
                is_selected = False
                # Skip selection if trying to select this option
                if self.selected_option == 1 and self.is_paused:
                    self.selected_option = 0  # Move to first option
            
            # Retro selection box - always draw for selected option
            if is_selected:
                select_rect = pygame.Rect(SCREEN_WIDTH//2 - 280, y_pos - 8, 560, 50)
                pygame.draw.rect(screen, RETRO_YELLOW, select_rect)
                pygame.draw.rect(screen, RETRO_BLACK, select_rect, 3)
                
                # Retro arrow for selected option
                arrow_points = [
                    (SCREEN_WIDTH//2 - 260, y_pos + 12),
                    (SCREEN_WIDTH//2 - 240, y_pos + 22),
                    (SCREEN_WIDTH//2 - 260, y_pos + 32)
                ]
                pygame.draw.polygon(screen, RETRO_BLACK, arrow_points)
            
            # Option text with proper colors
            if self.is_paused and i == 1:  # "Resting on Tyres" - grayed out
                color = (100, 100, 100)
            elif is_selected:
                color = RETRO_BLACK  # Selected text is black on yellow background
            else:
                color = RETRO_WHITE  # Normal text is white
            
            RetroFont.render_retro_text(screen, option["text"], SCREEN_WIDTH//2 - 220, y_pos, 38, color, True)
        
        # Retro instructions
        inst_bg = pygame.Rect(SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT - 100, 500, 60)
        pygame.draw.rect(screen, RETRO_BLACK, inst_bg)
        pygame.draw.rect(screen, RETRO_GREEN, inst_bg, 3)
        
        RetroFont.render_retro_text(screen, "↑↓ NAVIGATE    ENTER SELECT", SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT - 85, 24, RETRO_GREEN, True)
        RetroFont.render_retro_text(screen, "ESC RETURN TO MENU", SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT - 60, 20, RETRO_WHITE, False)
    
    def draw_retro_tree(self, screen, x, y, size):
        """Draw retro chunky tree"""
        # Trunk
        trunk_rect = pygame.Rect(x - 8, y + size//2, 16, size//2)
        pygame.draw.rect(screen, RETRO_BROWN, trunk_rect)
        pygame.draw.rect(screen, RETRO_BLACK, trunk_rect, 3)
        # Canopy (chunky circles)
        pygame.draw.circle(screen, DARK_GREEN, (x, y), size//2)
        pygame.draw.circle(screen, RETRO_BLACK, (x, y), size//2, 4)
        pygame.draw.circle(screen, JUNGLE_GREEN, (x, y), size//3)
    
    def draw_retro_elephant_silhouette(self, screen, x, y):
        """Draw retro elephant silhouette"""
        # Body (chunky rectangle)
        pygame.draw.rect(screen, (60, 60, 60), (x - 30, y - 20, 60, 35))
        pygame.draw.rect(screen, RETRO_BLACK, (x - 30, y - 20, 60, 35), 3)
        # Head
        pygame.draw.circle(screen, (60, 60, 60), (x - 35, y - 10), 18)
        pygame.draw.circle(screen, RETRO_BLACK, (x - 35, y - 10), 18, 3)
        # Trunk (simple line)
        pygame.draw.line(screen, (60, 60, 60), (x - 45, y - 5), (x - 55, y + 10), 8)
        pygame.draw.line(screen, RETRO_BLACK, (x - 45, y - 5), (x - 55, y + 10), 2)
    
    def draw_retro_tiger_silhouette(self, screen, x, y):
        """Draw retro tiger silhouette"""
        # Body
        pygame.draw.ellipse(screen, (80, 80, 80), (x - 25, y - 15, 50, 25))
        pygame.draw.ellipse(screen, RETRO_BLACK, (x - 25, y - 15, 50, 25), 3)
        # Head
        pygame.draw.circle(screen, (80, 80, 80), (x + 20, y - 8), 12)
        pygame.draw.circle(screen, RETRO_BLACK, (x + 20, y - 8), 12, 3)
    
    def draw_retro_deer_silhouette(self, screen, x, y):
        """Draw retro deer silhouette"""
        # Body
        pygame.draw.ellipse(screen, (70, 70, 70), (x - 15, y - 12, 30, 20))
        pygame.draw.ellipse(screen, RETRO_BLACK, (x - 15, y - 12, 30, 20), 3)
        # Head
        pygame.draw.circle(screen, (70, 70, 70), (x + 12, y - 10), 8)
        pygame.draw.circle(screen, RETRO_BLACK, (x + 12, y - 10), 8, 2)
        # Antlers
        pygame.draw.line(screen, RETRO_BLACK, (x + 10, y - 15), (x + 8, y - 22), 3)
        pygame.draw.line(screen, RETRO_BLACK, (x + 14, y - 15), (x + 16, y - 22), 3)
    
    def draw_retro_bird_silhouette(self, screen, x, y):
        """Draw retro bird silhouette"""
        # Body
        pygame.draw.ellipse(screen, (50, 50, 50), (x - 8, y - 5, 16, 10))
        pygame.draw.ellipse(screen, RETRO_BLACK, (x - 8, y - 5, 16, 10), 2)
        # Wing
        wing_flap = math.sin(self.title_animation * 2) * 3
        pygame.draw.ellipse(screen, (50, 50, 50), (x - 5, y - 8 + wing_flap, 12, 6))
    
    def draw_detailed_retro_jeep(self, screen, x, y):
        """Draw large detailed retro jeep for menu"""
        # Main body (chunky retro style)
        body_rect = pygame.Rect(x - 80, y - 40, 160, 80)
        pygame.draw.rect(screen, MILITARY_GREEN, body_rect)
        pygame.draw.rect(screen, RETRO_BLACK, body_rect, 5)
        
        # Hood
        hood_rect = pygame.Rect(x + 50, y - 30, 30, 60)
        pygame.draw.rect(screen, (70, 90, 40), hood_rect)
        pygame.draw.rect(screen, RETRO_BLACK, hood_rect, 4)
        
        # Windshield (chunky)
        windshield_points = [(x - 30, y - 35), (x + 40, y - 35), (x + 30, y - 10), (x - 40, y - 10)]
        pygame.draw.polygon(screen, (100, 150, 200), windshield_points)
        pygame.draw.polygon(screen, RETRO_BLACK, windshield_points, 4)
        
        # Canvas top
        canvas_points = [(x - 70, y - 40), (x + 40, y - 40), (x + 35, y - 55), (x - 75, y - 55)]
        pygame.draw.polygon(screen, (100, 120, 60), canvas_points)
        pygame.draw.polygon(screen, RETRO_BLACK, canvas_points, 4)
        
        # Wheels (chunky retro)
        for wheel_x in [x - 40, x + 40]:
            # Tire
            pygame.draw.circle(screen, RETRO_BLACK, (wheel_x, y + 35), 30, 10)
            # Rim
            pygame.draw.circle(screen, (150, 150, 150), (wheel_x, y + 35), 20)
            pygame.draw.circle(screen, RETRO_BLACK, (wheel_x, y + 35), 20, 4)
            # Hub
            pygame.draw.circle(screen, (80, 80, 80), (wheel_x, y + 35), 10)
            # Spokes
            for i in range(5):
                angle = i * 72
                spoke_x1 = wheel_x + 8 * math.cos(math.radians(angle))
                spoke_y1 = y + 35 + 8 * math.sin(math.radians(angle))
                spoke_x2 = wheel_x + 18 * math.cos(math.radians(angle))
                spoke_y2 = y + 35 + 18 * math.sin(math.radians(angle))
                pygame.draw.line(screen, RETRO_BLACK, (spoke_x1, spoke_y1), (spoke_x2, spoke_y2), 4)
        
        # Headlight
        pygame.draw.circle(screen, RETRO_YELLOW, (x + 70, y - 10), 15)
        pygame.draw.circle(screen, RETRO_WHITE, (x + 70, y - 10), 12)
        pygame.draw.circle(screen, RETRO_BLACK, (x + 70, y - 10), 15, 3)
        
        # Military star (large)
        star_points = []
        for i in range(5):
            angle = i * 72 - 90
            outer_x = x + 20 * math.cos(math.radians(angle))
            outer_y = y + 20 * math.sin(math.radians(angle))
            star_points.append((outer_x, outer_y))
            inner_angle = angle + 36
            inner_x = x + 10 * math.cos(math.radians(inner_angle))
            inner_y = y + 10 * math.sin(math.radians(inner_angle))
            star_points.append((inner_x, inner_y))
        pygame.draw.polygon(screen, RETRO_WHITE, star_points)
        pygame.draw.polygon(screen, RETRO_BLACK, star_points, 3)
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jungle Drive - Retro Adventure")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = MENU
        self.menu = Menu()
        self.refuel_menu = RefuelMenu()
        
        # Game objects
        self.jeep = None
        self.camera_x = 0
        self.world_width = 5000
        self.finish_x = self.world_width - 200
        
        # Game data
        self.terrain_height = []
        self.obstacles = []
        self.animals = []
        
        # Game flags
        self.game_won = False
        self.game_over = False
        self.keys_pressed_last_frame = set()  # Initialize properly
        
        self.init_game_world()
    
    def init_game_world(self):
        """Initialize the game world safely"""
        try:
            self.jeep = Jeep(100, SCREEN_HEIGHT - 200)
            self.camera_x = 0
            self.terrain_height = self.generate_terrain()
            self.obstacles = self.generate_obstacles()
            self.animals = self.generate_animals()
            self.game_won = False
            self.game_over = False
        except Exception as e:
            print(f"Error initializing game world: {e}")
            # Fallback initialization
            self.jeep = Jeep(100, SCREEN_HEIGHT - 200)
            self.camera_x = 0
            self.terrain_height = [SCREEN_HEIGHT - 120] * self.world_width
            self.obstacles = []
            self.animals = []
            self.game_won = False
            self.game_over = False
    
    def generate_terrain(self):
        """Generate retro jungle terrain"""
        terrain = []
        base_height = SCREEN_HEIGHT - 120
        
        for x in range(self.world_width):
            # Create hills and valleys with retro chunky feel
            hill_factor = math.sin(x * 0.008) * 60
            noise = math.sin(x * 0.05) * 20  # Add some noise
            
            # Mountain at the end
            if x > self.world_width * 0.75:
                mountain_factor = ((x - self.world_width * 0.75) / (self.world_width * 0.25)) * 250
                height = base_height - hill_factor - mountain_factor - noise
            else:
                height = base_height - hill_factor - noise
            
            terrain.append(max(150, height))
        
        return terrain
    
    def generate_obstacles(self):
        """Generate only stones and wood logs as obstacles"""
        obstacles = []
        
        for i in range(300, self.world_width - 300, 160):  # Better spacing
            if random.random() < 0.5:  # Reduced density for easier gameplay
                obstacle_type = random.choice(["rock", "log"])  # Only rocks and logs
                
                if obstacle_type == "rock":
                    width, height = random.randint(45, 80), random.randint(30, 55)  # Stones
                else:  # log
                    width, height = random.randint(80, 140), 35  # Wood logs
                
                x = i + random.randint(-60, 60)
                y = self.terrain_height[x] - height//2
                
                obstacles.append(Obstacle(x, y, width, height, obstacle_type))
        
        return obstacles
    
    def generate_animals(self):
        """Generate realistic retro jungle animals"""
        animals = []
        animal_types = ["elephant", "tiger", "deer", "bear", "squirrel", "bird"]  # Updated animal list
        
        for i in range(200, self.world_width - 200, 200):  # Better spacing
            if random.random() < 0.4:  # Reduced density for cleaner look
                animal_type = random.choice(animal_types)
                x = i + random.randint(-80, 80)
                
                # Position animals in background
                if animal_type == "bird":
                    y = self.terrain_height[x] - random.randint(100, 180)  # Birds fly higher
                elif animal_type == "squirrel":
                    y = self.terrain_height[x] - random.randint(60, 100)  # Squirrels in trees
                else:
                    y = self.terrain_height[x] - random.randint(25, 45)  # Ground animals
                
                animals.append(Animal(x, y, animal_type))
        
        return animals
    
    def update_camera(self):
        """Update camera to follow jeep with retro smoothing"""
        target_x = self.jeep.x - SCREEN_WIDTH // 3
        self.camera_x = max(0, min(target_x, self.world_width - SCREEN_WIDTH))
    
    def draw_terrain(self):
        """Draw realistic jungle terrain with static background elements"""
        # Clear and draw realistic sky gradient
        for y in range(0, SCREEN_HEIGHT//2, 2):
            sky_intensity = int(135 + (y / (SCREEN_HEIGHT//2)) * 120)
            sky_color = (135, sky_intensity, 255)
            pygame.draw.rect(self.screen, sky_color, (0, y, SCREEN_WIDTH, 2))
        
        # Fill lower half with base ground color first
        pygame.draw.rect(self.screen, (34, 100, 34), (0, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT//2))
        
        # Ground with realistic texture
        ground_points = [(0, SCREEN_HEIGHT)]
        
        for x in range(int(self.camera_x), min(int(self.camera_x) + SCREEN_WIDTH + 1, len(self.terrain_height))):
            screen_x = x - self.camera_x
            ground_points.append((screen_x, self.terrain_height[x]))
        
        ground_points.append((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        if len(ground_points) > 2:
            # Main ground color
            pygame.draw.polygon(self.screen, (34, 100, 34), ground_points)
            # Ground texture lines
            pygame.draw.polygon(self.screen, RETRO_BLACK, ground_points, 2)
            
            # Add realistic ground details
            for i in range(len(ground_points) - 2):
                if i % 3 == 0:  # Every third point
                    x, y = ground_points[i + 1]
                    # Small grass tufts
                    for j in range(3):
                        grass_x = x + j * 5 - 5
                        grass_y = y - random.randint(5, 15)
                        pygame.draw.line(self.screen, DARK_GREEN, (grass_x, y), (grass_x, grass_y), 2)
        
        # Static jungle background elements (NO ROTATION/LOOPS)
        # Pre-calculated positions to avoid random generation in draw loop
        background_positions = []
        for i in range(0, self.world_width, 200):  # Fixed spacing
            background_positions.append({
                'x': i,
                'type': 'tree' if (i // 200) % 3 == 0 else 'bush',
                'size': 35 + ((i // 100) % 3) * 10  # Deterministic size based on position
            })
        
        # Draw only visible background elements
        for bg_element in background_positions:
            if int(self.camera_x) - 100 <= bg_element['x'] <= int(self.camera_x) + SCREEN_WIDTH + 100:
                screen_x = bg_element['x'] - self.camera_x
                
                if bg_element['type'] == 'tree':
                    # Background tree (static)
                    tree_y = self.terrain_height[bg_element['x']] - 80
                    tree_size = bg_element['size']
                    # Tree trunk
                    pygame.draw.rect(self.screen, RETRO_BROWN, 
                                   (screen_x - 8, tree_y + tree_size, 16, 40))
                    # Tree canopy (static circles)
                    pygame.draw.circle(self.screen, DARK_GREEN, 
                                     (int(screen_x), int(tree_y)), tree_size)
                    pygame.draw.circle(self.screen, (0, 80, 0), 
                                     (int(screen_x), int(tree_y)), tree_size - 10)
                    
                else:  # bush
                    # Background bushes (static)
                    bush_y = self.terrain_height[bg_element['x']] - 30
                    bush_size = bg_element['size'] // 2
                    pygame.draw.ellipse(self.screen, JUNGLE_GREEN, 
                                      (screen_x - bush_size, bush_y - bush_size//2, 
                                       bush_size * 2, bush_size))
                    pygame.draw.ellipse(self.screen, RETRO_BLACK, 
                                      (screen_x - bush_size, bush_y - bush_size//2, 
                                       bush_size * 2, bush_size), 2)
    
    def draw_finish_line(self):
        """Draw retro finish flag"""
        flag_x = self.finish_x - self.camera_x
        if -100 < flag_x < SCREEN_WIDTH + 100:
            flag_y = self.terrain_height[self.finish_x] - 120
            
            # Flag pole (retro thick)
            pygame.draw.line(self.screen, RETRO_BROWN, (flag_x, flag_y), (flag_x, flag_y + 100), 8)
            
            # Flag (retro checkered)
            flag_width, flag_height = 80, 40
            for row in range(4):
                for col in range(8):
                    color = RETRO_WHITE if (row + col) % 2 == 0 else RETRO_BLACK
                    rect = pygame.Rect(flag_x + col * 10, flag_y + row * 10, 10, 10)
                    pygame.draw.rect(self.screen, color, rect)
            
            pygame.draw.rect(self.screen, RETRO_BLACK, (flag_x, flag_y, flag_width, flag_height), 3)
            
            # "FINISH" text (retro style)
            RetroFont.render_retro_text(self.screen, "FINISH", flag_x - 30, flag_y - 40, 32, RETRO_YELLOW)
    
    def draw_hud(self):
        """Draw retro HUD with pause instruction"""
        # Health bar (retro style)
        health_width = 250
        health_height = 25
        health_fill = (self.jeep.health / 100) * health_width
        
        # Health bar background
        pygame.draw.rect(self.screen, RETRO_BLACK, (25, 25, health_width + 6, health_height + 6))
        pygame.draw.rect(self.screen, RETRO_RED, (28, 28, health_fill, health_height))
        pygame.draw.rect(self.screen, RETRO_WHITE, (25, 25, health_width + 6, health_height + 6), 3)
        
        RetroFont.render_retro_text(self.screen, f"HEALTH: {int(self.jeep.health)}", 25, 60, 28, RETRO_WHITE)
        
        # Fuel bar (retro style)
        fuel_fill = (self.jeep.fuel / 100) * health_width
        pygame.draw.rect(self.screen, RETRO_BLACK, (25, 95, health_width + 6, health_height + 6))
        pygame.draw.rect(self.screen, RETRO_BLUE, (28, 98, fuel_fill, health_height))
        pygame.draw.rect(self.screen, RETRO_WHITE, (25, 95, health_width + 6, health_height + 6), 3)
        
        RetroFont.render_retro_text(self.screen, f"FUEL: {int(self.jeep.fuel)}", 25, 130, 28, RETRO_WHITE)
        
        # Distance and speed (retro style)
        distance = max(0, self.finish_x - self.jeep.x)
        RetroFont.render_retro_text(self.screen, f"DISTANCE: {int(distance)}m", SCREEN_WIDTH - 350, 25, 28, RETRO_WHITE)
        
        current_speed = abs(self.jeep.velocity_x)
        RetroFont.render_retro_text(self.screen, f"SPEED: {int(current_speed * 12)} mph", SCREEN_WIDTH - 280, 60, 28, RETRO_WHITE)
        
        # Pause instruction (top right corner) - more prominent
        pause_bg = pygame.Rect(SCREEN_WIDTH - 220, 95, 200, 35)
        pygame.draw.rect(self.screen, RETRO_BLACK, pause_bg)
        pygame.draw.rect(self.screen, RETRO_YELLOW, pause_bg, 2)
        RetroFont.render_retro_text(self.screen, "Press P to Pause", SCREEN_WIDTH - 210, 105, 24, RETRO_YELLOW)
        
        # Controls (retro style)
        RetroFont.render_retro_text(self.screen, "↑Jump  →Accelerate  ←Reverse  ↓Fast Drop", 
                                   25, SCREEN_HEIGHT - 40, 24, RETRO_YELLOW)
    
    def check_win_condition(self):
        """Check if player reached finish"""
        if abs(self.jeep.x - self.finish_x) < 60:
            self.game_won = True
    
    def check_game_over(self):
        """Check game over conditions - modified for refuel option"""
        if self.jeep.health <= 0:
            self.game_over = True
        elif self.jeep.fuel <= 0:
            # Instead of game over, show refuel menu
            self.state = REFUEL_MENU
    
    def draw_game_over_screen(self):
        """Draw retro game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(RETRO_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        if self.game_won:
            RetroFont.render_retro_text(self.screen, "MISSION COMPLETE!", SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2 - 100, 72, RETRO_YELLOW)
            RetroFont.render_retro_text(self.screen, "You conquered the jungle!", SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 20, 36, RETRO_WHITE)
        else:
            RetroFont.render_retro_text(self.screen, "MISSION FAILED!", SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 100, 72, RETRO_RED)
            if self.jeep.health <= 0:
                RetroFont.render_retro_text(self.screen, "Your jeep was destroyed!", SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2 - 20, 36, RETRO_WHITE)
            else:
                RetroFont.render_retro_text(self.screen, "You ran out of fuel!", SCREEN_WIDTH//2 - 160, SCREEN_HEIGHT//2 - 20, 36, RETRO_WHITE)
        
        RetroFont.render_retro_text(self.screen, "Press R to Restart or ESC for Menu", SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2 + 60, 32, RETRO_YELLOW)
    
    def handle_input(self):
        """Handle input based on game state with proper key detection"""
        keys_pressed = pygame.key.get_pressed()
        keys_just_pressed = set()
        
        # Detect keys just pressed (not held) - this is crucial for menu navigation
        for key in range(512):  # Check all possible keys
            if key < len(keys_pressed) and keys_pressed[key] and key not in self.keys_pressed_last_frame:
                keys_just_pressed.add(key)
        
        # Update last frame keys
        self.keys_pressed_last_frame = {key for key in range(512) if key < len(keys_pressed) and keys_pressed[key]}
        
        if self.state == MENU:
            # Handle menu navigation directly here for better control
            if pygame.K_UP in keys_just_pressed:
                if self.menu.selected_option > 0:
                    self.menu.selected_option -= 1
            elif pygame.K_DOWN in keys_just_pressed:
                if self.menu.selected_option < len(self.menu.options) - 1:
                    self.menu.selected_option += 1
            elif pygame.K_RETURN in keys_just_pressed:
                selected = self.menu.selected_option
                
                if selected == 0:  # Start the Drive / Start the Engine Again
                    if self.menu.is_paused:
                        self.menu.set_pause_mode(False)
                        self.state = PLAYING
                    else:
                        self.state = PLAYING
                        self.init_game_world()
                elif selected == 1:  # Rest on Tyres
                    if not self.menu.is_paused and hasattr(self, 'jeep') and self.jeep and not self.game_over and not self.game_won:
                        self.menu.set_pause_mode(True)
                elif selected == 2:  # Park Out of Jungle (Quit)
                    return False
        
        elif self.state == PLAYING:
            if pygame.K_p in keys_just_pressed:  # Pause with P key
                self.menu.set_pause_mode(True)
                self.state = MENU  # Go to menu in paused state
            elif pygame.K_ESCAPE in keys_just_pressed:
                self.menu.set_pause_mode(False)
                self.state = MENU
            elif self.game_over or self.game_won:
                if pygame.K_r in keys_just_pressed:
                    self.init_game_world()
                elif pygame.K_ESCAPE in keys_just_pressed:
                    self.menu.set_pause_mode(False)
                    self.state = MENU
        
        elif self.state == REFUEL_MENU:
            refuel_result = self.refuel_menu.handle_input(keys_just_pressed)
            if refuel_result >= 0:
                selected_option = self.refuel_menu.options[refuel_result]
                if selected_option["fuel"] > 0:
                    # Refuel the jeep
                    self.jeep.fuel = min(100, self.jeep.fuel + selected_option["fuel"])
                # Return to game
                self.state = PLAYING
        
        return True
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Handle input
            if not self.handle_input():
                running = False
                continue
            
            # Update based on state
            if self.state == MENU:
                self.menu.update()
            elif self.state == REFUEL_MENU:
                self.refuel_menu.update()
            elif self.state == PLAYING and not self.game_over and not self.game_won:
                keys_pressed = pygame.key.get_pressed()
                self.jeep.update(keys_pressed, self.obstacles, self.terrain_height)
                self.update_camera()
                
                # Update animals
                for animal in self.animals:
                    animal.update()
                
                self.check_win_condition()
                self.check_game_over()
            
            # Draw based on state
            # Clear screen first to prevent rendering artifacts
            self.screen.fill((0, 0, 0))  # Clear with black
            
            if self.state == MENU:
                self.menu.draw(self.screen)
            elif self.state == REFUEL_MENU:
                # Draw game world in background
                self.draw_terrain()
                
                # Draw animals (background)
                for animal in self.animals:
                    animal.draw(self.screen, self.camera_x)
                
                # Draw obstacles
                for obstacle in self.obstacles:
                    obstacle.draw(self.screen, self.camera_x)
                
                self.draw_finish_line()
                self.jeep.draw(self.screen, self.camera_x)
                
                # Draw refuel menu on top
                self.refuel_menu.draw(self.screen, self.jeep.fuel)
            else:
                # Draw game world
                self.draw_terrain()
                
                # Draw animals (background)
                for animal in self.animals:
                    animal.draw(self.screen, self.camera_x)
                
                # Draw obstacles
                for obstacle in self.obstacles:
                    obstacle.draw(self.screen, self.camera_x)
                
                self.draw_finish_line()
                self.jeep.draw(self.screen, self.camera_x)
                self.draw_hud()
                
                if self.game_over or self.game_won:
                    self.draw_game_over_screen()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
