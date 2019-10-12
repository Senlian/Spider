#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import peewee,os

from playhouse.sqlite_ext import SqliteExtDatabase
from peewee import BaseModelSelect, JOIN, fn

__path__ = ['.']
# peewee文档：http://docs.peewee-orm.com/en/latest/peewee/quickstart.html#quickstart

db = peewee.SqliteDatabase(database=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sqlite3.db'), pragmas={'journal_mode': 'wal'})


class BaseModel(peewee.Model):
    class Meta:
        database = db


class UnionLottoModel(BaseModel):
    issue = peewee.IntegerField(verbose_name='期号', unique=True, primary_key=True)
    red1 = peewee.IntegerField(verbose_name='红色1号球')
    red2 = peewee.IntegerField(verbose_name='红色2号球')
    red3 = peewee.IntegerField(verbose_name='红色3号球')
    red4 = peewee.IntegerField(verbose_name='红色4号球')
    red5 = peewee.IntegerField(verbose_name='红色5号球')
    red6 = peewee.IntegerField(verbose_name='红色6号球')
    blue = peewee.IntegerField(verbose_name='蓝色球')

    class Meta:
        indexes = ('issue', 'red1', 'red2', 'red3', 'red4', 'red5', 'red6', 'blue')
        # primary_key = peewee.CompositeKey('issue')


class UnionLottoExtendModel(BaseModel):
    # RESTRICT（限制外表中的外键改动）
    # CASCADE（跟随外键改动）
    # SET NULL（设空值）
    # SET DEFAULT（设默认值）
    # NO ACTION（无动作，默认的）
    issue = peewee.ForeignKeyField(UnionLottoModel, to_field='issue', on_delete='CASCADE', related_name='infos',
                                   primary_key=True)
    sale = peewee.IntegerField(verbose_name='本期销量', null=True)
    residue = peewee.IntegerField(verbose_name='奖池滚存', null=True)
    url = peewee.CharField(max_length=200, verbose_name='详情链接', null=True)

    lottery_dates = peewee.DateField(verbose_name='开奖日期', null=True)
    limite_dates = peewee.DateField(verbose_name='兑奖截止日期', null=True)

    prize_1_count = peewee.IntegerField(verbose_name='一等奖中奖注数', null=True)
    prize_2_count = peewee.IntegerField(verbose_name='二等奖中奖注数', null=True)
    prize_3_count = peewee.IntegerField(verbose_name='三等奖中奖注数', null=True)
    prize_4_count = peewee.IntegerField(verbose_name='四等奖中奖注数', null=True)
    prize_5_count = peewee.IntegerField(verbose_name='五等奖中奖注数', null=True)
    prize_6_count = peewee.IntegerField(verbose_name='六等奖中奖注数', null=True)

    prize_1_money = peewee.IntegerField(verbose_name='一等奖单注奖金（元）', null=True)
    prize_2_money = peewee.IntegerField(verbose_name='二等奖单注奖金（元）', null=True)
    prize_3_money = peewee.IntegerField(verbose_name='三等奖单注奖金（元）', null=True)
    prize_4_money = peewee.IntegerField(verbose_name='四等奖单注奖金（元）', null=True)
    prize_5_money = peewee.IntegerField(verbose_name='五等奖单注奖金（元）', null=True)
    prize_6_money = peewee.IntegerField(verbose_name='六等奖单注奖金（元）', null=True)


if __name__ == '__main__':
    db.connect()
    new = UnionLottoModel.create(issue=20191116, red1=1, red2=8, red3=9, red4=13, red5=16, red6=33, blue=1)

    db.close()
