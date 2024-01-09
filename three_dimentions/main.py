import os
import sys
from openai import OpenAI

from chat_gpt import dialog
from config import config
from tools import functions
from config.logger import logger, log_directory, file_name
from simulations import simulator


def initiate_dialog():
    """
    初始化对话信息，告诉chatgpt场景，问题，以及回答方法
    :return:
    """
    logger.info("SYSTEM: %s " % MyDialog.system_message.get('content'))
    # 基于目标和机器人坐标，制作user_message，并加入ChatGpt对话
    MyDialog.create_user_message(simulator=RobotSimulator)
    logger.info("USER: %s" % MyDialog.user_message.get('content'))

    # 基于目标和机器人坐标，本地进行思维链推理
    local_engine_ans = RobotSimulator.local_engine()
    # 将本地思维链推理结果，作为学习内容，加入ChatGpt对话
    MyDialog.create_assistant_message(response=local_engine_ans)
    # 解析assistant_message，获得执行动作
    action = MyDialog.analyze_action(MyDialog.assistant_message.get('content'))
    logger.info("ASSISTANT示例动作: %s" % action)
    logger.info("ASSISTANT示例逻辑: %s" % MyDialog.assistant_message.get('content'))

    RobotSimulator.turn += 1
    # 根据action，”仿真“机器人的下一步动作导致的新位置信息
    RobotSimulator.update_simulation(action=action)
    # 然后制作成prompt格式
    MyDialog.create_user_message(simulator=RobotSimulator)
    logger.info("USER: %s" % MyDialog.user_message.get('content'))


def interact_with_gpt():
    """
    在规定仿真次数以内，逐次调用chatgpt api，得到机器人动作方案，然后根据该动作，仿真机器人的位置信息
    :return:
    """
    logger.info('以下开始调用%s进行推理\n' % config.MODEL)

    while RobotSimulator.turn < config.TURN_MAX:
        RobotSimulator.turn += 1
        # 调用OpenAI的chat.completions.create接口，生成助手的消息，即水下机器人的动作
        gpt_response = client.chat.completions.create(model=config.MODEL,
                                                      messages=MyDialog.dialog,
                                                      temperature=config.TEMPERATURE)

        assistant_message = gpt_response.choices[0].message.content
        assistant_message = assistant_message.replace("\n", "")
        action = MyDialog.analyze_action(assistant_message)
        logger.info("ASSISTANT: %s" % action)
        logger.info("Chatgpt判断逻辑: %s" % assistant_message)
        local_engine_ans = RobotSimulator.local_engine()
        logger.info("本地计算判断逻辑: %s \n" % local_engine_ans)

        MyDialog.create_assistant_message(response=assistant_message)
        # 根据action，”仿真“机器人的下一步动作导致的新位置信息
        RobotSimulator.update_simulation(action=action)
        # 然后制作成prompt格式
        MyDialog.create_user_message(simulator=RobotSimulator)
        logger.info("USER: %s" % MyDialog.user_message.get('content'))

        if functions.distance(RobotSimulator.robot, RobotSimulator.target) < config.DISTANCE_THRESHOLD:
            # 结束循环
            logger.info('机器人接近目标，探索完成')
            break
    if RobotSimulator.turn == config.TURN_MAX:
        print('机器人在规定探索次数内没有接近目标，探索终止')


def simulation():
    """
    仿真主程序
    :return:
    """
    # 初始化对话信息，告诉chatgpt场景，问题，以及回答方法
    initiate_dialog()
    # 在规定仿真次数以内，逐次调用chatgpt api，得到机器人动作方案，然后根据该动作，仿真机器人的位置信息
    interact_with_gpt()


if __name__ == '__main__':
    # 初始化OpenAI客户端
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    # 初始化仿真器
    RobotSimulator = simulator.Simulator()
    # 初始化ChatGpt对话对象
    MyDialog = dialog.ChatGptDialog()
    # 仿真主程序
    simulation()
    RobotSimulator.plot_figure(directory=log_directory, elev=30, azim=0, snapshot=True)
    logger.info('程序结束')
