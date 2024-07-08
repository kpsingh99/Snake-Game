import numpy as np
import pygame
import random
from enum import Enum  # Used for enumerations
from collections import namedtuple

pygame.init()
font = pygame.font.Font("Pacifico-Regular.ttf", 26)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


# namedTuple assigns a meaning to every position in a tuple and allow for a more readable and more self documenting code
Point = namedtuple('Point', 'x, y')


def manhatten_distance(point1, point2):
    return abs(point1.x-point2.x) + abs(point2.y-point1.y)


BLOCK_SIZE = 20
SPEED = 500


# we'll edit the play_step method to inculcate things like reset, reward, play(action) -> direction, keep track of
# game_iteration  and a is_collision function.

class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)
                      ]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0  # keeping track of game iteration

    def _place_food(self):  # randomly places the food
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        self._move(action)  # updates the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward -= 10
            return reward, game_over, self.score


        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward += 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill('Black')

        # draw the snake
        for pt in self.snake:
            if pt == self.head:
                pygame.draw.rect(self.display, (34, 139, 34), pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.display, (100, 255, 100), pygame.Rect(pt.x+4, pt.y+4, 12, 12))
                eye_size = BLOCK_SIZE // 6
                eye_offset_x = BLOCK_SIZE // 3
                eye_offset_y = BLOCK_SIZE // 3
                pygame.draw.circle(self.display, (0, 0, 0), (pt.x + eye_offset_x, pt.y + eye_offset_y), eye_size)
                pygame.draw.circle(self.display, (0, 0, 0), (pt.x + eye_offset_x, pt.y + BLOCK_SIZE - eye_offset_y),
                                   eye_size)
            else:
                pygame.draw.rect(self.display, (30, 144, 255), pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.display, (0, 100, 255), pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, (255, 0, 0), pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.display.blit(text, [0, 0])  # putting the text on the display with position at the top left
        pygame.display.flip()  # updates the full display surface to the screen

    def _move(self, action):

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        new_dir = self.direction
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        if np.array_equal(action, [0, 1, 0]):
            new_dir = clock_wise[(idx+1) % 4]
        if np.array_equal(action, [0, 0, 1]):
            new_dir = clock_wise[(idx-1) % 4]

        self.direction = new_dir

        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)


