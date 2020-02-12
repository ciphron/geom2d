from raster import Raster
import geom2d
from PIL import Image

class ImageRaster(Raster):
    def __init__(self, width, height, color=geom2d.BLACK):
        super(ImageRaster, self).__init__(width, height)
        self._img = Image.new('RGB', (width, height),
                              color=color.totuple())
        self._pixels = self._img.load()

    def set_pixel(self, x, y, color):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            self._pixels[x, y] = (color.red, color.green, color.blue)

    def flush(self):
        pass
    
    def save(self, filename, image_format=None):
        self._img.save(filename, image_format)        
