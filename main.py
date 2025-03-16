import pygame
import sys
import math
import random
import time

# Initialize pygame
pygame.init()

# Initialize the mixer
pygame.mixer.init()

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
turtle_image = pygame.image.load('FlyingFred.png')
circle_image = pygame.image.load('bread.png')
background_image = pygame.image.load('Scrapy_Background.png')
bread_image = pygame.image.load('bread.png')
title_bg_image = pygame.image.load('Title.png')
shrek_image = pygame.image.load('Shrek.png')
oreos_image = pygame.image.load('oreos.png')
pizza_coupon_image = pygame.image.load('pizza_coupon.png')
coupon_image = pygame.image.load('coupon.png')

# Load MP3 file
pygame.mixer.music.load('Temu_LOUD.mp3')

# Scale images down by 3 times
turtle_image = pygame.transform.scale(turtle_image, (turtle_image.get_width() // 3, turtle_image.get_height() // 3))
circle_image = pygame.transform.scale(circle_image, (circle_image.get_width() // 3, circle_image.get_height() // 3))
bread_image = pygame.transform.scale(bread_image, (bread_image.get_width() // 3, bread_image.get_height() // 3))

# Scale background images to match the window size
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
title_bg_image = pygame.transform.scale(title_bg_image, (screen_width, screen_height))

ads_images = [shrek_image, oreos_image, pizza_coupon_image, coupon_image]

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def draw_progress_bar(surface, x, y, width, height, progress):
    pygame.draw.rect(surface, black, (x, y, width, height), 2)  # Draw border
    pygame.draw.rect(surface, red, (x, y, width * progress, height))  # Draw progress

def blank_screen():
    while True:
        screen.fill(white)  # Fill the screen with white

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def flash_bread():
    for _ in range(2):
        screen.fill(white)
        draw_text("That's not a fred, that's bread!", button_font, red, screen, screen_width // 2, 50)
        pygame.display.update()
        pygame.time.delay(100)  # Delay for 100 milliseconds
        screen.blit(bread_image, (screen_width // 2 - bread_image.get_width() // 2, screen_height // 2 - bread_image.get_height() // 2))
        draw_text("That's not a fred, that's bread!", button_font, red, screen, screen_width // 2, 50)
        pygame.display.update()
        pygame.time.delay(100)  # Delay for 100 milliseconds

    show_ads()

def show_ads():
    # Play the MP3 file
    pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

    ads = []
    start_time = time.time()
    while time.time() - start_time < 10:
        if len(ads) < 50:
            for _ in range(50 - len(ads)):
                img = random.choice(ads_images)
                width = random.randint(50, 150)
                height = random.randint(50, 150)
                img = pygame.transform.scale(img, (width, height))
                x = random.randint(0, screen_width - width)
                y = random.randint(0, screen_height - height)
                ads.append((img, x, y, width, height))

        screen.fill(white)
        draw_text("QUICK, CLICK ON THE COUPONS!", button_font, red, screen, screen_width // 2, 50)
        for img, x, y, width, height in ads:
            screen.blit(img, (x, y))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for i, (img, x, y, width, height) in enumerate(ads):
                    if x <= mx <= x + width and y <= my <= y + height:
                        ads.pop(i)
                        for _ in range(3):  # Add three new ads
                            img = random.choice(ads_images)
                            width = random.randint(50, 150)
                            height = random.randint(50, 150)
                            img = pygame.transform.scale(img, (width, height))
                            x = random.randint(0, screen_width - width)
                            y = random.randint(0, screen_height - height)
                            ads.append((img, x, y, width, height))
                        break

    # Stop the MP3 file
    pygame.mixer.music.stop()

    return

def main_menu():
    while True:
        screen.blit(title_bg_image, (0, 0))  # Draw the title background image

        draw_text('Counting Freds!', title_font, black, screen, screen_width // 2, screen_height // 5)  # Adjusted y-coordinate

        mx, my = pygame.mouse.get_pos()

        start_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
        pygame.draw.rect(screen, black, start_button_rect)  # Draw solid rectangle
        draw_text('Start', button_font, white, screen, screen_width // 2, screen_height // 2 + 25)

        if start_button_rect.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                start_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def start_game():
    clock = pygame.time.Clock()
    show_turtle_button = True
    show_bread_button = False
    score = 0
    total_turtles = 0
    button_pressed = False
    turtle_clicked = False  # Flag to track if the turtle button was clicked

    turtle = None  # Start with no turtle on screen
    circle = None  # Start with no circle on screen
    last_spawn_time = 0  # Keep track of when the last turtle spawned
    turtle_spawn_delay = random.uniform(1, 3)  # Random delay between 1 and 3 seconds for turtle
    circle_spawn_delay = random.uniform(3, 6)  # Random delay between 3 and 6 seconds for circle

    while True:
        screen.blit(background_image, (0, 0))  # Draw the background image
        
        # Check if it's time to spawn a new turtle
        current_time = time.time()
        if turtle is None and current_time - last_spawn_time >= turtle_spawn_delay:
            # Spawn a new turtle
            turtle = {
                'x': -50,  # Start position off the left side
                'y': screen_height - random.randint(50, 100),  # Random vertical position
                'speed': random.randint(3, 6)  # Random speed for each turtle
            }
            last_spawn_time = current_time  # Update last spawn time
            turtle_spawn_delay = random.uniform(1, 3)  # Set a new random delay for the next turtle
            if score >= 9:
                total_turtles += 0.1  # Increment the count of total turtles spawned by 0.1
            else:
                total_turtles += 1  # Increment the count of total turtles spawned by 1
            turtle_clicked = False  # Reset the flag when a new turtle spawns

        # Check if it's time to spawn a new circle
        if circle is None and current_time - last_spawn_time >= circle_spawn_delay:
            # Spawn a new circle
            circle = {
                'x': -50,  # Start position off the left side
                'y': screen_height - random.randint(50, 100),  # Random vertical position
                'speed': random.randint(3, 6)  # Random speed for each circle
            }
            last_spawn_time = current_time  # Update last spawn time
            circle_spawn_delay = random.uniform(3, 6)  # Set a new random delay for the next circle

        if turtle is not None:
            # Move the turtle along the path
            turtle['x'] += turtle['speed']
            
            # Calculate the y position for the turtle to move in an arc
            turtle['y'] = screen_height - int((screen_height * 0.75) * math.sin(math.radians((turtle['x'] / screen_width) * 180)))

            # Draw the turtle image centered
            screen.blit(turtle_image, (turtle['x'] - turtle_image.get_width() // 2, turtle['y'] - turtle_image.get_height() // 2))

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

            # Draw the circle image centered
            screen.blit(circle_image, (circle['x'] - circle_image.get_width() // 2, circle['y'] - circle_image.get_height() // 2))

            # Remove the circle if it goes off the screen
            if circle['x'] > screen_width + 50:
                circle = None  # Reset circle after it leaves the screen

        # Draw the turtle button
        if show_turtle_button:
            turtle_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height - 100, 200, 50)
            pygame.draw.rect(screen, black, turtle_button_rect)  # Draw solid rectangle
            draw_text('Fred!', button_font, white, screen, screen_width // 2, screen_height - 75)

            mx, my = pygame.mouse.get_pos()
            if turtle_button_rect.collidepoint((mx, my)) and button_pressed:
                if score >= 9:
                    score += 0.1
                else:
                    score += 1
                turtle_clicked = True  # Set the flag when the button is clicked
                button_pressed = False  # Reset the button press state

        # Draw the bread button
        if show_bread_button:
            bread_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height - 100, 200, 50)
            screen.blit(bread_image, (bread_button_rect.x, bread_button_rect.y))

            mx, my = pygame.mouse.get_pos()
            if bread_button_rect.collidepoint((mx, my)) and button_pressed:
                flash_bread()
                show_ads()
                score = 0  # Reset the score after flashing and showing ads
                show_bread_button = False
                show_turtle_button = True
                button_pressed = False  # Reset the button press state

        # Reset the score if the counter exceeds the number of total turtles
        if score > total_turtles:
            score = 0
            total_turtles = 0

        # Draw the progress bar
        progress = min(score / 9.9, 1)  # Calculate progress (max 1)
        draw_progress_bar(screen, 50, 20, screen_width - 100, 30, progress)

        # Draw the score slightly below the progress bar
        draw_text(f'Score: {score:.1f}', button_font, black, screen, screen_width // 2, 70)

        # Switch to bread button if score reaches 9.8
        if score >= 9.8:
            show_turtle_button = False
            show_bread_button = True

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
