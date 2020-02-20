# -*- coding: utf-8 -*-
import scrapy
from tc_Scrapy.items import TencentItem

class CourseSpider(scrapy.Spider):
    name = 'course'
    allowed_domains = ['ke.qq.com']
    #start_urls = ['http://ke.qq.com/']
    url = 'https://ke.qq.com/course/list/python爬虫?price_min=1&page=%d'
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'
    }
    page_no = 1


    def start_requests(self):
        # 构建爬取的网页
        request = scrapy.Request(
            url=self.url % self.page_no,
            callback=self.extract_course,
            method='GET',
            headers=self.headers)
        return [request]


    def error_handle(self,err):
        print('无数据可爬')


    def extract_course(self, response):
        # 解析数据，并保存成csv文件
        output = []
        print('开始处理数据')
        # xpath
        courses = response.xpath('//div[@data-report-module="middle-course"]/ul/li')
        for course in courses:
            # 数据项
            item_ = TencentItem()
            # 课程连接
            link = course.xpath('h4/a[@class="item-tt-link"]/@href').get()
            item_['link'] = link.strip() if link else ''

            # 课程名称
            name = course.xpath('h4/a[@class="item-tt-link"]/text()').get()
            item_['name'] = '{}'.format(name.strip() if name else '')

            # 培训机构org[@class="line-cell item-source-link"]
            #item_['org'] = course.xpath("div[contains(@class, 'item-line--middle')]/a[contains(@class, 'item-source-link')]/text()").extract()
            org = course.xpath('div[@class="item-line item-line--middle"]/a/text()').get()
            item_['org'] = org.strip() if org else ''

            # 课程价格[@class="line-cell item-price custom-string"]
            #item_['price'] = course.xpath("div[contains(@class, 'item-line--bottom')]/span[contains(@class, 'item-price')]/text()").extract()
            price = course.xpath('div[@class="item-line item-line--bottom"]/span/text()').get()
            item_['price'] = price.strip() if price else ''

            # 购买人数
            number = course.xpath('div[@class="item-line item-line--bottom"]/span[@class="line-cell item-user custom-string"]/text()').get()
            item_['number'] = number.strip()  if number else ''

            output.append(item_)
        print('------------------------------')
        if self.page_no <= 10:
            self.page_no += 1
            request = scrapy.Request(
                url=self.url % self.page_no,
                callback=self.extract_course,
                method='GET',
                headers=self.headers, dont_filter=True)
            output.append(request)
        # 返回数据项到管道
        return output