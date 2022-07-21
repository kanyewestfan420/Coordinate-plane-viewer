import pygame
from pygame.locals import QUIT
from objects import Axes, PointCollection
import numpy as np
import warnings

pygame.init()
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

fps = 60
fpsClock = pygame.time.Clock()

width, height = 1100, 1100
screen = pygame.display.set_mode((width, height))

POINT_RADIUS = 5

points = []

points = [[[5, 4], [0, 0], [255, 255, 0], 5, []],
          [[3, 1], [0, 0], [0, 255, 0], 5, []]]

# lines = np.empty(shape=(0, 2), dtype=object)

# lines = np.vstack(points, np.asarray([[800, 10], [100, 100]]))

axes = Axes(screen)

points = axes.calculate_many_points(points, POINT_RADIUS)


point_collection = PointCollection(screen, points, POINT_RADIUS)
start_point = None

# Game loop.
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                if start_point:
                    end_point = point_collection.check_mouse(pos)
                    if end_point:
                        point_collection.add_line(start_point, end_point)
                    start_point = None
                    end_point = None
                else:
                    start_point = point_collection.check_mouse(pos)

    axes.draw_axes()
    point_collection.draw()
    pygame.display.flip()
    fpsClock.tick(fps)
