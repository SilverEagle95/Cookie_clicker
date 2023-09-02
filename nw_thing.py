import pygame
import random
import os

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

# Define the screen size and create a window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the window title and icon
pygame.display.set_caption("Cookie Clicker")
icon = pygame.image.load("C:\\Users\\alizb\\Downloads\\COOKIE.jpg")
pygame.display.set_icon(icon)

# Load the cookie image and scale it by half
cookie = pygame.image.load("C:\\Users\\alizb\\Downloads\\COOKIE.jpg")
cookie = pygame.transform.scale(cookie, (cookie.get_width() // 2, cookie.get_height() // 2))

# Get the cookie rect and center it on the screen
cookie_rect = cookie.get_rect()
cookie_rect.centerx = SCREEN_WIDTH // 2
cookie_rect.centery = SCREEN_HEIGHT // 2

# Create a font object for rendering text
font = pygame.font.SysFont("Arial", 32)

# Define a variable to store the score
score = 0

# Define a variable to control the main loop
running = True

# Define a variable to store the cookie scale factor
scale = 1

# Define a list to store the particles
particles = []

# Define a function to create a new particle
def create_particle():
    particle = {}
    particle["x"] = cookie_rect.centerx + random.randint(-25, 25)
    particle["y"] = cookie_rect.centery + random.randint(-25, 25)
    particle["size"] = random.randint(2, 5)
    particle["color"] = BROWN
    particle["vx"] = random.randint(-5, 5)
    particle["vy"] = random.randint(-5, 5)
    return particle

# Define a variable to store the shop button rect
shop_button_rect = pygame.Rect(SCREEN_WIDTH - 200, 10, 180, 50)

# Define a variable to store the shop state (True if open, False if closed)
shop_open = False

# Define a variable to store the multiplier value (how many points per click)
multiplier = 1

# Define a variable to store the multiplier price (how many points to buy or upgrade)
multiplier_price = 100

# Main loop
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if cookie_rect.collidepoint(mouse_x, mouse_y) and not shop_open:
                score += multiplier
                scale = 0.9
                for i in range(10):
                    particles.append(create_particle())
            elif shop_button_rect.collidepoint(mouse_x, mouse_y):
                shop_open = not shop_open
            elif shop_open and mouse_x > SCREEN_WIDTH // 2 and mouse_y > SCREEN_HEIGHT // 2:
                if score >= multiplier_price:
                    score -= multiplier_price
                    multiplier += 1
                    multiplier_price += multiplier_price // 2

    scale += (1 - scale) * 0.1

    for particle in particles:
        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]
        particle["size"] -= 1
        pygame.draw.rect(screen, particle["color"], (particle["x"], particle["y"], particle["size"], particle["size"]))

    particles = [particle for particle in particles if particle["size"] > 0]

    temp_surface = pygame.Surface((cookie_rect.width, cookie_rect.height))
    temp_surface.blit(cookie, (0, 0))
    temp_surface = pygame.transform.scale(temp_surface, (int(cookie_rect.width * scale), int(cookie_rect.height * scale)))
    temp_rect = temp_surface.get_rect()
    temp_rect.centerx = cookie_rect.centerx
    temp_rect.centery = cookie_rect.centery
    screen.blit(temp_surface, temp_rect)

    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect()
    score_rect.topleft = (10, 10)
    screen.blit(score_text, score_rect)

    pygame.draw.rect(screen, GREEN, shop_button_rect)
    shop_text = font.render("Shop", True, WHITE)
    shop_text_rect = shop_text.get_rect()
    shop_text_rect.centerx = shop_button_rect.centerx
    shop_text_rect.centery = shop_button_rect.centery
    screen.blit(shop_text, shop_text_rect)

    if shop_open:
        shop_bg_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(screen, (128, 128, 128), shop_bg_rect)
        shop_title_text = font.render("Shop", True, WHITE)
        shop_title_text_rect = shop_title_text.get_rect()
        shop_title_text_rect.centerx = shop_bg_rect.centerx
        shop_title_text_rect.top = shop_bg_rect.top + 10
        screen.blit(shop_title_text, shop_title_text_rect)
        multiplier_button_rect = pygame.Rect(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 10, SCREEN_WIDTH // 4 - 20, SCREEN_HEIGHT // 4 - 20)
        pygame.draw.rect(screen, BLUE, multiplier_button_rect)
        multiplier_button_text = font.render(f"Multiplier x{multiplier}", True, WHITE)
        multiplier_button_text_rect = multiplier_button_text.get_rect()
        multiplier_button_text_rect.centerx = multiplier_button_rect.centerx
        multiplier_button_text_rect.centery = multiplier_button_rect.centery - 10
        screen.blit(multiplier_button_text, multiplier_button_text_rect)
        multiplier_price_text = font.render(f"Price: {multiplier_price}", True, WHITE)
        multiplier_price_text_rect = multiplier_price_text.get_rect()
        multiplier_price_text_rect.centerx = multiplier_button_rect.centerx
        multiplier_price_text_rect.centery = multiplier_button_rect.centery + 30
        screen.blit(multiplier_price_text, multiplier_price_text_rect)

    pygame.display.flip()

pygame.quit()
