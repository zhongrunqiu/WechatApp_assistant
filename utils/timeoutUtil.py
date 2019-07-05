# -*- coding=utf-8 -*-


import datetime


def get_day_left_in_second():
    """
    Args:None

    Returns:
        int:一天剩余的时间（单位：秒）
    """
    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta(days=1)
    left = (datetime.datetime(tomorrow.year,tomorrow.month,tomorrow.day,0,0,0)-now)
    left_second = left.total_seconds()
    return int(left_second)