# -*- coding: utf-8 -*-
# 工具函数
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import gzip
import os

import numpy
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
#import tensorflow
from six.moves import urllib
from six.moves import xrange  # pylint: disable=redefined-builtin

from constants import *


def data_type(argv):
    """
    返回激活，权重，占位符变量类型.
    根据argv.use_fp16返回是否使用半精度
    """
    if argv.use_fp16:
        return tf.float16
    else:
        return tf.float32


def maybe_download(filename):
    """
    如果没有下载文件filename，那么把文件下载到WORK_DIRECTORY
    """
    if not tf.gfile.Exists(WORK_DIRECTORY):
        tf.gfile.MakeDirs(WORK_DIRECTORY)
    filepath = os.path.join(WORK_DIRECTORY, filename)
    if not tf.gfile.Exists(filepath):
        filepath, _ = urllib.request.urlretrieve(SOURCE_URL + filename, filepath)
        with tf.gfile.GFile(filepath) as f:
            size = f.size()
        print('Successfully downloaded', filename, size, 'bytes.')
    return filepath


def extract_data(filename, num_images):
    """
    解压filename指定的图像数据集为4D tensor [num_images,  y, x, channels]。
    图像的值从[0, 255]被缩放到了[-0.5, 0.5]
    """
    print('Extracting', filename)
    with gzip.open(filename) as bytestream:
        bytestream.read(16)
        buf = bytestream.read(IMAGE_SIZE * IMAGE_SIZE * num_images * NUM_CHANNELS)
        data = numpy.frombuffer(buf, dtype=numpy.uint8).astype(numpy.float32)
        data = (data - (PIXEL_DEPTH / 2.0)) / PIXEL_DEPTH
        data = data.reshape(num_images, IMAGE_SIZE, IMAGE_SIZE, NUM_CHANNELS)
        return data


def extract_labels(filename, num_images):
    """
    解压标签为一个int64的向量
    """
    print('Extracting', filename)
    with gzip.open(filename) as bytestream:
        bytestream.read(8)
        buf = bytestream.read(1 * num_images)
        labels = numpy.frombuffer(buf, dtype=numpy.uint8).astype(numpy.int64)
    return labels


def fake_data(num_images):
    """
    生成MNIST需要的假数据集
    """
    data = numpy.ndarray(
        shape=(num_images, IMAGE_SIZE, IMAGE_SIZE, NUM_CHANNELS),
        dtype=numpy.float32)
    labels = numpy.zeros(shape=(num_images,), dtype=numpy.int64)
    for image in xrange(num_images):
        label = image % 2
        data[image, :, :, 0] = label - 0.5
        labels[image] = label
    return data, labels


def error_rate(predictions, labels):
    """
    返回基于密集预测和稀疏标签的错误率
    """
    return 100.0 - (
            100.0 *
            numpy.sum(numpy.argmax(predictions, 1) == labels) /
            predictions.shape[0])
