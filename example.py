# Example of how to use geom2d; in this case to draw a simple
# crosshair

import geom2d
from geom2d import Point, Circle

from geom2dimpl.svg import SVGPlane
from geom2dimpl.raster import RasterPlane
from geom2dimpl.image import ImageRaster


PLANE_WIDTH = 12
PLANE_HEIGHT = 9
CROSSHAIR_RADIUS = 3.0

IMAGE_WIDTH = 400
IMAGE_HEIGHT = 300




def draw_crosshair(plane, center, radius):
    circle = Circle(center, radius)
    plane.draw_circle(circle, geom2d.BLACK)
    plane.draw_line(Point(center.x, center.y - radius),
                    Point(center.x, center.y + radius),
                    geom2d.RED)
    plane.draw_line(Point(center.x - radius, center.y),
                    Point(center.x + radius, center.y),
                    geom2d.RED)

planes = []

image_raster = ImageRaster(IMAGE_WIDTH, IMAGE_HEIGHT, geom2d.WHITE)
image_plane = RasterPlane(PLANE_WIDTH, PLANE_HEIGHT, image_raster)
planes.append(image_plane)

svg_plane = SVGPlane(PLANE_WIDTH, PLANE_HEIGHT, 'crosshair.svg')
planes.append(svg_plane)

for plane in planes:
    draw_crosshair(plane, Point(PLANE_WIDTH / 2.0, PLANE_HEIGHT / 2.0),
                   CROSSHAIR_RADIUS)


image_raster.save('crosshair.png')
svg_plane.save()
