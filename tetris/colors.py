class Colors:
    orange = (206, 119, 50)
    green = (91, 149, 88)
    _green = (91, 149, 0)
    light_python_grey = (60, 63, 65)
    dark_python_grey = (43, 43, 43)
    pink = (240, 60, 123)
    blue = (126, 170, 199)
    red = (197, 58, 22)
    black = (0, 0, 0)
    pale_blue = (0, 30, 54)

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)

    @classmethod
    def get_cell_colors(cls):
        return [cls.BLACK, cls.pink, cls.RED, cls.GREEN, cls.BLUE, cls.CYAN, cls.MAGENTA, cls.YELLOW, cls.ORANGE]
