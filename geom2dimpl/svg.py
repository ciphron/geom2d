from geom2d import Plane
from math import sqrt, floor, pi, cos, sin, acos, asin
import svgwrite

class SVGPlane(Plane):
    MAGNIFIER = 100
    
    def __init__(self, plane_width, plane_height, filename,
                 drawing_width=None):
        super(SVGPlane, self).__init__(plane_width, plane_height)
        dw = 0
        dh = 0
        if drawing_width is None:
            dw = round(plane_width * self.MAGNIFIER)
        else:
            dw = round(drawing_width)
        dh = round((float(plane_height) / plane_width) * dw)
        self._dwg = svgwrite.Drawing(filename=filename,
                                     size=(dw, dh))
        self._drawing_width = dw
        self._drawing_height = dh

    def draw_line(self, start, end, color):
        self._dwg.add(self._dwg.line(start=self._scale(start.topair()),
                                     end=self._scale(end.topair()),
                                     stroke=color_to_str(color)))

    def draw_circle(self, circle, color):
        scircle = self._dwg.circle(center=self._scale(circle.center.topair()),
                                   r=self._scale(circle.radius),
                                   fill='none',
                                   stroke=color_to_str(color))
        self._dwg.add(scircle)

    def draw_point(self, point, color):
        srect = self._dwg.rect(insert=self._scale(point.topair()),
                               size=(2*mm, 2*mm),
                               fill=color_to_str(color))
        self._dwg.add(srect)


    # start and end are normalized angles on the unit interval
    # moving in an anticlockwise direction
    def draw_arc(self, center, radius, start, end, color):
        ordered = [start % 1.0, end % 1.0]
        ordered.sort()
        is_large = 0
        is_sweep = 0
        if end < start:
            is_large = 1
            is_sweep = 1
            d = start - end
            if d < 0:
                t += 1
            if d > 0.5: 
                is_large = 0
        else:
            if end - start > 0.5:
                is_large = 1

        start_radians = ordered[0] * 2*pi
        end_radians = ordered[1] * 2*pi
        x0 = center.x + radius*cos(start_radians)
        y0 = center.y - radius*sin(start_radians)
        x0, y0 = self._scale((x0, y0))
        
        x1 = center.x + radius*cos(end_radians)
        y1 = center.y - radius*sin(end_radians)
        x1, y1 = self._scale((x1, y1))

        m0 = round(x0, 2)
        n0 = round(y0, 2)
        r = round(self._scale(radius), 2)
        m1 = round((x1 - x0), 2)
        n1 = round((y1 - y0), 2)
        dstr = "M {0},{1} a {2},{2} 0 {3},{4} {5},{6}".format(m0, n0,
                                                          r,
                                                          is_large,
                                                          is_sweep,
                                                          m1, n1)
        sarc = self._dwg.path(d=dstr, stroke=color_to_str(color),
                              fill="none")
        self._dwg.add(sarc)
        
    def save(self):
        self._dwg.save()

    def _scale(self, p):
        if isinstance(p, tuple):
            x0, y0 = p
            x1 = (float(x0) / self.width) * self._drawing_width
            y1 = (float(y0) / self.height) * self._drawing_height
            return (round(x1, 2), round(y1, 2))
        else:
            h_plane = sqrt(self.width**2 + self.height**2)
            h_drawing = sqrt(self._drawing_width**2 + self._drawing_height**2)
            return round((p / h_plane) * h_drawing, 2)

def color_to_str(color):
    return '#%02X%02X%02X' % (color.red, color.green, color.blue)
