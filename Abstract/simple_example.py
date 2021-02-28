import abc


class BaseCar(metaclass=abc.ABCMeta): # 메타클래스에 abc.ABCMeta를 넣어주면 됨
    def __init__(self, color, manufacture):
        self.color = color
        self.manufacture = manufacture

    @abc.abstractmethod
    def _start_up(self):
        raise NotImplemented("추상 메서드입니다.")

    @abc.abstractmethod
    def speed_up(self, amount):
        raise NotImplemented("추상 메서드입니다.")


class SportsCar(BaseCar):
    def __init__(self, color, manufacture, owner):
        super().__init__(color, manufacture)  # 보통 이렇게 추상 클래스의 생성자를 확장하는 경우도 많음.
        self.owner = owner
        self.current_speed = 0
        self.is_startup = False

    def print_owner(self):
        print(f'this car\'s owner {self.owner}')

    def insert_key(self):
        self._start_up()

    def _start_up(self): # 추상 메서드의 구현부, 구현하지 않고 사용하면 예외 발생
        self.is_startup = True
        print("시동이 켜졌습니다.")

    def speed_up(self, amount): # 추상 메서드의 구현부, 구현하지 않고 사용하면 예외 발생
        if not self.is_startup:
            print("시동을 켜야합니다.")
        self.current_speed += amount
        return self.current_speed


if __name__ == "__main__":
    # base_car = BaseCar(color="black", manufacture="hyundai")
    # print(base_car.color)
    # base_car.speed_up(50)
    # 위 코드 모두 에러
    my_car = SportsCar(color="black", manufacture="Ferrari", owner="kim")
    my_car.insert_key()
    my_car.speed_up(50)
    print(my_car.current_speed)
