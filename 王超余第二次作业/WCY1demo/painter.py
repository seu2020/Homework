# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'painter.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image, ImageGrab
from recognize import rec_the_img
import numpy as np


class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setMouseTracking(False)
        self.pos = []  # 存储鼠标的位置
        self.setObjectName("MainWindow")
        self.resize(480, 320)
        self.move(100, 100)

        self.pushButtonReg = QtWidgets.QPushButton("识别", self)
        self.pushButtonReg.setGeometry(QtCore.QRect(200, 240, 50, 30))
        self.pushButtonReg.setObjectName("pushButtonReg")
        self.pushButtonReg.clicked.connect(self.pushButtonReg_click_on)

        self.pushButtonClr = QtWidgets.QPushButton("清空", self)
        self.pushButtonClr.setGeometry(QtCore.QRect(300, 10, 140, 81))
        self.pushButtonClr.setObjectName("pushButtonClr")
        self.pushButtonClr.clicked.connect(self.pushButtonClr_click_on)

        self.pushButtonShowBin = QtWidgets.QPushButton("显示捕获图片", self)
        self.pushButtonShowBin.setGeometry(QtCore.QRect(300, 210, 140, 81))
        self.pushButtonShowBin.setObjectName("pushButtonClr")
        self.pushButtonShowBin.clicked.connect(self.pushButtonShowBin_click_on)

        self.result_title = QtWidgets.QLabel("训练结果", self)
        self.result_title.setGeometry(QtCore.QRect(10, 240, 71, 31))
        self.result_title.setObjectName("result_title")

        self.result = QtWidgets.QLabel("", self)
        self.result.setGeometry(QtCore.QRect(100, 240, 61, 31))
        self.result.setTextFormat(QtCore.Qt.AutoText)
        self.result.setOpenExternalLinks(False)
        self.result.setObjectName("result")

        self.label = QtWidgets.QLabel('', self)
        self.label.setGeometry(QtCore.QRect(10, 10, 261, 211))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setText("")
        self.label.setObjectName("label")

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        pen = QtGui.QPen(QtCore.Qt.black, 10, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        if len(self.pos) > 1:
            pos_last = self.pos[0]
            for pos_temp in self.pos:
                pos_current = pos_temp
                # 防止松开鼠标后轨迹不断开
                if pos_current == (-1, -1):  # 如果遇到断点
                    pos_last = (-1, -1)
                    continue
                if pos_last == (-1, -1):
                    pos_last = pos_current
                    continue
                # 每次画一小段线段，遍历完轨迹数组以后，便可以显示出鼠标移动的轨迹
                painter.drawLine(pos_last[0], pos_last[1], pos_current[0], pos_current[1])
                pos_last = pos_current
        painter.end()

    def mouseMoveEvent(self, QMouseEvent):
        # 鼠标移动时，更新当前位置，并在上一个位置和当前位置间画线
        pos_temp = (QMouseEvent.pos().x(), QMouseEvent.pos().y())
        self.pos.append(pos_temp)

        self.update()  # 更新显示

    def mouseReleaseEvent(self, event):
        self.pos.append((-1, -1))  # 松开鼠标后，增加断点
        self.update()

    def pushButtonReg_click_on(self):
        bbox = (150, 180, 350, 330)
        img = ImageGrab.grab(bbox)  # 截屏
        img = img.convert('L')  # 转成灰度图
        img = img.resize((28, 28), Image.ANTIALIAS)  # 将截图转换成28*28
        reg_result = rec_the_img(img)
        self.result.setText(str(reg_result))  # 显示识别结果
        self.update()

    def pushButtonClr_click_on(self):
        self.result.setText("")
        self.pos = []  # 清空数组
        self.update()

    def pushButtonShowBin_click_on(self):
        bbox = (120, 160, 370, 360)
        img = ImageGrab.grab(bbox)  # 截屏
        img = img.convert('L')
        img = img.resize((28, 28), Image.ANTIALIAS)  # 将截图转换成28*28
        img.show()
        img_val = np.array(img, 'f')
        print(img_val)
        self.update()

    def pushButtonCor_click_on(self):
        cvl = self.CorrectVal.text()
        print(int(cvl))


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    app.exec_()
