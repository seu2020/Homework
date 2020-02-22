import scipy.io as sio
import tensorflow as tf
import numpy as np
from PIL import Image, ImageGrab
import matplotlib.pyplot as plt
from function import weight_variable, bias_variable, conv2d, max_pool_2X2


def rec_the_img(img):
    net = sio.loadmat('net.mat')

    # 载入网络数据
    W_conv1 = net['W_conv1']
    b_conv1 = net['b_conv1']
    W_conv2 = net['W_conv2']
    b_conv2 = net['b_conv2']
    W_fc1 = net['W_fc1']
    b_fc1 = net['b_fc1']
    W_fc2 = net['W_fc2']
    b_fc2 = net['b_fc2']

    img_val = list(img.getdata())  # 获取图片像素值
    img_val = [(255 - x) * 1.0 / 255.0 for x in img_val]  # 转换像素范围到[0 1], 0是纯白 1是纯黑
    # img_val = np.array(img_val, 'f')

    img_val = tf.reshape(img_val, [-1, 28, 28, 1])

    # 计算第一层输出
    h_conv1 = tf.nn.relu(conv2d(img_val, W_conv1) + b_conv1)
    h_pool1 = max_pool_2X2(h_conv1)

    # 计算第二层输出
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2X2(h_conv2)

    # 计算密集连接层输出
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    # 计算最终输出
    y_conv = tf.nn.softmax(tf.matmul(h_fc1, W_fc2) + b_fc2)

    # 预测结果
    result = tf.argmax(y_conv, 1)

    with tf.Session() as sess:
        result = result.eval()
        # print(img_val.eval())
        print("It is number %d" % result)
        return result
