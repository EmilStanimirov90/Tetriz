from grid import Grid
from bricks import *
import random
import pygame


class Game:
    def __init__(self):
        self.grid = Grid()
        self.bricks = [IBrick(), JBrick(), LBrick(), OBrick(), SBrick(), ZBrick(), TBrick()]
        self.current_brick = self.get_random_brick()
        self.next_brick = self.get_random_brick()
        self.game_over = False
        self.score = 0
        self.total_lines_cleared = 0
        self.level = 0
        self.game_speed = 600  # ms
        self.rotate_sound = [pygame.mixer.Sound("sounds/swing-whoosh-5-198498.mp3"),
                             pygame.mixer.Sound("sounds/swing-whoosh-4-198496.mp3"),
                             pygame.mixer.Sound("sounds/swing-whoosh-9-198502.mp3")]

        self.clear_sound = pygame.mixer.Sound("sounds/large-underwater-explosion-190270.mp3")

        pygame.mixer.music.load("sounds/Voyage 👾 (16-Bit Arcade No Copyright Music).mp3")
        pygame.mixer.music.play(-1)

        # sound volume
        pygame.mixer.music.set_volume(0.2)

        self.clear_sound.set_volume(2)

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 40 * (self.level + 1)
        elif lines_cleared == 2:
            self.score += 100 * (self.level + 1)
        elif lines_cleared == 3:
            self.score += 300 * (self.level + 1)
        elif lines_cleared == 4:
            self.score += 1200 * (self.level + 1)
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
        if rows_cleared > 0:
            self.clear_sound.play()

            self.update_score(rows_cleared, 0)
            self.increase_game_speed(rows_cleared)

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
        else:
            rotate_sound = random.choice(self.rotate_sound)
            rotate_sound.set_volume(0.2)
            rotate_sound.play()

    def brick_inside(self):
        tiles = self.current_brick.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside_the_grid(tile.row, tile.col):
                return False
        return True

    def increase_game_speed(self, lines_cleared):
        self.total_lines_cleared += lines_cleared
        self.level = self.total_lines_cleared // 1
        self.game_speed -= (self.level + 1) * 200

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_brick.draw(screen, 11, 11)

        if self.next_brick.id == 3:
            self.next_brick.draw(screen, 255, 290)
        elif self.next_brick.id == 4:
            self.next_brick.draw(screen, 250, 280)
        else:
            self.next_brick.draw(screen, 270, 270)
