import abc


class Shape(metaclass=abc.ABCMeta):
    """A demo shape class"""

    @abc.abstractmethod
    def draw(self):
        """Draw a shape"""
        raise NotImplemented


class Circle(Shape):
    """A demo circle class"""

    def draw(self):
        """Draw a circle"""
        pass


class Square(Shape):
    """A demo square class"""

    def draw(self):
        """Draw a square"""
        pass
