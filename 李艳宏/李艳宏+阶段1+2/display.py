import pandas as pda
import matplotlib.pylab as pyl

data = pda.read_csv("E:\Workspace\Scrapy\Tencent_Crawl\course.csv", nrows=25)
print(data.describe())

data1 = data.values
data2 = data1.T
x = data2[2]  # 价格
y = data2[1]  # 报名人数

pyl.rcParams['font.sans-serif'] = ['SimHei']
data['price'].value_counts().plot(kind='barh')
pyl.title('课程价格统计图')
pyl.show()

pyl.subplot(2, 2, 1)
pyl.title('（价格-报名人数）折线图')
pyl.plot(x, y)

pyl.subplot(2, 2, 2)
pyl.title('（价格-报名人数）散点图')
pyl.plot(x, y, 'o')

pyl.suptitle('课程的价格与报名人数的关系')
pyl.show()
