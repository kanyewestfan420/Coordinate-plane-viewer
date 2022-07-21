from abc import ABC, abstractmethod
import pygame
import numpy as np
import math


class Object(ABC):

    @abstractmethod
    def __init__(
            self, screen, coordinates=None, color=(255, 255, 255)):
        self.color = color
        self.screen = screen
        self.coordinates = coordinates


class Axes(Object):

    def __init__(
        self, screen, length=1, pixel_length=100, coordinates=(
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
        x = self.coordinates[0] + \
            (self.pixel_length * (self.length * point[0][0]))
        y = self.coordinates[1] - \
            (self.pixel_length * (self.length * point[0][1]))
        return ((x + point_radius, y + point_radius))

    def calculate_many_points(self, points, point_radius):
        for point in points:
            point[1] = self.calculate_point_plane(point, point_radius)
        return points


class PointCollection(Object):

    def __init__(self, screen, points, radius=None, color=None):
        super().__init__(screen, color)
        self.points = points
        self.radius = radius

    def draw(self):
        for point in self.points:
            if not self.color:
                color = self.color
            else:
                color = point[2]
            if not self.radius:
                radius = self.radius
            else:
                radius = point[3]
            pygame.draw.circle(
                self.screen,
                color,
                point[1],
                radius)
            self.draw_text(point[0], point[1], color)
            if point[4]:
                for line in point[4]:
                    # print(len(point[4]))
                    pygame.draw.line(
                        self.screen, line[1], point[1], line[0], 5)

    def draw_text(self, show_coordinates, coordinates, color):
        font = pygame.font.Font(None, 32)
        text = font.render(str(show_coordinates), True, color)
        self.screen.blit(
            text, (coordinates[0] + 15, coordinates[1] + 15))

    def check_mouse(self, pos):
        for point in self.points:
            if self.radius:
                radius = self.radius
            else:
                radius = point[3]
            if math.sqrt((point[1][0] - pos[0])**2 +
                         (point[1][1] - pos[1]) ** 2) <= radius:
                return point
        return None

    def add_line(self, start_point, end_point):
        for point in self.points:
            if point[1] == start_point[1] and point[1] != end_point[1]:
                for line in point[4]:
                    if line[0] == end_point[1]:
                        return
                line = []
                line.append(end_point[1])
                line.append(
                    self.get_average_color(
                        start_point, end_point))
                line.append(math.sqrt((point[0][0] - end_point[0][0])**2 + (point[0][1] - end_point[0][0]) ** 2))
                point[4].append(line)
                print(point[4])

    def get_average_color(self, point_1, point_2):
        color = []
        for i in range(3):
            color.append((point_1[2][i] + point_2[2][i]) / 2)
        return tuple(color)
