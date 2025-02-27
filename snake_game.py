import pygame
import random
import sys
from pygame.math import Vector2

# Initialize pygame
pygame.init()

# Constants
CELL_SIZE = 40
CELL_NUMBER = 15
SCREEN_WIDTH = CELL_SIZE * CELL_NUMBER
SCREEN_HEIGHT = CELL_SIZE * CELL_NUMBER

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SNAKE_COLOR = (50, 168, 82)
BACKGROUND_COLOR = (175, 215, 70)
GRID_COLOR = (167, 209, 61)

# Fonts
GAME_FONT = pygame.font.SysFont('comicsansms', 25)

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        
        # Load head images
        self.head_up = pygame.transform.scale(pygame.image.load('head_up.png'), (CELL_SIZE, CELL_SIZE))
        self.head_down = pygame.transform.scale(pygame.image.load('head_down.png'), (CELL_SIZE, CELL_SIZE))
        self.head_right = pygame.transform.scale(pygame.image.load('head_right.png'), (CELL_SIZE, CELL_SIZE))
        self.head_left = pygame.transform.scale(pygame.image.load('head_left.png'), (CELL_SIZE, CELL_SIZE))
        
    def draw(self, screen):
        # Draw the head with the appropriate direction
        head_rect = pygame.Rect(self.body[0].x * CELL_SIZE, self.body[0].y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        
        if self.direction == Vector2(0, -1):  # Up
            screen.blit(self.head_up, head_rect)
        elif self.direction == Vector2(0, 1):  # Down
            screen.blit(self.head_down, head_rect)
        elif self.direction == Vector2(1, 0):  # Right
            screen.blit(self.head_right, head_rect)
        else:  # Left
            screen.blit(self.head_left, head_rect)
            
        # Draw the rest of the body
        for i, block in enumerate(self.body[1:], 1):
            block_rect = pygame.Rect(block.x * CELL_SIZE, block.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, SNAKE_COLOR, block_rect)
            pygame.draw.rect(screen, GRID_COLOR, block_rect, 1)
            
    def move(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            
    def add_block(self):
        self.new_block = True
        
    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        
    def check_collision(self):
        # Check if snake hits wall
        if not 0 <= self.body[0].x < CELL_NUMBER or not 0 <= self.body[0].y < CELL_NUMBER:
            return True
            
        # Check if snake hits itself
        for block in self.body[1:]:
            if block == self.body[0]:
                return True
                
        return False
        
class Fruit:
    def __init__(self):
        self.randomize()
        self.apple = pygame.transform.scale(pygame.image.load('apple.png'), (CELL_SIZE, CELL_SIZE))
        
    def draw(self, screen):
        fruit_rect = pygame.Rect(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        screen.blit(self.apple, fruit_rect)
        
    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.score = 0
        self.game_over = False
        
    def update(self):
        if not self.game_over:
            self.snake.move()
            self.check_collision()
            self.check_fail()
        
    def draw_elements(self, screen):
        # Draw background grid
        for row in range(CELL_NUMBER):
            for col in range(CELL_NUMBER):
                cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if (row + col) % 2 == 0:
                    pygame.draw.rect(screen, BACKGROUND_COLOR, cell_rect)
                else:
                    pygame.draw.rect(screen, GRID_COLOR, cell_rect)
        
        self.fruit.draw(screen)
        self.snake.draw(screen)
        self.draw_score(screen)
        
        if self.game_over:
            self.draw_game_over(screen)
    
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.score += 1
            
            # Make sure fruit doesn't spawn on snake
            while self.fruit.pos in self.snake.body:
                self.fruit.randomize()
    
    def check_fail(self):
        if self.snake.check_collision():
            self.game_over = True
    
    def reset(self):
        self.snake.reset()
        self.fruit.randomize()
        self.score = 0
        self.game_over = False
    
    def draw_score(self, screen):
        score_text = GAME_FONT.render(f'Score: {self.score}', True, BLACK)
        screen.blit(score_text, (10, 10))
        
    def draw_game_over(self, screen):
        game_over_surface = GAME_FONT.render('GAME OVER!', True, RED)
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 30))
        
        restart_surface = GAME_FONT.render('Press SPACE to Restart', True, BLACK)
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 10))
        
        screen.blit(game_over_surface, game_over_rect)
        screen.blit(restart_surface, restart_rect)

def main():
    # Initialize screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')
    
    # Initialize clock
    clock = pygame.time.Clock()
    
    # Initialize game
    game = Game()
    
    # Create a custom event for snake movement
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)  # Snake moves every 150ms
    
    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == SCREEN_UPDATE:
                game.update()
                
            if event.type == pygame.KEYDOWN:
                if not game.game_over:
                    if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                        game.snake.direction = Vector2(0, -1)
                    elif event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                        game.snake.direction = Vector2(0, 1)
                    elif event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                        game.snake.direction = Vector2(1, 0)
                    elif event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                        game.snake.direction = Vector2(-1, 0)
                        
                if game.game_over and event.key == pygame.K_SPACE:
                    game.reset()
                    
        # Fill screen with background color
        screen.fill(BACKGROUND_COLOR)
        
        # Draw game elements
        game.draw_elements(screen)
        
        # Update display
        pygame.display.flip()
        
        # Limit frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()