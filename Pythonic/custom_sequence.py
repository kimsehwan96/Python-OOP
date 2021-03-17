class Foo:
    def __init__(self):
        self.bar = list()

    def add(self, item):
        self.bar.append(item)

    def remove(self, index):
        self.bar.pop(index)

    def __str__(self):
        return str(self.bar)

    def __contains__(self, item):
        """
        매직메서드, 멤버십 테스트에 이용된다.
        """
        return item in self.bar

    def __iter__(self):
        return iter(item for item in self.bar)

    def __getitem__(self, index):
        return self.bar[index]

    def __setitem__(self, key, value):
        self.bar[key] = value

    def __delitem__(self, key):
        del self.bar[key]

    def __len__(self):
        return len(self.bar)

if __name__ == "__main__":
    f = Foo()
    f.add(1)
    f.add(2)
    print(f)
    f[0] = 100
    print(100 in f)
    print(len(f))