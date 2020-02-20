# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cv2
import numpy as np

from tensorflow import keras


if __name__ == '__main__':
    # 读图片
    # read image
    testexample = cv2.imread('testexample.png', cv2.IMREAD_UNCHANGED)
    print(testexample.shape)
    # 扩展维度为4维，因为模型的输入需要是4维
    testexample = np.resize(testexample, (1, testexample.shape[0], testexample.shape[1], 1))
    print(testexample.shape)

    # 恢复模型以及权重
    # read model and weights
    model = keras.models.load_model('mnist-model.h5')
    # 获取模型最后一层，也就是softmax层的输出，输出的shape为(1, 10)
    last_layer_output = model.predict(testexample)


    # 获取最大值的索引
    max_index = np.argmax(last_layer_output, axis=-1)
    print('predict number: %d' % (int(max_index[0])))
    print('probability: ', last_layer_output[0][max_index])
