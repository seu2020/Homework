# -*- coding: utf-8 -*-
import scrapy

from  Scra_DataFlow.items import ScraDataflowItem

class CourseSpider(scrapy.Spider):
    name = 'course'
    allowed_domains = ['ke.qq.com']
    start_urls = ['https://ke.qq.com/course/list?mt=1001&st=2002&tt=3019&price_min=1&page=1']

    def parse(self, response):
        result = response.xpath('//section[1]/div/div[3]/ul/li')
        items = []

        for course_ in result:
            # self.log(type(course_))
            # 课程名称
            item_ = ScraDataflowItem()
            course_name = course_.xpath('h4[@class="item-tt item-tt--oneline"]/a/text()').get()
            item_['course_name'] = '{}'.format(course_name.strip() if course_name else '')
            # 培训机构
            course_organization = course_.xpath(
                'div[@class="item-line item-line--middle"]/a[@class="line-cell item-source-link "]/text()').get()
            item_['course_organization'] = course_organization.strip() if course_organization else ''
            # 课程连接
            course_link = course_.xpath('h4[@class="item-tt item-tt--oneline"]/a/@href').get()
            item_['course_link'] = course_link.strip() if course_link else ''
            # 报名人数
            course_number = course_.xpath(
                'div[@class="item-line item-line--bottom"]/span[@class="line-cell item-user custom-string"]/text()').get()
            item_['course_number'] = course_number.strip() if course_number else ''
            # 课程状态
            course_status = course_.xpath('div[@class="item-line item-line--middle"]/span/text()').get()
            item_['course_status'] = course_status.strip() if course_status else ''
            # 课程价格
            course_price = course_.xpath('div[@class="item-line item-line--bottom"]/span/text()').get()
            item_['course_price'] = course_price.strip() if course_price else ''

            items.append(item_)
            yield item_

        for i in range(1, 34):
            next_page = "https://ke.qq.com/course/list?page=" + str(i)
            yield scrapy.Request(next_page, callback=self.parse)