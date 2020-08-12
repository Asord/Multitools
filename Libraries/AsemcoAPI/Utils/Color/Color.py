from math import floor
from random import randint

class RatioAdjustment:
    def __init__(self, red_green=0.0, red_blue=0.0, green_red=0.0, green_blue=0.0, blue_red=0.0, blue_green=0.0):
        self.red_green  = red_green
        self.red_blue   = red_blue
        self.green_red  = green_red
        self.green_blue = green_blue
        self.blue_red   = blue_red
        self.blue_green = blue_green

    @classmethod
    def fromDict(cls, dct):
        red_green  = dct["rg"] if "rg" in dct else 0.0
        red_blue   = dct["rb"] if "rb" in dct else 0.0
        green_red  = dct["gr"] if "gr" in dct else 0.0
        green_blue = dct["gb"] if "gb" in dct else 0.0
        blue_red   = dct["br"] if "br" in dct else 0.0
        blue_green = dct["bg"] if "bg" in dct else 0.0

        return cls( red_green, red_blue, green_red, green_blue, blue_red, blue_green)

class Color:
    def __init__(self, red=0, green=0, blue=0):

        self._red = 0
        self._green = 0
        self._blue = 0

        if 0 <= red <= 255:   self._red   = int(red)
        if 0 <= green <= 255: self._green = int(green)
        if 0 <= blue <= 255:  self._blue  = int(blue)

    def getRed(self):
        return self._red

    def getGreen(self):
        return self._green

    def getBlue(self):
        return self._blue

    def getColor(self):
        return self._red, self._green, self._blue

    def setRed(self, val):
        self._red = val % 256

    def setGreen(self, val):
        self._green = val % 256

    def setBlue(self, val):
        self._blue = val % 256

    def setColor(self, red, gre, blu):
        if 0 <= red <= 255: self._red   = int(red)
        if 0 <= gre <= 255: self._green = int(gre)
        if 0 <= blu <= 255: self._blue  = int(blu)
        return self

    def fromHex(self, hexVal):
        hexValue = hexVal.replace("#", "")
        self._red   = int(hexValue[0:2], 16)
        self._green = int(hexValue[2:4], 16)
        self._blue  = int(hexValue[4:6], 16)
        return self

    def fromHSV(self, h, s, v):
        h = float(h)
        s = float(s)
        v = float(v)
        h60 = h / 60.0
        h60f = floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0:
            r, g, b = v, t, p
        elif hi == 1:
            r, g, b = q, v, p
        elif hi == 2:
            r, g, b = p, v, t
        elif hi == 3:
            r, g, b = p, q, v
        elif hi == 4:
            r, g, b = t, p, v
        elif hi == 5:
            r, g, b = v, p, q
        self._red, self._green, self._blue = int(r * 255), int(g * 255), int(b * 255)

        return self
 
    def fromHue(self, h):
        h = float(h)
        h60 = h / 60.0
        h60f = floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        
        p = 0
        q = 1 - f
        t = 1 - (1 - f)
        r, g, b = 0, 0, 0
        if hi == 0:
            r, g, b = 1, t, 0
        elif hi == 1:
            r, g, b = q, 1, 0
        elif hi == 2:
            r, g, b = 0, 1, t
        elif hi == 3:
            r, g, b = 0, q, 1
        elif hi == 4:
            r, g, b = t, 0, 1
        elif hi == 5:
            r, g, b = 1, 0, q
        self._red, self._green, self._blue = int(r * 255), int(g * 255), int(b * 255)

        return self    

    def random(self):
        self._red   = randint(0, 255)
        self._green = randint(0, 255)
        self._blue  = randint(0, 255)
        return self

    def randomColor(self):
        return self.fromHSV(randint(0, 360), 1.0, 1.0)

    def black(self):
        self._red, self._green, self._blue = 0, 0, 0
        return self

    def white(self):
        self._red, self._green, self._blue = 255, 255, 255
        return self

    def copy(self):
        return Color(*self.getColor())

    def __sub__(self, other):
        assert type(other) is Color, "Only Color - Color is possible"
        return Color(
            (self._red   - other.getRed()  ) % 256,
            (self._green - other.getGreen()) % 256,
            (self._blue  - other.getBlue() ) % 256
        )

    def __add__(self, other):
        assert type(other) is Color, "Only Color + Color is possible"
        return Color(
            (self._red   + other.getRed()  ) % 256,
            (self._green + other.getGreen()) % 256,
            (self._blue  + other.getBlue() ) % 256)

    def __mul__(self, other):
        assert type(other) is float, "Color can only be multiplied by floats"
        if type(other) is float:
            return Color(
                (self._red   * other) % 256,
                (self._green * other) % 256,
                (self._blue  * other) % 256)

    def enhance(self, ratio):
        #assert type(ratio) is RatioAdjustment, "Ratio need to be a ratioAdjustment object"

        #norms = list(self.normalize())
        #self.setNormalized(
        #    norms[0] - ratio.red_green * norms[1] - ratio.red_blue   * norms[2],
        #    norms[1] - ratio.green_red * norms[0] - ratio.red_blue   * norms[2],
        #    norms[2] - ratio.blue_red  * norms[0] - ratio.blue_green * norms[1])
        
        self._red = int(self._red * 1.0)
        self._green = int(self._green * 0.65)
        self._blue = int(self._blue * 0.35)
        
        return self

    def grayScale(self):
        return (self._red+self._green+self._blue) / 3

    def normalize(self):
        return self._red/255.0, self._green/255.0, self._blue/255.0
        
    def setNormalized(self, red, green, blue):
        self.setColor(
            int(red   * 255),
            int(green * 255),
            int(blue  * 255))

    def toHSV(self):
        r, g, b = self.normalize()
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        else: # mx == b:
            h = (60 * ((r - g) / df) + 240) % 360

        if mx == 0:
            s = 0
        else:
            s = df / mx
        v = mx
        return h, s, v

    def toHex(self):
        rh = format(self._red, '02x')
        gh = format(self._green, '02x')
        bh = format(self._blue, '02x')
        return '%s%s%s' % (rh, gh, bh)

    def toInt(self):
        integer = self._blue
        integer += self._green << 8
        integer += self._red   << 16
        return integer

    def toList(self):
        return [self._red, self._green, self._blue]

    def __repr__(self):
        return "color (%s, %s, %s)" % (self._red, self._green, self._blue)

    def __str__(self):
        return self.__repr__()