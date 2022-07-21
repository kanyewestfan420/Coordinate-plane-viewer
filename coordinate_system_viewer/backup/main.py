import pygame
from pygame.locals import QUIT
from objects import Axes, Point
import numpy as np

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 1100, 1100
screen = pygame.display.set_mode((width, height))

POINT_RADIUS = 5

points = np.array([[5, 4], [3, 1], [2, 1]])

axes = Axes(screen, 1)

for point in points:
    point_coord = axes.calculate_point_plane((5, 4), POINT_RADIUS)
    point = Point(screen, (5, 4), point_coord, POINT_RADIUS)


# Game loop.
while True:
    # screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    axes.draw_axes()
    point.draw()
    pygame.display.flip()
    fpsClock.tick(fps)
