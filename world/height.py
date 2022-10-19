from .layer import Layer


class Height(Layer):
    def __init__(self, size, initial, world):
        Layer.__init__(self, size, initial, world)

    @staticmethod
    def get_color(value):
        return value * 200, value * 200, value * 200

    def get_height_difference(self, x1, y1, x2, y2):
        height1 = self.grid[x1][y1]
        height2 = self.grid[x2][y2]
        return height2 - height1
