from win32process import GetWindowThreadProcessId
from win32gui import IsWindowVisible, IsWindowEnabled, EnumWindows, ExtractIconEx, GetDC
from win32api import GetSystemMetrics
from win32con import SM_CXICON
from win32ui import CreateDCFromHandle, CreateBitmap

try:
    from psutil import Process
    from PIL import Image
except ImportError as ie:
    raise ImportError("To use AsemcoAPI.Library.ProcessReader, you need to install 'psutil' and 'PIL' libraries.") from ie


def _callback(hwnd, hwnds):
    if IsWindowVisible(hwnd) and IsWindowEnabled(hwnd):
        _, found_pid = GetWindowThreadProcessId(hwnd)
        hwnds.add(found_pid)
    return True

class ProcessReader:
    def __init__(self):

        self.__imageList = []
        self.__processConfig = []

        self.__getProccessConfig()

    def getProcessConfig(self):
        return self.__processConfig

    def getImageList(self):
        return self.__imageList

    def __getProccessConfig(self):
        pids = set()
        EnumWindows(_callback, pids)


        for pid in pids:
            try:
                proc = Process(pid)

                self.__getIconFromProc(proc)
                self.__processConfig.append({
                    'name': proc.name(),
                    'image': self.__imageList[-1],
                    'pid': proc.pid
                })
            except Exception as e: print(e)

    def __getIconFromProc(self, proc):

        path = proc.cmdline()[0]

        ico_size = GetSystemMetrics(SM_CXICON)

        large,_ = ExtractIconEx(path, 0)

        hdc = CreateDCFromHandle(GetDC(0))
        hbmp = CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, ico_size, ico_size)
        hdc = hdc.CreateCompatibleDC()

        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), large[0])

        bmpstr = hbmp.GetBitmapBits(True)

        image = Image.frombuffer(
            'RGB',
            (ico_size, ico_size),
            bmpstr, 'raw', 'BGRX', 0, 1
        )

        self.__imageList.append(image)