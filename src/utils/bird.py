import pygame
import os

# Load in images
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("docs/imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("docs/imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("docs/imgs", "bird3.png"))),
]


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25  # How much the bird tilts
    ROT_VEL = 20  # How much we rotate the bird each frame
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0  # keep track of image
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0  # keep track when we need to jump
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = (
            self.vel * self.tick_count + 1.5 * self.tick_count ** 2
        )  # displayment = how many pixel goes up or down the frame

        if d >= 16:  # moving down to be more than 16 pixels
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d  # update the position
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):  # win = window
        self.img_count += 1

        # Show what imgs base on the img_count
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # Rotate image around the center
        rotate_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotate_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center
        )
        win.blit(rotate_image, new_rect.topleft)

    # Do collision for image
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
