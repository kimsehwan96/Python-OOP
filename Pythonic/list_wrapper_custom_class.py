class Items:
    def __init__(self, *values):
        self._values = list(values)

    def __len__(self):
        return len(self._values)

    def __getitem__(self, item):
        return self._values.__getitem__(item)


if __name__ == '__main__':
    items = Items(1,2,3,4,5,6,7,8)
    print(len(items))
    print(items[0]) # 1
    print(items[1]) # 2
