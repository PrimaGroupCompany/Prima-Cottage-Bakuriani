import pygame
import sys

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_SPEED = [5, 5]
PADDLE_SPEED = 7

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

# Ball setup
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
ball_speed = BALL_SPEED.copy()

# Paddles setup
player = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 60, 10, 120)
opponent = pygame.Rect(10, HEIGHT // 2 - 60, 10, 120)

# Score
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 50)

# Clock
clock = pygame.time.Clock()

def reset_ball():
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed[0] *= -1

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += PADDLE_SPEED

    # Opponent AI
    if opponent.centery < ball.centery:
        opponent.y += PADDLE_SPEED
    if opponent.centery > ball.centery:
        opponent.y -= PADDLE_SPEED
    opponent.y = max(opponent.y, 0)
    opponent.y = min(opponent.y, HEIGHT - opponent.height)

    # Ball Movement
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Collision with top/bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] *= -1

    # Collision with paddles
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed[0] *= -1

    # Scoring
    if ball.left <= 0:
        player_score += 1
        reset_ball()
    if ball.right >= WIDTH:
        opponent_score += 1
        reset_ball()

    # Drawing
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, opponent)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Score Display
    player_text = font.render(f"{player_score}", True, WHITE)
    opponent_text = font.render(f"{opponent_score}", True, WHITE)
    screen.blit(player_text, (WIDTH // 2 + 20, 20))
    screen.blit(opponent_text, (WIDTH // 2 - 40, 20))

    pygame.display.flip()
    clock.tick(60)
