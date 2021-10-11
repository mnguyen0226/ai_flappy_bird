import pygame
import neat
import time
import os
import random

pygame.font.init()
from utils.bird import Bird
from utils.base import Base
from utils.pipe import Pipe
from utils.drawer import draw_window

GENS = 0
WIN_WIDTH = 500
WIN_HEIGHT = 800
PIPE_DIST = 600

#########################################################################
def main(genomes, config):
    global GENS
    GENS += 1
    nets = []  # keep track of each neural net for each bird
    ge = []  # keep track of the genomes
    birds = []

    for _, g in genomes:  # Set a neural net for each genomes
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(PIPE_DIST)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    clock = pygame.time.Clock()
    score = 0

    run = True
    while run:
        clock.tick(30)  # at most 30 tick every seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # Set the pipe index
        pipe_ind = 0
        if len(birds) > 0:
            if (
                len(pipes) > 1
                and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width()
            ):
                pipe_ind = 1

        else:  # if there is no bird left
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate(
                (
                    bird.y,
                    abs(bird.y - pipes[pipe_ind].height),
                    abs(bird.y - pipes[pipe_ind].bottom),
                )
            )

            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[
                        x
                    ].fitness -= 1  # if hit the pipe then remove 1 from fitness score
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if (
                    not pipe.passed and pipe.x < bird.x
                ):  # check if the bird pass by the pipe
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:  # remove the pipe
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(PIPE_DIST))

        for r in rem:  # Get rid of the pipe in the remove array
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if (
                bird.y + bird.img.get_height() >= 730 or bird.y < 0
            ):  # we hit the floor or jump over the screen
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        if score > 50:
            break

        base.move()
        draw_window(win, birds, pipes, base, score, GENS)

#########################################################################
# Set up NEAT
def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    p = neat.Population(config)  # set population

    # give the output
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)  # call the main 50 times

#########################################################################
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)  # Get path to the current dir
    config_path = os.path.join(local_dir, "algorithms/neat/config-feedforward.txt")
    run(config_path)
