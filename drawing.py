import dim2
import tkinter as tk
import math

def rotate(points:list, angle):
    cos_val = math.cos(angle)
    sin_val = math.sin(angle)
    new_points = []
    for x_old, y_old in points:
        x_new = x_old * cos_val + y_old * sin_val
        y_new = x_old * sin_val - y_old * cos_val
        new_points.append((x_new, y_new))
    return new_points

def draw_rect(canvas:tk.Canvas, position:dim2.Vector, size:dim2.Vector, angle:float=0, **kwargs):
    width, height = size.as_tuple
    width = max(2, width)
    height = max(2, height)
    points = list(map(
        lambda x: (position + x).as_tuple,
        rotate((
            (-width/2, -height/2),
            ( width/2, -height/2),
            ( width/2,  height/2),
            (-width/2,  height/2),
        ), angle)
    ))

    canvas.create_polygon(points, **kwargs)

def draw_line(canvas:tk.Canvas, line:dim2.Segment, **kwargs):
    canvas.create_line(*line.a.as_tuple, *line.b.as_tuple, **kwargs)

def draw_dot(canvas:tk.Canvas, p:dim2.Vector, radius=5, **kwargs):
    if type(p) == tuple:
        p = dim2.Vector(p)
    canvas.create_oval(
                float(p.x-radius),
                float(p.y-radius),
                float(p.x+radius),
                float(p.y+radius),
                **kwargs
            )