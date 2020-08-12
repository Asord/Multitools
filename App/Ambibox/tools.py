from App.Ambibox.settingsLineParser import SettingsLineParser
from Settings import ambiboxConf

def unserializeLedsConfig(profileSettings):
    ledsConfig = []
    for i in range(0, len(profileSettings), 122):
        ledsConfig.append(SettingsLineParser(profileSettings[i:i + 122]))
    return ledsConfig

def serializeLedsConfig(ledsConfig_list):
    ledsConfig = ""
    for ledCfg in ledsConfig_list:
        ledsConfig += ledCfg.output()

    for _ in range(len(ledsConfig_list), ambiboxConf["AmbiboxNumberOfLeds"]):
        led = SettingsLineParser()
        led.disable()
        ledsConfig += led.output()

    return ledsConfig

def formatWarningOutputs(lst):
    out = ""
    for e in lst:
        if type(e) is list:
            out += "[%d]" % len(e)
        else:
            out += "%s " % str(e)
    return out