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
        db.connect()
        makemigrate(models)
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

    def save_db(self, item):
        issue = int(item['issue'])
        red_1 = int(item['reds'][0] if item['reds'][0].isdigit else 0)
        red_2 = int(item['reds'][1] if item['reds'][0].isdigit else 0)
        red_3 = int(item['reds'][2] if item['reds'][0].isdigit else 0)
        red_4 = int(item['reds'][3] if item['reds'][0].isdigit else 0)
        red_5 = int(item['reds'][4] if item['reds'][0].isdigit else 0)
        red_6 = int(item['reds'][5] if item['reds'][0].isdigit else 0)
        blue = int(item['blue'])
        sale = int(''.join(filter(str.isdigit, item['sale'])))
        residue = int(''.join(filter(str.isdigit, item['residue'])))


        print(UnionLottoModel.select().where(UnionLottoModel.issue == issue).count())
        try:
            if not UnionLottoModel.select().where(UnionLottoModel.issue == issue).count():
                print('---'*100)
                print(issue,red_1,red_2,red_3,red_4,red_5,red_6,blue)
                newNote = UnionLottoModel.create(issue=issue,
                                       red1=red_1,
                                       red2=red_2,
                                       red3=red_3,
                                       red4=red_4,
                                       red5=red_5,
                                       red6=red_6,
                                       blue=blue)
                print('newNote=',newNote)
                # newNote.save()
                print('---' * 100)
        except Exception as e:
            raise e

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
        db.close()
        out_html = os.path.join('output', 'shuangseqiu.html')
        with open(out_html, 'a') as f:
            f.write('\t\t</table>\n')
            f.write('\t</body>\n')
            f.write('</html>')
        return None
