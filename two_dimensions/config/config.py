# MODEL = "gpt-3.5-turbo"
MODEL = "gpt-4-1106-preview"
TEMPERATURE = 0.7

# 给变量赋初始值
TARGET_X = 3.0  # 假设目标物体在x轴上的坐标为target_x米
TARGET_Y = 4.0  # 假设目标物体在y轴上的坐标为target_y米
ROBOT_X = 0.0  # 假设水下机器人的初始位置在x轴上的坐标为0米
ROBOT_Y = 0.0  # 假设水下机器人的初始位置在y轴上的坐标为0米

TURN = 0  # 假设初始对话轮数为0
TURN_MAX = 10  # 最大仿真次数

DISTANCE_THRESHOLD = 1  # 目标与机器人距离阈值
