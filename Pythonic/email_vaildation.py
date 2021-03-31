import re

EMAIL_FORMAT = re.compile(r"[^@]+@[^@]+[^@]+")


def is_valid_email(potentially_valid_email: str):
    return re.match(EMAIL_FORMAT, potentially_valid_email) is not None


class User:
    def __init__(self, username):
        self.username = username
        self._email = None

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        if not is_valid_email(new_email):
            raise ValueError("유효한 이메일이 아닙니다.")
        self._email = new_email


if __name__ == '__main__':
    u1 = User('kim')
    # u1.email = 'kim@'  # ValueError
    u1.email = 'kim@kim.com'
    print(u1.email)
