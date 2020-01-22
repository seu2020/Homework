# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from Tencent_Crawl.items import TencentCrawlItem


class CourseSpider(scrapy.Spider):
    name = 'course'
    allowed_domains = ['ke.qq.com']
    start_urls = ['https://ke.qq.com/course/list/']

    def parse(self, response):
        items = []
        # result = response.xpath("//div[@class = 'market-bd market-bd-6 course-list course-card-list-multi-wrap "
        # "js-course-list']")
        result = response.xpath("//section[1]/div/div[3]/ul/li")
        for course in result:
            item = TencentCrawlItem()
            item['title'] = course.xpath("h4/a/text()").extract()
            item['task'] = course.xpath("div[1]/span/text()").extract()
            item['agency'] = course.xpath("div[1]/a/text()").extract()
            item['price'] = course.xpath("div[2]/span[1]/text()").extract()
            item['custom'] = course.xpath("normalize-space(div[2]/span[2]/text())").extract()
            # item['task'] = course.xpath("//div[contains(@class, 'item-line--middle')]/span/text()").extract()
            # item['agency'] = course.xpath("//div[contains(@class, 'item-line--middle')]/a[contains("
            # "@class, 'item-source-link')]/text()").extract()
            # item['price'] = course.xpath("//div[contains(@class, 'item-line--bottom')]/span[contains("
            # "@class, 'item-price')]/text()").extract()
            # item['custom'] = course.xpath("//div[contains(@class, 'item-line--bottom')]/span[contains("
            # "@class, 'item-user')]/text()").extract()
            items.append(item)
            yield item
        # yield item
        for i in range(1, 34):
            next_page = "https://ke.qq.com/course/list?page=" + str(i)
            yield scrapy.Request(next_page, callback=self.parse)
