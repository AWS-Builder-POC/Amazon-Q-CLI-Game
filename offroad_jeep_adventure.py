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

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255)
MOUNTAIN_COLOR = (105, 105, 105)

class Jeep:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 40
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_speed = 8
        self.acceleration = 0.5
        self.jump_power = 12
        self.gravity = 0.6
        self.friction = 0.85
        self.health = 100
        self.fuel = 100
        self.on_ground = True
        self.facing_right = True
        
    def update(self, keys_pressed, obstacles, terrain_height):
        # Handle horizontal movement
        if keys_pressed[pygame.K_RIGHT]:
            self.velocity_x += self.acceleration
            self.facing_right = True
        elif keys_pressed[pygame.K_LEFT]:
            self.velocity_x -= self.acceleration
            self.facing_right = False
        else:
            # Apply friction when no input
            self.velocity_x *= self.friction
        
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
        
        # Terrain collision
        if 0 <= int(self.x) < len(terrain_height):
            ground_y = terrain_height[int(self.x)]
            
            if self.y + self.height//2 >= ground_y:
                self.y = ground_y - self.height//2
                self.velocity_y = 0
                self.on_ground = True
            else:
                self.on_ground = False
        
        # Check collision with obstacles
        jeep_rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
        
        for obstacle in obstacles:
            if jeep_rect.colliderect(obstacle.rect):
                # Simple collision - stop and take damage
                self.x, self.y = old_x, old_y
                self.velocity_x *= -0.3
                self.health -= 8
                break
        
        # Fuel consumption
        if abs(self.velocity_x) > 0.1:
            self.fuel -= 0.08
        else:
            self.fuel -= 0.02  # Idle consumption
        
        # Prevent negative values
        self.health = max(0, self.health)
        self.fuel = max(0, self.fuel)
    
    def draw(self, screen, camera_x):
        # Calculate screen position
        screen_x = self.x - camera_x
        screen_y = self.y
        
        # Military jeep side view
        # Main body (rectangular with military green)
        body_color = (85, 107, 47)  # Dark olive green
        body_rect = pygame.Rect(screen_x - self.width//2, screen_y - self.height//2, self.width, self.height)
        pygame.draw.rect(screen, body_color, body_rect)
        pygame.draw.rect(screen, (60, 80, 30), body_rect, 3)  # Darker outline
        
        # Hood (front part)
        hood_rect = pygame.Rect(screen_x + (self.width//2 - 20 if self.facing_right else -self.width//2), 
                               screen_y - self.height//2 + 5, 20, self.height - 10)
        pygame.draw.rect(screen, (70, 90, 40), hood_rect)
        
        # Windshield
        windshield_points = []
        if self.facing_right:
            windshield_points = [
                (screen_x - 10, screen_y - self.height//2 + 2),
                (screen_x + 15, screen_y - self.height//2 + 2),
                (screen_x + 10, screen_y - 5),
                (screen_x - 15, screen_y - 5)
            ]
        else:
            windshield_points = [
                (screen_x + 10, screen_y - self.height//2 + 2),
                (screen_x - 15, screen_y - self.height//2 + 2),
                (screen_x - 10, screen_y - 5),
                (screen_x + 15, screen_y - 5)
            ]
        
        pygame.draw.polygon(screen, (150, 200, 255), windshield_points)  # Light blue windshield
        
        # Military canvas top
        canvas_points = []
        if self.facing_right:
            canvas_points = [
                (screen_x - self.width//2 + 5, screen_y - self.height//2),
                (screen_x + self.width//2 - 15, screen_y - self.height//2),
                (screen_x + self.width//2 - 20, screen_y - self.height//2 - 8),
                (screen_x - self.width//2, screen_y - self.height//2 - 8)
            ]
        else:
            canvas_points = [
                (screen_x + self.width//2 - 5, screen_y - self.height//2),
                (screen_x - self.width//2 + 15, screen_y - self.height//2),
                (screen_x - self.width//2 + 20, screen_y - self.height//2 - 8),
                (screen_x + self.width//2, screen_y - self.height//2 - 8)
            ]
        
        pygame.draw.polygon(screen, (100, 120, 60), canvas_points)
        
        # Wheels (side view - 2 wheels visible)
        wheel_y = screen_y + self.height//2 - 5
        front_wheel_x = screen_x + (25 if self.facing_right else -25)
        rear_wheel_x = screen_x + (-25 if self.facing_right else 25)
        
        # Draw wheels
        for wheel_x in [front_wheel_x, rear_wheel_x]:
            # Tire
            pygame.draw.circle(screen, BLACK, (int(wheel_x), int(wheel_y)), 15)
            # Rim
            pygame.draw.circle(screen, GRAY, (int(wheel_x), int(wheel_y)), 10)
            # Hub
            pygame.draw.circle(screen, (40, 40, 40), (int(wheel_x), int(wheel_y)), 5)
            # Tire treads
            for i in range(4):
                angle = i * 90
                tread_x = wheel_x + 12 * math.cos(math.radians(angle))
                tread_y = wheel_y + 12 * math.sin(math.radians(angle))
                pygame.draw.circle(screen, (60, 60, 60), (int(tread_x), int(tread_y)), 2)
        
        # Headlight
        headlight_x = screen_x + (self.width//2 - 5 if self.facing_right else -self.width//2 + 5)
        headlight_y = screen_y - 5
        pygame.draw.circle(screen, YELLOW, (int(headlight_x), int(headlight_y)), 8)
        pygame.draw.circle(screen, WHITE, (int(headlight_x), int(headlight_y)), 5)
        
        # Military star emblem
        star_x = screen_x
        star_y = screen_y - 5
        star_points = []
        for i in range(5):
            angle = i * 72 - 90  # Start from top
            outer_x = star_x + 8 * math.cos(math.radians(angle))
            outer_y = star_y + 8 * math.sin(math.radians(angle))
            star_points.append((outer_x, outer_y))
            
            # Inner point
            inner_angle = angle + 36
            inner_x = star_x + 4 * math.cos(math.radians(inner_angle))
            inner_y = star_y + 4 * math.sin(math.radians(inner_angle))
            star_points.append((inner_x, inner_y))
        
        pygame.draw.polygon(screen, WHITE, star_points)
        
        # Exhaust pipe
        exhaust_x = screen_x + (-self.width//2 + 5 if self.facing_right else self.width//2 - 5)
        exhaust_y = screen_y + self.height//2 - 8
        pygame.draw.rect(screen, (50, 50, 50), (exhaust_x - 3, exhaust_y - 2, 6, 4))
        
        # Jump indicator (when in air)
        if not self.on_ground:
            pygame.draw.circle(screen, (255, 255, 0), (int(screen_x), int(screen_y - self.height//2 - 15)), 5, 2)

class Animal:
    def __init__(self, x, y, animal_type):
        self.x = x
        self.y = y
        self.type = animal_type
        self.animation_frame = 0
        self.direction = random.choice([-1, 1])
        self.speed = random.uniform(0.5, 2.0)
        
        if animal_type == "elephant":
            self.width, self.height = 60, 40
        elif animal_type == "monkey":
            self.width, self.height = 25, 30
        elif animal_type == "tiger":
            self.width, self.height = 50, 30
        elif animal_type == "bird":
            self.width, self.height = 20, 15
        else:  # deer
            self.width, self.height = 35, 35
    
    def update(self):
        self.animation_frame += 0.1
        # Simple movement for some animals
        if self.type in ["monkey", "bird"]:
            self.x += self.direction * self.speed
            if random.randint(0, 200) == 0:  # Change direction occasionally
                self.direction *= -1
    
    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        if -100 < screen_x < SCREEN_WIDTH + 100:  # Only draw if on screen
            if self.type == "elephant":
                self.draw_elephant(screen, screen_x)
            elif self.type == "monkey":
                self.draw_monkey(screen, screen_x)
            elif self.type == "tiger":
                self.draw_tiger(screen, screen_x)
            elif self.type == "bird":
                self.draw_bird(screen, screen_x)
            else:  # deer
                self.draw_deer(screen, screen_x)
    
    def draw_elephant(self, screen, screen_x):
        # Body
        pygame.draw.ellipse(screen, (105, 105, 105), (screen_x - 30, self.y - 20, 60, 40))
        # Head
        pygame.draw.circle(screen, (105, 105, 105), (int(screen_x - 35), int(self.y - 10)), 20)
        # Trunk
        trunk_points = [(screen_x - 50, self.y - 5), (screen_x - 60, self.y + 5), (screen_x - 55, self.y + 15)]
        pygame.draw.lines(screen, (105, 105, 105), False, trunk_points, 8)
        # Legs
        for leg_x in [screen_x - 20, screen_x - 10, screen_x + 10, screen_x + 20]:
            pygame.draw.rect(screen, (90, 90, 90), (leg_x - 3, self.y + 15, 6, 15))
        # Eye
        pygame.draw.circle(screen, BLACK, (int(screen_x - 40), int(self.y - 15)), 3)
    
    def draw_monkey(self, screen, screen_x):
        # Body
        pygame.draw.ellipse(screen, (139, 69, 19), (screen_x - 12, self.y - 15, 25, 30))
        # Head
        pygame.draw.circle(screen, (160, 82, 45), (int(screen_x), int(self.y - 20)), 12)
        # Arms (animated)
        arm_offset = math.sin(self.animation_frame) * 5
        pygame.draw.line(screen, (139, 69, 19), (screen_x - 8, self.y - 10), (screen_x - 15, self.y - 5 + arm_offset), 4)
        pygame.draw.line(screen, (139, 69, 19), (screen_x + 8, self.y - 10), (screen_x + 15, self.y - 5 - arm_offset), 4)
        # Legs
        pygame.draw.line(screen, (139, 69, 19), (screen_x - 5, self.y + 10), (screen_x - 8, self.y + 20), 4)
        pygame.draw.line(screen, (139, 69, 19), (screen_x + 5, self.y + 10), (screen_x + 8, self.y + 20), 4)
        # Face
        pygame.draw.circle(screen, BLACK, (int(screen_x - 4), int(self.y - 22)), 2)
        pygame.draw.circle(screen, BLACK, (int(screen_x + 4), int(self.y - 22)), 2)
        pygame.draw.circle(screen, BLACK, (int(screen_x), int(self.y - 18)), 1)
    
    def draw_tiger(self, screen, screen_x):
        # Body
        pygame.draw.ellipse(screen, (255, 140, 0), (screen_x - 25, self.y - 15, 50, 30))
        # Head
        pygame.draw.circle(screen, (255, 140, 0), (int(screen_x + 20), int(self.y - 10)), 15)
        # Stripes
        for stripe_x in [screen_x - 15, screen_x - 5, screen_x + 5, screen_x + 15]:
            pygame.draw.line(screen, BLACK, (stripe_x, self.y - 12), (stripe_x, self.y + 8), 2)
        # Legs
        for leg_x in [screen_x - 15, screen_x - 5, screen_x + 5, screen_x + 15]:
            pygame.draw.rect(screen, (255, 140, 0), (leg_x - 2, self.y + 10, 4, 12))
        # Ears
        pygame.draw.polygon(screen, (255, 140, 0), [(screen_x + 15, self.y - 20), (screen_x + 20, self.y - 25), (screen_x + 25, self.y - 20)])
        pygame.draw.polygon(screen, (255, 140, 0), [(screen_x + 20, self.y - 20), (screen_x + 25, self.y - 25), (screen_x + 30, self.y - 20)])
        # Eyes
        pygame.draw.circle(screen, BLACK, (int(screen_x + 18), int(self.y - 12)), 2)
        pygame.draw.circle(screen, BLACK, (int(screen_x + 22), int(self.y - 12)), 2)
    
    def draw_bird(self, screen, screen_x):
        # Body
        pygame.draw.ellipse(screen, (255, 0, 0), (screen_x - 10, self.y - 8, 20, 15))
        # Wing (animated)
        wing_flap = math.sin(self.animation_frame * 3) * 8
        pygame.draw.ellipse(screen, (200, 0, 0), (screen_x - 5, self.y - 12 + wing_flap, 15, 8))
        # Head
        pygame.draw.circle(screen, (255, 0, 0), (int(screen_x + 8), int(self.y - 5)), 6)
        # Beak
        pygame.draw.polygon(screen, YELLOW, [(screen_x + 12, self.y - 5), (screen_x + 18, self.y - 3), (screen_x + 12, self.y - 1)])
        # Eye
        pygame.draw.circle(screen, BLACK, (int(screen_x + 10), int(self.y - 6)), 1)
    
    def draw_deer(self, screen, screen_x):
        # Body
        pygame.draw.ellipse(screen, (139, 69, 19), (screen_x - 17, self.y - 15, 35, 25))
        # Head
        pygame.draw.circle(screen, (160, 82, 45), (int(screen_x + 15), int(self.y - 15)), 10)
        # Antlers
        pygame.draw.line(screen, (101, 67, 33), (screen_x + 12, self.y - 22), (screen_x + 8, self.y - 30), 3)
        pygame.draw.line(screen, (101, 67, 33), (screen_x + 18, self.y - 22), (screen_x + 22, self.y - 30), 3)
        pygame.draw.line(screen, (101, 67, 33), (screen_x + 10, self.y - 28), (screen_x + 6, self.y - 32), 2)
        pygame.draw.line(screen, (101, 67, 33), (screen_x + 20, self.y - 28), (screen_x + 24, self.y - 32), 2)
        # Legs
        for leg_x in [screen_x - 10, screen_x - 2, screen_x + 6, screen_x + 14]:
            pygame.draw.rect(screen, (139, 69, 19), (leg_x - 1, self.y + 5, 2, 15))
        # Eye
        pygame.draw.circle(screen, BLACK, (int(screen_x + 18), int(self.y - 17)), 2)
        # Tail
        pygame.draw.circle(screen, WHITE, (int(screen_x - 17), int(self.y - 5)), 4)

class Obstacle:

class Animal:
    def __init__(self, x, y, animal_type):
        self.x = x
        self.y = y
        self.type = animal_type
        self.animation_frame = 0
        self.direction = random.choice([-1, 1])
        self.speed = random.uniform(0.5, 2.0)
        
        if animal_type == "elephant":
            self.width, self.height = 60, 40
        elif animal_type == "monkey":
            self.width, self.height = 25, 30
        elif animal_type == "tiger":
            self.width, self.height = 50, 30
        elif animal_type == "bird":
            self.width, self.height = 20, 15
        else:  # deer
            self.width, self.height = 35, 35
    
    def update(self):
        self.animation_frame += 0.1
        # Simple movement for some animals
        if self.type in ["monkey", "bird"]:
            self.x += self.direction * self.speed
            if random.randint(0, 200) == 0:  # Change direction occasionally
                self.direction *= -1
    
    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        if -100 < screen_x < SCREEN_WIDTH + 100:  # Only draw if on screen
            if self.type == "elephant":
                self.draw_elephant(screen, screen_x)
            elif self.type == "monkey":
                self.draw_monkey(screen, screen_x)
            elif self.type == "tiger":
                self.draw_tiger(screen, screen_x)
            elif self.type == "bird":
                self.draw_bird(screen, screen_x)
            else:  # deer
                self.draw_deer(screen, screen_x)
    
    def draw_elephant(self, screen, screen_x):
        # Body
        pygame.draw.ellipse(screen, (105, 105, 105), (screen_x - 30, self.y - 20, 60, 40))
        # Head
        pygame.draw.circle(screen, (105, 105, 105), (int(screen_x - 35), int(self.y - 10)), 20)
        # Trunk
        trunk_points = [(screen_x - 50, self.y - 5), (screen_x - 60, self.y + 5), (screen_x - 55, self.y + 15)]
        pygame.draw.lines(screen, (105, 105, 105), False, trunk_points, 8)
        # Legs
        for leg_x in [screen_x - 20, screen_x - 10, screen_x + 10, screen_x + 20]:
            pygame.draw.rect(screen, (90, 90, 90), (leg_x - 3, self.y + 15, 6, 15))
        # Eye
        pygame.draw.circle(screen, BLACK, (int(screen_x - 40), int(self.y - 15)), 3)
    
    def draw_monkey(self, screen, screen_x):
        # Body
        pygame.draw.ellipse(screen, (139, 69, 19), (screen_x - 12, self.y - 15, 25, 30))
        # Head
        pygame.draw.circle(screen, (160, 82, 45), (int(screen_x), int(self.y - 20)), 12)
        # Arms (animated)
        arm_offset = math.sin(self.animation_frame) * 5
        pygame.draw.line(screen, (139, 69, 19), (screen_x - 8, self.y - 10), (screen_x - 15, self.y - 5 + arm_offset), 4)
        pygame.draw.line(screen, (139, 69, 19), (screen_x + 8, self.y - 10), (screen_x + 15, self.y - 5 - arm_offset), 4)
        # Legs
        pygame.draw.line(screen, (139, 69, 19), (screen_x - 5, self.y + 10), (screen_x - 8, self.y + 20), 4)
        pygame.draw.line(screen, (139, 69, 19), (screen_x + 5, self.y + 10), (screen_x + 8, self.y + 20), 4)
        # Face
        pygame.draw.circle(screen, BLACK, (int(screen_x - 4), int(self.y - 22)), 2)
        pygame.draw.circle(screen, BLACK, (int(screen_x + 4), int(self.y - 22)), 2)
        pygame.draw.circle(screen, BLACK, (int(screen_x), int(self.y - 18)), 1)
    
    def draw_tiger(self, screen, screen_x):
        # Body
        pygame.draw.ellipse(screen, (255, 140, 0), (screen_x - 25, self.y - 15, 50, 30))
        # Head
        pygame.draw.circle(screen, (255, 140, 0), (int(screen_x + 20), int(self.y - 10)), 15)
        # Stripes
        for stripe_x in [screen_x - 15, screen_x - 5, screen_x + 5, screen_x + 15]:
            pygame.draw.line(screen, BLACK, (stripe_x, self.y - 12), (stripe_x, self.y + 8), 2)
        # Legs
        for leg_x in [screen_x - 15, screen_x - 5, screen_x + 5, screen_x + 15]:
            pygame.draw.rect(screen, (255, 140, 0), (leg_x - 2, self.y + 10, 4, 12))
        # Ears
        pygame.draw.polygon(screen, (255, 140, 0), [(screen_x + 15, self.y - 20), (screen_x + 20, self.y - 25), (screen_x + 25, self.y - 20)])
        pygame.draw.polygon(screen, (255, 140, 0), [(screen_x + 20, self.y - 20), (screen_x + 25, self.y - 25), (screen_x + 30, self.y - 20)])
        # Eyes
        pygame.draw.circle(screen, BLACK, (int(screen_x + 18), int(self.y - 12)), 2)
        pygame.draw.circle(screen, BLACK, (int(screen_x + 22), int(self.y - 12)), 2)
    
    def draw_bird(self, screen, screen_x):
        # Body
        pygame.draw.ellipse(screen, (255, 0, 0), (screen_x - 10, self.y - 8, 20, 15))
        # Wing (animated)
        wing_flap = math.sin(self.animation_frame * 3) * 8
        pygame.draw.ellipse(screen, (200, 0, 0), (screen_x - 5, self.y - 12 + wing_flap, 15, 8))
        # Head
        pygame.draw.circle(screen, (255, 0, 0), (int(screen_x + 8), int(self.y - 5)), 6)
        # Beak
        pygame.draw.polygon(screen, YELLOW, [(screen_x + 12, self.y - 5), (screen_x + 18, self.y - 3), (screen_x + 12, self.y - 1)])
        # Eye
        pygame.draw.circle(screen, BLACK, (int(screen_x + 10), int(self.y - 6)), 1)
    
    def draw_deer(self, screen, screen_x):
        # Body
        pygame.draw.ellipse(screen, (139, 69, 19), (screen_x - 17, self.y - 15, 35, 25))
        # Head
        pygame.draw.circle(screen, (160, 82, 45), (int(screen_x + 15), int(self.y - 15)), 10)
        # Antlers
        pygame.draw.line(screen, (101, 67, 33), (screen_x + 12, self.y - 22), (screen_x + 8, self.y - 30), 3)
        pygame.draw.line(screen, (101, 67, 33), (screen_x + 18, self.y - 22), (screen_x + 22, self.y - 30), 3)
        pygame.draw.line(screen, (101, 67, 33), (screen_x + 10, self.y - 28), (screen_x + 6, self.y - 32), 2)
        pygame.draw.line(screen, (101, 67, 33), (screen_x + 20, self.y - 28), (screen_x + 24, self.y - 32), 2)
        # Legs
        for leg_x in [screen_x - 10, screen_x - 2, screen_x + 6, screen_x + 14]:
            pygame.draw.rect(screen, (139, 69, 19), (leg_x - 1, self.y + 5, 2, 15))
        # Eye
        pygame.draw.circle(screen, BLACK, (int(screen_x + 18), int(self.y - 17)), 2)
        # Tail
        pygame.draw.circle(screen, WHITE, (int(screen_x - 17), int(self.y - 5)), 4)
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
                pygame.draw.ellipse(screen, GRAY, (screen_x - self.width//2, self.y - self.height//2, self.width, self.height))
            elif self.type == "tree":
                # Tree trunk
                pygame.draw.rect(screen, BROWN, (screen_x - 10, self.y - self.height//2, 20, self.height))
                # Tree leaves
                pygame.draw.circle(screen, DARK_GREEN, (int(screen_x), int(self.y - self.height//2)), 30)
            elif self.type == "log":
                pygame.draw.rect(screen, BROWN, (screen_x - self.width//2, self.y - self.height//2, self.width, self.height))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Offroad Jeep Adventure")
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.jeep = Jeep(100, SCREEN_HEIGHT - 200)
        self.camera_x = 0
        self.world_width = 5000  # Total world width
        self.finish_x = self.world_width - 200
        
        # Generate terrain
        self.terrain_height = self.generate_terrain()
        
        # Generate obstacles
        self.obstacles = self.generate_obstacles()
        
        # Generate animals
        self.animals = self.generate_animals()
        
        # Game state
        self.game_won = False
        self.game_over = False
        
    def generate_terrain(self):
        """Generate jungle terrain with hills leading to mountain"""
        terrain = []
        base_height = SCREEN_HEIGHT - 100
        
        for x in range(self.world_width):
            # Create hills and valleys
            hill_factor = math.sin(x * 0.01) * 50
            # Mountain at the end
            if x > self.world_width * 0.8:
                mountain_factor = ((x - self.world_width * 0.8) / (self.world_width * 0.2)) * 200
                height = base_height - hill_factor - mountain_factor
            else:
                height = base_height - hill_factor
            
            terrain.append(max(100, height))  # Minimum height
        
        return terrain
    
    def generate_obstacles(self):
        """Generate jungle obstacles"""
        obstacles = []
        
        for i in range(200, self.world_width - 200, 100):
            if random.random() < 0.7:  # 70% chance of obstacle
                obstacle_type = random.choice(["rock", "tree", "log"])
                
                if obstacle_type == "rock":
                    width, height = random.randint(30, 60), random.randint(20, 40)
                elif obstacle_type == "tree":
                    width, height = 40, random.randint(80, 120)
                else:  # log
                    width, height = random.randint(60, 100), 25
                
                x = i + random.randint(-30, 30)
                y = self.terrain_height[x] - height//2
                
                obstacles.append(Obstacle(x, y, width, height, obstacle_type))
        
        return obstacles
    
    def generate_animals(self):
        """Generate jungle animals for background"""
        animals = []
        animal_types = ["elephant", "monkey", "tiger", "bird", "deer"]
        
        for i in range(100, self.world_width - 100, 150):
            if random.random() < 0.4:  # 40% chance of animal
                animal_type = random.choice(animal_types)
                x = i + random.randint(-50, 50)
                
                # Position animals in background (further from path)
                if random.choice([True, False]):
                    y = self.terrain_height[x] - 100 - random.randint(20, 80)  # Above ground
                else:
                    y = self.terrain_height[x] - random.randint(10, 30)  # On ground
                
                animals.append(Animal(x, y, animal_type))
        
        return animals
    
    def update_camera(self):
        """Update camera to follow jeep"""
        target_x = self.jeep.x - SCREEN_WIDTH // 3
        self.camera_x = max(0, min(target_x, self.world_width - SCREEN_WIDTH))
    
    def draw_terrain(self):
        """Draw jungle terrain"""
        # Draw ground
        ground_points = [(0, SCREEN_HEIGHT)]
        
        for x in range(int(self.camera_x), min(int(self.camera_x) + SCREEN_WIDTH + 1, len(self.terrain_height))):
            screen_x = x - self.camera_x
            ground_points.append((screen_x, self.terrain_height[x]))
        
        ground_points.append((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        if len(ground_points) > 2:
            pygame.draw.polygon(self.screen, GREEN, ground_points)
        
        # Draw jungle background elements
        for i in range(int(self.camera_x // 50), int((self.camera_x + SCREEN_WIDTH) // 50) + 1):
            x = i * 50
            if 0 <= x < self.world_width:
                screen_x = x - self.camera_x
                if random.randint(0, 3) == 0:  # Random jungle plants
                    pygame.draw.circle(self.screen, DARK_GREEN, (int(screen_x), int(self.terrain_height[x] - 20)), random.randint(10, 25))
    
    def draw_finish_line(self):
        """Draw the finish flag on the mountain"""
        flag_x = self.finish_x - self.camera_x
        if -100 < flag_x < SCREEN_WIDTH + 100:
            flag_y = self.terrain_height[self.finish_x] - 100
            
            # Flag pole
            pygame.draw.line(self.screen, BROWN, (flag_x, flag_y), (flag_x, flag_y + 80), 5)
            
            # Flag
            flag_points = [(flag_x, flag_y), (flag_x + 60, flag_y + 15), (flag_x, flag_y + 30)]
            pygame.draw.polygon(self.screen, YELLOW, flag_points)
            
            # "FINISH" text
            font = pygame.font.Font(None, 24)
            text = font.render("FINISH", True, BLACK)
            self.screen.blit(text, (flag_x - 20, flag_y - 30))
    
    def draw_hud(self):
        """Draw heads-up display"""
        font = pygame.font.Font(None, 36)
        
        # Health bar
        health_width = 200
        health_height = 20
        health_fill = (self.jeep.health / 100) * health_width
        pygame.draw.rect(self.screen, RED, (20, 20, health_fill, health_height))
        pygame.draw.rect(self.screen, WHITE, (20, 20, health_width, health_height), 2)
        health_text = font.render(f"Health: {int(self.jeep.health)}", True, WHITE)
        self.screen.blit(health_text, (20, 50))
        
        # Fuel bar
        fuel_fill = (self.jeep.fuel / 100) * health_width
        pygame.draw.rect(self.screen, BLUE, (20, 80, fuel_fill, health_height))
        pygame.draw.rect(self.screen, WHITE, (20, 80, health_width, health_height), 2)
        fuel_text = font.render(f"Fuel: {int(self.jeep.fuel)}", True, WHITE)
        self.screen.blit(fuel_text, (20, 110))
        
        # Distance to finish
        distance = max(0, self.finish_x - self.jeep.x)
        distance_text = font.render(f"Distance to Finish: {int(distance)}m", True, WHITE)
        self.screen.blit(distance_text, (SCREEN_WIDTH - 300, 20))
        
        # Speed
        current_speed = abs(self.jeep.velocity_x)
        speed_text = font.render(f"Speed: {int(current_speed * 10)} mph", True, WHITE)
        self.screen.blit(speed_text, (SCREEN_WIDTH - 200, 50))
        
        # Controls instruction
        instructions_font = pygame.font.Font(None, 24)
        controls_text = instructions_font.render("↑Jump  →Accelerate  ←Reverse  ↓Fast Descent", True, WHITE)
        self.screen.blit(controls_text, (20, SCREEN_HEIGHT - 30))
    
    def check_win_condition(self):
        """Check if player reached the finish line"""
        if abs(self.jeep.x - self.finish_x) < 50:
            self.game_won = True
    
    def check_game_over(self):
        """Check game over conditions"""
        if self.jeep.health <= 0 or self.jeep.fuel <= 0:
            self.game_over = True
    
    def draw_game_over_screen(self):
        """Draw game over or victory screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        
        if self.game_won:
            title_text = font_large.render("VICTORY!", True, YELLOW)
            subtitle_text = font_medium.render("You reached the mountain top!", True, WHITE)
        else:
            title_text = font_large.render("GAME OVER", True, RED)
            if self.jeep.health <= 0:
                subtitle_text = font_medium.render("Your jeep was destroyed!", True, WHITE)
            else:
                subtitle_text = font_medium.render("You ran out of fuel!", True, WHITE)
        
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        
        self.screen.blit(title_text, title_rect)
        self.screen.blit(subtitle_text, subtitle_rect)
        
        restart_text = font_medium.render("Press R to Restart or Q to Quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
        self.screen.blit(restart_text, restart_rect)
    
    def reset_game(self):
        """Reset game to initial state"""
        self.jeep = Jeep(100, SCREEN_HEIGHT - 200)
        self.camera_x = 0
        self.game_won = False
        self.game_over = False
        # Regenerate animals for variety
        self.animals = self.generate_animals()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_r and (self.game_over or self.game_won):
                        self.reset_game()
            
            if not self.game_over and not self.game_won:
                # Get pressed keys
                keys_pressed = pygame.key.get_pressed()
                
                # Update game objects
                self.jeep.update(keys_pressed, self.obstacles, self.terrain_height)
                self.update_camera()
                
                # Update animals
                for animal in self.animals:
                    animal.update()
                
                # Check win/lose conditions
                self.check_win_condition()
                self.check_game_over()
            
            # Draw everything
            self.screen.fill(GREEN)  # Sky color
            
            self.draw_terrain()
            
            # Draw animals (in background)
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
