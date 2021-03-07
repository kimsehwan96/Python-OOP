import abc


class Shape(metaclass=abc.ABCMeta):
    """A demo shape class"""

    @abc.abstractmethod
    def draw_circle(self):
        """Draw a circle"""
        raise NotImplemented

    @abc.abstractmethod
    def draw_square(self):
        """ Draw a square"""
        raise NotImplemented


class Circle(Shape):
    """A demo circle class"""

    def draw_circle(self):
        """
        원을 그리는 메서드
        :param  None
        :return: None
        """
        print("원 그리기 !")

    def draw_square(self):
        """
        사각형을 그리는 메서드 사용하지 않음.
        """
        pass


if __name__ == '__main__':
    circle = Circle()
    circle.draw_circle()
