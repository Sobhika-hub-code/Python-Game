import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 1280, 700
BIRD_X = 50
BIRD_Y = HEIGHT // 2
BIRD_VELOCITY = 5
PIPE_GAP = 150
PIPE_WIDTH = 70
PIPE_VELOCITY = 3
GROUND_HEIGHT = 50

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Load Background Images
start_bg = pygame.image.load("D:/MiniProject/front.png")
start_bg = pygame.transform.scale(start_bg, (WIDTH, HEIGHT))

gameover_bg = pygame.image.load("D:/MiniProject/result.png")
gameover_bg = pygame.transform.scale(gameover_bg, (WIDTH, HEIGHT))

background_img = pygame.image.load("D:/MiniProject/background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Load Bird Image
bird_img = pygame.image.load("D:/MiniProject/bird.png")
bird_img = pygame.transform.scale(bird_img, (60, 40))

# Define Bird
class Bird:
    def __init__(self):
        self.x = BIRD_X
        self.y = BIRD_Y

    def move(self, keys):
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= BIRD_VELOCITY
        if keys[pygame.K_DOWN] and self.y < HEIGHT - GROUND_HEIGHT - 30:
            self.y += BIRD_VELOCITY
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= BIRD_VELOCITY
        if keys[pygame.K_RIGHT] and self.x < WIDTH - 40:
            self.x += BIRD_VELOCITY

    def draw(self, screen):
        screen.blit(bird_img, (self.x, self.y))

# Define Pipe
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(100, 400)
        self.passed = False

    def update(self):
        self.x -= PIPE_VELOCITY

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP - GROUND_HEIGHT))

# Show Start Screen
def show_start_screen():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird - Start")

    font = pygame.font.Font(None, 48)
    title_text = font.render("Flappy Bird", True, RED)
    start_text = font.render("Start", True, WHITE)

    button_x, button_y, button_w, button_h = WIDTH // 2 - 50, HEIGHT // 2, 100, 50

    while True:
        screen.blit(start_bg, (0, 0))
        screen.blit(title_text, (WIDTH // 2 - 100, HEIGHT // 2 - 100))
        pygame.draw.rect(screen, RED, (button_x, button_y, button_w, button_h))
        screen.blit(start_text, (button_x + 25, button_y + 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if button_x < mouse_x < button_x + button_w and button_y < mouse_y < button_y + button_h:
                    return

# Show Restart Screen
def show_restart_screen(score):
    restart_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Over")

    font = pygame.font.Font(None, 48)
    score_text = font.render(f"Your Score: {score}", True, RED)
    restart_text = font.render("Restart", True, WHITE)

    button_x, button_y, button_w, button_h = WIDTH // 2 - 50, HEIGHT // 2, 100, 50

    while True:
        restart_screen.blit(gameover_bg, (0, 0))
        restart_screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2 - 100))
        pygame.draw.rect(restart_screen, RED, (button_x, button_y, button_w, button_h))
        restart_screen.blit(restart_text, (button_x + 20, button_y + 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if button_x < mouse_x < button_x + button_w and button_y < mouse_y < button_y + button_h:
                    main()

# Game Loop
def game_loop():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird - User Controlled")

    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    game_over = False

    while True:
        screen.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if game_over:
            show_restart_screen(score)
            return

        bird.move(keys)
        bird.draw(screen)

        if pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe())

        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                score += 1
            if (bird.x < pipe.x + PIPE_WIDTH and bird.x + 40 > pipe.x and (bird.y < pipe.height or bird.y + 30 > pipe.height + PIPE_GAP)):
                game_over = True

        pipes = [pipe for pipe in pipes if pipe.x > -PIPE_WIDTH]

        pygame.draw.rect(screen, BLACK, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, RED)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(30)

# Main Function
def main():
    pygame.quit()
    pygame.init()
    game_loop()

# Run Game
if __name__ == "__main__":
    show_start_screen()
    main()
