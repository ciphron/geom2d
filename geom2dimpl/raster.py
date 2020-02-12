from geom2d import Plane, Point, Circle, Color
from math import sqrt, floor, pi, cos, sin, acos, asin

class Raster(object):
    def __init__(self, width, height):
        self._width = width
        self._height = height

    def set_pixel(self, x, y, color):
        pass

    def flush(self):
        pass

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height


class RasterPlane(Plane):
    def __init__(self, width, height, raster):
        super(RasterPlane, self).__init__(width, height)
        self._raster = raster
        self._wratio = float(raster.width) / self.width
        self._hratio = float(raster.height) / self.height

    def draw_line(self, start, end, color):
        delta_x = end.x - start.x
        delta_y = end.y - start.y
        npoints = self.line_span(start.distance_to(end))
        x = start.x
        if delta_x == 0:
            step = float(delta_y) / npoints
            y = start.y
            for i in range(npoints):
                self.draw_point(Point(x, y), color)
                y += step
        else:
            slope = delta_y / delta_x
            step = float(delta_x) / npoints
        
            c = start.y - x*slope
            for i in range(npoints):
                y = x*slope + c
                self.draw_point(Point(x, y), color)
                x += step
            
 
    def draw_circle(self, circle, color):
        npoints = int(round(circle.radius * max(self._wratio, self._hratio) * self._wratio**2))
        step = 1.0 / self._wratio**2
        x = circle.center.x - circle.radius
        while x < circle.center.x - (circle.radius * 0.9):
            ys = circle.eval_at_x(x)
            for y in ys:
                self.draw_point(Point(x, y), color)
                self.draw_point(Point((circle.center.x - x) + circle.center.x,
                                      y), color)
            x += step

        step *= self._wratio / 2.0
        while x <= circle.center.x:
            ys = circle.eval_at_x(x)
            for y in ys:
                self.draw_point(Point(x, y), color)
                self.draw_point(Point((circle.center.x - x) + circle.center.x,
                                      y), color)
            x += step


    # start and end are normalized angles on the unit interval
    # moving in an anticlockwise direction
    def draw_arc(self, center, radius, start, end, color):
        start_rad = start * 2*pi
        end_rad = end * 2*pi
        delta = end_rad - start_rad
        if end_rad < start_rad:
            delta += 2*pi
        step = delta / (max(self._wratio, self._hratio)**2)
        npoints = int(abs(delta / step))
        current_rad = start_rad
        for i in range(npoints):
            point = Point(center.x + radius*cos(current_rad),
                          center.y - radius*sin(current_rad))
            self.draw_point(point, color)
            current_rad += step
            

    def line_span(self, dist):
        wratio = float(self._raster.width) / self.width
        hratio = float(self._raster.height) / self.height
        return int(round(40 * dist * max(wratio, hratio)))

    def draw_point(self, point, color):
        if color is not None:
            self._raster.set_pixel(int(round(point.x * self._wratio)),
                                   int(round(point.y * self._hratio)), color)
