from json import load as _load, dump as _dump

def loadf(file):
    with open(file, "r") as fs:
        data = _load(fs)
    return data

def dumpf(data, file, **kwargs):
    with open(file, "w") as fs:
        _dump(data, fs, **kwargs)
