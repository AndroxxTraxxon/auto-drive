from fractions import Fraction
import math

class Vector:

    def __init__(self, value, value2=None):
        if isinstance(value, (int, float, Fraction)) and isinstance(value2, (int, float, Fraction)):
            self.x, self.y = value, value2
        elif not isinstance(value, (self.__class__, tuple, list)):
            raise ValueError("%s.__init__ is not defined for %s" % (self.__class__.__name__, value.__class__.__name__))
        elif isinstance(value, self.__class__):
            self.x = value.x
            self.y = value.y
        else:
            self.x, self.y = value
        self.x = Fraction(self.x)
        self.y = Fraction(self.y)

    def __iadd__(self, other):
        if not isinstance(other, (self.__class__, tuple, list)):
            raise ValueError("__iadd__ is not defined between %s and %s" % (self.__class__.__name__, other.__class__.__name__))
        if isinstance(other, (tuple, list)):
            x, y = other
            self.x += x
            self.y += y
            return self

        else:
            self.x += other.x
            self.y += other.y
            return self

    def __add__(self, other):
        if not isinstance(other, (self.__class__, tuple, list)):
            raise ValueError("__add__ is not defined between %s and %s" % (self.__class__.__name__, other.__class__.__name__))
        if isinstance(other, (tuple, list)):
            x, y = other
            x += self.x
            y += self.y
            return self.__class__(x,y)

        else:
            x, y = other.x, other.y
            x += self.x
            y += self.y
            return self.__class__(x,y)

    def __isub__(self, other):
        if not isinstance(other, (self.__class__, tuple, list)):
            raise ValueError("__isub__ is not defined between %s and %s" % (self.__class__.__name__, other.__class__.__name__))
        if isinstance(other, (tuple, list)):
            x, y = other
            self.x -= x
            self.y -= y
            return self

        else:
            self.x -= other.x
            self.y -= other.y
            return self

    def __sub__(self, other):
        if not isinstance(other, (self.__class__, tuple, list)):
            raise ValueError("__sub__ is not defined between %s and %s" % (self.__class__.__name__, other.__class__.__name__))
        if isinstance(other, (tuple, list)):
            x, y = other
        else:
            x, y = other.x, other.y
        return self.__class__(self.x - x, self.y - y)

    def __eq__(self, other):
        if not isinstance(other, (self.__class__, tuple)):
            return False
        if self.y != other.y:
            return False
        if self.x != other.x:
            return False
        return True
    
    def __ne__(self, other):
        return not self == other

    def __mul__(self, other):
        if not isinstance(other, (int, float, Fraction)):
            raise ValueError("__mul__ is not defined between %s and %s" % (self.__class__.__name__, other.__class__.__name__))
        return self.__class__(self.x * other, self.y * other)

    def __rmul__(self, other):
        if not isinstance(other, (int, float, Fraction)):
            raise ValueError("__rmul__ is not defined between %s and %s" % (self.__class__.__name__, other.__class__.__name__))
        return self.__class__(self.x * other, self.y * other)
        
    def __imul__(self, other):
        if not isinstance(other, (int, float, Fraction)):
            raise ValueError("__imul is not defined between %s and %s" % (self.__class__.__name__, other.__class__.__name__))
        self.x *= other
        self.y *= other

        return self

    def __truediv__(self, other):
        if not isinstance(other, (int, float, Fraction)):
            raise ValueError("__truediv__ is not defined between %s and %s" % (self.__class__.__name__, other.__class__.__name__))
        return self.__class__(self.x / other, self.y / other)
        

    def __rtruediv__(self, other):
        if not isinstance(other, (int, float, Fraction)):
            raise ValueError("__rtruediv__ is not defined between %s and %s" % (self.__class__.__name__, other.__class__.__name__))
        return self.__class__(self.x / other, self.y / other)
        
    def __itruediv__(self, other):
        if not isinstance(other, (int, float, Fraction)):
            raise ValueError("__itruediv__ is not defined between %s and %s" % (self.__class__.__name__, other.__class__.__name__))
        self.x /= other
        self.y /= other

        return self

    def __str__(self):
        return "<%s : (%.01f, %.01f)>" % (self.__class__.__name__, self.x, self.y)

    @property
    def norm(self):
        return (self.x ** 2 + self.y ** 2) ** .5

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    @property
    def as_tuple(self):
        return (float(self.x), float(self.y))

    @classmethod
    def from_heading(cls, heading) -> 'Vector':
        return cls(-math.sin(heading), math.cos(heading))

