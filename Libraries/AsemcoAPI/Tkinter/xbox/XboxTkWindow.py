from Libraries.AsemcoAPI.Tkinter.TkXbox import XboxController
from Libraries.AsemcoAPI.Tkinter.tkgen import TkJson

class XboxTkWindow(TkJson, XboxController):

    def __init__(self, tkInterface, title="Tk"):
        TkJson.__init__(self, tkInterface, title)
        XboxController.__init__(self, 0)

        # Binding attributes
        self.__xBindings = []
        self.__xAxis = []

        # Last axis event
        self.__xJoyLastID = 0
        self.__xJoyLastEventID = -1

    def xbind(self, button, func):
        self.__xBindings.append((button, func))

    def joybind(self, joy, func):
        self.__xAxis.append((joy, func, self.__xJoyLastID))
        self.__xJoyLastID += 1

    def _StartXHandler(self):

        @self.event
        def on_button(button, pressed):

            if pressed == 1:
                for signal in self.__xBindings:
                    if button == signal[0]:
                        signal[1]()
                        return

        @self.event
        def on_axis(axis, value):

            for signal in self.__xAxis:
                if axis == signal[0]:
                    signal[1](value)
                    return

        def callback():
            self.dispatch_events()
            self.after(50, callback)

        callback()

    def _signalHandler(self, Event=None):
        assert False, "This method is depracted... Use joybind and xbind"