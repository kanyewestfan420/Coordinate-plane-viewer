from abc import ABC, abstractmethod
import pygame
import math


class Object(ABC):

    @abstractmethod
    def __init__(
        self, screen, coordinates, color=(
            255, 255, 255), font=pygame.font.Font(
            None, 32)):
        self.color = color
        self.screen = screen
        self.coordinates = coordinates
        self.font = font


class Axes(Object):

    def __init__(
        self, screen, length=1, pixel_length=100, coordinates=(
            100, 900), color=(
            255, 255, 255), x_axis_color=(
                255, 0, 0), y_axis_color=(
                    0, 255, 0), z_axis_color=(
                        0, 0, 255)):
        super().__init__(screen, coordinates, color)
        size = (coordinates[1] - coordinates[0], 10)
        self.x_axis = pygame.Rect(coordinates, (size[0] + size[1], size[1]))
        self.y_axis = pygame.Rect(
            (coordinates[0], coordinates[0]), (size[1], size[0]))
        self.length = length
        self.pixel_length = pixel_length
        self.x_axis_color = x_axis_color
        self.y_axis_color = y_axis_color
        self.z_axis_color = z_axis_color
        self.mode = "x"

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
        if self.mode == "z":
            pygame.draw.rect(self.screen, self.z_axis_color, self.x_axis)
        else:
            pygame.draw.rect(self.screen, self.x_axis_color, self.x_axis)
        pygame.draw.rect(self.screen, self.y_axis_color, self.y_axis)

        for i, line in enumerate(self.y_axis_lines):
            pygame.draw.rect(self.screen, self.color, line)
            text = self.font.render(
                str(len(self.y_axis_lines) - i), True, self.color)
            self.screen.blit(text, (line.x - 50, line.y))

        for i, line in enumerate(self.x_axis_lines):
            pygame.draw.rect(self.screen, self.color, line)
            text = self.font.render(str(i + 1), True, self.color)
            self.screen.blit(text, (line.x, line.y + 80))

    def calculate_point_plane(self, point, point_radius):
        x = self.coordinates[0] + \
            (self.pixel_length * (self.length * point[0]))
        y = self.coordinates[1] - \
            (self.pixel_length * (self.length * point[1]))
        z = self.coordinates[0] + \
            (self.pixel_length * (self.length * point[2]))
        return ((x + point_radius, y + point_radius, z + point_radius))

    def calculate_many_points(self, points, point_radius):
        for point in points:
            point[1] = self.calculate_point_plane(point, point_radius)
        return points

    def change_mode(self):
        if self.mode == "x":
            self.mode = "z"
        else:
            self.mode = "x"


class Point(Object):

    def __init__(
            self,
            screen, plane_coordinates, coordinates, color=(255, 255, 255),
            radius=5,
            text=True):
        super().__init__(screen, coordinates, color)
        self.radius = radius
        self.plane_coordinates = plane_coordinates
        self.lines = []
        self.text = text
        self.selected = False

    def draw(self, mode):
        coordinates = self.account_for_mode(mode)
        if self.lines:
            self.draw_lines(coordinates, mode)
        if self.selected:
            pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            coordinates,
            self.radius+2)
        pygame.draw.circle(
            self.screen,
            self.color,
            coordinates,
            self.radius)
        if self.text:
            self.draw_text(coordinates)

    def draw_lines(self, coordinates, mode):
        for line in self.lines:
            if line[4] == mode:
                pygame.draw.line(
                    self.screen,
                    line[1],
                    coordinates,
                    line[0],
                    self.radius)
                self.draw_line_text(line, mode)

    def draw_text(self, coordinates):
        text = self.font.render(str(self.plane_coordinates), True, self.color)
        self.screen.blit(
            text, (coordinates[0] + 10, coordinates[1] + 10))

    def draw_line_text(self, line, mode):
        coordinates = line[3]
        text = self.font.render(str(line[2]), True, line[1])
        self.screen.blit(
            text, (coordinates[0] + 10, coordinates[1] + 10))

    def check_mouse(self, pos, mode):
        coordinates = self.account_for_mode(mode)
        if math.sqrt((coordinates[0] - pos[0])**2 +
                     (coordinates[1] - pos[1]) ** 2) <= self.radius:
            return self
        return None

    def add_line(self, end_point, mode):
        if end_point == self:
            return
        for line in self.lines:
            if line[0] == end_point.coordinates:
                return

        end_coordinates = self.account_for_mode(mode, coordinates=end_point.coordinates)
        coordinates = self.account_for_mode(mode)
        
        plane_coords = self.account_for_mode(mode, coordinates=self.plane_coordinates)
        end_plane_coords = self.account_for_mode(mode, coordinates=end_point.plane_coordinates)
        
        self.lines.append(
            (end_coordinates,
             self.get_average_color(
                 end_point.color),
            # Length to display
                math.sqrt(
                 (plane_coords[0] - end_plane_coords[0])**2 + (
                     plane_coords[1] - end_plane_coords[1]) ** 2),
            # Coordinates of text
                ((coordinates[0] + end_coordinates[0]) / 2,
                 (coordinates[1] + end_coordinates[1]) / 2), mode))

    def get_average_color(self, point_color):
        color = []
        for i in range(3):
            color.append((self.color[i] + point_color[i]) / 2)
        return tuple(color)

    def account_for_mode(self, mode, coordinates=None):
        if not coordinates:
            coordinates = self.coordinates
        if mode == "x":
            coordinates = (coordinates[0], coordinates[1])
        else:
            coordinates = (coordinates[2], coordinates[1])
        return coordinates

class CommandBox(Object):

    def __init__(
        self,
        screen,
        screen_heigth,
        heigth=70,
        color=(
            255,
            255,
            255)):
        coordinates = (32, screen_heigth - heigth)
        super().__init__(screen, coordinates, color)

    def draw(self, text):
        text = self.font.render(text, True, self.color)
        self.screen.blit(text, (self.coordinates))
