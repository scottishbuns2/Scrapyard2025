import pygame
import sys
import math
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
light_blue = (173, 216, 230)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Fonts
title_font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Start Menu")

# Load images
turtle_image = pygame.image.load('turtle.png')
circle_image = pygame.image.load('circle.png')

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def draw_progress_bar(surface, x, y, width, height, progress):
    pygame.draw.rect(surface, black, (x, y, width, height), 2)  # Draw border
    pygame.draw.rect(surface, red, (x, y, width * progress, height))  # Draw progress

def main_menu():
    while True:
        screen.fill(light_blue)

        draw_text('Counting Freds!', title_font, black, screen, screen_width // 2, screen_height // 4)

        mx, my = pygame.mouse.get_pos()

        start_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
        if start_button_rect.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                start_game()

        pygame.draw.rect(screen, black, start_button_rect, 2)
        draw_text('Start', button_font, black, screen, screen_width // 2, screen_height // 2 + 25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def start_game():
    clock = pygame.time.Clock()
    show_turtle_button = True
    score = 0
    total_turtles = 0
    button_pressed = False
    turtle_clicked = False  # Flag to track if the turtle button was clicked

    turtle = None  # Start with no turtle on screen
    circle = None  # Start with no circle on screen
    last_spawn_time = 0  # Keep track of when the last turtle spawned
    spawn_delay = random.uniform(1, 3)  # Random delay between 1 and 3 seconds

    while True:
        screen.fill(white)
        
        # Check if it's time to spawn a new turtle or circle
        current_time = time.time()
        if turtle is None and current_time - last_spawn_time >= spawn_delay:
            # Spawn a new turtle
            turtle = {
                'x': -50,  # Start position off the left side
                'y': screen_height - random.randint(50, 100),  # Random vertical position
                'speed': random.randint(3, 6)  # Random speed for each turtle
            }
            last_spawn_time = current_time  # Update last spawn time
            spawn_delay = random.uniform(1, 3)  # Set a new random delay for the next turtle
            if score >= 14:
                total_turtles += 0.1  # Increment the count of total turtles spawned by 0.1
            else:
                total_turtles += 1  # Increment the count of total turtles spawned by 1
            turtle_clicked = False  # Reset the flag when a new turtle spawns

        if circle is None and current_time - last_spawn_time >= spawn_delay:
            # Spawn a new circle
            circle = {
                'x': -50,  # Start position off the left side
                'y': screen_height - random.randint(50, 100),  # Random vertical position
                'speed': random.randint(3, 6)  # Random speed for each circle
            }
            last_spawn_time = current_time  # Update last spawn time
            spawn_delay = random.uniform(1, 3)  # Set a new random delay for the next circle

        if turtle is not None:
            # Move the turtle along the path
            turtle['x'] += turtle['speed']
            
            # Calculate the y position for the turtle to move in an arc
            turtle['y'] = screen_height - int((screen_height * 0.75) * math.sin(math.radians((turtle['x'] / screen_width) * 180)))

            # Draw the turtle image
            screen.blit(turtle_image, (turtle['x'], turtle['y']))

            # Remove the turtle if it goes off the screen
            if turtle['x'] > screen_width + 50:
                if not turtle_clicked:
                    score = 0  # Reset the score if the turtle was not clicked
                turtle = None  # Reset turtle after it leaves the screen

        if circle is not None:
            # Move the circle along the path
            circle['x'] += circle['speed']
            
            # Calculate the y position for the circle to move in an arc
            circle['y'] = screen_height - int((screen_height * 0.75) * math.sin(math.radians((circle['x'] / screen_width) * 180)))

            # Draw the circle image
            screen.blit(circle_image, (circle['x'], circle['y']))

            # Remove the circle if it goes off the screen
            if circle['x'] > screen_width + 50:
                circle = None  # Reset circle after it leaves the screen

        # Draw the turtle button
        if show_turtle_button:
            turtle_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height - 100, 200, 50)
            pygame.draw.rect(screen, black, turtle_button_rect)
            draw_text('Turtle', button_font, white, screen, screen_width // 2, screen_height - 75)

            mx, my = pygame.mouse.get_pos()
            if turtle_button_rect.collidepoint((mx, my)) and button_pressed:
                if score >= 14:
                    score += 0.1
                else:
                    score += 1
                turtle_clicked = True  # Set the flag when the button is clicked
                button_pressed = False  # Reset the button press state

        # Reset the score if the counter exceeds the number of total turtles
        if score > total_turtles:
            score = 0
            total_turtles = 0

        # Draw the progress bar
        progress = min(score / 15, 1)  # Calculate progress (max 1)
        draw_progress_bar(screen, 50, 20, screen_width - 100, 30, progress)

        # Draw the score slightly below the progress bar
        draw_text(f'Score: {score:.1f}', button_font, black, screen, screen_width // 2, 70)

        # Handle events like quitting or pressing the button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                button_pressed = False

        pygame.display.update()
        clock.tick(30)  # Control the frame rate

if __name__ == "__main__":
    main_menu()
