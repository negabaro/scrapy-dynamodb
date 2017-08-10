# -*- coding: utf-8 -*-
import scrapy


class NetflixSpider(scrapy.Spider):
    name = 'netflix'
    allowed_domains = ['https://www.netflix.com/jp/title/80117470']
    start_urls = ['http://https://www.netflix.com/jp/title/80117470/']

    def parse(self, response):
        pass
