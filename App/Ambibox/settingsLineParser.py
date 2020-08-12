from Libraries.AsemcoAPI.Tools.List import chunks
from Libraries.AsemcoAPI.Utils.Color import Color

class SpectrumTooHighException(Exception):
    def __init__(self, *args):
        Exception.__init__(self, "Chosen spectrum is too high: ", *args)

class ColorNumberTooHighException(Exception):
    def __init__(self, *args):
        Exception.__init__(self, "Number of colors are greater than 8: ", *args)

class ColorNumberTooLowException(Exception):
    def __init__(self, *args):
        Exception.__init__(self, "Number of colors are lower than 1: ", *args)

class SettingsLineParser:

    def __init__(self, line="FF6B4C000000000000000000000000000000000000000000000000000000000000000000000000001B0000000100000000F60000001C00000000000000"):

        colors_chunk   = line[ 0:80 ]
        spectrum_chunk = line[80:82 ]
        unk2_chunk     = line[82:88 ]
        on_chunk       = line[88:90 ]
        nbcolors_chunk = line[90:92 ]
        unk3_chunk     = line[92:98 ]
        visual_chunk   = line[98:122]

        self._colors   = self._getColors(colors_chunk)
        self._spectrum =           int(spectrum_chunk, 16)
        self._unk2     =                   unk2_chunk
        self._on       =           int(      on_chunk, 16)
        self._nbColors =           int(nbcolors_chunk, 16)
        self._unk3     =                   unk3_chunk
        self._visual   =                 visual_chunk

    def setSpectrum(self, nv):
        if nv > 80:
            raise SpectrumTooHighException("%d/80" % nv)
        self._spectrum = nv

    def clearAllColors(self):
        for color in self._colors:
            color.black()

    def getNbColors(self):
        return len(self._colors)

    def _getColors(self, chunk):
        self._colors = []
        for color in list(chunks(chunk, 8)):
            self._colors.append(Color().fromHex("#" + color[0:6]))
        return self._colors

    def getColor(self, i):
        return self._colors[i]

    def setColor(self, i, color):
        self._colors[i] = color

    def enable(self):
        self._on = 1

    def disable(self):
        self._on = 0

    def setNbColors(self, nbColors):
        if   nbColors < 1: raise ColorNumberTooLowException(nbColors)
        elif nbColors > 8: raise ColorNumberTooHighException(nbColors)
        else:              self._nbColors = nbColors -1

    def output(self):
        out = ""
        for color in self._colors:
            out += color.toHex() + "00"

        out += format(self._spectrum, '02x').upper()
        out += self._unk2
        out += format(self._on, '02x').upper()
        out += format(self._nbColors, '02x').upper()
        out += self._unk3
        out += self._visual

        return out

    def __str__(self):
        return "Colors:\t%s\nSpectrum:\t%i\nOn?:\t%i\nNbColors:\t%i\n" % (str(self._colors), self._spectrum, self._on, self._nbColors)

    def __repr__(self):
        return str(self)

if __name__ == '__main__':
    sample = "FF00000080800000808040008080800040808000C0C0C000400040004000800038DF2F013C61AF750000000001000000005B0000000000000000000000"
    lc = SettingsLineParser(sample)
    c1 = lc.getColor(0)
    c1.setColor(255, 255, 255)
    print(lc)
    print(sample)
    print(lc.output())