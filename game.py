import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Fans!")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont(None, 48)
big_font = pygame.font.SysFont(None, 72)

# Load fixed images
player_img = pygame.image.load("girl.png")  # Girl
fire_img = pygame.image.load("sephora.png")    # Sephora
fan_img = pygame.image.load("coins.png")     # Money jar

# Resize images
player_width = 80
player_height = 100
player_img = pygame.transform.scale(player_img, (player_width, player_height))

object_width = 50
object_height = 50
fan_img = pygame.transform.scale(fan_img, (object_width, object_height))
fire_img = pygame.transform.scale(fire_img, (object_width, object_height))

# Player attributes
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 8

# Object attributes
object_speed = 5
spawn_rate = 30  # Frames between object spawns

# Score
score = 0
winner_achieved = False  # To display winner only once

# Object list
objects = []  # Each object will be a dictionary: {'type': 'fan' or 'fire', 'rect': pygame.Rect}

# Main Game Loop
frame_count = 0
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key Presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_q]:
        pygame.quit()
        sys.exit()

    # Spawn Objects
    frame_count += 1
    if frame_count >= spawn_rate:
        frame_count = 0
        object_type = random.choice(["fan", "fire"])
        object_x = random.randint(0, WIDTH - object_width)
        object_rect = pygame.Rect(object_x, 0, object_width, object_height)
        objects.append({"type": object_type, "rect": object_rect})

    # Move Objects
    for obj in objects:
        obj["rect"].y += object_speed

    # Check for collisions
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    new_objects = []
    for obj in objects:
        if player_rect.colliderect(obj["rect"]):
            if obj["type"] == "fan":
                score += 1
            else:
                score -= 1  # Losing point if catching fire
        else:
            if obj["rect"].y < HEIGHT:
                new_objects.append(obj)
    objects = new_objects

    # Draw Player
    screen.blit(player_img, (player_x, player_y))

    # Draw Objects
    for obj in objects:
        if obj["type"] == "fan":
            screen.blit(fan_img, obj["rect"])
        else:
            screen.blit(fire_img, obj["rect"])

    # Draw Score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Show achievement if score reaches 10
    if score >= 10 and not winner_achieved:
        winner_text = big_font.render("🏆 YOU ARE A WINNER! 🏆", True, (0, 128, 0))
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(3000)  # Pause for 3 seconds
        winner_achieved = True

    # Update Display
    pygame.display.flip()
