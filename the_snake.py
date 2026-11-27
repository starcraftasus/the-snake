"""Игра «Изгиб Питона»: змейка, которая собирает яблоки."""

from random import choice

import pygame


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

KEY_DIRECTIONS = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
}

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Изгиб Питона')
clock = pygame.time.Clock()


class GameObject:
    """Общие свойства игровых объектов."""

    def __init__(self):
        """Задать начальную позицию и цвет игрового объекта."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Определить отрисовку в дочернем классе."""
        pass

    def draw_cell(self, position):
        """Нарисовать клетку с рамкой и цветом игрового объекта."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Яблоко, которое увеличивает длину змейки."""

    def __init__(self, occupied_positions=()):
        """Создать яблоко в случайной свободной клетке."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=()):
        """Выбрать случайную клетку, не занятую змейкой."""
        occupied = set(occupied_positions)
        free_positions = [
            (x, y)
            for x in range(0, SCREEN_WIDTH, GRID_SIZE)
            for y in range(0, SCREEN_HEIGHT, GRID_SIZE)
            if (x, y) not in occupied
        ]
        self.position = choice(free_positions)

    def draw(self):
        """Нарисовать яблоко на игровом поле."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Змейка, её сегменты и направление движения."""

    def __init__(self):
        """Создать зелёную змейку, которая движется вправо."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset(RIGHT)

    def update_direction(self):
        """Применить направление, выбранное с клавиатуры."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Передвинуть змейку на одну клетку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_head = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Стереть старый хвост и нарисовать все сегменты змейки."""
        if self.last is not None:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        for position in self.positions:
            self.draw_cell(position)

    def get_head_position(self):
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def reset(self, direction=None):
        """Вернуть змейку в центр с заданным или случайным направлением."""
        self.length = 1
        self.positions = [self.position]
        self.direction = (
            choice((UP, DOWN, LEFT, RIGHT))
            if direction is None else direction
        )
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обработать закрытие окна и нажатия стрелок без разворота назад."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            direction = KEY_DIRECTIONS.get(event.key)
            direction_x, direction_y = game_object.direction
            opposite_direction = (-direction_x, -direction_y)
            if direction is not None and direction != opposite_direction:
                game_object.next_direction = direction


def main():
    """Запустить игру и обновлять её состояние до закрытия окна."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head_position = snake.get_head_position()
        apple_eaten = head_position == apple.position
        if apple_eaten:
            snake.length += 1

        # Сбросить игру при столкновении или заполнении поля.
        if (
            head_position in snake.positions[1:]
            or snake.length == GRID_WIDTH * GRID_HEIGHT
        ):
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        if apple_eaten or apple.position in snake.positions:
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
