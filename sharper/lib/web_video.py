# -*- coding: utf-8 -*-
"""
    lib/web_video.py
    ~~~~~~~~~~~~~~

    get web video url by web url

    :date:2012-03-08

"""
__author__ = '"linnchord gao" <linnchord@gmail.com>'

from BeautifulSoup import BeautifulSoup
import urllib2
import re


def get_video_url(page_url):
    if 'youku.com' in page_url: return get_youku_video_url(page_url)
    if 'tudou.com' in page_url: return get_tudou_video_url(page_url)
    if 'ku6.com' in page_url: return get_ku6_video_url(page_url)
    return None


def get_youku_video_url(page_url):
    m = re.findall(r'v\_show\/id\_(\w{5,})\.', page_url)
    if m:
        return 'http://player.youku.com/player.php/sid/%s/v.swf' % m[0]
    else:
        return get_url_by_id(page_url, 'link2')


def get_tudou_video_url(page_url):
    rex = m = ''
    if 'tudou.com/playlist' in page_url: rex = r'i(\d{5,})\.htm'
    if 'tudou.com/programs/view/' in page_url: rex = r'\/programs\/view\/([\w\-\_]{5,})[\/]?'
    if rex: m = re.findall(rex, page_url)
    return 'http://www.tudou.com/v/' + m[0] if m else None


def get_ku6_video_url(page_url):
    m = re.findall(r'\/([\w\-\_]{5,}[\.]{0,2})\.htm', page_url)
    if m:
        return 'http://player.ku6.com/refer/%s/v.swf' % m[0]
    else:
        return get_url_by_id(page_url, 'swf_url')


def get_url_by_id(page_url, el_id):
    try:
        res = urllib2.urlopen(page_url)
        soup = BeautifulSoup(res)
        res.close()
    except:
        return None
    items = soup.findAll(id=el_id)
    if items:
        url = items[0].get('value')
        if url: return url
    return None