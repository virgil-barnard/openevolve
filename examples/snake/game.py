"""
A minimal head-less Snake engine suitable for evolutionary code search.
Grid coordinates: (0,0)=top-left.  Direction vectors: U,D,L,R.
Game ends on wall collision or self-collision, or when max_steps reached.
"""

from enum import Enum
import random

class Direction(Enum):
    UP    = ( -1,  0)
    DOWN  = (  1,  0)
    LEFT  = (  0, -1)
    RIGHT = (  0,  1)

OPPOSITE = {
    Direction.UP:    Direction.DOWN,
    Direction.DOWN:  Direction.UP,
    Direction.LEFT:  Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}

class Game:
    def __init__(self, rows=12, cols=12, max_steps=200):
        self.rows = rows
        self.cols = cols
        self.max_steps = max_steps
        self.reset()

    # ------------------------------------------------------------------ utils
    def reset(self):
        mid_r, mid_c = self.rows // 2, self.cols // 2
        self.snake = [(mid_r, mid_c)]
        self.dir = random.choice(list(Direction))
        self.spawn_food()
        self.steps = 0
        self.score = 0
        self.alive = True

    def spawn_food(self):
        cells = {(r, c) for r in range(self.rows) for c in range(self.cols)}
        cells -= set(self.snake)
        self.food = random.choice(list(cells))

    # ---------------------------------------------------------------- sensors
    def get_sensor(self):
        """Return a lightweight dictionary visible to the player."""
        head_r, head_c = self.snake[0]

        # Manhattan distance to food
        food_vec = (self.food[0] - head_r, self.food[1] - head_c)

        # one-hot collision danger in each direction (wall or body)
        danger = {}
        for d in Direction:
            dr, dc = d.value
            r, c = head_r + dr, head_c + dc
            danger[d.name] = (
                r < 0 or r >= self.rows or
                c < 0 or c >= self.cols or
                (r, c) in self.snake
            )

        return {
            "food_vec": food_vec,
            "danger": danger,
            "current_dir": self.dir.name,
            "length": len(self.snake),
            "steps": self.steps,
        }

    # -------------------------------------------------------------- game step
    def step(self, action: str):
        """Advance one tick given an action string ('UP','DOWN',...)."""
        if not self.alive:
            return

        try:
            chosen = Direction[action.upper()]
        except KeyError:
            chosen = self.dir  # illegal text -> keep going straight

        # Disallow 180-degree turn
        if chosen == OPPOSITE[self.dir]:
            chosen = self.dir
        self.dir = chosen

        # move head
        dr, dc = self.dir.value
        head_r, head_c = self.snake[0]
        new_head = (head_r + dr, head_c + dc)
        self.steps += 1

        # collisions
        r, c = new_head
        if (r < 0 or r >= self.rows or
            c < 0 or c >= self.cols or
            new_head in self.snake):
            self.alive = False
            return

        # eat
        ate = new_head == self.food
        self.snake.insert(0, new_head)
        if ate:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()  # move tail

        if self.steps >= self.max_steps:
            self.alive = False

    # -------------------------------------------------------- run full episode
    def play(self, player, seed=None):
        """Run to termination with the supplied Player object."""
        if seed is not None:
            random.seed(seed)
        self.reset()
        while self.alive:
            sensors = self.get_sensor()
            action = player.decide(sensors)
            self.step(action)
        return self.score, self.steps
