import numpy as np

from three_dimentions.tools.functions import distance


class ChatGptDialog:
    # 初始化方法
    def __init__(self):
        self.system_message = {"role": "system",
                               "content": "这是一个水下机器人根据目标物体位置进行探索的模拟实验。"
                                          "根据目标与机器人的相对位置和运动预期，制定运动指令，从而让机器人逐渐靠近目标。"
                                          "role的user角色，输入的内容包括目标物体target和水下机器人robot的3维坐标，以及水流速度向量。"
                                          "role的assistant角色，先估算target在仿真时间间隔后的新位置坐标，"
                                          "然后计算robot的实际航行单位方向, "
                                          "robot有一个实际航行的速度值, 该值不能超过配置常数值SubmarineSpeed)"
                                          "最后，将水流速度纳入考虑，得到robot的掌舵航行速度向量，"
                                          "该掌舵航行速度向量作为最终指令(一个包含3个数字的list)，输出给robot"}
        self.user_message = dict()
        self.assistant_message = dict()
        self.dialog = [self.system_message]

    @staticmethod
    def analyze_action(response):
        """
        对chatgpt assistant返回的答案，解析出结论动作
        :param response:
        :return:
        """
        act = None
        if response and isinstance(response, str):
            # 找到最后一个[]的位置
            start = response.rfind('[')
            end = response[start:].find(']')

            # 提取[]中的内容
            subtext = response[start + 1:start + end]

            # 用逗号分割字符串，得到一个列表
            sublist = subtext.split(',')

            # 用map函数将列表中的每个元素转换为浮点数
            act = list(map(float, sublist))
        return act

    def create_user_message(self, simulator):
        """
        基于目标和当前机器人位置，返回格式化的user prompt，并加入chatgpt的对话记录中
        :param simulator:
        :return:
        """
        robot_target_distance = distance(loc1=simulator.robot, loc2=simulator.target)
        user_content = (("这是第%s轮对话。target当前坐标为：%s, target历史坐标为：%s, "
                         "robot坐标为：%s, target与机器人距离为：%s(米), 水流速度water_v为：%s(米/秒)。"
                         "请根据目标的运动预期与机器人的相对位置，给出水下机器人的掌舵航行速度向量(一个包含3个数字的list)，从而让机器人逐渐靠近目标。")
                        % (simulator.turn, simulator.target[-1], simulator.target[-2],
                           np.around(simulator.robot, decimals=2),
                           np.around(robot_target_distance, decimals=2), simulator.water_v))
        self.user_message = {"role": "user",
                             "content": user_content}
        self.dialog.append(self.user_message)

    def create_assistant_message(self, response):
        """
        基于本地引擎推理结果，或者chatgpt返回的assistant结果，重新格式化，并加入chatgpt的对话记录中
        :param response:
        :return:
        """
        self.assistant_message = {"role": "assistant", "content": response}
        self.dialog.append(self.assistant_message)
