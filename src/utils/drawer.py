import pygame
import os

BG_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("docs/imgs", "bg.png"))
)
STAT_FONT = pygame.font.SysFont("comicsans", 50)
WIN_WIDTH = 500

def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0, 0))  # topleft position

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Scores: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Gens: " + str(gen), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()