def main():
    bird = Bird(230, 350)
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

        # bird.move()
        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(PIPE_DIST))

        for r in rem:  # Get rid of the pipe in the remove array
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730:  # we hit the floor
            pass

        base.move()
        draw_window(win, bird, pipes, base, score)
    pygame.quit()
    quit()
