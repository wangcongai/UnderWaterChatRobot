from two_dimensions.config import config


class ChatGptDialog:
    # 初始化方法
    def __init__(self):
        self.system_message = {"role": "system",
                               "content": "这是一个水上机器人根据目标物体位置进行探索的模拟实验。"
                                          "根据目标与机器人的相对位置和运动预期，制定运动指令，从而让机器人逐渐靠近目标。"
                                          "role的user角色，输入的内容包括目标物体的二维坐标，以及水下机器人的二维坐标。"
                                          "role的assistant角色，分别评估所有可能的执行动作（“直行1米“或“后退1米“或“左行1米“或“右行1米“）"
                                          "所对应的机器人与目标的距离。最后选择其中一个最优动作输出结论。"}
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
            keywords = ["直行1米", "后退1米", "左行1米", "右行1米"]  # 定义一个关键词列表
            index = -1  # 初始化索引为-1
            for word in keywords:  # 遍历关键词列表
                index_t = response.rfind(word)  # 从右向左查找关键词在字符串中的索引
                if index_t > index:  # 如果索引大于当前的最大索引
                    index = index_t  # 更新最大索引
                    act = word  # 更新结果为当前关键词
        return act

    def create_user_message(self, target, robot):
        """
        基于目标和当前机器人位置，返回格式化的user prompt，并加入chatgpt的对话记录中
        :param target:
        :param robot:
        :return:
        """
        self.user_message = {"role": "user",
                             "content": ("这是第{}轮对话。目标物体的位置是({:.2f}, {:.2f})。水上机器人的位置是({:.2f}, {:.2f})。"
                                         "根据目标与机器人的相对位置和运动预期，请给出水下机器人的运动指令，从而让机器人逐渐靠近目标。"
                                         ).format(config.TURN, target[0], target[1], robot[0], robot[1])}
        self.dialog.append(self.user_message)

    def create_assistant_message(self, response):
        """
        基于本地引擎推理结果，或者chatgpt返回的assistant结果，重新格式化，并加入chatgpt的对话记录中
        :param response:
        :return:
        """
        self.assistant_message = {"role": "assistant", "content": response}
        self.dialog.append(self.assistant_message)
