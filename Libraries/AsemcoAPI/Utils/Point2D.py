class Point2D:

    def __init__(self, x=0, y=0, boundx = 0, boundy = 0):
        self.x = x
        self.y = y
        self.bx = boundx
        self.by = boundy

    def __add__(self, other):
        x = (self.x+other.x)%self.bx
        y = (self.y+other.y)%self.by
        return Point2D(x, y, self.bx, self.by)

    def __sub__(self, other):
        x = (self.x-other.x)%self.bx
        y = (self.y-other.y)%self.by
        return Point2D(x, y, self.bx, self.by)

    def __invert__(self):
        return self.y * self.bx + self.x

    def zero(self):
        self.x = 0
        self.y = 0
