import tkinter as tk
import drawing
import math
import threading

from dim2 import Vector, Segment

class Entity:

    def move(self):
        raise NotImplementedError()

class Car(Entity):

    def __init__(self, world, position):
        self.world = world
        self.position = Vector(position)
        self.velocity = Vector(0,0)
        self.size = Vector(20, 40)
        self.heading = math.pi
        self.accel = 0
        self.ang_v = 0
        self.view_distance = 400

    def render(self, canvas: tk.Canvas):
        drawing.draw_rect(canvas, self.position, self.size, self.heading, fill="blue")
        for _, sensor in self.sensors:
            drawing.draw_line(canvas, sensor)
        for point in self.detected_obstacles:
            drawing.draw_dot(canvas, point)
        # canvas.create_line(*self.position.as_tuple, *(self.direction * self.view_distance + self.position).as_tuple)

    @property
    def sensor_directions(self):
        for angle in (-math.pi/2, -math.pi/4, -math.pi/8, 0, math.pi/8, math.pi/4, math.pi/2, math.pi):
            yield Vector.from_heading(self.heading + angle)

    @property
    def sensors(self):
        for direction in self.sensor_directions:
            yield direction, Segment(
                self.position, 
                (direction * self.view_distance) + self.position
            )

    @property
    def detected_obstacles(self):
        for direction, sensor in self.sensors:
            closest = self.view_distance
            for wall in self.world.outer_walls():
                detected = wall@sensor
                if detected is not None:
                    if closest is not None:
                        if closest > (detected - self.position).norm:
                            closest = detected.norm
            for wall in self.world.inner_walls():
                detected = wall@sensor
                if detected is not None:
                    if closest is not None:
                        if closest > (detected - self.position).norm:
                            closest = detected.norm
            # print(closest, direction.norm)
            yield (closest * direction) + self.position
            

    @property
    def direction(self)-> Vector:
        return Vector.from_heading(self.heading)

    def move(self):
        self.velocity += self.accel * self.direction
        if self.velocity.norm != 0.0:
            self.velocity *= ((abs(self.direction.dot(self.velocity)))/(self.velocity.norm))**0.25
        self.position += self.velocity
        self.heading += self.ang_v



class World:

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.car = Car(self, (150, 500))
        self.outer_points = list()
        self.inner_points = list()
        self.car.accel = 0.001
        self.car.ang_v = 0.001

    def load_points(self, inner_points, outer_points):
        self.inner_points = inner_points
        self.outer_points = outer_points


    def outer_walls(self):
        if len(self.outer_points) < 2:
            return
        i = 0
        while i < len(self.outer_points):
            yield Segment(self.outer_points[i-1], self.outer_points[i])
            i += 1

    def inner_walls(self):
        if len(self.inner_points) < 2:
            return
        i = 0
        while i < len(self.inner_points):
            yield Segment(self.inner_points[i-1], self.inner_points[i])
            i += 1

    def draw_terrain(self):
        return 
        for point in self.outer_points:
            drawing.draw_dot(self.canvas, point, fill="black")

        for wall in self.outer_walls():
            drawing.draw_line(self.canvas, wall, fill="black")
        
        for point in self.inner_points:
            drawing.draw_dot(self.canvas, point, fill="red")

        for wall in self.inner_walls():
            drawing.draw_line(self.canvas, wall, fill="red")
        

    def render(self):
        self.draw_terrain()
        self.car.render(self.canvas)

    def tick(self):
        self.car.move()