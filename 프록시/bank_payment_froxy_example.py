from abc import ABCMeta, abstractmethod


class Payment(metaclass=ABCMeta):

    @abstractmethod
    def do_pay(self):
        pass


class Bank(Payment):

    def __init__(self):
        self.card = None
        self.account = None

    def __get_account(self):
        """
        카드 번호로부터 은행 계좌를 받아옴, 이 예제에서는 두개가 동일하다고 판단.
        :return: 계좌 번호
        """
        self.account = self.card
        return self.account

    def __has_funds(self):
        """
        계좌에 충분한 금액이 있는지 확인하는 메서드, 테스트를 위해 금액 체크를 하지 않고 무조건 True 리턴
        :return: True
        """
        print('Bank : 계좌에 충분한 금액이 있는지 확인 중', self.__get_account())
        return True

    def set_card(self, card):
        """
        카드 번호를 입력받아 카드 어트리뷰트에 설정
        :param card: any
        :return: None
        """
        self.card = card

    def do_pay(self):
        """
        실제 결제를 하는 과정, __has_funds를 호출하여 체크하는 일종의 래핑된 메서드임.
        :return: boolean
        """
        if self.__has_funds():
            print('Bank: 금액 결제중..')
            return True
        else:
            print('Bank: 계좌에 금액이 충분하지 않습니다.')
            return False


class DebitCard(Payment):
    """
    Bank 클래스의 프록시
    실 객체의 민감한 메서드 (잔고 확인, 계좌번호를 받아오는 등)을 호출하지 않도록 보호한다.
    상속받은 클래스인 Payment 클래스에는 Bank 클래스의 민감한 메서드들이 구현 되어 있지 않다.
    또한 Bank 클래스와  DebitCard 클래스는 모두 Payment 클래스를 상속하였다. 따라서 공통 메서드(인터페이스)인  do_pay 메서드를 갖고있다.
    이 프록시 클래스는 Bank 라는 실 객체를 생성하고, 실 객체의 do_pay 메서드를 호출함으로서 동작한다. 물론 메서드 호출 전에 셋업(카드번호)은 들어간다.
    """

    def __init__(self):
        self.bank = Bank()

    def do_pay(self):
        card = input('Proxy : 카드 번호 입력하세요 : ')
        self.bank.set_card(card)
        return self.bank.do_pay()


class Client:

    def __init__(self):
        print("clinet  : 물품 구매 중")
        self.debit_card = DebitCard()  # 클라이언트는 프록시 객체에 접근한다.
        self.is_purchased = None

    def make_payment(self):
        self.is_purchased = self.debit_card.do_pay()

    def __del__(self):
        if self.is_purchased:
            print('client  : 구매 완료')
        else:
            print('client :  금액 부족')


if __name__ ==  '__main__':
    client =  Client()
    client.make_payment()

"""
result:

clinet  : 물품 구매 중
Proxy : 카드 번호 입력하세요 : 1-3
Bank : 계좌에 충분한 금액이 있는지 확인 중 1-3
Bank: 금액 결제중..
client  : 구매 완료

"""