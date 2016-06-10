# -*- coding: utf-8 -*-

class MainDBRouter(object):
    def db_for_read(self, model, **hints):
        # if model._meta.app_label == 'core':
        #     return 'core'
        if model._meta.app_label == 'claims':
            return 'claims'
        return 'default'

    def db_for_write(self, model, **hints):
        # if model._meta.app_label == 'core':
        #     return 'core'
        if model._meta.app_label == 'claims':
            return 'claims'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_syncdb(self, db, model):
        if model._meta.app_label == 'core':
            return False
        if model._meta.app_label == 'claims':
            return False
        return True

    def allow_migrate(self, db, model):
        if model._meta.app_label == 'core':
            return False
        return True

