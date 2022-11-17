"""
https://www.youtube.com/watch?v=8dfePlONtls&ab_channel=freeCodeCamp.org

TO DO:

Use variables for stuff like screen resolution and do calculations with these variables

Queue instructions:
    - Find a way to prevent you from inputting 3 moves at once, and then only using the last one
    - Probably create a FIFO stack of inputs, consecutive similar inputs would be turned into just 1
    - A move would be entered on a valid key input, a move would be taken out every frame/iteration of the run loop

Style points:
    - Special image for the head of the snake
    - Create a grid of dark and less dark green squares for better perception of size/position

"""

import pygame
import time
import random
from collections import deque

size = 40

class Apple:

    def __init__(self, parent_screen, x, y):
        self.apple_img = pygame.image.load("/Users/evan/PycharmProjects/AHProject/snake/Resources/apple.jpeg").convert()
        self.parent_screen = parent_screen
        self.coord = (x, y)

    def draw(self):
        self.parent_screen.blit(self.apple_img, self.coord)


class Snake:
    snake_size = 5
    starting_x = 3 * size
    starting_y = 3 * size

    def __init__(self, parent_screen):
        self.parent_screen = parent_screen

        # Assigns this object representing an image to the variable Block
        self.block = pygame.image.load("/Users/evan/PycharmProjects/AHProject/snake/Resources/block.jpeg").convert()

        self.x = deque([self.starting_x]*(self.snake_size-1))
        self.x.appendleft(self.starting_x + size)
        self.y = deque([self.starting_y + size]*self.snake_size)

        self.direction = None

    def draw(self):
        for x, y in zip(self.x, self.y):
            self.parent_screen.blit(self.block, (x, y))

    def grow(self, coordinates):
        self.x.append(coordinates[0])
        self.y.append(coordinates[1])
        self.snake_size += 1

    def move_up(self):
        # If the snake is not going down
        if self.direction != "Down":
            # Let the snake travel up
            self.direction = "Up"

    def move_down(self):
        # If the snake is not going up
        if self.direction != "Up":
            # Let the snake travel down
            self.direction = "Down"

    def move_left(self):
        # If the snake is not going right
        if self.direction != "Right":
            # Let the snake travel left
            self.direction = "Left"

    def move_right(self):
        # If the snake is not going left
        if self.direction != "Left":
            # Let the snake travel right
            self.direction = "Right"

    def walk(self, direction):
        # Move the snake according to the direction
        if direction == "Up":
            # For example if moving up, calculate the new coordinates for the head, append it to the front/left of
            # the list
            self.y.appendleft(self.y[0] - size)
            self.x.appendleft(self.x[0])

            # Then pop the last coordinates in the list and return it in case we need to add it back after growing
            return self.x.pop(), self.y.pop()

        elif direction == "Down":
            self.y.appendleft(self.y[0] + size)
            self.x.appendleft(self.x[0])

            return self.x.pop(), self.y.pop()

        elif direction == "Left":
            self.y.appendleft(self.y[0])
            self.x.appendleft(self.x[0] - size)

            return self.x.pop(), self.y.pop()

        elif direction == "Right":
            self.y.appendleft(self.y[0])
            self.x.appendleft(self.x[0] + size)

            return self.x.pop(), self.y.pop()

        else:
            return None


