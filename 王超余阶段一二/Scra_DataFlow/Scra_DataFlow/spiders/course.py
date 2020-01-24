# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from  Scra_DataFlow.items import ScraDataflowItem

class CourseSpider(scrapy.Spider):
    name = 'course'
    allowed_domains = ['ke.qq.com']


    start_urls = ['https://ke.qq.com/course/list?page=1',
                  # 'https://ke.qq.com/course/list?page=2',
                  # 'https://ke.qq.com/course/list?page=3',
                  # 'https://ke.qq.com/course/list?page=4',
                  # 'https://ke.qq.com/course/list?page=5',
                  # 'https://ke.qq.com/course/list?page=6',
                  # 'https://ke.qq.com/course/list?page=7',
                  # 'https://ke.qq.com/course/list?page=8',
                  # 'https://ke.qq.com/course/list?page=9',
                  # 'https://ke.qq.com/course/list?page=10',
                  # 'https://ke.qq.com/course/list?page=11',
                  ]

    def parse(self, response):
        result = response.xpath('//section[1]/div/div[3]/ul/li')
        items = []    # 数据项数组列表
        for course_ in result:
            # 数据项
            item_ = ScraDataflowItem()
            course_name = course_.xpath('h4[@class="item-tt item-tt--oneline"]/a/text()').get()
            item_['course_name'] = '{}'.format(course_name.strip() if course_name else '')
            course_organization = course_.xpath(
                'div[@class="item-line item-line--middle"]/a[@class="line-cell item-source-link "]/text()').get()
            item_['course_organization'] = course_organization.strip() if course_organization else ''
            # 课程连接
            course_link = course_.xpath('h4[@class="item-tt item-tt--oneline"]/a/@href').get()
            item_['course_link'] = course_link.strip() if course_link else ''
            # 报名人数
            course_number = course_.xpath(
                'div[@class="item-line item-line--bottom"]/span[@class="line-cell item-user custom-string"]/text()').get()
            item_['course_number'] = course_number.strip()  if course_number else ''
            # 课程状态
            course_task = course_.xpath('div[@class="item-line item-line--middle"]/span/text()').get()
            item_['course_task'] = course_task.strip() if course_task else ''
            # 课程价格
            course_price = course_.xpath('div[@class="item-line item-line--bottom"]/span/text()').get()
            item_['course_price'] = course_price.strip() if course_price else ''
            items.append(item_)
            yield item_
        #     items.append(item_)
        # # 返回数据项到管道
        # return items
        i = 2
        while i <= 30:
            next_url = "https://ke.qq.com/course/list?page=1" + str(i)
            i = i + 1
            yield Request(next_url)
