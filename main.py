#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
# @license    : (C) Copyright 2013-{YEAR}, Node Supply Chain Manager Corporation Limited.
# @author     : Administrator
# @Email      :
# @Time       : 2019/10/14 14:24
# @File       : main.py
# @Software   : PyCharm
# @Modules     :python3 -m pip install 
# @Desc       : 
'''
import sys
import os
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    execute('scrapy crawl ssq_spider'.split())
