import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
PACMAN_SIZE = 20
PACMAN_SPEED = 5
GHOST_SIZE = 20
GHOST_SPEED = 3
PILL_SIZE = 10
PILL_SPEED = 2

# Set up some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the fonts
font = pygame.font.Font(None, 36)

# Set up the game state
pacman_x, pacman_y = WIDTH / 2, HEIGHT / 2
pacman_dir = 'right'
pacman_speed = PACMAN_SPEED
ghost_x, ghost_y = random.randint(0, WIDTH - GHOST_SIZE), random.randint(0, HEIGHT - GHOST_SIZE)
pill_x, pill_y = random.randint(0, WIDTH - PILL_SIZE), random.randint(0, HEIGHT - PILL_SIZE)
score = 0

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and pacman_dir!= 'right':
                pacman_dir = 'left'
            elif event.key == pygame.K_RIGHT and pacman_dir!= 'left':
                pacman_dir = 'right'
            elif event.key == pygame.K_UP and pacman_dir!= 'down':
                pacman_dir = 'up'
            elif event.key == pygame.K_DOWN and pacman_dir!= 'up':
                pacman_dir = 'down'

    # Move the pacman
    if pacman_dir == 'left':
        pacman_x -= pacman_speed
    elif pacman_dir == 'right':
        pacman_x += pacman_speed
    elif pacman_dir == 'up':
        pacman_y -= pacman_speed
    elif pacman_dir == 'down':
        pacman_y += pacman_speed

    # Move the ghost
    if random.random() < 0.1:
        if pacman_x < ghost_x:
            ghost_x -= GHOST_SPEED
        elif pacman_x > ghost_x:
            ghost_x += GHOST_SPEED
        if pacman_y < ghost_y:
            ghost_y -= GHOST_SPEED
        elif pacman_y > ghost_y:
            ghost_y += GHOST_SPEED

    # Check for collisions
    if pacman_x < 0 or pacman_x > WIDTH - PACMAN_SIZE or pacman_y < 0 or pacman_y > HEIGHT - PACMAN_SIZE:
        pacman_x, pacman_y = WIDTH / 2, HEIGHT / 2
    if pacman_x < ghost_x < pacman_x + PACMAN_SIZE or pacman_x < ghost_x + GHOST_SIZE < pacman_x + PACMAN_SIZE:
        if pacman_y < ghost_y < pacman_y + PACMAN_SIZE or pacman_y < ghost_y + GHOST_SIZE < pacman_y + PACMAN_SIZE:
            print("Game Over")
            pygame.quit()
            sys.exit()
    if pacman_x < pill_x < pacman_x + PACMAN_SIZE or pacman_x < pill_x + PILL_SIZE < pacman_x + PACMAN_SIZE:
        if pacman_y < pill_y < pacman_y + PACMAN_SIZE or pacman_y < pill_y + PILL_SIZE < pacman_y + PACMAN_SIZE:
            score += 1
            pill_x, pill_y = random.randint(0, WIDTH - PILL_SIZE), random.randint(0, HEIGHT - PILL_SIZE)

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, YELLOW, (pacman_x, pacman_y, PACMAN_SIZE, PACMAN_SIZE))
    pygame.draw.rect(screen, RED, (ghost_x, ghost_y, GHOST_SIZE, GHOST_SIZE))
    pygame.draw.rect(screen, GREEN, (pill_x, pill_y, PILL_SIZE, PILL_SIZE))
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))
    pygame.display.flip()
    pygame.time.Clock().tick(60)