class Game:

    running = True

    def __init__(self):
        # Initialise pygame
        pygame.init()
        # Initialise window/screen of some size as surface
        self.surface = pygame.display.set_mode((1000, 600))
        # Does something to the surface being displayed (Filling it with white)
        self.surface.fill((255, 255, 255))

        self.num_of_apples = 2
        self.score = 0

        self.dead = False

        # Create snake
        self.snake = Snake(self.surface)
        # Create apples
        self.apples = []
        for x in range(self.num_of_apples):
            self.create_apple()

    def draw_new_frame(self):
        # Empty the whole screen
        self.surface.fill((255, 255, 255))
        # Draw snake on top
        self.snake.draw()

        # Draw apples
        for apple in self.apples:
            apple.draw()

        # Draw score
        self.display_score()

        # Refresh screen
        pygame.display.flip()

    def move(self):
        # Move the snake, keep the last position of its tail/segment just popped in case we need to add it back
        popped_coordinates = self.snake.walk(self.snake.direction)

        # If the head of the snake collides with the coordinates of one of the apples:
        for i in range(self.num_of_apples):
            if (self.snake.x[0], self.snake.y[0]) == self.apples[i].coord:

                # Remove collided apple from list of apples
                self.apples.pop(i)

                # Add a segment back to the end of the snake
                self.snake.grow(popped_coordinates)

                # Create a new apple
                self.create_apple()

                # Increment score and snakes length variables by 1
                self.score += 1

                break

        self.check_collision()

    def check_collision(self):
        # Check if the snake has moved out of bounds of the surface
        if (not (0 < self.snake.x[0] < 1000)) or (not (0 < self.snake.y[0] < 600)):
            self.dead = True
        # Check if the snake has collided with itself
        elif (self.snake.x[0], self.snake.y[0]) in [(self.snake.x[i], self.snake.y[i]) for i in range(1, self.snake.snake_size)]:
            self.dead = True

    def create_apple(self):
        # Start with a list of all positions within bounds of the screen
        all_positions = [(x * size, y * size) for x in range(25) for y in range(15)]
        # Get a list of all positions occupied by apples and snakes
        # Apples
        apple_positions = [apple.coord for apple in self.apples]
        # Snake
        snake_positions = [(self.snake.x[i], self.snake.y[i]) for i in range(self.snake.snake_size)]

        # Remove elements in all_positions which are the same as any element in apple_positions or snake_positions
        valid_positions = []
        for valid_pos in all_positions:
            if (valid_pos not in apple_positions) and (valid_pos not in snake_positions):
                valid_positions.append(valid_pos)

        # With a list of valid coordinates, create a new apple from one of these randomly selected positions
        # Append it to the list of apples on the board in game

        new_position = valid_positions[random.randint(0, len(valid_positions))]

        self.apples.append(Apple(self.surface, new_position[0], new_position[1]))

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score_counter = font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.surface.blit(score_counter, (0, 0))

    def game_over(self):
        # Draw the game over screen
        self.surface.fill((255, 255, 255))
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render("Game over!", True, (0, 0, 0))
        line2 = font.render(f"You have crashed with a score of {self.score}", True, (0, 0, 0))

        self.surface.blit(line1, (30, 30))
        self.surface.blit(line2, (30, 60))

        # Draw play again button
        pygame.draw.rect(self.surface, (100, 100, 100), [334, 200, 100, 40])
        play_again = font.render("Play again?", True, (0, 0, 0))
        self.surface.blit(play_again, (334, 200))
        # Create quit button
        pygame.draw.rect(self.surface, (100, 100, 100), [566, 200, 100, 40])
        button_quit = font.render("Quit :(", True, (0, 0, 0))
        self.surface.blit(button_quit, (566, 200))

        # Refresh the screen once (I don't need to animate anything, so I'll only loop to get mouse positions for buttons
        pygame.display.flip()

        while self.dead:

            for ev in pygame.event.get():

                if ev.type == pygame.QUIT:
                    pygame.quit()

                # checks if a mouse is clicked
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    # Get mouse position
                    mouse = pygame.mouse.get_pos()

                    # If the mouse was pressed within the bounds of the play again button:
                    if (334) <= mouse[0] <= (334 + 100) and (200) <= mouse[1] <= (200+40):
                        # Restart the game
                        self.game_restart()
                    # If the mouse was pressed within the bounds of the quit button:
                    if (566) <= mouse[0] <= (566 + 100) and (200) <= mouse[1] <= (200+40):
                        # Quit
                        pygame.quit()

    def game_restart(self):
        print("Restart")
        self.__init__()

    def run(self):
        while self.running:
            # Run this while playing
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        self.snake.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.snake.move_down()

                    if event.key == pygame.K_RIGHT:
                        self.snake.move_right()
                    elif event.key == pygame.K_LEFT:
                        self.snake.move_left()

                if event.type == pygame.QUIT:
                    running = False

            self.move()

            self.draw_new_frame()

            if self.dead:
                self.game_over()
            
            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()