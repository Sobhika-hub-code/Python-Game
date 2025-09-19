
import pygame
import random
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Brick Breaker")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Background Images
start_background = pygame.image.load('start.png')
game_background = pygame.image.load('playgame.png')
game_over_background = pygame.image.load('gameover.png')

paddle_width = 100
paddle_height = 20
paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 30, paddle_width, paddle_height)


paddle_speed = 5

# Ball
ball_radius = 12
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_radius * 2, ball_radius * 2)
ball_speed_x = 2
ball_speed_y = -2

# Bricks
brick_height = 20
brick_padding = 10
bricks = []
brick_strength = {}

# Score and Lives
score = 0
lives = 3
attempts = 3
high_score = 0
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())

# Font
font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 72)

# Game state
game_started = False
game_over = False
paused = False

def calculate_bricks():
    global bricks, brick_strength
    bricks.clear()
    brick_strength.clear()
    brick_cols = max(8, WIDTH // (brick_height + brick_padding))
    brick_width = (WIDTH - (brick_cols + 1) * brick_padding) // brick_cols
    brick_rows = 6

    for row in range(brick_rows):
        for col in range(brick_cols):
            brick = pygame.Rect(col * (brick_width + brick_padding) + brick_padding, row * (brick_height + brick_padding) + 50, brick_width, brick_height)
            bricks.append((brick, (row, col)))
            brick_strength[(row, col)] = random.randint(1, 3)

def draw_objects():
    # Draw Backgrounds
    if not game_started and not game_over:
        screen.blit(start_background, (0, 0))
        title_text = title_font.render("Brick Breaker", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 150))
    elif game_over:
        screen.blit(game_over_background, (0, 0))
    else:
        screen.blit(game_background, (0, 0))

    if not game_started and not game_over:
        start_button = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2, 160, 50)
        pygame.draw.rect(screen, GREEN, start_button)
        button_text = font.render("Start Game", True, WHITE)
        screen.blit(button_text, (WIDTH // 2 - button_text.get_width() // 2, HEIGHT // 2 + 10))
        return start_button

    if game_over:
        game_over_text = font.render(f"Game Over! Score: {score}", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        restart_button = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2, 160, 50)
        pygame.draw.rect(screen, RED, restart_button)
        button_text = font.render("Restart", True, WHITE)
        screen.blit(button_text, (WIDTH // 2 - button_text.get_width() // 2, HEIGHT // 2 + 10))
        return restart_button

    pause_button = pygame.Rect(WIDTH // 2 + 90, 10, 100, 40)
    pygame.draw.rect(screen, RED if paused else GREEN, pause_button)
    button_text = font.render("Continue" if paused else "Pause", True, WHITE)
    screen.blit(button_text, (WIDTH // 2 + 105, 20))

    pygame.draw.rect(screen, (0, 0, 0), paddle)

    if lives > 0:
        pygame.draw.ellipse(screen, RED, ball)

    for brick, (row, col) in bricks:
        color = RED if brick_strength[(row, col)] == 1 else (YELLOW if brick_strength[(row, col)] == 2 else GREEN)
        pygame.draw.rect(screen, color, brick)
    
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(high_score_text, (WIDTH // 2 - 130, 10))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 150, 10))

    return pause_button

calculate_bricks()
running = True

while running:
    pygame.time.delay(15)
    button_rect = draw_objects()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect and button_rect.collidepoint(event.pos):
                if not game_started and not game_over:
                    game_started = True
                elif game_over:
                    game_started = False
                    game_over = False
                    lives = 3
                    score = 0
                    calculate_bricks()
                else:
                    paused = not paused

    if not game_started or paused or game_over:
        pygame.display.flip()
        continue

    # Paddle Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    # Ball Movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x *= -1
    if ball.top <= 0:
        ball_speed_y *= -1

    if ball.colliderect(paddle):
        ball_speed_y *= -1

    for brick, (row, col) in bricks[:]:
        if ball.colliderect(brick):
            if brick_strength[(row, col)] > 1:
                brick_strength[(row, col)] -= 1
            else:
                bricks.remove((brick, (row, col)))
                score += 10
            ball_speed_y *= -1

    if ball.bottom >= HEIGHT:
        lives -= 1
        if lives <= 0:
            game_over = True
            if score > high_score:
                with open("highscore.txt", "w") as file:
                    file.write(str(score))
        else:
            ball.x, ball.y = WIDTH // 2, HEIGHT // 2
            ball_speed_y *= -1

    pygame.display.flip()

pygame.quit()