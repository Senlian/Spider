#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from CaiPiaoSpider import models
from peewee_migrate import Router
import os
def makemigrate(model, ignore=['basemodel'], name='auto'):
    if models.db.is_closed():
        models.db.connect()
    router = Router(model.db, ignore=['basemodel'], migrate_dir=os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'migrations'))
    router.create(name='auto', auto=model)
    router.run()
    if not models.db.is_closed():
        models.db.close()


if __name__ == '__main__':
    makemigrate(models)
    # models.db.connect()
    #
    # router = Router(models.db, ignore=['basemodel'])
    # # router.rollback('001_auto')
    # router.create(name='auto', auto=models)
    # router.run()
    # models.db.close()
