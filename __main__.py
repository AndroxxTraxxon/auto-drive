import sys
import os
import math
import re
import tkinter as tk
from tkinter.font import Font, NORMAL, BOLD, ITALIC, ROMAN
import game
from dim2 import Vector
import os
import gui
import csv
import time

pwd = os.path.dirname(os.path.realpath(__file__))
c_width = 1000
c_height = 1000
canvas_size = (c_width, c_height)
world = None


def left_click(event):
    world.outer_points.append((event.x, event.y))


def right_click(event):
    world.inner_points.append((event.x, event.y))

def load_points(event):
    inner = []
    outer = []
    terrain_points = {"inner": inner, "outer": outer}
    try:
        with open(os.path.join(pwd, "path_points.csv")) as terrain_csv:
            reader = csv.DictReader(terrain_csv)
            for item in reader:
                point = int(item['x']), int(item['y'])
                terrain_points[item['side']].append(point)
            world.load_points(inner, outer)

                
    except:
        pass


        
if __name__ == "__main__":
    mainWindow = tk.Tk()
    mainWindow.title("Auto-Drive: CS6375 Spring 2020 Semester Project")
    mainWindow.bind("<space>", load_points)
    frame = tk.Frame(mainWindow)
    frame.pack(fill=tk.BOTH, expand=tk.YES)
    canvas = gui.ResizingCanvas(
        frame, width=c_width, height=c_height, bg="DarkOliveGreen")
    # canvas.bind("<Button-1>", left_click)
    # canvas.bind("<Button-3>", right_click)
    canvas.pack(fill=tk.BOTH, expand=tk.YES)
    world = game.World(canvas)
    load_points(None)
    last_time = time.time()

    while True:
        try:
            this_time = time.time()
            print(1/(this_time-last_time))
            canvas.delete("all")
            world.tick()
            world.render()
            mainWindow.update_idletasks()
            mainWindow.update()
            last_time = this_time
        except tk.TclError as e:
            print("[Warning] %s" % str(e))
            break

try:
    with open(os.path.join(pwd, "path_points.csv"), "w+") as terrain_csv:
        writer = csv.DictWriter(terrain_csv, fieldnames=["x", "y", "side"])
        writer.writeheader()
        points = list()
        print(len(world.outer_points))
        for x, y in world.outer_points :
            points.append({
                "x": x,
                "y": y,
                "side": "outer"
            })
        print(len(world.inner_points))
        for x, y in world.inner_points:
            points.append({
                "x": x,
                "y": y,
                "side": "inner"
            })
        # points = sorted(points, key=lambda p: "%s: %09d" % (p['side'], (p['x']**2 + p['y'])))
        writer.writerows(points)
except:
    pass

print("That's all, folks!")
sys.exit(0)
