_upCheckList =    [( 0, -1), (-1, -1), ( 1, -1), ( 0, -2), (-1, -2), ( 1, -2), (-2, -2), ( 2, -2)]
_downCheckList =  [( 0,  1), (-1,  1), ( 1,  1), ( 0,  2), (-1,  2), ( 1,  2), (-2,  2), ( 2,  2)]
_leftCheckList =  [(-1,  0), (-1, -1), (-1,  1), (-2,  0), (-2, -1), (-2,  1), (-2, -2), (-2,  2)]
_rightCheckList = [( 1,  0), ( 1, -1), ( 1,  1), ( 2,  0), ( 2, -1), ( 2,  1), ( 2, -1), ( 2,  2)]

class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def key(self):
        return str(self)

    def __str__(self):
        return "{}.{}".format(self.x, self.y)

    def __repr__(self):
        return "Pos: ({})".format(self.__str__())

    def get(self):
        return self.x, self.y

    def set(self, x, y):
        self.x = x
        self.y = y

class Map:
    def __init__(self):
        self._map = {}

    def _maxX(self, y):
        _maxX = 0

        for key in self._map:
            _x, _y = self._keyToXY(key)
            if _x > _maxX:
                _maxX = _x

        return _maxX

    def _maxY(self, x):
        _maxY = 0

        for key in self._map:
            _x, _y = self._keyToXY(key)
            if _y > _maxY:
                _maxY = _y

        return _maxY

    def appendX(self, x, obj):
        maxY = self._maxY(x)
        self.set(x, maxY+1, obj)

    def appendY(self, y, obj):
        maxX = self._maxX(y)
        self.set(maxX+1, y, obj)

    def get(self, x, y):
        pos = self._coordsToStr(x, y)

        if pos in self._map:
            return self._map[pos]
        else:
            return None

    def set(self, x, y, obj):
        pos = self._coordsToStr(x, y)

        if pos in self._map:
            result = False
        else:
            result = True

        self._map[pos] = obj
        return result

    def remove(self, obj):
        res = None
        for pos,o in self._map.items():
            if o == obj:
                res = self._map.pop(pos, None)
                break

        return res is not None

    def removeAt(self, x, y):
        res = None
        pos = self._coordsToStr(x, y)

        if pos in self._map:
            res = self._map.pop(pos, None)

        return res is not None

    def find(self, obj):
        for pos,o in self._map.items():
            if o == obj:
                return self._keyToXY(pos)
        return None

    @staticmethod
    def _coordsToStr(x, y):
        return "{}.{}".format(x, y)

    @staticmethod
    def _keyToXY(key):
        _x, _y = key.split(".")
        return int(_x), int(_y)


class DirectionalMap(Map):
    def __init__(self):
        Map.__init__(self)

        self._position = Vec2D(0, 0)

    def _getRelativeX(self, x, y):
        if x < 0:
            nx = self._maxX(y)
        elif x > self._maxX(y):
            nx = 0
        else:
            nx = x

        return nx, y

    def _getRelativeY(self, x, y):
        if y < 0:
            ny = self._maxY(x)
        elif y > self._maxY(x):
            ny = 0
        else:
            ny = y

        return x, ny

    def SetPos(self, x, y):
        self._position.set(x, y)

    def _move(self, checkList, relativeFunc):
        x, y = self._position.get()

        for move in checkList:
            rx, ry = relativeFunc(x + move[0], y + move[1])
            if self.get(rx, ry) is not None:
                self._position.set(rx, ry)
                break

    def Up(self):
        self._move(_upCheckList, self._getRelativeY)

    def Down(self):
        self._move(_downCheckList, self._getRelativeY)

    def Left(self):
        self._move(_leftCheckList, self._getRelativeX)

    def Right(self):
        self._move(_rightCheckList, self._getRelativeX)

    def Zero(self):
        self._position.set(0, 0)

    def GetCurrentPosition(self):
        return self._position.get()

    def GetCurrentObject(self):
        return self.get(*self._position.get())

class FocusMap(DirectionalMap):
    def __init__(self, focusColor="#808080"):
        """ used along with tkinter focusable items """
        DirectionalMap.__init__(self)

        self._focus_color = focusColor
        self._focused_item_color = ""

    def set(self, x, y, obj):
        super().set(x, y, obj)
        if len(self._map) == 1:
            self._focusCurrentItem()

    def _unfocusCurrentItem(self):
        co = self.GetCurrentObject()
        if co is not None:
            co.configure(bg=self._focused_item_color)

    def _focusCurrentItem(self):
        co = self.GetCurrentObject()
        if co is not None:
            self._focused_item_color = co.cget("bg")
            co.configure(bg=self._focus_color)
            co.focus_set()

    def Up(self):
        self._unfocusCurrentItem()
        super().Up()
        self._focusCurrentItem()

    def Down(self):
        self._unfocusCurrentItem()
        super().Down()
        self._focusCurrentItem()

    def Left(self):
        self._unfocusCurrentItem()
        super().Left()
        self._focusCurrentItem()

    def Right(self):
        self._unfocusCurrentItem()
        super().Right()
        self._focusCurrentItem()

    def Zero(self):
        self._unfocusCurrentItem()
        super().Zero()
        self._focusCurrentItem()

