#!/usr/bin/env python3
"""
Simple Pacman Game for Mac Desktop
A basic Pacman-style game using Pygame
"""

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors - Grayscale theme
BLACK = (0, 0, 0)  # Background
PACMAN_YELLOW = (200, 200, 200)  # Light gray for Pac-Man
WALL_BLUE = (60, 60, 60)  # Dark gray for walls
WHITE = (255, 255, 255)  # White for dots and text
GHOST_RED = (180, 180, 180)  # Medium-light gray for ghost 1 (Blinky)
GHOST_CYAN = (160, 160, 160)  # Medium gray for ghost 2 (Inky)
GHOST_PINK = (140, 140, 140)  # Medium-dark gray for ghost 3 (Pinky)
GHOST_ORANGE = (120, 120, 120)  # Gray for ghost 4 (Clyde)
VULNERABLE_BLUE = (80, 80, 80)  # Dark gray for vulnerable ghosts
VULNERABLE_WHITE = (220, 220, 220)  # Light gray for flashing vulnerable ghosts
POWER_PELLET_COLOR = (190, 190, 190)  # Light gray for power pellets
TIMER_GREEN = (150, 150, 150)  # Medium gray for timer (high)
TIMER_YELLOW = (130, 130, 130)  # Medium-dark gray for timer (medium)
TIMER_RED = (110, 110, 110)  # Dark gray for timer (low)
GAME_OVER_RED = (100, 100, 100)  # Dark gray for game over text
WIN_GREEN = (170, 170, 170)  # Medium-light gray for win text

