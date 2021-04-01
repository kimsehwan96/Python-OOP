def gen():
    yield 0
    print('0을 발생시킴')
    yield 1
    print('1을 발생시킴')
    yield 2
    print('2을 발생시킴')


if __name__ == '__main__':
    for i in gen():
        print(i)

"""
output:
0
0을 발생시킴
1
1을 발생시킴
2
2을 발생시킴
"""