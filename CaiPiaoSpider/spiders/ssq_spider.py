# -*- coding: utf-8 -*-
import scrapy
import os

from CaiPiaoSpider.items import CaipiaospiderItem


class SsqSpiderSpider(scrapy.Spider):
    name = 'ssq_spider'
    # allowed_domains = ['www.cwl.gov.cn/cwl_admin']
    allowed_domains = ['kaijiang.500.com']
    # start_urls = ["http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=ssq&issueCount=&issueStart=&issueEnd=&dayStart=2003-02-16&dayEnd=2019-09-29&pageNo=11"]
    start_urls = ["http://kaijiang.500.com/ssq.shtml"]

    # def make_requests_from_url(self, url):
    #     headers = {"Accept": "application/json, text/javascript, */*; q=0.01",
    #                "Accept-Encoding": "gzip, deflate",
    #                "Accept-Language": "zh-CN,zh;q=0.9",
    #                "Connection": "keep-alive",
    #                "Cookie": "UniqueID=duy2eVhDCQs03rGl1569721080398; Sites=_21; _ga=GA1.3.628578396.1569720813; _gid=GA1.3.12329107.1569720813; 21_vq=27",
    #                "Host": "www.cwl.gov.cn",
    #                "Referer": "http://www.cwl.gov.cn/kjxx/ssq/kjgg/",
    #                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    #                "X-Requested-With": "XMLHttpRequest"
    #                }
    #     return scrapy.http.Request(url, headers=headers,dont_filter=True)

    def parse(self, response):
        # return self.parse_data(response)
        if not os.path.isdir('output'):
            os.mkdir('output')
        links = response.xpath('//div[@class="iSelectList"]//a/@href').extract()
        for link in links:
            return scrapy.Request(url=link, callback=self.parse_ball)

    def parse_ball(self, response):
        items = CaipiaospiderItem()
        items['id'] = '20' + \
                      response.xpath(r'//td[@class="td_title01"]//font[@class="cfont2"]/strong/text()').extract_first()
        items['reds'] = response.xpath('//div[@class="ball_box01"]//li[@class="ball_red"]/text()').extract()
        items['blue'] = response.xpath('//div[@class="ball_box01"]//li[@class="ball_blue"]/text()').extract_first()
        items['url'] = response.url
        yield items
