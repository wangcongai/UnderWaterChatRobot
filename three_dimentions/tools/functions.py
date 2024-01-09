import math


def distance(loc1, loc2):
    """
    计算两点的欧式距离
    :param loc1:
    :param loc2:
    :return:
    """
    x1, y1, z1 = loc1
    x2, y2, z2 = loc2[-1]
    # 计算两点之间的距离
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
