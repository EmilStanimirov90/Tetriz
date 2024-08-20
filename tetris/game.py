from grid import Grid
from bricks import *
import random


class Game:
    def __init__(self):
        self.grid = Grid()
        self.bricks = [IBrick(), JBrick(), LBrick(), OBrick(), SBrick(), ZBrick(), TBrick()]
        self.current_brick = self.get_random_brick()
        self.next_brick = self.get_random_brick()
        self.game_over = False
        self.score = 0

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 700
        self.score += move_down_points

    def get_random_brick(self):
        if len(self.bricks) == 0:
            self.bricks = [IBrick(), JBrick(), LBrick(), OBrick(), SBrick(), ZBrick(), TBrick()]
        brick = random.choice(self.bricks)
        self.bricks.remove(brick)
        return brick

    def move_left(self):
        self.current_brick.move(0, -1)
        if not self.brick_inside() or not self.brick_fits():
            self.current_brick.move(0, 1)

    def move_right(self):
        self.current_brick.move(0, 1)
        if not self.brick_inside() or not self.brick_fits():
            self.current_brick.move(0, -1)

    def move_down(self):
        self.current_brick.move(1, 0)
        if not self.brick_inside() or not self.brick_fits():
            self.current_brick.move(-1, 0)
            self.lock_brick()

    def lock_brick(self):
        tiles = self.current_brick.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.col] = self.current_brick.id
        self.current_brick = self.next_brick
        self.next_brick = self.get_random_brick()
        rows_cleared = self.grid.clear_all_full_rows()
        self.update_score(rows_cleared, 0)
        if not self.brick_fits():
            self.game_over = True

    def reset(self):
        self.grid.reset()
        self.bricks = [IBrick(), JBrick(), LBrick(), OBrick(), SBrick(), ZBrick(), TBrick()]
        self.current_brick = self.get_random_brick()
        self.next_brick = self.get_random_brick()
        self.score = 0

    def brick_fits(self):
        tiles = self.current_brick.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.col):
                return False
        return True

    def rotate(self):
        self.current_brick.rotate()
        if not self.brick_inside() or not self.brick_fits():
            self.current_brick.undo_rotation()

    def brick_inside(self):
        tiles = self.current_brick.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside_the_grid(tile.row, tile.col):
                return False
        return True

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_brick.draw(screen, 11, 11)

        if self.next_brick.id == 3:
            self.next_brick.draw(screen,255,290)
        elif self.next_brick.id == 4:
            self.next_brick.draw(screen, 250, 280)
        else:
            self.next_brick.draw(screen, 270, 270 )
