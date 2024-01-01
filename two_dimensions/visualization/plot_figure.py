# 导入正则表达式模块
import re
import os
import numpy as np
# 导入matplotlib.pyplot模块
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Songti SC']
# 正常显示坐标轴负号
plt.rcParams['axes.unicode_minus'] = False

# 切换到./logs目录
new_dir = "../logs"
os.chdir(new_dir)


def analyze_log(file_name):
    """
    解析日志，获得机器人运行路径和目标位置
    :param file_name:
    :return: target, result
    """
    # 打开文件
    file = open(file_name, "r")
    # 获取所有行
    lines = file.readlines()
    # 关闭文件
    file.close()
    target = tuple()
    # 定义一个空列表，用于存储提取的元组
    result = []
    # 定义一个正则表达式，用于匹配括号里的内容
    pattern = re.compile(r"\((\d+\.\d+),\s*(\d+\.\d+)\)")
    # 遍历所有的行
    for line in lines:
        # 判断是否含有"USER:"关键词
        if "USER:" in line:
            # 匹配括号里的内容
            match = pattern.search(line[line.index('水上机器人'):])
            # 如果匹配成功
            if match:
                # 获取匹配的两个数字
                x = match.group(1)
                y = match.group(2)
                # 将两个数字转换为浮点数，并组成一个元组
                tup = (float(x), float(y))
                # 将元组添加到结果列表中
                result.append(tup)
                # 匹配括号里的内容
            match = pattern.search(line[line.index('目标物体的位置'):])
            # 如果匹配成功
            if match:
                # 获取匹配的两个数字
                x = match.group(1)
                y = match.group(2)
                # 将两个数字转换为浮点数，并组成一个元组
                target = (float(x), float(y))
    return target, result


def plot_save_2d_figure(target: tuple, robot_position: list):
    """
    绘制并保存2维水上机器人运行轨迹图
    :param target: 目标坐标
    :param robot_position: 运行轨迹
    :return:
    """

    plt.figure(figsize=(6, 6), dpi=100)
    # 使用plt.plot()函数，将水下机器人的位置坐标绘制成一条折线图，表示机器人的运动轨迹
    plt.scatter([x[0] for x in robot_position], [y[1] for y in robot_position], color='blue', marker='o')
    plt.plot([x[0] for x in robot_position], [y[1] for y in robot_position], color='blue', linestyle='-', linewidth=2)

    # 使用plt.scatter()函数，将目标物体的位置坐标绘制成一个散点图，表示目标物体的位置
    plt.scatter(target[0], target[1], color='red', marker='*', s=100)

    # 使用plt.grid()函数，为图形添加网格线，表示每隔一米的距离
    plt.grid(color='gray', linestyle='--', linewidth=0.5)

    # 设置x轴和y轴的刻度值，每隔1个单位显示一个刻度
    plt.xticks(np.arange(-1, 6, 1))
    plt.yticks(np.arange(-1, 6, 1))

    # 设置x和y轴的单位长度相等
    plt.axis('equal')

    # 使用plt.xlabel()，plt.ylabel()，plt.title()等函数，为图形添加坐标轴标签，标题等注释信息
    plt.xlabel('x坐标')
    plt.ylabel('y坐标')
    plt.title('2维水上机器人的运动轨迹图')
    # 使用plt.show()函数，显示图形，或者使用plt.savefig()函数，保存图形到文件
    plt.savefig(FileName.replace(".log", ".jpeg"))
    plt.show()


if __name__ == '__main__':
    FileName = "gpt-4-1106-preview_temp-0.7_2023-12-30-21-21-09.log"
    # 从程序的运行日志log中提取出水下机器人的位置坐标
    Target, RobotPosition = analyze_log(FileName)
    # 绘制并保存2维水上机器人运行轨迹图
    plot_save_2d_figure(target=Target, robot_position=RobotPosition)


