from ctypes import windll

def isAdmin():
        try:
            return windll.shell32.IsUserAnAdmin()
        except Exception as e:
            return False