import Tkinter
from geom2d import Plane, Circle, Point, Color

def color_to_str(color):
    return '#%02X%02X%02X' % (color.red, color.green, color.blue)

class TkinterCanvasPlane(Plane):
    def __init__(self, width, height, canvas):
        super(TkinterCanvasPlane, self).__init__(width, height)
        config = canvas.config()
        self._canvas_width = int(config['width'][4])
        self._canvas_height = int(config['height'][4])
        self._canvas = canvas

    def draw_line(self, start, end, color):
        sx, sy = self._transform(start)
        ex, ey = self._transform(end)
        self._canvas.create_line(sx, xy, ex, ey, outline=color_to_str(color))

    def draw_circle(self, circle, color):
        x1, y1, x2, y2 = self._circle_to_rect(circle)
        self._canvas.create_oval(x1, y1, x2, y2, outline=color_to_str(color))

    # start and extent are normalized angles on the unit interval
    # moving in an anticlockwise direction
    def draw_circle_arc(self, circle, start, extent, color):
        x1, y1, x2, y2 = self._circle_to_rect(circle)
        start_deg = (start % 1.0) * 360
        extent_deg = (extent % 1.0) * 360
        self._canvas.create_arc((x1, y1, x2, y2), start=start_deg,
                                extent=extent_deg, style='arc',
                                outline=color_to_str(color))
        

    def _transform(self, point):
        x = int(round((float(point.x) / self.width) * self._canvas_width))
        y = int(round((float(point.y) / self.height) * self._canvas_height))
        return (x, y)

    def _circle_to_rect(self, circle):
        x1, y1 = self._transform(Point(circle.center.x - circle.radius,
                                       circle.center.y - circle.radius))
        x2, y2 = self._transform(Point(circle.center.x + circle.radius,
                                       circle.center.y + circle.radius))
        return (x1, y1, x2, y2)
