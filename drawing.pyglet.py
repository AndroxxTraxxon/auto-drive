import pyglet.gl as gl
import pyglet.graphics as graphics
import dim2

class Polygon:

    def __init__(self, *vectors, color=(100, 200, 220), colors=None, draw_method=gl.GL_TRIANGLES, z=0,):
        self.vectors = []
        for vector in vectors:
            if type(vector) == tuple:
                vector = dim2.Vector(vector)
            assert isinstance(vector, dim2.Vector)
            self.vectors.append(vector)

        if colors is not None:
            self.colors = colors
        else:
            self.colors = color * len(self.vectors)
        
        self.draw_method = draw_method
        self.z=0

    def render(self, method=None):
        if method is None:
            method = self.draw_method
        self.vertices.draw(method)

    @property
    def vertices(self):
        points = tuple(dim for v in self.vectors for dim in (*v.as_tuple, self.z))
        print(len(self.vectors))
        return graphics.vertex_list(
            len(self.vectors),
            ('v3f', points),
            ('c3B', self.colors)
        )

class Triangle(Polygon):
    def __init__(self, *args, **kwargs):
        assert len(args) == 3
        kwargs["draw_method"] = gl.GL_TRIANGLES
        super().__init__(*args, **kwargs)

class Rect(Polygon):

    def __init__(self, *args, indices=(0,1,2, 2,3,0), **kwargs):
        assert len(args) == 4
        kwargs["draw_method"] = gl.GL_TRIANGLES
        self.indices = indices
        super().__init__(*args, **kwargs)

    @property
    def vertices(self):
        return graphics.vertex_list_indexed(
            len(self.vectors), self.indices,
            ('v3f', tuple(dim for v in self.vectors for dim in (*v.as_tuple, self.z))),
            ('c3B', self.colors)
        )