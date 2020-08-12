from ctypes import windll, c_uint, byref
from win32api import EnumDisplayMonitors, GetSystemMetrics

PROCESS_PER_MONITOR_DPI_AWARE = 1
MDT_EFFECTIVE_DPI = 0

def getMonitorScale():
    shcore = windll.shcore
    monitors = EnumDisplayMonitors()
    hresult = shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    #assert hresult == 0
    dpiX = c_uint()
    dpiY = c_uint()
    shcore.GetDpiForMonitor(
        monitors[0][0].handle,
        MDT_EFFECTIVE_DPI,
        byref(dpiX),
        byref(dpiY))

    if dpiX.value == dpiY.value:
        dpi = 100/96 * dpiX.value
        return int(dpi)
    else:
        return 100


_factor = getMonitorScale()

def rescale(size):
    size = int(size)
    return int(size / _factor * 100)

def centerGeometryS(pos="0*0"):
    w, h = pos.split("*")
    return centerGeometry(int(w), int(h))

def centerGeometry(width=0, height=0):
    xoff = GetSystemMetrics(0)/2 - width /2
    yoff = GetSystemMetrics(1)/2 - height/2


    if width == 0 or height == 0: return "+%i+%i"      %                (xoff, yoff)
    else:                         return "%ix%i+%i+%i" % (width, height, xoff, yoff)
