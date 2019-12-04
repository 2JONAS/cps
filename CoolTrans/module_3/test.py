a = 10


def f():
    if a == 0:
        return 0
    a = a -1
    raise Exception("err")