# Game settings
PACMAN_SIZE = 20
GHOST_SIZE = 20
DOT_SIZE = 4
POWER_PELLET_SIZE = 8
WALL_SIZE = 20
PACMAN_SPEED = 3
POWER_PELLET_DURATION = 300  # Duration in frames (5 seconds at 60 FPS)

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 'RIGHT'
        self.next_direction = 'RIGHT'
        
    def update(self, maze):
        # Try to change direction if possible
        new_x, new_y = self.x, self.y
        
        if self.next_direction == 'UP':
            new_y -= PACMAN_SPEED
        elif self.next_direction == 'DOWN':
            new_y += PACMAN_SPEED
        elif self.next_direction == 'LEFT':
            new_x -= PACMAN_SPEED
        elif self.next_direction == 'RIGHT':
            new_x += PACMAN_SPEED
            
        # Check if new direction is valid
        if not self.check_wall_collision(new_x, new_y, maze):
            self.direction = self.next_direction
            self.x, self.y = new_x, new_y
        else:
            # Continue in current direction if possible
            if self.direction == 'UP':
                new_y = self.y - PACMAN_SPEED
            elif self.direction == 'DOWN':
                new_y = self.y + PACMAN_SPEED
            elif self.direction == 'LEFT':
                new_x = self.x - PACMAN_SPEED
            elif self.direction == 'RIGHT':
                new_x = self.x + PACMAN_SPEED
                
            if not self.check_wall_collision(new_x, new_y, maze):
                self.x, self.y = new_x, new_y
                
        # Keep Pacman within screen bounds
        self.x = max(PACMAN_SIZE//2, min(WINDOW_WIDTH - PACMAN_SIZE//2, self.x))
        self.y = max(PACMAN_SIZE//2, min(WINDOW_HEIGHT - PACMAN_SIZE//2, self.y))
    
    def check_wall_collision(self, x, y, maze):
        # Simple collision detection with maze walls
        maze_x = x // WALL_SIZE
        maze_y = y // WALL_SIZE
        
        if 0 <= maze_y < len(maze) and 0 <= maze_x < len(maze[0]):
            return maze[maze_y][maze_x] == 1
        return True
    
    def draw(self, screen):
        pygame.draw.circle(screen, PACMAN_YELLOW, (int(self.x), int(self.y)), PACMAN_SIZE)
        
        # Draw simple mouth based on direction
        mouth_points = []
        if self.direction == 'RIGHT':
            mouth_points = [(self.x, self.y), (self.x + PACMAN_SIZE//2, self.y - PACMAN_SIZE//3), 
                           (self.x + PACMAN_SIZE//2, self.y + PACMAN_SIZE//3)]
        elif self.direction == 'LEFT':
            mouth_points = [(self.x, self.y), (self.x - PACMAN_SIZE//2, self.y - PACMAN_SIZE//3), 
                           (self.x - PACMAN_SIZE//2, self.y + PACMAN_SIZE//3)]
        elif self.direction == 'UP':
            mouth_points = [(self.x, self.y), (self.x - PACMAN_SIZE//3, self.y - PACMAN_SIZE//2), 
                           (self.x + PACMAN_SIZE//3, self.y - PACMAN_SIZE//2)]
        elif self.direction == 'DOWN':
            mouth_points = [(self.x, self.y), (self.x - PACMAN_SIZE//3, self.y + PACMAN_SIZE//2), 
                           (self.x + PACMAN_SIZE//3, self.y + PACMAN_SIZE//2)]
        
        if mouth_points:
            pygame.draw.polygon(screen, BLACK, mouth_points)

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.original_color = color
        self.color = color
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.speed = 2
        self.vulnerable = False
        self.vulnerable_timer = 0
        self.respawn_timer = 0
        self.eaten = False
        
    def update(self, maze, power_pellet_active=False, power_pellet_timer=0):
        # Handle vulnerability state
        if power_pellet_active and not self.eaten:
            self.vulnerable = True
            self.vulnerable_timer = power_pellet_timer
            # Make ghost blue when vulnerable, flashing white when timer is low
            if power_pellet_timer < 60 and (power_pellet_timer // 10) % 2:  # Flash in last second
                self.color = VULNERABLE_WHITE
            else:
                self.color = VULNERABLE_BLUE
        else:
            self.vulnerable = False
            self.color = self.original_color
            
        # Handle respawn after being eaten
        if self.eaten:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.eaten = False
                self.vulnerable = False
                # Return to ghost house area (randomized position)
                self.x = 300 + random.randint(0, 9) * 20
                self.y = 220 + random.randint(0, 4) * 20
                self.color = self.original_color
            return  # Don't move while respawning
            
        # Simple AI: change direction randomly sometimes
        if random.randint(1, 30) == 1:
            self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
            
        new_x, new_y = self.x, self.y
        
        # Slow down when vulnerable
        current_speed = self.speed * 0.5 if self.vulnerable else self.speed
        
        if self.direction == 'UP':
            new_y -= current_speed
        elif self.direction == 'DOWN':
            new_y += current_speed
        elif self.direction == 'LEFT':
            new_x -= current_speed
        elif self.direction == 'RIGHT':
            new_x += current_speed
            
        # Check wall collision
        if not self.check_wall_collision(new_x, new_y, maze):
            self.x, self.y = new_x, new_y
        else:
            # Change direction if hit wall
            self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
            
        # Keep ghost within screen bounds
        self.x = max(GHOST_SIZE//2, min(WINDOW_WIDTH - GHOST_SIZE//2, self.x))
        self.y = max(GHOST_SIZE//2, min(WINDOW_HEIGHT - GHOST_SIZE//2, self.y))
    
    def check_wall_collision(self, x, y, maze):
        maze_x = x // WALL_SIZE
        maze_y = y // WALL_SIZE
        
        if 0 <= maze_y < len(maze) and 0 <= maze_x < len(maze[0]):
            return maze[maze_y][maze_x] == 1
        return True
    
    def draw(self, screen):
        if self.eaten and self.respawn_timer > 0:
            # Draw ghost eyes only when eaten
            pygame.draw.circle(screen, WHITE, (int(self.x - 6), int(self.y - 6)), 4)
            pygame.draw.circle(screen, WHITE, (int(self.x + 6), int(self.y - 6)), 4)
            pygame.draw.circle(screen, BLACK, (int(self.x - 6), int(self.y - 6)), 2)
            pygame.draw.circle(screen, BLACK, (int(self.x + 6), int(self.y - 6)), 2)
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), GHOST_SIZE)
            # Draw eyes
            pygame.draw.circle(screen, WHITE, (int(self.x - 6), int(self.y - 6)), 4)
            pygame.draw.circle(screen, WHITE, (int(self.x + 6), int(self.y - 6)), 4)
            pygame.draw.circle(screen, BLACK, (int(self.x - 6), int(self.y - 6)), 2)
            pygame.draw.circle(screen, BLACK, (int(self.x + 6), int(self.y - 6)), 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Simple Pacman Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.lives = 3
        self.power_pellet_timer = 0
        self.ghost_eat_score = 200  # Base score for eating ghosts
        
        # Simple maze (1 = wall, 0 = empty, 2 = dot, 3 = power pellet)
        self.maze = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
            [1,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,1],
            [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
            [1,2,2,2,2,2,2,1,1,2,2,2,2,2,2,1,1,1,1,2,2,2,1,1,1,1,2,2,2,2,2,1,1,2,2,2,2,2,2,1],
            [1,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,1,2,2,2,1,1,1,1,2,1,1,1,1,1,1,2,1,1,1,1,1,1],
            [0,0,0,0,0,1,2,1,1,1,1,1,1,1,2,1,1,1,1,2,2,2,1,1,1,1,2,1,1,1,1,1,1,2,1,0,0,0,0,0],
            [1,1,1,1,1,1,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,2,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,1,2,1,1,1,1,1,1,1],
            [2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,2],
            [1,1,1,1,1,1,2,1,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,1,2,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,1,2,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,1,2,2,2,1,1,1,1,2,1,1,1,1,1,1,2,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,2,2,2,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,2,1],
            [1,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,1],
            [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
            [1,2,2,2,2,2,2,1,1,2,2,2,2,2,2,1,1,1,1,2,2,2,1,1,1,1,2,2,2,2,2,1,1,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,2,2,2,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,2,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
            [1,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
        
        # Initialize game objects
        self.pacman = Pacman(40, 40)

        # Create 4 ghosts with varied colors and spawn positions
        ghost_colors = [GHOST_RED, GHOST_CYAN, GHOST_PINK, GHOST_ORANGE]
        self.ghosts = []

        # Ghost house center area
        ghost_positions = [
            (360, 240),
            (400, 240),
            (360, 280),
            (400, 280)
        ]

        for i in range(4):
            color = ghost_colors[i]
            x, y = ghost_positions[i]
            self.ghosts.append(Ghost(x, y, color))
        
        # Count total dots (including power pellets)
        self.total_dots = sum(row.count(2) + row.count(3) for row in self.maze)
        
        # Font for UI
        self.font = pygame.font.Font(None, 36)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.pacman.next_direction = 'UP'
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.pacman.next_direction = 'DOWN'
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.pacman.next_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.pacman.next_direction = 'RIGHT'
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        self.pacman.update(self.maze)
        
        # Update power pellet timer
        if self.power_pellet_timer > 0:
            self.power_pellet_timer -= 1
        
        for ghost in self.ghosts:
            ghost.update(self.maze, self.power_pellet_timer > 0, self.power_pellet_timer)
        
        # Check dot and power pellet collection
        maze_x = self.pacman.x // WALL_SIZE
        maze_y = self.pacman.y // WALL_SIZE
        
        if (0 <= maze_y < len(self.maze) and 0 <= maze_x < len(self.maze[0])):
            if self.maze[maze_y][maze_x] == 2:  # Regular dot
                self.maze[maze_y][maze_x] = 0
                self.score += 10
            elif self.maze[maze_y][maze_x] == 3:  # Power pellet
                self.maze[maze_y][maze_x] = 0
                self.score += 50
                self.power_pellet_timer = POWER_PELLET_DURATION
                # Reset ghost eat score multiplier
                self.ghost_eat_score = 200
        
        # Check ghost collision
        for ghost in self.ghosts:
            if ghost.eaten:
                continue
                
            distance = ((self.pacman.x - ghost.x) ** 2 + (self.pacman.y - ghost.y) ** 2) ** 0.5
            if distance < PACMAN_SIZE + GHOST_SIZE - 10:
                if ghost.vulnerable and self.power_pellet_timer > 0:
                    # Eat the ghost
                    ghost.eaten = True
                    ghost.respawn_timer = 180  # 3 seconds at 60 FPS
                    self.score += self.ghost_eat_score
                    self.ghost_eat_score *= 2  # Double the score for each subsequent ghost
                else:
                    # Ghost catches Pacman
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over()
                    else:
                        # Reset positions
                        self.pacman.x, self.pacman.y = 40, 40
                        # Reset ghosts to their spawn positions
                        ghost_positions = [
                            (360, 240),
                            (400, 240),
                            (360, 280),
                            (400, 280)
                        ]
                        for i, g in enumerate(self.ghosts):
                            g.x, g.y = ghost_positions[i]
                            g.eaten = False
                            g.vulnerable = False
                            g.respawn_timer = 0
                        # Clear power pellet effect
                        self.power_pellet_timer = 0
        
        # Check win condition
        current_dots = sum(row.count(2) + row.count(3) for row in self.maze)
        if current_dots == 0:
            self.win_game()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw maze
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                pixel_x = x * WALL_SIZE
                pixel_y = y * WALL_SIZE
                
                if cell == 1:  # Wall
                    pygame.draw.rect(self.screen, WALL_BLUE,
                                   (pixel_x, pixel_y, WALL_SIZE, WALL_SIZE))
                elif cell == 2:  # Dot
                    pygame.draw.circle(self.screen, WHITE,
                                     (pixel_x + WALL_SIZE//2, pixel_y + WALL_SIZE//2), DOT_SIZE)
                elif cell == 3:  # Power pellet
                    # Animate power pellet with pulsing effect
                    pulse = abs(pygame.time.get_ticks() // 200 % 2)
                    size = POWER_PELLET_SIZE + pulse * 2
                    pygame.draw.circle(self.screen, POWER_PELLET_COLOR,
                                     (pixel_x + WALL_SIZE//2, pixel_y + WALL_SIZE//2), size)
        
        # Draw game objects
        self.pacman.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        
        # Draw power pellet timer
        if self.power_pellet_timer > 0:
            timer_seconds = self.power_pellet_timer // 60 + 1
            power_text = self.font.render(f"POWER TIME: {timer_seconds}", True, TIMER_GREEN)
            self.screen.blit(power_text, (10, 90))

            # Draw power pellet indicator bar
            bar_width = 200
            bar_height = 10
            bar_x = 10
            bar_y = 120

            # Background bar
            pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height))

            # Progress bar
            progress = self.power_pellet_timer / POWER_PELLET_DURATION
            progress_width = int(bar_width * progress)

            # Color changes as time runs out (green -> yellow -> red)
            if progress > 0.5:
                bar_color = TIMER_GREEN
            elif progress > 0.2:
                bar_color = TIMER_YELLOW
            else:
                bar_color = TIMER_RED

            pygame.draw.rect(self.screen, bar_color, (bar_x, bar_y, progress_width, bar_height))
        
        # Draw instructions
        instruction_text = self.font.render("Use WASD or Arrow Keys to move, ESC to quit", True, WHITE)
        text_rect = instruction_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 30))
        self.screen.blit(instruction_text, text_rect)
        
        pygame.display.flip()
    
    def game_over(self):
        # Show game over screen
        self.screen.fill(BLACK)
        game_over_text = self.font.render("GAME OVER!", True, GAME_OVER_RED)
        final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.font.render("Press any key to quit", True, WHITE)
        
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(final_score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        
        # Wait for key press
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    waiting = False
                    self.running = False
    
    def win_game(self):
        # Show win screen
        self.screen.fill(BLACK)
        win_text = self.font.render("YOU WIN!", True, WIN_GREEN)
        final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.font.render("Press any key to quit", True, WHITE)
        
        win_rect = win_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
        
        self.screen.blit(win_text, win_rect)
        self.screen.blit(final_score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        
        # Wait for key press
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    waiting = False
                    self.running = False
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """Main function to start the game"""
    try:
        game = Game()
        game.run()
    except pygame.error as e:
        print(f"Pygame error: {e}")
        print("Make sure you have Pygame installed: pip install pygame")
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()