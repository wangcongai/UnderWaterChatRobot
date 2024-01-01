import numpy as np

# 导入其他文件中定义的模块
from config import config
from tools import functions


# 定义一个仿真类
class Simulator:
    def __init__(self):
        """
        定义一个初始化位置的方法
        :return:
        """
        # 从config文件中读取水下机器人的初始位置
        self.robot = [config.ROBOT_X, config.ROBOT_Y]
        # 从config文件中读取目标物体的位置
        self.target = [config.TARGET_X, config.TARGET_Y]
        # 计算水下机器人和目标物体之间的距离
        self.distance = functions.distance(self.robot, self.target)

    def local_engine(self):
        """
        基于环境里的目标和机器人坐标，设计本地的推理思维链，作为chatgpt学习的内容
        :return:
        """
        candidate_actions = ["直行1米", "后退1米", "左行1米", "右行1米"]
        new_positions = [(self.robot[0], self.robot[1] + 1), (self.robot[0], self.robot[1] - 1),
                         (self.robot[0] - 1, self.robot[1]), (self.robot[0] + 1, self.robot[1])]
        candidate_distances = [functions.distance(self.target, new_position) for new_position in new_positions]
        # 求列表的最小值序号对应的动作
        act = candidate_actions[np.argmin(candidate_distances)]
        thought1 = ("1. 直行1米后，机器人的位置为%s，与目标%s的欧式距离为: sqrt((%s-%s)**2+(%s-%s)**2)=%.2f米(小数点两位)；"
                    % (new_positions[0], self.target, self.target[0], new_positions[0][0],
                       self.target[1], new_positions[0][1], candidate_distances[0]))
        thought2 = ("2. 后退1米后，机器人的位置为%s，与目标%s的欧式距离为: sqrt((%s-%s)**2+(%s-%s)**2)=%.2f米(小数点两位)；"
                    % (new_positions[1], self.target, self.target[0], new_positions[1][0],
                       self.target[1], new_positions[1][1], candidate_distances[1]))
        thought3 = ("3. 左行1米后，机器人的位置为%s，与目标%s的欧式距离为: sqrt((%s-%s)**2+(%s-%s)**2)=%.2f米(小数点两位)；"
                    % (new_positions[2], self.target, self.target[0], new_positions[2][0],
                       self.target[1], new_positions[2][1], candidate_distances[2]))
        thought4 = ("4. 右行1米后，机器人的位置为%s，与目标%s的欧式距离为: sqrt((%s-%s)**2+(%s-%s)**2)=%.2f米(小数点两位)；"
                    % (new_positions[3], self.target, self.target[0], new_positions[3][0],
                       self.target[1], new_positions[3][1], candidate_distances[3]))
        thought5 = "所以，应该选择最短距离对应的“%s”这个动作。" % act
        assistant_answer = "".join([thought1, thought2, thought3, thought4, thought5])
        return assistant_answer

    def update_simulation(self, action):
        """
        基于执行动作，更新环境里的机器人位置信息
        :param action:
        :return:
        """
        # 根据role的assistant的语句，更新水下机器人的加速度和姿态
        if "直行1米" == action:
            self.robot[1] += 1.0
        elif "后退1米" == action:
            self.robot[1] -= 1.0
        elif "左行1米" == action:
            self.robot[0] -= 1.0
        elif "右行1米" == action:
            self.robot[0] += 1.0
