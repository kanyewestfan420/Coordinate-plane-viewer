from abc import ABC, abstractmethod
import copy
import pygame


class Object(ABC):

    @abstractmethod
    def __init__(
            self, screen, coordinates, color=(255, 255, 255)):
        self.color = color
        self.screen = screen
        self.coordinates = coordinates


class Axes(Object):

    def __init__(
        self, screen, length, pixel_length=100, coordinates=(
            100, 900), color=(
            255, 255, 255)):
        super().__init__(screen, coordinates, color)
        size = (coordinates[1] - coordinates[0], 10)
        self.x_axis = pygame.Rect(coordinates, (size[0] + size[1], size[1]))
        self.y_axis = pygame.Rect(
            (coordinates[0], coordinates[0]), (size[1], size[0]))
        self.length = length
        self.pixel_length = pixel_length

        self.x_axis_lines = []
        for i in range(
                coordinates[0] +
                self.pixel_length,
                coordinates[1] +
                self.pixel_length,
                self.pixel_length):
            self.x_axis_lines.append(pygame.Rect(
                i, coordinates[1] - 50, 10, 50))

        self.y_axis_lines = []
        for i in range(coordinates[0], coordinates[1], self.pixel_length):
            self.y_axis_lines.append(pygame.Rect(
                coordinates[0] + 10, i, 50, 10))

    def draw_axes(self):
        pygame.draw.rect(self.screen, self.color, self.x_axis)
        pygame.draw.rect(self.screen, self.color, self.y_axis)
        for line in self.y_axis_lines:
            pygame.draw.rect(self.screen, self.color, line)
        for line in self.x_axis_lines:
            pygame.draw.rect(self.screen, self.color, line)

    def calculate_point_plane(self, point, point_radius):
        # Point(1,1) = 200, 800
        # length = 1
        starting_point = copy.copy(self.coordinates)
        x = self.coordinates[0] + \
            (self.pixel_length * (self.length * point[0]))
        y = self.coordinates[1] - \
            (self.pixel_length * (self.length * point[1]))
        return ((x + 5, y + 5))


class Point(Object):

    def __init__(
        self, screen, show_coordinates, coordinates, size, color=(
            255, 255, 255)):
        super().__init__(screen, coordinates, color)
        self.radius = size * 2
        self.show_coordinates = show_coordinates

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            self.coordinates,
            self.radius)
        self.draw_text()

    def draw_text(self):
        font = pygame.font.Font(None, 32)
        text = font.render(str(self.show_coordinates), True, (255, 255, 255))
        self.screen.blit(
            text, (self.coordinates[0] + 15, self.coordinates[1] + 15))
