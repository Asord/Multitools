from App.Ambibox.defaultValues import *
from App.Ambibox.tools import formatWarningOutputs

from Libraries.AsemcoAPI.Utils.Color import hsv_generatorTT, hsv_generatorT, curvedDistribution, Color, RatioAdjustment, getColor

class EffectParser:

    @staticmethod
    def Raw(effect, coef, palette):
        """leds = [getColor(led, palette) for led in [ledChunk for ledChunk in effect["data"]]]
        for led in leds:
            for color in led:
                color.enhance(coef)
        return leds"""
        raise NotImplementedError("Raw effect is depracted.")

    @staticmethod
    def Rainbow(effect, coef, palette, length):
        start_color         = getColor(effect["start"], palette).toHSV()
        end_color           = getColor(effect["end"]  , palette).toHSV()
        direction_clockwise =          effect["clockwise"]
        return hsv_generatorTT(start_color, end_color, length, direction_clockwise, coef)
        
    @staticmethod
    def RainbowCurved(effect, coef, length):
        direction_clockwise = effect["clockwise"]
        red = effect["red"]
        green = effect["green"]
        blue = effect["blue"]
        curve = curvedDistribution(length, direction_clockwise, red, green, blue)
        return [[Color().fromHue(point).enhance(coef)] for point in curve]

    @staticmethod
    def Color(effect, palette, coef, length):
        colors = [getColor(effect["color"], palette).enhance(coef)]
        return [[Color.copy(color) for color in colors] for _ in range(length)]

    @staticmethod
    def Colors(effect, palette, coef, length):
        colors = [c.enhance(coef) for c in getColor(effect["colors"], palette)]
        return [[Color.copy(color) for color in colors] for _ in range(length)]

    @staticmethod
    def Shades(effect, palette, coef, length):
        start_color         = getColor(effect["start"], palette).toHSV()
        end_color           = getColor(effect["end"]  , palette).toHSV()
        direction_clockwise =          effect["clockwise"]
        colors = hsv_generatorT(start_color, end_color.toHSV(), 7, direction_clockwise, coef) + [end_color.enhance(coef)]
        return [[Color.copy(color) for color in colors] for _ in range(length)]

    @staticmethod
    def createSpectrum(spectrum):
        if spectrum["type"] == "manual":
            return spectrum["values"]

        elif spectrum["type"] == "automatic":
            values = spectrum["values"]
            start = values["start"]
            stop  = values["stop"]
            step  = values["step"]
            return [i for i in range(start, stop+1, step)]

    @staticmethod
    def Generate(effect, coef, palette):

        if "length" in effect:
            length = effect["length"]
        else:
            length = 1

        if "spectrum" in effect:
            spectrum = EffectParser.createSpectrum(effect["spectrum"])
        else:
            spectrum = [1]

        result = [Color(0, 0, 0)]

        if effect["type"] == "Raw":
            result = EffectParser.Raw(effect, coef, palette)
        elif effect["type"] == "Rainbow":
            result = EffectParser.Rainbow(effect, coef, palette, length)
        elif effect["type"] == "Color":
            result = EffectParser.Color(effect, palette, coef, length)
        elif effect["type"] == "Colors":
            result = EffectParser.Colors(effect, palette, coef, length)
        elif effect["type"] == "Shades":
            result = EffectParser.Shades(effect, palette, coef, length)
        elif effect["type"] == "Curve":
            result = EffectParser.RainbowCurved(effect, coef, length)

        return result, spectrum


def effectConfigParser(data):
    output = []
    spectrum = []

    palette = DEFAULT_PALETTE; palette.update(data["palette"])

    effects = data["effects"]["leds"]
    coef    = data["coefs"] if "coefs" in data else {}
    nbLeds  = data["effects"]["numberOfLeds"]

    ratio = RatioAdjustment.fromDict(coef)

    for effect in effects:
        results   = EffectParser.Generate(effect, ratio, palette)
        output   += results[0]
        spectrum += results[1]

    settings = DEFAULT_SETTINGS; settings.update(data["settings"] if "settings" in data else {})
    config = DEFAULT_SETTINGS_TEXT.format(**settings)


    warnings = ""
    """ Integrity Checks..."""
    if len(output) != len(spectrum):
        warnings += "Warning: %s\n" % DIFFERENT_LENGTH_WARN.format(s=formatWarningOutputs(spectrum), slen=len(spectrum),
                                                                   o=formatWarningOutputs(output)  , olen=len(output))
    elif len(output) != nbLeds:
        print("Warning: %s\n" % INCORRECT_LENGTH_WARN.format(o=formatWarningOutputs(output), olen=len(output),
                                                             nb=nbLeds))
    elif max(spectrum) >= settings["BandsCount"]:
        print("Warning: %s\n" % SPECTRUM_TO_HIGH_WARN.format(s=formatWarningOutputs(spectrum),
                                                             bc=settings["BandsCount"]))

    return config, output, spectrum, warnings