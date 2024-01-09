import os
import time
# 导入logging模块
import logging
from three_dimentions.config import config

# 切换到./logs目录
os.chdir("./logs")
# 创建一个Logger对象，命名为demo
logger = logging.getLogger("3_dimensions_demo")

# 设置Logger的日志级别为DEBUG，表示记录DEBUG及以上级别的日志
logger.setLevel(logging.DEBUG)

# 创建一个Formatter对象，用于设置日志的格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# 创建一个Handler对象，用于将日志输出到控制台
console_handler = logging.StreamHandler()

# 设置Handler的日志级别为INFO，表示输出INFO及以上级别的日志
console_handler.setLevel(logging.INFO)

# 将Formatter对象添加到Handler对象中
console_handler.setFormatter(formatter)

# 将Handler对象添加到Logger对象中
logger.addHandler(console_handler)

# 创建一个Handler对象，用于将日志保存到文件
# 使用time.strftime函数，根据当前的日期和时间，生成文件名
log_directory = (config.MODEL + "_temp-" + str(config.TEMPERATURE) +
                 "_" + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
os.mkdir(log_directory)
file_name = os.path.join(log_directory, log_directory + ".txt")
file_handler = logging.FileHandler(file_name, encoding="utf-8")

# 设置Handler的日志级别为DEBUG，表示保存DEBUG及以上级别的日志
file_handler.setLevel(logging.DEBUG)

# 将Formatter对象添加到Handler对象中
file_handler.setFormatter(formatter)

# 将Handler对象添加到Logger对象中
logger.addHandler(file_handler)