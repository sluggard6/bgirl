# -*- coding:utf-8 -*-

__author__ = [
    '"liubo" <liubo@51domi.com>'
]

EPSILON = 0.001


def large_or_equal(a, b):
    return large(a, b) or equal(a, b)


def equal(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a == b
    else:
        return abs(float(a) - float(b)) <= EPSILON


def large(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a > b
    else:
        return abs(float(a) - float(b)) > EPSILON and (float(a) - float(b)) > EPSILON


def less(a, b):
    return large(b, a)

