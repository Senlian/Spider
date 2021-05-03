# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from CaiPiaoSpider import models
from CaiPiaoSpider.migrate import makemigrate
from CaiPiaoSpider.models import UnionLottoModel, UnionLottoExtendModel, db


class CaipiaospiderPipeline(object):
    def open_spider(self, spider):
        out_html = os.path.join('output', 'shuangseqiu.html')
        with open(out_html, 'w') as f:
            f.write('<html>\n')
            f.write('\t<head>\n')
            f.write('\t<meta http-equiv="Content-Type" content="text/html; charset=gb2312"/>\n')
            f.write('\t\t<title>福彩双色球开奖记录</title>\n')
            f.write('\t</head>\n')
            f.write('\t<body>\n')
            f.write('\t\t<table border="1">\n')
        return spider

    def process_item(self, item, spider):
        if item['issue'] == '2017001':
            item['issue'] = '2017001'
            item['reds'] = ['09', '11', '14', '20', '25', '26']
            item['blue'] = '15'
            item['sale'] = '376155592'
            item['residue'] = '1007519355'
            item['prize_1'] = ['一等奖', '9', '7522351']
            item['prize_2'] = ['二等奖', '184', '154219']
            item['prize_3'] = ['三等奖', '1511', '3000']
            item['prize_4'] = ['四等奖', '72564', '200']
            item['prize_5'] = ['五等奖', '1361887', '10']
            item['prize_6'] = ['六等奖', '7629153', '5']

        self.save_db(item)
        return item

    @db.atomic()
    def save_db(self, item):
        issue = int(item['issue'])
        red_1 = int(item['reds'][0] if item['reds'][0].isdigit() else 0)
        red_2 = int(item['reds'][1] if item['reds'][1].isdigit() else 0)
        red_3 = int(item['reds'][2] if item['reds'][2].isdigit() else 0)
        red_4 = int(item['reds'][3] if item['reds'][3].isdigit() else 0)
        red_5 = int(item['reds'][4] if item['reds'][4].isdigit() else 0)
        red_6 = int(item['reds'][5] if item['reds'][5].isdigit() else 0)
        blue = int(item['blue'])
        newNote = False
        try:
            newNote = UnionLottoModel.select().where(UnionLottoModel.issue == issue)
            if not newNote:
                newNote = UnionLottoModel.create(issue=issue,
                                                 red1=red_1,
                                                 red2=red_2,
                                                 red3=red_3,
                                                 red4=red_4,
                                                 red5=red_5,
                                                 red6=red_6,
                                                 blue=blue)
        except Exception as e:
            raise e
        sale = self.to_int(item['sale'])
        residue = self.to_int(item['residue'])
        url = item['url']
        dates = item['dates'].split()

        lottery_dates = dates[0].split('：')[1]
        limite_dates = dates[1].split('：')[1]
        if newNote and not UnionLottoExtendModel.select().where(UnionLottoExtendModel.issue == newNote.get().issue):
            try:
                UnionLottoExtendModel.create(issue=newNote.get().issue,
                                             sale=sale,
                                             residue=residue,
                                             url=url,
                                             lottery_dates=lottery_dates,
                                             limite_dates=limite_dates,
                                             prize_1_count=self.to_int(item['prize_1'][1]),
                                             prize_2_count=self.to_int(item['prize_2'][1]),
                                             prize_3_count=self.to_int(item['prize_3'][1]),
                                             prize_4_count=self.to_int(item['prize_4'][1]),
                                             prize_5_count=self.to_int(item['prize_5'][1]),
                                             prize_6_count=self.to_int(item['prize_6'][1]),
                                             prize_1_money=self.to_int(item['prize_1'][2]),
                                             prize_2_money=self.to_int(item['prize_2'][2]),
                                             prize_3_money=self.to_int(item['prize_3'][2]),
                                             prize_4_money=self.to_int(item['prize_4'][2]),
                                             prize_5_money=self.to_int(item['prize_5'][2]),
                                             prize_6_money=self.to_int(item['prize_6'][2]))
            except Exception as e:
                raise e
    def to_int(self, itemStr):
        digits = ''.join(filter(str.isdigit, itemStr))
        return  0 if not digits else int(digits)

    def save_html(self, item):
        out_html = os.path.join('output', 'shuangseqiu.html')
        with open(out_html, 'a') as f:
            f.write('\t\t\t<tr>\n')
            f.write('\t\t\t\t<td>%s</td>\n' % item['issue'])
            f.write('\t\t\t\t<td style="color:red;">%s</td>\n' % item['reds'])
            f.write('\t\t\t\t<td style="color:white; border-radius: 50%%; background-color: blue;">%s</td>\n' % item[
                'blue'])
            f.write('\t\t\t\t<td>%s</td>\n' % item['sale'])
            f.write('\t\t\t\t<td>%s</td>\n' % item['residue'])
            f.write('\t\t\t\t<td>%s</td>\n' % item['prize_1'])
            f.write('\t\t\t\t<td>%s</td>\n' % item['prize_2'])
            f.write('\t\t\t\t<td>%s</td>\n' % item['prize_3'])
            f.write('\t\t\t\t<td>%s</td>\n' % item['prize_4'])
            f.write('\t\t\t\t<td>%s</td>\n' % item['prize_5'])
            f.write('\t\t\t\t<td>%s</td>\n' % item['prize_6'])
            f.write('\t\t\t\t<td><a target="_blank" href=%s>%s</a></td>\n' % (
                item['url'], item['url']))
            f.write('\t\t\t</tr>\n')

        return out_html

    def close_spider(self, spider):
        out_html = os.path.join('output', 'shuangseqiu.html')
        with open(out_html, 'a') as f:
            f.write('\t\t</table>\n')
            f.write('\t</body>\n')
            f.write('</html>')
        return None
