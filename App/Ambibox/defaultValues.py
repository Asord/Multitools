DEFAULT_SETTINGS = {
    "BandsCount": 100,
    "AutoLevel" : True,
    "Fading"    : 5,
    "Tempo"     : 100
}

DEFAULT_SETTINGS_TEXT = \
"""[Settings]
ProfileCount=1
CurrentProfile=0
ProfileName_0=Default
AudioDevice_0=-1
BandsCount_0={BandsCount}
Tempo_0={Tempo}
Fading_0={Fading}
Effect_0=0
AutoLevel_0={AutoLevel}
ProfileSettings_0="""

DEFAULT_PALETTE = {
    "red": "#ff0000",
    "yellow": "#ffff00",
    "green": "#00ff00",
    "cyan": "#00ffff",
    "lightblue": "#4040ff",
    "blue": "#0000ff",
    "magenta": "#ff00ff",
    "white": "#ffffff",
    "black": "#000000",
    "darkgray": "#010101",
}
DIFFERENT_LENGTH_WARN = \
"""spectrum length is not equal to output length:
\nspectrum: {s} ({slen})\noutput: {o} ({olen})"""

INCORRECT_LENGTH_WARN = \
"""output length is not equal to numberOfLeds:
\noutput: {o} ({olen})\nnumber of leds: {nb}"""

SPECTRUM_TO_HIGH_WARN = \
"""One of the spectrum value exceed BandsCount value:
\nspectrum: {s}\nBandsCount value: {bc}"""

"""
special config - to keep in case
  "__special": {
    "OVERRIDE": {
    "type"     : "shades",
      "from"     : "red",
      "to"       : "cyan",
      "clockwise": false,
      "length"   : 21
    },
    "__": {
      "type"  : "color",
      "color" : "#0000ff",
      "length": 21,
      "spectrum": {
        "type"  : "automatic",
        "values": [1, 22, 1]
      }

    }
  },
"""