# -*- coding:utf-8 -*-
"""
    util/color.py
    ~~~~~~~~~~~~~~

    color util
"""
__authors__ = ['"linnchord gao" <linnchord@gmail.com>']


def rgb2htmlcolor(rgb_tuple):
    """ convert an (R, G, B) tuple to #RRGGBB """
    return '#%02x%02x%02x' % rgb_tuple


def htmlcolor2rgb(color_str):
    """ convert #RRGGBB to an (R, G, B) tuple """
    color_str = color_str.strip()[-6:]
    if len(color_str) != 6:
        raise ValueError("input #%s is not in #RRGGBB format" % color_str)
    r, g, b = color_str[:2], color_str[2:4], color_str[4:]
    return (int(n, 16) for n in (r, g, b))


def htmlcolor2rgb_float(color_str):
    """convert #RRGGBB to an (0.32, 0.12, 0.453) tuple """
    return (x / 256.0 for x in htmlcolor2rgb(color_str))
