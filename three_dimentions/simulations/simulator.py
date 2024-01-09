import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch

from three_dimentions.chat_gpt import dialog
from three_dimentions.config import config


# 定义一个3D箭头类，继承自FancyArrowPatch
class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)


class Simulator:
    def __init__(self):
        """
        定义一个初始化位置的方法
        :return:
        """
        # 从config文件中读取水下机器人的初始位置
        self.robot = np.array(config.SubmarinePos, dtype="float64")
        self.robot_trajectory = np.array([self.robot], dtype="float64")
        # 从config文件中读取目标物体的位置
        self.target = np.array(config.TargetPos, dtype="float64")
        # 从config文件中读取水流速度
        self.water_v = np.array(config.WaterVelocity, dtype="float64")
        self.turn = 0

    def local_engine(self):
        """
        根据水下机器人的当前3维坐标和目标3维坐标，计算在水流作用下，水下机器人的实际航行方向，预估时间，掌舵单位向量和掌舵速度值
        该函数的计算逻辑用于测试chatGpt的逻辑推理能力
        :return: ans
        """
        target = self.target[-1] + (self.target[-1] - self.target[-2])
        # 潜艇与目标位置之间的距离
        distance_v = target - self.robot
        distance = np.linalg.norm(distance_v)
        # 航线方向单位向量
        direction = np.divide(distance_v, distance)
        # 预估时间
        eta = distance / config.SubmarineSpeed

        submarine_speed = config.SubmarineSpeed
        # 如果预估时间大于一次仿真时间，那么按规定SubmarineSpeed计算
        if eta > config.DeltaT:
            # 潜艇的掌舵速度向量
            submarine_vector = config.SubmarineSpeed * direction - self.water_v
        # 如果预估时间小于等于一次仿真时间，那么重新计算submarine_speed（比较小的一个值）
        else:
            submarine_speed = distance / config.DeltaT
            # 潜艇的掌舵速度向量
            submarine_vector = submarine_speed * direction - self.water_v

        action = list(submarine_vector)

        thought1 = ("1. 根据target的当前坐标和历史坐标信息，假设target匀速运动，预计在%s秒后，target会出现在：%s + (%s - %s) = %s"
                    % (config.DeltaT, self.target[-1], self.target[-1], self.target[-2], target))
        thought2 = ("2. robot与target的位移向量distance_v= %s - %s  = %s，robot与target距离distance=norm(distance_v)= %s，"
                    "所以实际航行单位向量direction=distance_v/norm(distance)=%s/%s = %s"
                    % (target, self.robot, distance_v, np.around(distance, decimals=2),
                       distance_v, np.around(distance, decimals=2), np.around(direction, decimals=2)))
        thought3 = ("3. 设置机器人水下实际运行速度SubmarineSpeed=%s(米/秒), 那么预计航行：eta=%s/%s=%s秒，会到达目的地"
                    % (config.SubmarineSpeed, np.around(distance, decimals=2),
                       config.SubmarineSpeed, np.around(eta, decimals=2)))
        thought4 = ("4. 鉴于eta=%s(秒)大于单次仿真时间%s(秒)，那么该次仿真机器人的实际运行速度SubmarineSpeed可以维持在%s米/秒, "
                    "如果eta小于单次仿真时间，那么机器人的实际运行速度SubmarineSpeed需要降低，"
                    "从而保证机器人在单次仿真时间后正好到达目的地附近"
                    "根据向量法则，机器人的掌舵速度向量submarine_vector + 水流速度向量water_v等于机器人实际航行速度向量，"
                    "所以submarine_vector=SubmarineSpeed*direction-water_v=%s*%s-%s=%s"
                    % (np.around(eta, decimals=2), config.DeltaT, config.SubmarineSpeed, submarine_speed,
                       np.around(direction, decimals=2), self.water_v, np.around(submarine_vector, decimals=2)))
        thought6 = "综上所述，最后输出的掌舵速度向量为：%s" % action
        assistant_answer = " ".join([thought1, thought2, thought3, thought4, thought6])
        return assistant_answer

    def update_simulation(self, action):
        # 根据机器人的掌舵向量，更新机器人的三维坐标
        self.robot += (np.array(action) + self.water_v) * config.DeltaT
        # 将更新机器人的三维坐标存入轨迹中
        self.robot_trajectory = np.vstack([self.robot_trajectory, self.robot])

        # 根据目标的运动速度和当前位置，仿真目标的下一个位置
        target = self.target[-1] + np.array(config.TargetVelocity, dtype="float64") * config.DeltaT
        # 将仿真得到的新目标坐标，加入目标的历史坐标中
        self.target = np.vstack([self.target, target])

    def plot_figure(self, elev=30, azim=45, directory='test', snapshot=False):
        # 创建一个3D图形对象
        fig = plt.figure(figsize=(8, 8), dpi=100)
        ax = fig.add_subplot(111, projection='3d')

        # 从RobotSimulator获取robot_trajectory和target
        robot_trajectory = self.robot_trajectory
        target = self.target

        # 设置坐标轴的标签
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        plt.title('3D under-water robot follows target \n'
                  'under CHATGPT instruction')
        # 设置3d角度
        ax.view_init(elev, azim)

        ax.plot(robot_trajectory[0, 0], robot_trajectory[0, 1], robot_trajectory[0, 2], 'ro-',
                label='robot_trajectory')
        ax.plot(target[1, 0], target[1, 1], target[1, 2], 'b*-', label='target')

        if snapshot:

            file_name = directory + '_0' + '.jpeg'
            ax.legend()
            ax.set_xlim3d([0, 25])
            ax.set_ylim3d([0, 50])
            ax.set_zlim3d([-25, 0])
            plt.savefig('../logs/' + directory + '/' + file_name)

            for idx in range(len(robot_trajectory)-1):
                # 绘制robot_trajectory的轨迹，用红色实线表示
                ax.plot(robot_trajectory[idx:idx+2, 0],
                        robot_trajectory[idx:idx+2, 1],
                        robot_trajectory[idx:idx+2, 2], 'ro-')

                # 绘制target的轨迹，用蓝色虚线表示
                ax.plot(target[idx+1:idx+3, 0],
                        target[idx+1:idx+3, 1],
                        target[idx+1:idx+3, 2], 'b*-')
                file_name = directory + '_' + str(idx+1) + '.jpeg'
                ax.legend()
                ax.set_xlim3d([0, 25])
                ax.set_ylim3d([0, 50])
                ax.set_zlim3d([-25, 0])
                plt.savefig('../logs/' + directory + '/' + file_name)

        # 绘制robot_trajectory的轨迹，用红色实线表示
        ax.plot(robot_trajectory[:, 0], robot_trajectory[:, 1], robot_trajectory[:, 2], 'ro-')

        # 绘制target的轨迹，用蓝色虚线表示
        ax.plot(target[1:, 0], target[1:, 1], target[1:, 2], 'b*-')

        # 在轨迹线上添加箭头，表示运动的方向
        # 可以根据需要调整箭头的数量和位置
        arrow_prop_dict1 = dict(mutation_scale=20, arrowstyle='-|>', color='r', shrinkA=0, shrinkB=0)

        middle_index = int(len(robot_trajectory)/2)
        # 在robot_trajectory的轨迹线上添加1个箭头
        a = Arrow3D([robot_trajectory[middle_index-1, 0], robot_trajectory[middle_index, 0]],
                    [robot_trajectory[middle_index-1, 1], robot_trajectory[middle_index, 1]],
                    [robot_trajectory[middle_index-1, 2], robot_trajectory[middle_index, 2]],
                    **arrow_prop_dict1)
        ax.add_artist(a)

        arrow_prop_dict2 = dict(mutation_scale=20, arrowstyle='-|>', color='b', shrinkA=0, shrinkB=0)
        # 在target的轨迹线上添加1个箭头
        b = Arrow3D([target[middle_index, 0], target[middle_index+1, 0]],
                    [target[middle_index, 1], target[middle_index+1, 1]],
                    [target[middle_index, 2], target[middle_index+1, 2]],
                    **arrow_prop_dict2)
        ax.add_artist(b)

        # 显示图例
        # ax.legend()
        ax.set_xlim3d([0, 25])
        ax.set_ylim3d([0, 50])
        ax.set_zlim3d([-25, 0])
        # 使用plt.show()函数，显示图形，或者使用plt.savefig()函数，保存图形到文件
        file_name = directory + '.jpeg'
        plt.savefig('../logs/' + directory + '/' + file_name)
        # 显示图形
        plt.show()


