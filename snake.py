import pygame, sys, random
from pygame.math import Vector2
from button import BUTTON
from pygame import mixer

class SNAKE:
    # Initialize the snake
    def __init__(self):
        # Body of snake
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        # Snake graphics
        self.head_up = pygame.image.load('Images/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Images/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Images/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Images/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('Images/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Images/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Images/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Images/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Images/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Images/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Images/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Images/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Images/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Images/body_bl.png').convert_alpha()

        # Snake sound
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
    
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body): # Enumerate gives the index of the block in the list
            # Draw a rect for the positioning
            x_pos_block = int(block.x * cell_size)
            y_pos_block =  int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos_block, y_pos_block, cell_size, cell_size) # (x, y, width, height)
            
            # Check what direction each part of the snake is facing
            if index == 0:
                # Draw head
                screen.blit(self.head, block_rect)

            elif index == len(self.body) - 1:
                # Draw tail
                screen.blit(self.tail, block_rect)

            else:
                # Draw body
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0] # E.g. (4, 10) - (5, 10) = (-1, 0) -> head is to the right of the body
        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        
        else:
            # Body of snake minus the last item (slicing)
            body_copy = self.body[:-1]
            # Insert the first element of the previous list (which is the head) at the front of the new list + the direction its moving
            body_copy.insert(0, body_copy[0] + self.direction)
            # Return the list back to the body
            self.body = body_copy[:]

    # Add a block after the snake eats fruit
    def add_block(self):
       self.new_block = True 

    def play_crunch_sound(self):
        self.crunch_sound.play()

    # Reset the snake's length after game over
    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

class FRUIT:
    # Initialize the fruit at a random position
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        # Create rectangle for the fruit
        x_pos_fruit = int(self.pos.x * cell_size)
        y_pos_fruit = int(self.pos.y * cell_size)
        fruit_rect = pygame.Rect(x_pos_fruit, y_pos_fruit, cell_size, cell_size) 
        # Draw the fruit
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)
        screen.blit(apple, fruit_rect)

    # Randomize the fruit position after the snake eats it
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    # Initialize a game that happens entirely in the main class - snake and fruit are created
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    # Add background music in the main menu
    def menu_music(self):
        # By simmys_recycle_bin from freesound.org
        mixer.music.load('Sound/menu_music.wav')
        mixer.music.play(-1)
   
    # Update the snake when it moves
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    # Draw the snake and fruit
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    # Check if the snake eats the fruit 
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            # Reposition the fruit
            self.fruit.randomize()

            # Add a new block to the snake
            self.snake.add_block()

            # Play the crunch sound
            self.snake.play_crunch_sound()

        # Randomise again if the fruit is on the snake
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    # Check if snake hits something
    def check_fail(self):
        # Check if snake is outside of the screen
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
    
        # Check if snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    # Game over - reset snake
    def game_over(self):
        self.snake.reset()

    # Draw grass background
    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    # Display score
    def draw_score(self):
        # Our score will be the length of the snake - 3 turned into a string
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12)) # (text, antialiasing, color)
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 750)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        # Apple image next to score
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        # Rectangle around score
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)
        screen.blit(score_surface, score_rect) # (text, position)
        screen.blit(apple, apple_rect)

# Fix sound delay
pygame.mixer.pre_init(44100, -16, 2, 512)
# Initialize Pygame
pygame.init()
cell_size = 40
cell_number = 20
# Display surface - canvas where the game is drawn (there is only 1 by default)
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size)) # Set the screen size (width, height)
# Set fps (without it the game will run as fast as it can)
clock = pygame.time.Clock()
# Import assets
apple = pygame.image.load('Images/apple.png').convert_alpha()
background = pygame.image.load('Images/snake_bg.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-regular.ttf', 25) # (font, font size)

'''
If you run the code above, you will see a window appear for a second and then disappear.
This is because the program is running too fast and the window is closing before you can see it.
To keep the window open, you add a loop that keeps the window open until you close it.
'''

# Trigger this event every 150 ms
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

# Main game loop
def play():
    while True:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Stops Pygame
                pygame.quit()
                # Stops all code
                sys.exit()

            if event.type == SCREEN_UPDATE:
                main_game.update()

            # Keyboard inputs
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if main_game.snake.direction.y != 1: # Prevents the snake from moving into itself
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if main_game.snake.direction.x != -1:    
                        main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)

        # Fill the screen with a color
        screen.fill((175, 215, 70))
        # Draw the elements
        main_game.draw_elements()
        # Update the display
        pygame.display.update()
        # Limit the game to 60 fps
        clock.tick(60) 

def options():
    # Set the title of the window
    pygame.display.set_caption('Options')

    while True:
        option_mouse_pos = pygame.mouse.get_pos()

        # Draw the background
        screen.blit(background, (0, 0))

        # Create text
        option_text = game_font.render('OPTIONS', True, (56, 74, 12))
        option_rect = option_text.get_rect(center = (cell_number * cell_size // 2, cell_number * cell_size // 2 - 100))
        screen.blit(option_text, option_rect)

        # Create back button
        back_button = BUTTON(image = None, pos = (cell_number * cell_size // 2, cell_number * cell_size // 2), \
                                text_input = "BACK", font = game_font, base_colour = (56, 74, 12), \
                                    hover_colour = (167, 209, 61))
        
        # Update back button
        back_button.change_colour(option_mouse_pos)
        back_button.update(screen)

        # Check for events in the options menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_click(option_mouse_pos):
                    main_menu()

        pygame.display.update()

def main_menu():
    # Set the title of the window
    pygame.display.set_caption('Menu')

    # Play background music
    main_game.menu_music()

    while True:
       
        # Draw the background
        screen.blit(background, (0, 0))

        # Check mouse position
        menu_mouse_pos = pygame.mouse.get_pos()

        # Create text
        menu_text = game_font.render('MAIN MENU', True, (56, 74, 12))
        menu_rect = menu_text.get_rect(center = (cell_number * cell_size // 2, cell_number * cell_size // 2 - 100))

        # Create buttons
        play_button = BUTTON(image = pygame.image.load("images/play_rect.png"), \
                             pos = (cell_number * cell_size // 2, cell_number * cell_size // 2), \
                                text_input = "PLAY", font = game_font, base_colour = (56, 74, 12), \
                                    hover_colour = (167, 209, 61))

        options_button = BUTTON(image = pygame.image.load("images/options_rect.png"), \
                             pos = (cell_number * cell_size // 2, cell_number * cell_size // 2 + 120), \
                                text_input = "OPTIONS", font = game_font, base_colour = (56, 74, 12), \
                                    hover_colour = (167, 209, 61))
        quit_button = BUTTON(image = pygame.image.load("images/quit_rect.png"), \
                             pos = (cell_number * cell_size // 2, cell_number * cell_size // 2 + 240), \
                                text_input = "QUIT", font = game_font, base_colour = (56, 74, 12), \
                                    hover_colour = (167, 209, 61))

        # Put text on the screen
        screen.blit(menu_text, menu_rect)

        # Update buttons
        for button in [play_button, options_button, quit_button]:
            button.change_colour(menu_mouse_pos)
            button.update(screen)

        # Check for events in the menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_click(menu_mouse_pos):
                    play()
                if options_button.check_for_click(menu_mouse_pos):
                    options()
                if quit_button.check_for_click(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()

main_menu() 