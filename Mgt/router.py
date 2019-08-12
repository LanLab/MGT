from django.conf import settings


class GenericRouter(object):
    """
    A router to control all database operations on models for different
    databases.

    In case an app is not set in settings.APPS_DATABASE_MAPPING, the router
    will fallback to the `default` database.

    Settings example:

    APPS_DATABASE_MAPPING = {'app1': 'db1', 'app2': 'db2'}

    From: http://diegobz.net/2011/02/10/django-database-router-using-settings/

    """

    def db_for_read(self, model, **hints):
        """"Point all read operations to the specific database."""
        if model._meta.app_label in settings.APPS_DATABASE_MAPPING:
            return settings.APPS_DATABASE_MAPPING[model._meta.app_label]
        return None

    def db_for_write(self, model, **hints):
        """Point all write operations to the specific database."""
        if model._meta.app_label in settings.APPS_DATABASE_MAPPING:
            return settings.APPS_DATABASE_MAPPING[model._meta.app_label]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation between apps that use the same database."""
        db_obj1 = settings.APPS_DATABASE_MAPPING.get(obj1._meta.app_label)
        db_obj2 = settings.APPS_DATABASE_MAPPING.get(obj2._meta.app_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db in settings.APPS_DATABASE_MAPPING.values():
            return settings.APPS_DATABASE_MAPPING.get(app_label) == db
        elif app_label in settings.APPS_DATABASE_MAPPING:
            return False
        return None