import enum

class Orientation(enum.Enum):
    COLINEAR = 0
    CLOCKWISE = 1
    COUNTER_CLOCKWISE = 2

def gcd(a, b):
    if a == 0 or b == 0:
        return 1
    A = max(abs(a), abs(b))
    B = min(abs(a), abs(b))
    C = A % B
    while C != 0:
        A, B = B, C
        C = A % B
    
    return B

class Line:
    
    def __init__(self, a, b, c):
        """ standard form: a*x + b*y = c """
        d = gcd(a, gcd(b, c))
        self.a, self.b, self.c = Fraction(a)/d, Fraction(b)/d, Fraction(c)/d

    @classmethod
    def slope_intercept(cls, m, b) -> "Line":
        m = Fraction(m)
        n = Fraction(m.numerator)
        d = Fraction(m.denominator)
        return cls(-n, d, d*b)

    @classmethod
    def from_points(cls, a:Vector, b:Vector) -> "Line":
        A = Fraction(a.y - b.y)
        B = Fraction(b.x - a.x)
        C = Fraction(a.y * (b.x - a.x) + a.x * (a.y - b.y))
        return cls(A,B,C)

    def __matmul__(self, other) -> Vector:
        det = Fraction(self.a * other.b) - Fraction(self.b * other.a)
        if det == 0:
            # Parallel
            return None
        det_inv = 1/det
        x = (det_inv * other.b * self.c) - (det_inv * self.b * other.c)
        y = (det_inv * self.a  * other.c) - (det_inv * other.a * self.c)
        return Vector(x,y)

    def __floordiv__(self, other) -> bool:
        """ returns whether the two lines are parallel """
        assert isinstance(other, self.__class__)
        if self.b == 0:
            if other.b == 0:
                return self.a == other.a
            return False
        return self.a / self.b == other.a / other.b

    def __eq__(self, other) -> bool:
        c_self = self.c/gcd(self.a, gcd(self.b, self.c))
        c_other = other.c/gcd(other.a, gcd(other.b, other.c))
        return self // other and c_self == c_other

    def __contains__(self, point:Vector):
        return self.a*point.x + self.b*point.y == self.c

    def __str__(self) -> str:
        return "%s: %sx + %sy = %s" % (self.__class__.__name__, str(self.a), str(self.b), str(self.c))


class Segment:

    def __init__(self, a:Vector, b:Vector):
        if type(a) == tuple:
            a = Vector(a)
        if type(b) == tuple:
            b = Vector(b)
        self.a = a
        self.b = b
    
    @property
    def line(self):
        return Line.from_points(self.a, self.b)

    def __floordiv__(self, other:Line):
        return self.line // other.line

    def __matmul__(self, other) -> Vector:
        if self // other:
            if ( # the segments have a portion overlapping
                max(self.a.x, self.b.x) >= min(other.a.x, other.b.x) and 
                max(other.a.x, other.b.x) >= min(self.a.x, self.b.x) and

                max(self.a.y, self.b.y) >= min(other.a.y, other.b.y) and 
                max(other.a.y, other.b.y) >= min(self.a.y, self.b.y)
            ):
                key = None
                if(self.a.x == self.b.x): # if this is a vertical line, use the y's instead
                    key=lambda p: p.y
                else:
                    key = lambda p: p.x
                points = sorted((self.a, self.b, other.a, other.b), key=key)
                return points[1]

        else:
            intersect = self.line @ other.line
            if intersect in self and intersect in other:
                return intersect
        return None
    
    def __eq__(self, other):
        if self.a == other.a:
            return self.b == other.b
        return self.b == other.a and self.a == other.b

    def __contains__(self, point:Vector):
        if (min(self.a.x, self.b.x) <= point.x <= max(self.a.x, self.b.x) and 
                min(self.a.y, self.b.y) <= point.y <= max(self.a.y, self.b.y)
            ):
            return point in self.line
        return False