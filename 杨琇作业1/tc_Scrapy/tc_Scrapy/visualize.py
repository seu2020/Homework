# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
from matplotlib.colors import ListedColormap

# 获取数据集 
fee_course = pd.read_csv('fee_course.csv', nrows=226)
# 数据处理
print(fee_course.describe())

course_items = fee_course.values
lable = course_items.T
x = lable[4]  # 课程价格
y = lable[2]  # 报名人数

# 可视化
plb.rcParams['font.sans-serif'] = ['SimHei']
fee_course['price'].value_counts().plot(kind='barh')
plb.title('相同价格的课程门数')
plb.show()


# 获取数据集 
fee_course = pd.read_csv('fee_course.csv', usecols=['name', 'org'])

# 数据处理
fee_org = fee_course.groupby(['org'])
course_num = fee_org.count()
course_num = course_num['name']
print(course_num)

# 对结果进行可视化
hist = course_num.plot.hist(by='name', density=False, title='开设相同课程数目的机构数')
hist.set_xlabel('开设课程数目')
hist.set_ylabel('机构数')
plt.show()


