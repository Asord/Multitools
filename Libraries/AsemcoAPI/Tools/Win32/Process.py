try:
    from psutil import process_iter, NoSuchProcess, AccessDenied, ZombieProcess, Process
    from pywinauto import Desktop
except ImportError as ie:
    raise IndexError("To use AsemcoAPI.Tools.Win32 you need to have 'psutil' and 'pywinauto' libraries") from ie


def IsProcessRunning(processName):
    for proc in process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (NoSuchProcess, AccessDenied, ZombieProcess):
            pass
    return False

def GetAllForegroundProcesses(ignoreList=None):
    ignoreList = [] if ignoreList is None else ignoreList
    ignoreList += ["explorer"] # minimal ignore list must include windows relative apps

    processList = []

    windows = Desktop(backend="uia").windows()
    for w in windows:
        name = Process(w.process_id()).name().replace(".exe", "")
        if name not in ignoreList:
            processList.append(name)

    return processList

if __name__ == '__main__':
    print(GetAllForegroundProcesses())