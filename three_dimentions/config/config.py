# MODEL = "gpt-3.5-turbo"
MODEL = "gpt-4-1106-preview"
TEMPERATURE = 0.1

# 水下机器人三维坐标（米）
SubmarinePos = [0, 0, -5]
# 目标三维坐标（米）
TargetPos = [[30, 40, -20], [29, 41, -20]]
# 目标的移动速度（米/秒）
TargetVelocity = [-0.5, 0.5, 0]
# 水流速度（米/秒）
WaterVelocity = [0, 1, 0]
# 水下机器人的实际航行速度（米/秒）
SubmarineSpeed = 5.0
# 每次仿真的时间间隔（秒）
DeltaT = 2
# 最大仿真次数
TURN_MAX = 10
# 目标与机器人距离阈值
DISTANCE_THRESHOLD = 4
