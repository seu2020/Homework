# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import cv2

# 从tensorflow里导入keras和keras.layer
from tensorflow import keras
from tensorflow.keras import layers

# 导入工具函数
from utils import *


def inference(dtype):
    """
    使用keras定义mnist模型
    """
    # 定义truncated_normal initializer
    tn_init = keras.initializers.truncated_normal(0, 0.1, SEED, dtype=dtype)
    # 定义constant initializer
    const_init = keras.initializers.constant(0.1, dtype)
    # 定义L2 regularizer
    l2_reg = keras.regularizers.l2(5e-4)

    """ 
    输入占位符。如果输入图像的shape是(28, 28, 1)，输入的一批图像(16张图)的shape
    是(16, 28, 28, 1)；那么，在定义Input时，shape参数只需要一张图像的大小，也就
    是(28, 28, 1)，而不是(16, 28, 28, 1)。
    """
    # inputs: shape(None, 28, 28, 1)
    inputs = layers.Input(shape=(IMAGE_SIZE, IMAGE_SIZE, NUM_CHANNELS), dtype=dtype)

    """
    卷积，输出shape为(None, 28,18,32)。Conv2D的第一个参数为卷积核个数；第二个参数为卷积
    核大小，和tensorflow不同的是，卷积核的大小只需指定卷积窗口的大小，例如在tensorflow中，
    卷积核的大小为(BATCH_SIZE, 5, 5, 1)，那么在Keras中，只需指定卷积窗口的大小(5, 5)，
    最后一维的大小会根据之前输入的形状自动推算，假如上一层的shape为(None, 28, 28, 1)，那
    么最后一维的大小为1；第三个参数为strides，和上一个参数同理。其他参数可查阅Keras的官方文档。
    """
    # conv1: shape(None, 28, 28, 32)
    conv1 = layers.Conv2D(32, (5, 5), strides=(1, 1), padding='same',
                          activation='relu', use_bias=True,
                          kernel_initializer=tn_init, name='conv1')(inputs)
    # pool1: shape(None, 14, 14, 32)
    pool1 = layers.MaxPool2D(pool_size=(2, 2), strides=(2, 2), padding='same', name='pool1')(conv1)
    # conv2: shape(None, 14, 14, 64)
    conv2 = layers.Conv2D(64, (5, 5), strides=(1, 1), padding='same',
                          activation='relu', use_bias=True,
                          kernel_initializer=tn_init,
                          bias_initializer=const_init, name='conv2')(pool1)
    # pool2: shape(None, 7, 7, 64)
    pool2 = layers.MaxPool2D(pool_size=(2, 2), strides=(2, 2), padding='same', name='pool2')(conv2)
    # flatten: shape(None, 3136)
    flatten = layers.Flatten(name='flatten')(pool2)
    # fc1: shape(None, 512)
    fc1 = layers.Dense(512, 'relu', True, kernel_initializer=tn_init,
                       bias_initializer=const_init, kernel_regularizer=l2_reg,
                       bias_regularizer=l2_reg, name='fc1')(flatten)
    # dropout
    dropout1 = layers.Dropout(0.5, seed=SEED)(fc1)
    # dense2: shape(None, 10)
    fc2 = layers.Dense(NUM_LABELS, activation=None, use_bias=True,
                       kernel_initializer=tn_init, bias_initializer=const_init, name='fc2',
                       kernel_regularizer=l2_reg, bias_regularizer=l2_reg)(dropout1)
    # softmax: shape(None, 10)
    softmax = layers.Softmax(name='softmax')(fc2)
    # make new model
    model = keras.Model(inputs=inputs, outputs=softmax, name='nmist')
    return model


def main(argv=None):
    if argv.self_test:
        """
        为了测试模型是否可以运行，生成了一些随机数据集。
        """
        print('Running self-test...')
        # 生成训练集
        train_data, train_labels = fake_data(256)
        # 生成验证集
        validation_data, validation_labels = fake_data(EVAL_BATCH_SIZE)
        # 生成测试集
        test_data, test_labels = fake_data(EVAL_BATCH_SIZE)
        # 只训练一个epoch
        num_epochs = 1
    else:
        """
        准备手写数字数据集
        """
        # 下载数据集
        train_data_filename = maybe_download('train-images-idx3-ubyte.gz')
        train_labels_filename = maybe_download('train-labels-idx1-ubyte.gz')
        test_data_filename = maybe_download('t10k-images-idx3-ubyte.gz')
        test_labels_filename = maybe_download('t10k-labels-idx1-ubyte.gz')

        # 把下载的数据解压为numpy数组
        train_data = extract_data(train_data_filename, 60000)
        train_labels = extract_labels(train_labels_filename, 60000)
        test_data = extract_data(test_data_filename, 10000)
        test_labels = extract_labels(test_labels_filename, 10000)

        # 分割train_data与train_labels，得到训练集以及验证集validation set.
        validation_data = train_data[:VALIDATION_SIZE, ...]
        validation_labels = train_labels[:VALIDATION_SIZE]
        train_data = train_data[VALIDATION_SIZE:, ...]
        train_labels = train_labels[VALIDATION_SIZE:]
        num_epochs = NUM_EPOCHS

        # 保存一下第一张图片，用来测试
        img0 = test_data[0]
        # 因为test_data被缩放到了[-0.5, 0.5]，所以要恢复到原来的范围[0, 255]
        img0 = img0*PIXEL_DEPTH+PIXEL_DEPTH/2
        # 保存
        cv2.imwrite('test0.png', img0)

    # 对label进行one-hot编码，因为模型的最后一层有10个输出单元（10个类别）
    train_labels = keras.utils.to_categorical(train_labels)
    validation_labels = keras.utils.to_categorical(validation_labels)
    test_labels = keras.utils.to_categorical(test_labels)

    # 获取模型
    model = inference(data_type(argv))
    # 打印模型的信息
    model.summary()

    # 编译模型；第一个参数是优化器；第二个参数为loss，
    # 因为是多元分类问题，固为'categorical_crossentropy'；
    # 第三个参数为metrics，就是在训练的时候需要监控的指标列表。
    model.compile(optimizer=keras.optimizers.SGD(lr=0.01, momentum=0.9, decay=1e-5),
                  loss='categorical_crossentropy', metrics=['accuracy'])

    # 训练模型
    # 设置回调
    callbacks = [
        # 把TensorBoard的日志写入文件夹'./logs'
        keras.callbacks.TensorBoard(log_dir='./logs'),
    ]

    # 开始训练
    model.fit(train_data, train_labels, BATCH_SIZE, epochs=num_epochs,
              validation_data=(validation_data, validation_labels), callbacks=callbacks)

    # 评估模型
    print('', 'evaluating on test sets...')
    loss, accuracy = model.evaluate(test_data, test_labels)
    print('test loss:', loss)
    print('test Accuracy:', accuracy)

    # 保存模型
    model.save('mnist-model.h5')


if __name__ == '__main__':
    # 定义parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--use_fp16',
        default=False,
        help='Use half floats instead of full floats if True.',
        action='store_true')
    parser.add_argument(
        '--self_test',
        default=False,
        action='store_true',
        help='True if running a self test.')
    # 解析参数
    FLAGS, unparsed = parser.parse_known_args()
    # 调用主函数
    main(FLAGS)
