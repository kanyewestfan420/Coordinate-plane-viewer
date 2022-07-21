import pygame
from pygame.locals import QUIT

pygame.init()
# This has to be before because otherwise you get an error
from objects import Axes, Point, CommandBox

fps = 60
fpsClock = pygame.time.Clock()

width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Epic line drawing program")

BACKGROUND_COLOR = (0, 0, 0)


def add_point(plane_coordinates, color=(255, 255, 255)):
    points.append(
        Point(
            screen,
            plane_coordinates,
            axes.calculate_point_plane(
                (plane_coordinates),
                POINT_RADIUS), color))


def check_if_point_exists(pos):
    for point in points:
        found_point = point.check_mouse(pos, axes.mode)
        if found_point:
            return point

def deselect_points():
    for point in points:
        point.selected = False


def clear_dots():
    points.clear()


def process_command(command):
    # This could probably be made better
    r = 3.14159265359
    command_list = {"clear": clear_dots}
    try:
        action = command_list.get(command)
        action()
    except TypeError:
        pass
    try:
        command = eval(command)
    except (NameError, SyntaxError, TypeError):
        pass
    if isinstance(command, tuple):
        if len(command) == 3:
            add_point(command)
        elif len(command) == 6:
            add_point((command[0], command[1], command[2]), (round(
                command[3]), round(command[4]), round(command[5])))


POINT_RADIUS = 5

axes = Axes(screen)
commandbox = CommandBox(screen, height)

points = [Point(
    screen, (5, 4, 2), axes.calculate_point_plane(
            (5, 4, 1), POINT_RADIUS), (255, 0, 255)),
          Point(
    screen, (3, 1, 4), axes.calculate_point_plane(
        (3, 1, 4), POINT_RADIUS), (0, 255, 0))]

start_point = None
end_point = None
command = ""

while True:
    screen.fill(BACKGROUND_COLOR)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                if not end_point and start_point:
                    end_point = check_if_point_exists(pos)
                    if end_point:
                        start_point.add_line(end_point, axes.mode)
                    start_point = None
                    end_point = None
                else:
                    start_point = check_if_point_exists(pos)
                if not start_point:
                    start_point = None
                    deselect_points()
                else:
                    start_point.selected = True
            elif event.button == 3:
                point_del = check_if_point_exists(pos)
                if point_del in points:
                    points.remove(point_del)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                axes.change_mode()
            elif event.key == pygame.K_BACKSPACE:
                command = command[:-1]
            elif event.key == pygame.K_RETURN:
                process_command(command)
                command = ""
            else:
                command += event.unicode
            
    axes.draw_axes()
    for point in points:
        point.draw(axes.mode)
    commandbox.draw(command)
    pygame.display.flip()
    fpsClock.tick(fps)
