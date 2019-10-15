#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import numpy
import pandas

from playhouse.shortcuts import model_to_dict
from playhouse.sqlite_ext import fn
from CaiPiaoSpider.models import UnionLottoModel, UnionLottoExtendModel, db


class UnionLotto(object):
    def __init__(self):
        # 查询所有数据
        self.records = UnionLottoModel.select().order_by()

    def get_per_count(self, number):
        return self.records.where((UnionLottoModel.red1 == number) |
                                  (UnionLottoModel.red2 == number) |
                                  (UnionLottoModel.red3 == number) |
                                  (UnionLottoModel.red4 == number) |
                                  (UnionLottoModel.red5 == number) |
                                  (UnionLottoModel.red6 == number)).count()

    def get_per_limit_count(self, top, number):
        records_top = self.records.limit(top)
        count = 0
        for record in records_top:
            if (record.red1 == number) or \
                    (record.red2 == number) or \
                    (record.red3 == number) or \
                    (record.red4 == number) or \
                    (record.red5 == number) or \
                    (record.red6 == number):
                count += 1
        return count

    # 获取单个球已出现概率
    def get_per_rate(self, number):
        return self.get_per_count(number) / self.records.count() * 100

    # 获取给定球概率
    def get_rate(self, numbers):
        rate = 1
        for number in numbers:
            if number not in range(1, 34) and len(numbers) != 7:
                return 0
            rate *= self.get_per_rate(number) / 100
        return rate * 100

    def get_best_ball(self):
        pass

    # 生成一组随机号码球
    def get_random_ball(self):
        return random.sample(range(1, 34), 6)


if __name__ == '__main__':
    lotto = UnionLotto()
    new_balls = lotto.get_random_ball()

    for num in range(1, 34):
        print(lotto.get_per_limit_count(1, num))

    # print(lotto.get_rate([13, 22, 23, 4, 5, 33]))
    # print(lotto.records.count())

