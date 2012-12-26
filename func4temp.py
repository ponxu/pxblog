# -*- coding: utf-8 -*-
from model import *
from setting import page_size
from utils import fmt_time, now

def option(name):
    return Option.get(name)


def get_posts(paged, max=page_size):
    return [2, 3, 4, 8, 9]


def get_pages(max=page_size):
    return [2, 3, 4, 8, 9]


def get_tags():
    return Tag.all()


def if_out(flag, out):
    return flag and out or ''


def fmt(seconds, f='%Y-%m-%d %H:%M:%S'):
    return fmt_time(f, seconds)


def friend_time(seconds):
    diff = now() - seconds
    days = diff / 86400

    if days > 730:
        return '%s years ago' % (days / 365)
    if days > 365:
        return '1 year ago'
    if days > 60:
        return '%s months ago' % (days / 30)
    if days > 30:
        return '1 month ago'
    if days > 14:
        return '%s weeks ago' % (days / 7)
    if days > 7:
        return '1 week ago'
    if days > 1:
        return '%s days ago' % days

    if diff > 7200:
        return '%s hours ago' % (diff / 3600)
    if diff > 3600:
        return '1 hour ago'
    if diff > 120:
        return '%s minutes ago' % (diff / 60)
    if diff > 60:
        return '1 minute ago'
    if diff > 1:
        return '%s seconds ago' % diff

    return '%s second ago' % diff


all_funcs = locals()

# Test
if __name__ == "__main__":
    print friend_time(now() - 86300)