from math import sqrt, floor, pi, cos, sin, acos, asin
import random

FP_THRESHOLD = 0.00000001
PRECISION_DIGITS = 5


def _quadratic_roots(a, b, c):
    roots = set()
    discrim = b**2 - 4*a*c
    if a != 0 and discrim >= 0:
        roots.add((-b + sqrt(discrim)) / (2*a))
        roots.add((-b - sqrt(discrim)) / (2*a))  
    return roots

class Point(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def distance_to(self, other):
        deltax = other.x - self.x
        deltay = other.y - self.y

        return sqrt(deltax*deltax + deltay*deltay)

    def topair(self):
        return (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

class Circle(object):
    def __init__(self, center, radius):
        self._center = center
        self._radius = radius

    @property
    def center(self):
        return self._center

    @property
    def radius(self):
        return self._radius

    def eval_at_x(self, x):
        rhs = self.radius*self.radius - (x - self.center.x)*(x - self.center.x)
        if rhs < FP_THRESHOLD:
            rhs = 0

        if self.radius < 0:
            return []

        y = sqrt(rhs)
        if y == 0:
            return [self.center.y]
        return [self.center.y - y, self.center.y + y]

    def eval_at_y(self, y):
        rhs = self.radius*self.radius - (y - self.center.y)*(y - self.center.y)
        if rhs < FP_THRESHOLD:
            rhs = 0

        if self.radius < 0:
            return []

        x = sqrt(rhs)
        if x == 0:
            return [self.center.x]
        return [self.center.x - x, self.center.x + x]

    def intersection(self, other):
        x1 = float(self.center.x)
        y1 = float(self.center.y)
        x2 = float(other.center.x)
        y2 = float(other.center.y)
        r1 = float(self.radius)
        r2 = float(other.radius)

        d = 0
        inter = []
        if y1 - y2 == 0:
            if x1 - x2 == 0:
                return inter
            d = 1 / (x1 - x2)
            k = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2

            c = -r1**2 + x1**2 + y1**2 + \
                k*x1*d + \
                0.25*(k**2)*(d**2)

            b = -2*y1 + 2*(y1 - y2)*x1*d + \
                k*(y1 - y2)*(d**2)
            
            a = ((y1 - y2)**2)*(d**2) + 1

            roots = _quadratic_roots(a, b, c)
            for y in roots:
                xs1 = set(map(lambda x: round(x, PRECISION_DIGITS),
                              self.eval_at_y(y)))
                xs2 = set(map(lambda x: round(x, PRECISION_DIGITS),
                              other.eval_at_y(y)))
                common = xs1.intersection(xs2)
                if len(common) > 0:
                    x = xs1.intersection(xs2).pop()
                    inter.append(Point(x, y))
        else:
            d = 1 / (y1 - y2)
            k = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2

        
            c = -r1**2 + x1**2 + y1**2 + \
                k*y1*d + \
                0.25*(k**2)*(d**2)

            b = -2*x1 + 2*(x1 - x2)*y1*d + \
                k*(x1 - x2)*(d**2)

            a = ((x1 - x2)**2)*(d**2) + 1

            roots = _quadratic_roots(a, b, c)
            for x in roots:
                ys1 = set(map(lambda y: round(y, PRECISION_DIGITS),
                              self.eval_at_x(x)))
                ys2 = set(map(lambda y: round(y, PRECISION_DIGITS),
                              other.eval_at_x(x)))
                common = ys1.intersection(ys2)
                if len(common) > 0:
                    y = ys1.intersection(ys2).pop()
                    inter.append(Point(x, y))

        return inter

    def contains(self, point):
        return self.center.distance_to(point) < self.radius

    def __eq__(self, other):
        return self.radius == other.radius and self.center == other.center

    def __hash__(self):
        return hash((self.radius, self.center))
        

class Color(object):
    MAX_PIXEL = 0xFF
    
    def __init__(self, red, green, blue):
        self._red = red
        self._green = green
        self._blue = blue

    def totuple(self):
        return (self.red, self.green, self.blue)

    @property
    def red(self):
        return self._red

    @property
    def green(self):
        return self._green

    @property
    def blue(self):
        return self._blue

BLACK = Color(0, 0, 0)
WHITE = Color(Color.MAX_PIXEL, Color.MAX_PIXEL, Color.MAX_PIXEL)
RED = Color(Color.MAX_PIXEL, 0, 0)
GREEN = Color(0, Color.MAX_PIXEL, 0)
BLUE = Color(0, 0, Color.MAX_PIXEL)

def rand_color():
    parts = [random.randint(0, Color.MAX_PIXEL) for i in range(3)]
    return Color(parts[0], parts[1], parts[2])


class Plane(object):
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def draw_point(self, point, color):
        pass

    def draw_line(self, start, end, color):
        pass

    def draw_circle(self, circle, color):
        pass

    # start and end are normalized angles on the unit interval
    # moving in an anticlockwise direction
    def draw_arc(self, center, radius, start, end, color):
        pass



