#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from CaiPiaoSpider import models
from peewee_migrate import Router

def makemigrate(model, ignore=['basemodel'], name='auto'):
    router = Router(model.db, ignore=['basemodel'])
    router.create(name='auto', auto=model)
    router.run()


if __name__ == '__main__':
    models.db.connect()
    print(models.db.get_tables())
    router = Router(models.db, ignore=['basemodel'])
    # router.rollback('001_auto')
    router.create(name='auto', auto=models)
    router.run()
    models.db.close()
