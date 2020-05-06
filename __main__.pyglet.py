import pyglet
import pyglet.gl as gl
import pyglet.graphics as graphics
import drawing



class MyWindow(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        gl.glClearColor(0.2, 0.3, 0.2, 0.1)
        self.triangle = drawing.Triangle(
            (-.5, -.5), (.5, -.5), (0, .5)
        )
        self.rect = drawing.Rect(
            (-.5, -.5), (.5, -.5), (.5, .5), (-.5, .5),
            color = (180, 0, 0)
        )

    def on_draw(self):
        self.clear()
        self.rect.draw()
        # self.triangle.draw()

    def on_resize(self, width, height):
        gl.glViewport(0,0,width, height)


if __name__ == "__main__":
    window = MyWindow(1500, 1000, "Auto-Drive: CS6375 Spring 2020 Semester Project", resizable=True)
    window.on_draw()
    pyglet.app.run()
    
