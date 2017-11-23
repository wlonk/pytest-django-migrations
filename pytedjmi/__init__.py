from functools import wraps

from django.apps import apps
from django.db.migrations.executor import MigrationExecutor
from django.db import connection


class DjMiSetup:
    def __init__(self, migrate_from):
        self.migrate_from = migrate_from

    def decorate(self, fn):
        self.pre_run_fn = fn
        return self

    @property
    def app(self):
        return apps.get_containing_app_config(type(self).__module__).name

    def get_from_to(self):
        return (
            [(self.app, self.migrate_from)],
            [(self.app, self.migrate_to)],
        )

    def apply_migration(self):
        migrate_from, migrate_to = self.get_from_to()
        executor = MigrationExecutor(connection)
        old_apps = executor.loader.project_state(migrate_from).apps
        executor.migrate(migrate_to)
        return old_apps

    def revert_migration(self):
        migrate_from, migrate_to = self.get_from_to()
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()  # reload.
        executor.migrate(migrate_from)
        return executor.loader.project_state(self.migrate_to).apps

    def to_migration(self, migrate_to):
        def inner_decorator(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                try:
                    old_apps = self.revert_migration()
                    self.pre_run_fn(old_apps)
                    apps = self.apply_migration()
                    return fn(*args, apps=apps, **kwargs)
                finally:
                    self.revert_migration()
            return wrapper
        return inner_decorator


def setup(migrate_from):
    """
    Use::

        @setup("starting point")
        def some_setup(apps):
            pass


        @some_setup.to_migration("ending point")
        def test_bar(..., *, apps, ...):
            pass
    """
    def inner_decorator(fn):
        dj_mi_setup = DjMiSetup(migrate_from)
        dj_mi_setup.decorate(fn)
        return dj_mi_setup
    return inner_decorator
