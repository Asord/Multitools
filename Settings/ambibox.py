from json import load , dump
from os.path import join as joinPath

with open("Configs/Ambibox.json" , "r") as conf:
    ambiboxConf = load(conf)

ColormusicSettingsFile = joinPath(ambiboxConf["AmbiboxColormusicPath"], "Settings.ini")

AmbiboxSavePath = "Configs/saves/ambibox.json"
def AmbiboxLoad():
    with open(AmbiboxSavePath, "r") as fs:
        return load(fs)

def AmbiboxSave(save):
    with open(AmbiboxSavePath, "w") as fs:
        dump(save, fs)