def simulation_loop():
    while RobotSimulator.turn < config.TURN_MAX:
        print("当前是第%s轮仿真" % RobotSimulator.turn)
        print("target当前坐标为：%s target历史坐标为：%s robot坐标为：%s 水流速度water_v为：%s(米/秒)"
              % (RobotSimulator.target[-1], RobotSimulator.target[-2],
                 np.around(RobotSimulator.robot, decimals=2), RobotSimulator.water_v))
        assistant_message = RobotSimulator.local_engine()
        action = MyDialog.analyze_action(assistant_message)
        print("本地计算运动指令:  %s" % action)
        RobotSimulator.update_simulation(action)
        RobotSimulator.turn += 1
        distance = np.linalg.norm(RobotSimulator.robot - RobotSimulator.target[-1])
        if distance < config.DISTANCE_THRESHOLD:
            # 结束循环
            print('机器人接近目标，距离为：%.2f, 探索完成' % distance)
            print("目标的坐标为：%s 机器人的坐标为：%s"
                  % (RobotSimulator.target[-1], np.around(RobotSimulator.robot, decimals=2)))
            break
    if RobotSimulator.turn == config.TURN_MAX:
        print('机器人在规定探索次数内没有接近目标，探索终止')


if __name__ == '__main__':
    # 初始化仿真器
    RobotSimulator = Simulator()
    MyDialog = dialog.ChatGptDialog()
    simulation_loop()
    RobotSimulator.plot_figure(elev=30, azim=0, snapshot=True)
    print("finish")
