from .Color import Color

def getColor(color, palette):
    if type(color) is Color:
        return color

    elif type(color) is str:
        if "#" in color:
            return Color().fromHex(color)
        else:
            return Color().fromHex(palette[color])

    elif type(color) is list:
        ret = []
        for c in color:
            if "#" in c:
                ret.append(Color().fromHex(c))
            else:
                ret.append(Color().fromHex(palette[c]))
        return ret