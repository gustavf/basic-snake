import pygame
import os

# Create simple images for the game

# Initialize pygame
pygame.init()

# Create the directory if it doesn't exist
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create a surface for head_up
head_up = pygame.Surface((40, 40))
head_up.fill((50, 168, 82))  # Green color for the snake
pygame.draw.circle(head_up, (0, 0, 0), (10, 15), 3)  # Left eye
pygame.draw.circle(head_up, (0, 0, 0), (30, 15), 3)  # Right eye
pygame.image.save(head_up, "head_up.png")

# Create a surface for head_down
head_down = pygame.Surface((40, 40))
head_down.fill((50, 168, 82))
pygame.draw.circle(head_down, (0, 0, 0), (10, 25), 3)  # Left eye
pygame.draw.circle(head_down, (0, 0, 0), (30, 25), 3)  # Right eye
pygame.image.save(head_down, "head_down.png")

# Create a surface for head_left
head_left = pygame.Surface((40, 40))
head_left.fill((50, 168, 82))
pygame.draw.circle(head_left, (0, 0, 0), (15, 10), 3)  # Upper eye
pygame.draw.circle(head_left, (0, 0, 0), (15, 30), 3)  # Lower eye
pygame.image.save(head_left, "head_left.png")

# Create a surface for head_right
head_right = pygame.Surface((40, 40))
head_right.fill((50, 168, 82))
pygame.draw.circle(head_right, (0, 0, 0), (25, 10), 3)  # Upper eye
pygame.draw.circle(head_right, (0, 0, 0), (25, 30), 3)  # Lower eye
pygame.image.save(head_right, "head_right.png")

# Create a surface for apple
apple = pygame.Surface((40, 40), pygame.SRCALPHA)
apple.fill((0, 0, 0, 0))  # Transparent background
pygame.draw.circle(apple, (255, 0, 0), (20, 20), 15)  # Red apple
pygame.draw.line(apple, (101, 67, 33), (20, 5), (20, 12), 2)  # Brown stem
pygame.draw.ellipse(apple, (0, 100, 0), (15, 5, 10, 5))  # Green leaf
pygame.image.save(apple, "apple.png")

print("Images created successfully!")