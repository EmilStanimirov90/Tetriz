import sys
import pygame
from colors import Colors
from game import Game
from tetris.grid import Grid

# game initialisation /start/
pygame.init()

# create font and title plus score surface
title_font = pygame.font.Font(None, 40)
game_over_font = pygame.font.Font(None, 80)

score_surface = title_font.render("Score", True, Colors.WHITE)
next_surface = title_font.render("Next", True, Colors.WHITE)
level_surface = title_font.render("Level", True, Colors.WHITE)
game_over_surface = game_over_font.render("GAME OVER!", True, Colors.WHITE)
score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)
level_rect = pygame.Rect(320, 485, 170, 60)

# create game window
screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetriz")

# game speed
clock = pygame.time.Clock()

# instantiate game class
game = Game()

# move blocks down independently of game loop
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, game.game_speed)


# game loop
while True:

    # game exit and loop end
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if game.game_over:
                game.game_over = False
                game.reset()

            if (event.key == pygame.K_UP or event.key == pygame.K_w) and not game.game_over:
                game.rotate()
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and not game.game_over:
                game.move_down()
                game.update_score(0, 1)
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and not game.game_over:
                game.move_right()
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and not game.game_over:
                game.move_left()

        # move blocks down independently of game loop
        if event.type == GAME_UPDATE and not game.game_over:
            game.move_down()
    #update  game speed

    # create score text
    score_value_surface = title_font.render(str(game.score), True, Colors.WHITE)
    # create level text
    level_value_surface = title_font.render(str(game.level), True, Colors.WHITE)
    # fill in screen
    screen.fill(Colors.pale_blue)
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_surface, (375, 180, 50, 50))
    screen.blit(level_surface, (365, 450, 50, 50))

    pygame.draw.rect(screen, Colors.blue, score_rect, 0, 5)
    # we draw the score on top of the score rect, thats why the code is underneath
    # plus a trick to center it
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx,
                                                                  centery=score_rect.centery))
    pygame.draw.rect(screen, Colors.blue, next_rect, 0, 10)
    pygame.draw.rect(screen, Colors.blue, level_rect, 0, 5)
    screen.blit(level_value_surface, level_value_surface.get_rect(centerx=level_rect.centerx,
                                                                  centery=level_rect.centery))

    game.draw(screen)

    if game.game_over:
        screen.blit(game_over_surface, (75, 300, 50, 50))

    # refresh screen changes at certain fps
    pygame.display.update()
    clock.tick(60)
