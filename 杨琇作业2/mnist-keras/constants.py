# coding=utf-8

# 全局变量定义

SOURCE_URL = 'http://yann.lecun.com/exdb/mnist/'
# 指定工作目录，保存数据集
WORK_DIRECTORY = 'data'
# 图像的大小
IMAGE_SIZE = 28
# 图像的通道数，为1,即为灰度图像
NUM_CHANNELS = 1
# 图像想素值的范围
PIXEL_DEPTH = 255
# 分类数目，0~9总共有10类
NUM_LABELS = 10
# 验证集大小
VALIDATION_SIZE = 5000  
# 种子
SEED = 66478  # Set to None for random seed.
# 批次大小
BATCH_SIZE = 64
# 训练多少个epoch
NUM_EPOCHS = 10
# 验证集大小
EVAL_BATCH_SIZE = 64
