# -*- coding: utf-8 -*-
import scrapy
import os

from CaiPiaoSpider.items import CaipiaospiderItem
from CaiPiaoSpider.models import UnionLottoExtendModel
from CaiPiaoSpider.migrate import makemigrate
from CaiPiaoSpider import models


class SsqSpiderSpider(scrapy.Spider):
    name = 'ssq_spider'
    allowed_domains = ['kaijiang.500.com']
    start_urls = ["http://kaijiang.500.com/ssq.shtml"]
    def parse(self, response):
        makemigrate(models)
        if not os.path.isdir('output'):
            os.mkdir('output')
        links = response.xpath('//div[@class="iSelectList"]//a/@href').extract()
        for link in links:
            if UnionLottoExtendModel.select().where(UnionLottoExtendModel.url == link):
                continue
            else:
                return scrapy.Request(url=link, callback=self.parse_ball)

    def parse_ball(self, response):
        items = CaipiaospiderItem()
        items['issue'] = '20' + \
                         response.xpath(
                             r'//td[@class="td_title01"]//font[@class="cfont2"]/strong/text()').extract_first()
        items['reds'] = response.xpath('//div[@class="ball_box01"]//li[@class="ball_red"]/text()').extract()
        items['blue'] = response.xpath('//div[@class="ball_box01"]//li[@class="ball_blue"]/text()').extract_first()
        items['url'] = response.url
        items['sale'] = ''.join(filter(str.isdigit, response.xpath(
            '//table[@class="kj_tablelist02"]//span[starts-with(@class,"cfont1")][1]/text()').extract_first()))
        items['residue'] = ''.join(filter(str.isdigit, response.xpath(
            '//table[@class="kj_tablelist02"]//span[starts-with(@class,"cfont1")][2]/text()').extract_first()))
        items['prize_1'] = [x.strip() for x in response.xpath(
            '//table[@class="kj_tablelist02"]/tr[@align="center"][2]/td[not(@class)]/text()').extract()]
        items['prize_2'] = [x.strip() for x in response.xpath(
            '//table[@class="kj_tablelist02"]/tr[@align="center"][3]/td[not(@class)]/text()').extract()]
        items['prize_3'] = [x.strip() for x in response.xpath(
            '//table[@class="kj_tablelist02"]/tr[@align="center"][4]/td[not(@class)]/text()').extract()]
        items['prize_4'] = [x.strip() for x in response.xpath(
            '//table[@class="kj_tablelist02"]/tr[@align="center"][5]/td[not(@class)]/text()').extract()]
        items['prize_5'] = [x.strip() for x in response.xpath(
            '//table[@class="kj_tablelist02"]/tr[@align="center"][6]/td[not(@class)]/text()').extract()]
        items['prize_6'] = [x.strip() for x in response.xpath(
            '//table[@class="kj_tablelist02"]/tr[@align="center"][7]/td[not(@class)]/text()').extract()]
        items['dates'] = response.xpath(
            '//table[@class="kj_tablelist02"]//td[@class="td_title01"]/span[@class="span_right"]/text()').extract_first()
        yield items
