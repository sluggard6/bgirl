# -*- coding:utf-8 -*-


def expo_iterator(x, n):
    for i in range(n):
        yield x ** i


def expo_seq(x, n):
    """
    return sequence of x ** (0 ... n)
    """
    return [i for i in expo_iterator(x, n)]
